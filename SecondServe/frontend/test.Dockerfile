# ============================
# Frontend Testing Container
# ============================
FROM node:22-alpine

# Install Chromium and fonts for headless testing
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    bash \
    curl \
    git \
    tzdata

# Set environment variables for Karma/Jest
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY frontend/web/package*.json ./
RUN npm ci --legacy-peer-deps

# Copy Angular source code
COPY frontend/web/ ./

# Expose nothing — this container is for testing only
# EXPOSE is optional here

# Default command: start a shell
CMD ["sh"]
