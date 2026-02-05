import * as Lark from '@larksuiteoapi/node-sdk';

export interface FeishuConfig {
    appId: string;
    appSecret: string;
    encryptKey?: string;
    verificationToken?: string;
}

export interface FeishuMessage {
    msgId: string;
    from: string; // Open ID
    to: string;
    type: string;
    content: string;
    timestamp: number;
    isGroup: boolean;
    name?: string;
}

export class FeishuManager {
    private client: Lark.Client;
    private wsClient: Lark.WSClient | null = null;
    public onMessage: ((msg: FeishuMessage) => void) | null = null;

    constructor(private config: FeishuConfig) {
        this.client = new Lark.Client({
            appId: config.appId,
            appSecret: config.appSecret,
            appType: Lark.AppType.SelfBuild,
            domain: Lark.Domain.Feishu,
        });
    }

    async start() {
        console.log('[Feishu] Starting WebSocket client...');
        this.wsClient = new Lark.WSClient({
            appId: this.config.appId,
            appSecret: this.config.appSecret,
            loggerLevel: Lark.LoggerLevel.info,
        });

        const dispatcher = new Lark.EventDispatcher({}).register({
            'im.message.receive_v1': async (data) => {
                try {
                    await this.handleEvent(data);
                } catch (e) {
                    console.error('[Feishu] Handler error:', e);
                }
            }
        });

        await this.wsClient.start({ eventDispatcher: dispatcher });
        console.log('[Feishu] Connected!');
    }

    async stop() {
        // Lark WS Client doesn't have a clear stop method exposed in all versions, 
        // but usually disconnecting the process handles it.
        // We can try to close if the instance exposes it.
        // @ts-ignore
        if (this.wsClient && this.wsClient.ws) {
            // @ts-ignore
            this.wsClient.ws.close();
        }
    }

    private async handleEvent(data: any) {
        console.log('[Feishu] Raw Event:', JSON.stringify(data));

        // Handle Schema 2.0 (Direct) or Legacy (Nested in .event)
        const eventType = data.event_type || data?.header?.event_type;

        if (eventType === 'im.message.receive_v1') {
            // Flatten: data IS the event in Schema 2.0, or data.event is the event in 1.0
            const eventBody = data.message ? data : data.event;

            if (!eventBody || !eventBody.message) {
                // console.warn('[Feishu] Invalid event structure', data);
                return;
            }

            const msg = eventBody.message;
            const sender = eventBody.sender;

            // Field mapping (Schema 2.0 uses message_type, 1.0 uses msg_type)
            const msgType = msg.message_type || msg.msg_type;
            const msgId = msg.message_id;
            const createTime = msg.create_time;

            const isGroup = msg.chat_type === 'group';
            let text = '';

            if (msgType === 'text') {
                try {
                    const contentJson = JSON.parse(msg.content);
                    text = contentJson.text;
                } catch {
                    text = msg.content;
                }
            } else if (msgType === 'image') {
                // Parse image content to extract image_key
                try {
                    const contentJson = JSON.parse(msg.content);
                    if (contentJson.image_key) {
                        text = `[image:${contentJson.image_key}]`;
                    } else {
                        text = '[image]';
                    }
                } catch {
                    text = '[image]';
                }
            } else {
                text = `[${msgType}]`; // e.g. [post], [file]
            }

            const feishuMsg: FeishuMessage = {
                msgId: msgId,
                from: sender.sender_id.open_id,
                to: this.config.appId,
                type: msgType,
                content: text,
                timestamp: Number(createTime),
                isGroup: isGroup,
                name: sender.sender_id.user_id
            };

            console.log(`[Feishu] Parsed message: ${text} from ${feishuMsg.from}`);

            if (this.onMessage) {
                this.onMessage(feishuMsg);
            }
        }
    }

    /**
     * Check if text contains Markdown formatting
     */
    private hasMarkdown(text: string): boolean {
        // Check for common Markdown patterns
        const mdPatterns = [
            /^#{1,6}\s/m,           // Headers
            /\*\*.*\*\*/,           // Bold
            /\*.*\*/,               // Italic
            /`.*`/,                 // Inline code
            /```[\s\S]*```/,        // Code blocks
            /^\s*[-*+]\s/m,         // Unordered lists
            /^\s*\d+\.\s/m,         // Ordered lists
            /\[.*\]\(.*\)/,         // Links
            /^>\s/m,                // Blockquotes
        ];

        return mdPatterns.some(pattern => pattern.test(text));
    }

    /**
     * Send a message to Feishu
     * Automatically detects Markdown and sends as card if needed
     */
    async sendMessage(to: string, text: string) {
        // Determine if 'to' is a chat_id (group) or open_id (user)
        // Feishu IDs are tricky. Assuming we store the correct ID from 'receive'.
        // Usually receive_id_type defaults to open_id.

        const useMarkdown = this.hasMarkdown(text);

        if (useMarkdown) {
            // Send as interactive card with Markdown support
            await this.sendMarkdownCard(to, text);
        } else {
            // Send as plain text
            await this.sendPlainText(to, text);
        }
    }

    /**
     * Send plain text message
     */
    private async sendPlainText(to: string, text: string) {
        try {
            await this.client.im.message.create({
                params: {
                    receive_id_type: 'open_id',
                },
                data: {
                    receive_id: to,
                    msg_type: 'text',
                    content: JSON.stringify({ text }),
                },
            });
        } catch (e) {
            console.error('[Feishu] Send error, retrying as chat_id...', e);
            // Fallback or better ID detection logic needed
            await this.client.im.message.create({
                params: {
                    receive_id_type: 'chat_id',
                },
                data: {
                    receive_id: to,
                    msg_type: 'text',
                    content: JSON.stringify({ text }),
                },
            });
        }
    }

    /**
     * Send Markdown as interactive card
     */
    private async sendMarkdownCard(to: string, markdown: string) {
        // Build card with Markdown content
        const card = {
            config: {
                wide_screen_mode: true,
            },
            elements: [
                {
                    tag: 'markdown',
                    content: markdown,
                },
            ],
        };

        try {
            await this.client.im.message.create({
                params: {
                    receive_id_type: 'open_id',
                },
                data: {
                    receive_id: to,
                    msg_type: 'interactive',
                    content: JSON.stringify(card),
                },
            });
            console.log('[Feishu] ✅ Sent Markdown card');
        } catch (e) {
            console.error('[Feishu] Send Markdown card error, retrying as chat_id...', e);
            // Fallback to chat_id
            try {
                await this.client.im.message.create({
                    params: {
                        receive_id_type: 'chat_id',
                    },
                    data: {
                        receive_id: to,
                        msg_type: 'interactive',
                        content: JSON.stringify(card),
                    },
                });
                console.log('[Feishu] ✅ Sent Markdown card (chat_id)');
            } catch (e2) {
                console.error('[Feishu] Failed to send Markdown card, falling back to plain text...', e2);
                // Last resort: send as plain text
                await this.sendPlainText(to, markdown);
            }
        }
    }
}
