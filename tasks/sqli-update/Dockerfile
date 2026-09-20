FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /src
COPY pom.xml .
RUN mvn -q dependency:go-offline
COPY src src
RUN mvn -q package -DskipTests
FROM eclipse-temurin:17-jre
COPY --from=build /src/target/sqli-update-1.0.jar /app.jar
EXPOSE 80
ENTRYPOINT ["java","-jar","/app.jar"]
