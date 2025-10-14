# Multi-stage: build Angular, then serve via Nginx
# 1) Build stage
FROM node:22-alpine AS build
WORKDIR /app
COPY frontend/web/package*.json ./
RUN npm ci
COPY frontend/web/ ./
# Build production Angular app
RUN npm run build -- --configuration production

# 2) Serve stage
FROM nginx:alpine
# Copy Nginx conf
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
# Copy Angular dist (adjust "web" if your app name differs)
COPY --from=build /app/dist/web/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
