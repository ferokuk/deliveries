# === Build stage ===
FROM node:20 AS builder
WORKDIR /frontend

COPY package*.json tsconfig.json ./
RUN npm ci

COPY . .
RUN npm run build

# === Dev/Runtime stage ===
FROM node:20 AS dev
WORKDIR /frontend

# копируем готовые зависимости из билд-стадии
COPY --from=builder /frontend/node_modules ./node_modules

# копируем исходники и конфиги
COPY package*.json tsconfig.json ./
COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
