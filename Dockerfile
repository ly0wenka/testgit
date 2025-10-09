# Use the official GCC image
FROM gcc:latest

# Set the working directory
WORKDIR /app

# Copy the C source file into the container
COPY helloworld.c makefile .

# Run the compiled program
CMD ["make"]
