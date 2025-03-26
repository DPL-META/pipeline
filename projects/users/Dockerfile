FROM node:23.6.0-alpine 

WORKDIR app

COPY . .

RUN npm ci
RUN npm run migrate
RUN npm run seed
RUN npm run build

FROM node:23.6.0-alpine 

WORKDIR app

COPY --from=0 /app/package.json /package.json
COPY --from=0 /app/package-lock.json /package-lock.json
COPY --from=0 /app/dist /dist
COPY --from=0 /app/prisma /prisma
COPY --from=0 /app/.env  /.env

RUN npm ci --production
RUN npm run migrate

ENTRYPOINT ["npm"]
CMD ["start"]