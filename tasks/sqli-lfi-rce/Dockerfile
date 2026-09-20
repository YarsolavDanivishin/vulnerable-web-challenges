FROM golang:1.23-bookworm AS build
WORKDIR /src
COPY go.mod .
COPY main.go .
RUN go mod tidy
RUN CGO_ENABLED=0 go build -o /challenge .
FROM debian:bookworm-slim
COPY --from=build /challenge /challenge
EXPOSE 80
ENTRYPOINT ["/challenge"]
