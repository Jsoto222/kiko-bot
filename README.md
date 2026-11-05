# Kiko — Discord Community Automation Bot

A Python Discord bot created for the **Gaming After Hours** community. It automates new-member onboarding with randomized welcome embeds and starter roles, and provides an administrator-only command for publishing server rules.

> **Project status:** Successfully deployed and tested locally.

## Features

- **Automated onboarding:** Responds to Discord's `on_member_join` event and attempts to assign a predefined role.
- **Personalized welcomes:** Posts a randomized welcome title and greeting, member avatar, and server information in a rich Discord embed.
- **Server rules:** An administrator-only `!rules` command posts an embed containing the community code of conduct.
- **Testing:** `!testwelcome` lets members preview the welcome-message formatting.
- **Permission-aware errors:** Handles role-assignment and message-posting failures and logs actionable diagnostics.
- **Environment-based secrets:** Loads the bot token from a local `.env` file excluded from version control.

## Technology

Python 3 · discord.py · python-dotenv · Discord Gateway intents · asynchronous event handlers · Windows batch scripts

## Quick start (Windows)

1. Install Python 3 and check `py --version` in a new Command Prompt.
2. Run **`Setup Bot.bat`** to create a local virtual environment and install dependencies.
3. Copy **`.env.example`** to a new file named **`.env`**.
4. In the [Discord Developer Portal](https://discord.com/developers/applications), **reset any previously exposed bot token**. Paste the newly reset token into `.env` only. Never commit or share that file.
5. In the application settings under **Bot → Privileged Gateway Intents**, enable **Server Members Intent** and **Message Content Intent**.
6. Confirm `WELCOME_CHANNEL_ID` and `AUTO_ROLE_ID` in `.env` match your server. The bot needs **Manage Roles**, **View Channel**, **Send Messages**, and **Embed Links** permissions; its highest role must be above the role it assigns.
7. Run **`Run Bot.bat`**. Keep its terminal open while the bot is running.
8. Test `!testwelcome`. A server administrator can use `!rules`. To test onboarding, have a test account join the server (without violating Discord's rules).

### Manual setup (cross-platform)

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python bot.py
```

## Project structure

```text
Kiko_Discord_Bot/
├── bot.py               # Event handlers, embed builders, and commands
├── requirements.txt     # Python libraries
├── .env.example         # Safe example configuration; no real token
├── .gitignore           # Prevents uploading credentials and build files
├── Setup Bot.bat        # Create Python environment and install packages
├── Run Bot.bat          # Start bot with its Python environment
├── LINKEDIN_PROJECT.md  # Resume/LinkedIn-friendly project notes
└── README.md            # This guide
```

## Commands

| Command | Who can use it | Purpose |
| --- | --- | --- |
| `!testwelcome` | Server members | Preview a randomized welcome embed |
| `!rules` | Server administrators | Post the community rules embed |
| `!help` | Server members | List the bot's commands |

## Configuration and security

- **Never publish `.env`** or a Discord bot token. This repository includes only `.env.example`.
- If a token was shared previously, **reset it** before launching the bot. Removing it from a file does not invalidate a leaked token.
- Server/channel/role IDs aren't secrets, but must match your Discord server.
- This project uses **prefix commands**, not slash commands.
- `intents.members` and `intents.message_content` must be enabled both in code and the Developer Portal.

## Potential future improvements

Slash commands, configuration validation, automated tests, audit logging, multiple-server support, and deployment with process supervision.

## Portfolio context

See [LINKEDIN_PROJECT.md](LINKEDIN_PROJECT.md) for a truthful, copy-ready project description and bullet points. Only mark the bot as deployed once you've verified it running successfully in Discord.
