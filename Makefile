GENERATED_DATA_DIR := generated/data
HSV_MAPS := $(GENERATED_DATA_DIR)/hsv-map.npy $(GENERATED_DATA_DIR)/hsv-map-itd-removed.npy
BOUND_ERROR_RESULTS := $(GENERATED_DATA_DIR)/bound-error.npz
EXPERIMENT_VALUES := $(GENERATED_DATA_DIR)/experiment-values.tex
RESPONSES_RESULTS := $(GENERATED_DATA_DIR)/responses.npz
RESULTS := $(HSV_MAPS) $(BOUND_ERROR_RESULTS) $(RESPONSES_RESULTS)
HSV_FIGURES := generated/figures/hsv-map.pdf generated/figures/hsv-map-itd-removed.pdf
BOUND_ERROR_FIGURES := generated/figures/bound-error.pdf generated/figures/bound-error-legend.pdf
SCALABILITY_FIGURE := generated/figures/scalability.pdf
RESPONSES_FIGURES := generated/figures/responses-itd-removed-time.pdf generated/figures/responses-frequency.pdf generated/figures/responses-legend.pdf
FIGURES := $(HSV_FIGURES) $(SCALABILITY_FIGURE) $(BOUND_ERROR_FIGURES) $(RESPONSES_FIGURES)

.PHONY: all results figures paper clean

all: paper

results: $(RESULTS)

figures: $(FIGURES)

$(GENERATED_DATA_DIR)/hsv-map.npy: src/hsv_map.py src/utils.py
	uv run compute-hsv-map

$(GENERATED_DATA_DIR)/hsv-map-itd-removed.npy: src/hsv_map.py src/utils.py
	uv run compute-itd-removed-hsv-map

$(BOUND_ERROR_RESULTS): src/bound_error.py src/utils.py
	uv run compute-bound-error

$(HSV_FIGURES) &: $(HSV_MAPS) src/hsv_map.py src/plotting.py src/utils.py
	uv run hsv-map --no-show

$(SCALABILITY_FIGURE): src/scalability.py src/plotting.py
	uv run scalability --no-show

$(BOUND_ERROR_FIGURES) &: $(BOUND_ERROR_RESULTS) src/bound_error.py src/plotting.py src/utils.py
	uv run bound-error --no-show

$(RESPONSES_RESULTS): src/responses.py src/utils.py
	uv run compute-responses

$(RESPONSES_FIGURES) &: $(RESPONSES_RESULTS) src/responses.py src/plotting.py
	uv run responses --no-show

$(EXPERIMENT_VALUES): $(BOUND_ERROR_RESULTS) src/bound_error.py src/utils.py
	uv run export-experiment-values

paper: figures $(EXPERIMENT_VALUES)
	mkdir -p paper/build
	cd paper && latexmk main.tex

clean:
	cd paper && latexmk -C main.tex
	find generated paper/tikz -type f ! -name '.keep' -delete 2>/dev/null || true
	find generated paper/tikz -depth -type d -empty -delete 2>/dev/null || true
