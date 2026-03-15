# Frontend Dockerfile - Simplified
FROM node:20-alpine as builder

WORKDIR /app

# Copy dependency files
COPY package.json ./
RUN npm install

# Copy source
COPY . .

# Build - adapter-static outputs to build/
RUN npm run build

# --- Runtime ---
FROM nginx:alpine

# Copy static files
COPY --from=builder /app/build/ /usr/share/nginx/html/

# Simple SPA routing config
RUN echo "server { listen 80; root /usr/share/nginx/html; location / { try_files \$uri \$uri/ /index.html; } }" > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
