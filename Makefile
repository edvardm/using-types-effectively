DOC := ute.qmd
COMPILED_DOC := _site/ute.html
STATIC_DIR := _site/static

YELLOW := \033[1;33m
RESET := \033[0m

# Detect OS and set SED command accordingly
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    SED := gsed
else
    SED := sed
endif

.PHONY: help
help: ## show this help
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | \
		grep -v '^\.''[^:]*' | \
		sort | \
		awk -F':.*?## ' '{printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""

all: build

.PHONY: dev-init
dev-init: .venv .copy-sample-direnv .make-setup-quarto ## setup project
	@echo "remember to activate .venv (or prefix commands with 'uv')"


.PHONY: .make-setup-quarto
.make-setup-quarto:
	@command -v quarto > /dev/null 2>&1 || brew install quarto
	# TODO: idempotent way of adding modules
	# quarto add --no-prompt shafayetShafee/add-code-files
	touch $@



.PHONY: .copy-sample-direnv
	@cp -n .envrc.sample .envrc || echo ".envrc exists, skipping"

.venv:
	uv sync --frozen --no-install-workspace --python 3.10

.PHONY: build
build: fmt lint render $(STATIC_DIR)/code.zip .post-trim ## build project

.PHONY: publish
publish: fmt lint  ## publish to gh-pages
	quarto publish --no-render gh-pages

.PHONY: .post-trim
.post-trim:
	$(SED) -i /fmt\:/d $(COMPILED_DOC)

$(STATIC_DIR)/code.zip:
	mkdir -p $(STATIC_DIR) ; zip -r $@ examples/*.py

.PHONY: render
render: $(COMPILED_DOC) ## render document to single markup file

.PHONY: test
test: $(COMPILED_DOC)
	pytest --ff -x --markdown-docs $< tests

$(COMPILED_DOC): $(DOC) custom.scss _quarto.yml $(wildcard examples/*.py)
	quarto render $< -o ute.html

.PHONY: fmt
fmt: ## format code
	ruff format examples/*.py

.PHONY: lint
lint: ## lint code
	ruff check --fix **/*.py
	mypy examples/

.PHONY: clean
clean:  ## clean artifacts
	rm -f *.gz **/*.pyc
	rm -rf **/__pycache__/

.PHONY: export
 export: ## export relevant files to .tar.gz
	git ls-files --exclude-standard | tar -cvzf ute.tar.gz -T -
