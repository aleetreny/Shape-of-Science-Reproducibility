# Shape of Science: compact reproducibility release

Version **1.1.0**, 21 September 2026. Author: **Alejandro Treny Ortega**, independent researcher.

This distribution accompanies *How much does the map of science depend on the embedding model?* It provides scientific code and frozen analysis data for repeating the statistical comparisons. It does not include the manuscript or supplements.

- Dataset identifier (reserved; archival transfer in progress): [10.5281/zenodo.22876602](https://doi.org/10.5281/zenodo.22876602).
- [Versioned downloads](https://github.com/aleetreny/Shape-of-Science-Reproducibility/releases/tag/v1.1.0).
- [Source repository](https://github.com/aleetreny/Shape-of-Science-Reproducibility).
- Original scientific code snapshot: [cc61517](https://github.com/aleetreny/Shape-of-Science-Robustness/commit/cc61517dc2ea1e946c4fe391c4fcc80fa6e4819f). Scientific programs in this distribution retain their original contents. New reproduction and delivery utilities are identified separately.

## What to download

Download `code-and-guides.zip`, every `data-*.zip`, and `release-manifest.json` from the same release. Extract all ZIP files into **one new directory**. Their internal paths fit together; do not extract over an existing research checkout. The same assets are being transferred to the DOI archive above; GitHub downloads are already public. The article can be revised independently of these frozen data.

The data include the 500,000-record non-text metadata table; exact identifiers and sample selections; per-query neighbour intersection counts; per-model, area and repetition measurements; geometric measurements before and after centering; input, pooling, quality and other controls. `SELECTION.json` records every included file's origin and hash, together with the omitted historical files and reasons.

Excluded: model embedding shards, cached centre vectors, cached nearest-neighbour lists, model weights, plaintext title/abstract input tables, manuscripts, supplements, and internal work records. These exclusions reduce storage without removing the measurements used by the public statistical checks. They do mean that this route begins **after model inference and metric calculation**.

## Quick check: no dependencies or data downloads

With Python 3.12 or later, from the code directory:

```sh
python3 -I -S reproducibility/reproduce_summaries.py
```

This uses bundled per-condition inputs to recompute the principal aggregations of all four main figures. It works offline with Python's standard library.

## Recompute the statistical analyses

After extracting the data ZIPs beside the code:

```sh
python3.12 -m venv .venv-reproduce
.venv-reproduce/bin/python -m pip install -r requirements-analysis.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  .venv-reproduce/bin/python reproducibility/reproduce_analysis.py
```

The command first checks every supplied data file against its SHA-256 hash. It then recomputes **25 result tables (106,445 rows)** covering centres, text/model comparisons, geometric ordering, centering, alternative dimensions and quality filtering. It compares them with separate frozen reference tables. It also checks **17,550 local neighbour scores** directly from per-query intersection counts, recalculates the balanced local/global neighbour agreement, and runs the four-figure quick check. Results go into a new `reproduced/` directory; source data and reference reports remain untouched.

Integer counts and labels must match exactly. The CSV comparison tolerances are 1e-10 absolute and relative; neighbour checks use 1e-12 absolute. In the tested run, all 106,445 recomputed CSV rows matched the saved text exactly. See `REPRODUCTION_CHECK.json` and [coverage](COVERAGE.md). The test used the author's Python 3.12 analysis environment; the full statistical check also passed in a fresh Python 3.12 environment on Linux, with every CSV cell identical. See the [public verification run](https://github.com/aleetreny/Shape-of-Science-Reproducibility/actions/runs/35610529164) and [machine-readable receipt](reproducibility/verification-linux-v1.1.0.json). A complete rerun of every historical supplementary analysis is not claimed.

## Recomputing embeddings is a separate route

The source code, model revisions, seeds, pooling settings, corpus identities and text hashes are supplied. Historical title/abstract input tables are not redistributed because rights to the plaintext abstracts have not been established. Re-querying OpenAlex may return changed or unavailable text, so the identifiers alone cannot guarantee an identical historical inference run. Model weights must be obtained from their original providers under their terms.

This release supports exact reproduction of the documented **statistical calculations from frozen model-derived measurements**, not an independently certified rerun from historical texts to embeddings and all downstream outputs. The retained historical executors may require excluded caches or their original environment. Use the public commands above for the tested route; do not interpret a historical 'already complete' message as a new calculation.

## Licenses and citation

Original code is MIT. Original numerical results and documentation are CC BY 4.0. OpenAlex metadata retain CC0. Third-party model rights are unchanged. See `LICENSE`, `LICENSING.md` and `reproducibility/THIRD_PARTY.md`.

Cite this version as: Treny Ortega, A. (2026). *How much does the map of science depend on the embedding model? Compact reproducibility data and code* (Version 1.1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22876602
