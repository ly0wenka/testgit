# Use the official GCC image
FROM gcc:latest

# Set the working directory
WORKDIR /app

# Copy the C source file into the container
COPY helloworld.c .

# Compile the C program
RUN gcc -o hello helloworld.c

# Run the compiled program
CMD ["./hello"]
