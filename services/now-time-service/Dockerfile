FROM gradle:9-jdk21-alpine AS build

WORKDIR /home/gradle/project

COPY settings.gradle build.gradle ./
COPY src ./src

RUN gradle --no-daemon bootJar

FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

RUN addgroup -S app && adduser -S app -G app

COPY --from=build /home/gradle/project/build/libs/*.jar /app/app.jar

USER app
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
