FROM node:23.6.0-alpine

WORKDIR /app

COPY . .
RUN cp .env.example .env
RUN npm ci
RUN npx prisma generate
RUN npm run build
EXPOSE 3000

CMD ["npm", "run", "dev"]
