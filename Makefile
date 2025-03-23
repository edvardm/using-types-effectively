DOC := ute.qmd
COMPILED_DOC := _site/index.html
STATIC_DIR := _site/static

YELLOW := \033[1;33m
RESET := \033[0m

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

.PHONY: .post-trim
.post-trim:
	gsed -i /fmt\:/d $(COMPILED_DOC)

$(STATIC_DIR)/code.zip:
	mkdir -p $(STATIC_DIR) ; zip -r $@ examples/*.py

.PHONY: render
render: $(COMPILED_DOC) ## render document to single markup file

.PHONY: test
test: $(COMPILED_DOC)
	pytest --ff -x --markdown-docs $< tests

$(COMPILED_DOC): $(DOC) custom.scss _quarto.yml $(wildcard examples/*.py)
	quarto render $< -o index.html

.PHONY: fmt
fmt: ## format code
	ruff format examples/*.py

.PHONY: lint
lint: ## lint code
	ruff check --fix **/*.py
	mypy examples/

.PHONY: export-md
export-md: $(COMPILED_DOC).gz

$(COMPILED_DOC).gz: $(COMPILED_DOC)
	gzip < $< > $@

.PHONY: clean
clean:  ## clean artifacts
	rm -f *.gz **/*.pyc
	rm -rf **/__pycache__/


.PHONY: export
 export: ## export relevant files to .tar.gz
	git ls-files --exclude-standard | tar -cvzf ute.tar.gz -T -

.PHONY: zip
zip: render
	rm -f site.zip ; zip -r site.zip _site/
