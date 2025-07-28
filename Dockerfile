FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    nmap \
    iputils-ping \
    wget \
    redis-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Go
RUN wget https://go.dev/dl/go1.22.1.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz && \
    rm go1.22.1.linux-amd64.tar.gz

# Set Go environment
ENV PATH=$PATH:/usr/local/go/bin:/root/go/bin
ENV GOPATH=/root/go

# Install Go tools
RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Create symbolic link for httpx
RUN ln -s /root/go/bin/httpx /usr/local/bin/httpxx

# Copy application files
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create database directory and set permissions
RUN mkdir -p recon && \
    chmod 755 recon

# Configure Redis
RUN mkdir -p /var/run/redis && \
    chown redis:redis /var/run/redis && \
    chmod 755 /var/run/redis

# Set up supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

# Use supervisor to manage processes
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]