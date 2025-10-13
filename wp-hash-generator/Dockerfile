# Use a CLI PHP image
FROM php:8.2-cli

WORKDIR /app

# Install curl (if not present) and download class-phpass.php at build time
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Download the current class-phpass.php from WordPress repo
# (this downloads at build-time; you can change the URL if you want a specific version)
RUN curl -fsSL -o /app/class-phpass.php https://raw.githubusercontent.com/WordPress/WordPress/master/wp-includes/class-phpass.php

# Copy the hash script
COPY hash.php /app/hash.php

# Default command prints usage; override with arguments or env
ENTRYPOINT ["php", "/app/hash.php"]

