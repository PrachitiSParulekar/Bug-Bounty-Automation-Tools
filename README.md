# Bug Bounty Automation Tools 🔍

A modern web-based security reconnaissance platform for bug bounty hunters and penetration testers. Real-time network analysis with an intuitive interface.

## ✨ Features

- **🏓 Ping Tool** - Network connectivity testing
- **🌍 IP Lookup** - Geolocation and ISP information  
- **🔍 WHOIS Lookup** - Domain registration details
- **🔐 Certificate Search** - SSL certificate transparency logs
- **🚪 Port Scanner** - Network port enumeration using Nmap
- **🔗 Subdomain Finder** - Subdomain discovery using Subfinder

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Nmap (for port scanning)
- Subfinder (for subdomain enumeration)

### Installation

```bash
git clone https://github.com/ezhil56x/bugbounty.git
cd bugbounty
pip install -r requirements.txt
python app.py
```

### Docker Deployment

```bash
docker build -t bugbounty .
docker run -p 5000:5000 bugbounty
```

## 🌐 Access

- **Local**: http://127.0.0.1:5000
- **Network**: http://your-ip:5000

## 🛠️ Technology Stack

- **Backend**: Flask, SocketIO
- **Database**: SQLite
- **Rate Limiting**: Flask-Limiter
- **External Tools**: Nmap, Subfinder
- **APIs**: ip-api.com, crt.sh

## 📋 API Endpoints

| Tool | Endpoint | Description |
|------|----------|-------------|
| Main Dashboard | `/` | Home page |
| Ping | `/ping` | Network connectivity testing |
| IP Lookup | `/ip_lookup` | IP geolocation |
| WHOIS | `/whois` | Domain information |
| Certificates | `/certificate_search` | SSL certificate search |
| Port Scanner | `/open_ports` | Network port scanning |
| Subfinder | `/subfinder` | Subdomain enumeration |

## 🔧 Installation Guide

### External Tools Setup

#### Install Nmap
```bash
# Ubuntu/Debian
sudo apt-get install nmap

# Windows
# Download from https://nmap.org/download.html
```

#### Install Subfinder
```bash
# Using Go
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Or download binary from releases
```

## 🔒 Security Features

- Input validation for domains and IPs
- Rate limiting (200/day, 50/hour)
- Error handling and logging
- Secure subprocess execution

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized security testing purposes only. Always ensure you have permission before testing any systems.