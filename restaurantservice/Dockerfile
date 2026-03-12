# Multi-stage build for restaurantservice
FROM maven:3.9.9-eclipse-temurin-21 AS builder
WORKDIR /app

# Copy Maven files and download dependencies (cache layer)
COPY pom.xml .
RUN mvn dependency:go-offline -B


COPY src ./src

RUN mvn clean package -DskipTests

FROM eclipse-temurin:21-jdk AS runner
WORKDIR /app

# Copy built jar from build stage
COPY --from=builder /app/target/restaurantservice-0.0.1-SNAPSHOT.jar ./app.jar

EXPOSE 8086

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
