import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import websockets
from loguru import logger

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel
from nanobot.config.schema import FeishuConfig


class FeishuChannel(BaseChannel):
    """
    Feishu channel that connects to a Node.js bridge.
    
    The bridge uses @larksuiteoapi/node-sdk to handle the Feishu protocol via WebSocket.
    Communication between Python and Node.js is via WebSocket (ws://localhost:3001).
    """
    
    name = "feishu"
    
    def __init__(self, config: FeishuConfig, bus: MessageBus):
        super().__init__(config, bus)
        self.config: FeishuConfig = config
        self._ws = None
        self._connected = False
        self._bridge_proc = None
        self._spawn_retries = 0
    
    async def start(self) -> None:
        """Start the Feishu channel by connecting to the bridge."""
        bridge_url = "ws://localhost:3001"
        logger.info(f"Connecting to Feishu bridge at {bridge_url}...")
        
        self._running = True
        
        while self._running:
            try:
                async with websockets.connect(bridge_url) as ws:
                    self._ws = ws
                    self._connected = True
                    self._spawn_retries = 0 # Reset retries on successful connection
                    logger.info("Connected to Feishu bridge")
                    
                    # Listen for messages
                    async for message in ws:
                        try:
                            await self._handle_bridge_message(message)
                        except Exception as e:
                            logger.error(f"Error handling bridge message: {e}")
                    
            except (OSError, ConnectionRefusedError, websockets.exceptions.InvalidHandshake, websockets.exceptions.InvalidMessage) as e:
                # Bridge might not be running or is in a bad state.
                logger.warning(f"Bridge connection invalid: {e}")
                
                if not self._bridge_proc and self._spawn_retries < 3:
                    logger.info("Bridge not accessible. Attempting to start bridge process...")
                    self._spawn_retries += 1
                    if self._start_bridge_process():
                        logger.info("Bridge process started. Waiting for initialization...")
                        await asyncio.sleep(5)
                        continue
                    else:
                        logger.warning("Could not start bridge automatically. Please run 'npm start' in the bridge directory.")
                        await asyncio.sleep(10)
                else:
                     logger.info("Waiting for bridge to come online...")
                     await asyncio.sleep(5)

            except Exception as e:
                self._connected = False
                self._ws = None
                logger.warning(f"Feishu bridge connection error details: {e}")
                
                # If we haven't spawned the bridge yet and it seems down, try once
                if not self._bridge_proc and self._spawn_retries < 3:
                     logger.info("Attempting specific startup...")
                     self._spawn_retries += 1
                     self._start_bridge_process()
                     await asyncio.sleep(5)
                     continue
                
                if self._running:
                    await asyncio.sleep(5)

    def _start_bridge_process(self) -> bool:
        """Attempt to spawn the Node.js bridge process."""
        try:
            # Find bridge directory
            # Try user directory first
            bridge_dir = Path.home() / ".nanobot" / "bridge"
            if not (bridge_dir / "package.json").exists():
                # Try dev directory (relative to this file)
                # nanobot/channels/feishu.py -> ../../../bridge
                bridge_dir = Path(__file__).parent.parent.parent / "bridge"
            
            if not (bridge_dir / "package.json").exists():
                logger.error("Bridge directory not found.")
                return False

            env = os.environ.copy()
            # Pass Feishu config to bridge process via Env Vars
            if self.config.app_id:
                env["FEISHU_APP_ID"] = self.config.app_id
            if self.config.app_secret:
                env["FEISHU_APP_SECRET"] = self.config.app_secret

            logger.info(f"Spawning bridge in {bridge_dir}...")
            
            # Check if dependencies installed (heuristic)
            if not (bridge_dir / "node_modules").exists():
                 logger.info("Installing dependencies...")
                 # Use nvm to install if possible
                 install_cmd = "npm install"
                 if os.path.exists(os.path.expanduser("~/.nvm/nvm.sh")):
                     install_cmd = f"source ~/.nvm/nvm.sh && nvm use 20 && {install_cmd}"
                 
                 subprocess.run(
                     ["/bin/bash", "-c", install_cmd], 
                     cwd=bridge_dir, 
                     check=True
                 )

            # Construct command to run with NVM if available
            cmd = ["npm", "start"]
            shell = False
            
            nvm_path = os.path.expanduser("~/.nvm/nvm.sh")
            if os.path.exists(nvm_path):
                # Run via bash to source nvm
                cmd = ["/bin/bash", "-c", f"source {nvm_path} && nvm use 20 && npm start"]
                # When using shell=False with a list for bash -c, it works as expected.
                # But here cmd is a list, so we pass it directly to Popen
                # and we don't need shell=True if we are explicitly calling /bin/bash
            
            logger.info(f"Starting bridge with command: {cmd}")

            self._bridge_proc = subprocess.Popen(
                cmd,
                cwd=bridge_dir,
                env=env,
                # Redirect output to avoid cluttering console, or keep it for debug?
                # Keeping it for now as it's useful.
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to spawn bridge: {e}")
            return False
    
    async def stop(self) -> None:
        """Stop the Feishu channel."""
        self._running = False
        self._connected = False
        
        if self._ws:
            await self._ws.close()
            self._ws = None
            
        if self._bridge_proc:
            self._bridge_proc.terminate()
            self._bridge_proc = None
    
    async def send(self, msg: OutboundMessage) -> None:
        """Send a message through Feishu."""
        if not self._ws or not self._connected:
            logger.warning("Feishu bridge not connected")
            return
        
        try:
            payload = {
                "type": "send",
                "to": msg.chat_id,
                "text": msg.content
            }
            await self._ws.send(json.dumps(payload))
        except Exception as e:
            logger.error(f"Error sending Feishu message: {e}")
    
    async def _handle_bridge_message(self, raw: str) -> None:
        """Handle a message from the bridge."""
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return
        
        msg_type = data.get("type")
        
        if msg_type == "message":
            # Incoming message
            sender = data.get("from", "")
            content = data.get("body", "")
            # Feishu specific fields logic if needed
            
            await self._handle_message(
                sender_id=sender,
                chat_id=sender, # For Feishu OpenID is used for reply
                content=content,
                metadata={
                    "is_group": data.get("isGroup", False),
                    "name": data.get("name")
                }
            )
