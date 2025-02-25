FROM node:20-slim AS build

WORKDIR /app

ENV NODE_ENV=development

COPY package*.json ./

RUN npm install --legacy-peer-deps

RUN npm install -g typescript

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
