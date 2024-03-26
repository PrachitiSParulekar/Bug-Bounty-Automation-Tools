# Bug Bounty Automation

This is a Basic tool for Information Gathering with real time alerts using Telegram Bot 🚀

## Install with Docker

1. Pull the image from Docker Hub

```bash
docker pull ezhil56x/recon
```

2. Run the image

```bash
docker run --name recon -d -p 5000:5000 -e TELEGRAM_BOT_TOKEN="" -e TELEGRAM_CHAT_ID="" ezhil56x/recon
```

3. Go to [http://localhost:5000/recon](http://localhost:5000/recon) and add Organization Name and Domains

4. SSH into the container

```bash
docker exec -it recon /bin/bash
```

5. Run the `recon.sh`

```bash
cd recon
./recon.sh
```
