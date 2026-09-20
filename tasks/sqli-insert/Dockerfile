FROM composer:2 AS dependencies
WORKDIR /app
COPY composer.json .
RUN composer install --no-dev --prefer-dist --no-interaction --no-progress
FROM php:8.4-cli
RUN apt-get update \
    && apt-get install -y --no-install-recommends libsqlite3-dev libonig-dev \
    && docker-php-ext-install pdo_sqlite mbstring \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=dependencies /app/vendor vendor
COPY . .
RUN mkdir -p bootstrap/cache storage/framework/views \
    && chmod -R 777 bootstrap/cache storage
EXPOSE 80
CMD ["sh", "./entrypoint.sh"]
