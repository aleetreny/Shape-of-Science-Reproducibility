# Reproduction boundary and file selection

QSS requires the data essential to reproduce the key findings in a public repository providing a persistent identifier. Code sharing is strongly recommended. This is a requirement about evidence and access, not about retaining every computational cache. GitHub alone does not provide the journal's requested archival dataset identifier; this release therefore has a separate DOI archive. Source: [QSS submission guidelines](https://direct.mit.edu/qss/pages/submission-guidelines), official indexed text consulted 21 September 2026 and subsequently confirmed by reading the official page directly in the browser on the same date.

## What is retained and why

| Evidence | Retained files | Purpose |
| --- | --- | --- |
| Corpus and identities | `data/analysis_ready_v1/metadata.parquet`, `public_metadata/`, selection/query/candidate arrays | Identify the exact records, areas, periods, flags and sampled articles; retain input hashes without redistributing abstracts. |
| Broad structure | `data/analysis_v1/shape/`, macro controls, `data/robustness_v2/centroid_scales/`, closure centre measurements | Preserve model-pair measurements and repetitions; recalculate centre summaries and size/omission controls. |
| Neighbours | Per-query `shared_counts.npy`, query IDs, cell summaries and control measurements | Recalculate overlaps from integer intersections; inspect query-level variation. Nearest-neighbour identities themselves are excluded caches. |
| Text and pooling | Pilot and expanded comparison measurements, repeated effects, stability data, configurations | Repeat the reported statistical contrasts and distinguish the 26k pilot from the 52k expansion. |
| Geometry | Per-model/per-area/per-selection metrics, contrast arrays and selections, original and centered measurements | Repeat all area-pair classifications, effect cutoffs, retained opposing model pairs and alternative dimension comparisons. |
| Other controls | Time, discipline, families, quality, source examples and recorded alerts | Preserve the evidence for qualifications and supplementary comparisons rather than distributing only favorable summaries. |
| Implementation | Scientific source, pinned dependencies/model versions, protocols and source snapshots | Inspect how upstream quantities were defined; run the tested statistical entry points. |

`SELECTION.json` is the exact machine-readable list. Scientific data files are copied byte for byte from the previously verified frozen archives. The selection does not change scientific results, sampling rules, models or thresholds.

## Verification coverage

- The standard-library check recomputes aggregations for the four main figures.
- The full statistical check regenerates 25 closure tables, compares 106,445 rows, and checks 17,550 local neighbour scores from per-query counts, plus the balanced global/local averages.
- All supplied data are checked against source SHA-256 hashes before the statistical check.
- Other historical measurements and reports remain inspectable, but a fresh rerun of every historical supplementary analysis has not been certified.

## Deliberate limits

The release starts from frozen model-derived measurements. It cannot rederive all those measurements from embeddings because embedding shards and neighbour-list caches are omitted. It cannot exactly repeat historical inference from text because plaintext input tables are not distributed. OpenAlex rehydration can drift. These limitations must also be stated in the manuscript's availability section. This is a proposed implementation of the journal's data policy, not a guarantee of editorial acceptance.

## Repository choice

GitHub provides versioned source, automated checks and reliable release downloads. Figshare is a valid alternative with versioned DOIs and 20 GB of free personal storage, but changing services is not necessary for this compact deposit. Here GitHub Actions transfers the selected assets directly to Zenodo; the failed long uploads from the author's terminal are avoided. The original 51 GB draft remains unpublished and is not the cited record.

References: [GitHub release limits](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases), [Figshare storage](https://help.figshare.com/article/paid-services), [Figshare DOIs](https://help.figshare.com/article/guide-to-sharing-nih-funded-research-on-figshare-com), [Zenodo deposit API](https://developers.zenodo.org/).
