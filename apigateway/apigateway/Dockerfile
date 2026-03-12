FROM maven:3.9.9-eclipse-temurin-21 AS builder

# the directory in the container for the service
WORKDIR /app

# copy dependencies from pom.xml to the root directory of the container
COPY pom.xml . 

# mvn = maven
RUN mvn dependency:go-offline -B

COPY src ./src

# tells maven to create a new package from our springboot, i.e. into a single jar file
RUN mvn clean package
# so we can work on source code here, outside container. Then whenever we update the code, the container will create this package from the updated code




FROM eclipse-temurin:21-jdk AS runner

#maven to build, jdk to run


WORKDIR /app

# copy the jar created by builder to the specified location for the runner
COPY --from=builder /app/target/apigateway-0.0.1-SNAPSHOT.jar ./app.jar

# port for the app
EXPOSE 4005

ENTRYPOINT ["java","-jar","app.jar"]