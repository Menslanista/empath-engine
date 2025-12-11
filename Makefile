.PHONY: init dev-up dev-down build-emotion build-narrative build-llm build-character build-services test-emotion generate-proto

init: build-services generate-proto
	@echo "ready"

build-emotion:
	cd services/emotion-inference && pip install -r requirements.txt

build-narrative:
	cd services/narrative-director && npm install --omit=dev

build-llm:
	cd services/llm-gateway && go mod download || true && go build -o bin/llm-gateway cmd/main.go

build-character:
	cd services/character-memory && pip install -r requirements.txt

build-services: build-emotion build-narrative build-llm build-character

dev-up:
	docker-compose up -d

dev-down:
	docker-compose down

test-emotion:
	curl -s http://localhost:8000/health

generate-proto:
	@if exist "scripts\generate-proto.bat" ( \
		call scripts\generate-proto.bat \
	) else ( \
		sh scripts/generate-proto.sh \
	)
