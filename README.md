![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fartpelling%2Ffa26-hrtf-ssm%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21727073.svg)](https://doi.org/10.5281/zenodo.21727073)

# Code for Numerical Experiments in "State-space modelling of head-related transfer functions"

> Art J. R. Pelling, Ennes Sarradj
> **State-space modelling of head-related transfer functions**, Forum Acusticum 2026.

This repository contains code for numerical experiments reported in the accompanying Forum Acusticum 2026 paper.

To run the experiments and create the plots, Python 3.13, [uv](https://docs.astral.sh/uv/), and `make` are needed. The first data-backed command downloads the FABIAN dataset and caches it in `data/`.

```shell
make results  # compute the numerical results
make figures  # create figures from the results
make paper    # create figures and build the paper
make clean    # remove generated artifacts and LaTeX build output
```

Results are written to `generated/data/`; figures are written to `generated/figures/`.
