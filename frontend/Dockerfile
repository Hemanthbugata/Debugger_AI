# Use Debian slim images to avoid Alpine/musl native binary build failures (esbuild/swc)
FROM node:18-bullseye-slim AS build
WORKDIR /app
# Install minimal build dependencies required to compile native modules (esbuild/swc)
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 build-essential make g++ ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-bullseye-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
COPY --from=build /app/ ./
EXPOSE 3000
# Use next start for production, but allow running dev when NODE_ENV=development or DEV=true
CMD ["sh","-c","if [ \"$NODE_ENV\" = \"development\" ] || [ \"$DEV\" = \"true\" ]; then npm run dev; else npm run start; fi"]