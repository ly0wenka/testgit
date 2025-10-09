FROM ruby:3.1.7

WORKDIR /app
COPY . .

RUN gem install bundler \
 && bundle config set path 'vendor' \
 && bundle install

# Default command: run local Jekyll server
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--watch"]
