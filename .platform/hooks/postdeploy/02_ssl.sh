#!/bin/bash
# 1. Install certbot if not present
if ! command -v certbot &> /dev/null; then
    dnf install -y certbot || true
fi

DOMAIN="litwise-ai-agent.us-east-1.elasticbeanstalk.com"
EMAIL="vedanthraj@gmail.com"

# 2. If certificate doesn't exist, request it
if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    systemctl stop nginx || true
    certbot certonly --standalone -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL" || true
    systemctl start nginx || true
fi

# 3. If certificate exists, install SSL config
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
cat << 'EOF' > /etc/nginx/conf.d/ssl.conf
server {
    listen 443 ssl default_server;
    server_name litwise-ai-agent.us-east-1.elasticbeanstalk.com;

    ssl_certificate /etc/letsencrypt/live/litwise-ai-agent.us-east-1.elasticbeanstalk.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/litwise-ai-agent.us-east-1.elasticbeanstalk.com/privkey.pem;

    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log main;

    client_header_timeout 60;
    client_body_timeout   60;
    keepalive_timeout     60;
    gzip                  off;

    # Include the Elastic Beanstalk generated locations
    include conf.d/elasticbeanstalk/*.conf;
}
EOF

cat << 'EOF' > /etc/nginx/conf.d/elasticbeanstalk/02_redirect.conf
if ($server_port = 80) {
    return 301 https://$host$request_uri;
}
EOF

    nginx -t && systemctl reload nginx || true
fi
