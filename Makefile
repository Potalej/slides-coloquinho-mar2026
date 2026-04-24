# Makefile para compilar LaTeX com temporarios no build/
# Usa pdfLaTeX
# Exemplo:
# make ARQUIVO=main

# Nome do arquivo ARQUIVO passado pelo terminal
ARQUIVO ?= main

BUILD_DIR := build
$(shell mkdir -p $(BUILD_DIR))

ARQ_DIR  := $(dir $(ARQUIVO))
ARQ_BASE := $(notdir $(ARQUIVO))

PDF := $(ARQ_BASE).pdf

all:
	@echo "Compilando $(ARQUIVO).tex..."
	-@pdflatex -interaction=nonstopmode \
		-output-directory=$(BUILD_DIR) \
		$(ARQUIVO).tex

	-@if grep -q "Package biblatex" $(BUILD_DIR)/$(ARQ_BASE).log 2>/dev/null; then \
		echo "Rodando biber..."; \
		biber $(BUILD_DIR)/$(ARQ_BASE); \
	fi

	-@pdflatex -interaction=nonstopmode -output-directory=$(BUILD_DIR) $(ARQUIVO).tex
	-@pdflatex -interaction=nonstopmode -output-directory=$(BUILD_DIR) $(ARQUIVO).tex

	@echo "Movendo PDF para pasta principal..."
	@cp $(BUILD_DIR)/$(PDF) ./

clean:
	rm -f $(BUILD_DIR)/* $(PDF)
