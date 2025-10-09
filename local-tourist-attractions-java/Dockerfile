FROM openjdk:21

WORKDIR /app
COPY . .

RUN javac Main.java

EXPOSE 8080
CMD ["java", "Main"]
