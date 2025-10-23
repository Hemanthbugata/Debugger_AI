# Use Debian slim images to avoid Alpine/musl native binary build failures (esbuild/swc)
FROM node:18-bullseye-slim AS build
WORKDIR /app
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
# Use next start for production
CMD ["npm", "run", "start"]