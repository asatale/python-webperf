.PHONY: all
all:

FRAMEWORK ?= flask

.PHONY:build
build:
ifeq ($(FRAMEWORK), flask)
	@echo "DOCKERFILE=dockerfiles/Dockerfile.flask" > .env
	@docker-compose build
else
ifeq ($(FRAMEWORK), fastapi)
	@echo "DOCKERFILE=dockerfiles/Dockerfile.fastapi" > .env
	@docker-compose build
else
	$(error "Unsupported framework $(FRAMEWORK)")
endif
endif
