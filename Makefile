COMPILED_DOC := ute.md
TMPL := tmpl.md

YELLOW := \033[1;33m
CYAN := \033[1;36m
RESET := \033[0m

.PHONY: help
help: ## show this help
	@echo ""
	@echo "$(CYAN)Available targets:$(RESET)"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | \
		grep -v '^\.''[^:]*' | \
		sort | \
		awk -F':.*?## ' '{printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""


.PHONY: dev-init
dev-init: .venv .copy-sample-direnv ## setup project
	@echo "remember to activate .venv (or prefix commands with 'uv')"

.PHONY: .copy-sample-direnv
	@cp -n .envrc.sample .envrc || echo ".envrc exists, skipping"

.venv:
	uv sync --frozen --no-install-workspace --python 3.10

.PHONY: build
build: fmt lint render ## build project

.PHONY: render
render: $(COMPILED_DOC)

$(COMPILED_DOC): $(TMPL)
	pandoc --filter pandoc-include $< -t markdown > $@ 2> /dev/null

.PHONY: test
test: $(COMPILED_DOC)
	pytest --ff -x --markdown-docs $< tests

.PHONY: fmt
fmt: ## format code
	ruff format **/*.py

.PHONY: lint
lint:
	ruff check --fix src/*.py

watch: delay?=5
watch:
	watchexec -d $(delay)s -w $(TMPL) -w Makefile -w src/ $(MAKE) -j4 build

.PHONY: export
export: $(COMPILED_DOC).gz

$(COMPILED_DOC).gz: $(COMPILED_DOC)
	gzip < $< > $@

.PHONY: clean
clean:
	rm -f *.gz **/*.pyc
	rm -rf **/__pycache__/
