FROM golang:1.20-alpine
WORKDIR /app
COPY go.mod /app/go.mod
RUN go mod download || true
COPY cmd /app/cmd
RUN go build -o /app/bin/llm-gateway /app/cmd/main.go
EXPOSE 8080
CMD ["/app/bin/llm-gateway"]