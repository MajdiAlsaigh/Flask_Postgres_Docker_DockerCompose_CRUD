FROM node:18-alpine

WORKDIR /app/frontend

COPY package.json package-lock.json ./
RUN npm install

COPY . .

CMD ["npx", "tailwindcss", "-i", "./input.css", "-o", "../app/static/css/output.css", "--watch"]
