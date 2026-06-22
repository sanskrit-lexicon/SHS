# SHS — *Shabda-Sagara* (Śabda-sāgara) (1900)

Development and correction repository for **Kulapati Jibananda Vidyāsāgara's *Shabda-Sagara, or A Comprehensive Sanscrit-English Dictionary***, a Sanskrit→English dictionary, part of the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL). The canonical source text lives in [`csl-orig/v02/shs/shs.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/shs/shs.txt) (46,730 entries); this repository holds the development, correction, and enrichment work.

Empirically a descendant of Wilson (WIL ⊆ SHS ≈ 0.953 by headword containment) in the CDSL genealogy.

## Documentation

- [CLAUDE.md](CLAUDE.md) — repository guide and data-format reference.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — markup tag reference.
- [CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Contents

| Path | Purpose |
|---|---|
| `issues/` | Per-issue working files |
| `prefaces/` | Front-matter OCR (title + abbreviations) with EN + RU — see [Front matter](#front-matter-prefaces) below |

## Front matter (`prefaces/`)

Faithful OCR + translation of the dictionary's **front matter** — the **title page** and the **List of Abbreviations** — from the Cologne scans, with a Russian translation of each page. Source language is **English**, so the base per-page `.md` is the English edition and each page also has a `.ru.md`. Digitizer header/footer stamps are omitted.

- Cologne source: <https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/shspref.html>
- Consolidated editions: [prefaces/shspref_all.en.md](prefaces/shspref_all.en.md) · [prefaces/shspref_all.ru.md](prefaces/shspref_all.ru.md)
- In-folder index: [prefaces/README.md](prefaces/README.md)
- Imprint found: *First Edition, Calcutta 1900*, Calcutta Press (No. 8 Bowbazar Street), printed by Mookerjee & Co.; published by Ashu Bodha & Nitya Bodha Bhattacharyya.
- The Abbreviations page includes a Devanāgarī **साङ्केतिकाः शब्दाः** table (सङ्केतः → सङ्केतबोधः); its left abbreviation column is cut off in the binding margin of the scan and is marked `[?]`.

<details>
<summary><strong>OCR run notes (2026-06-22)</strong> — cost, timing, and technical lessons</summary>

Produced by the `/cologne-preface-ocr` skill (vision OCR + translation). Process retrospective, not part of the deliverable.

**Method.** Done on the **main thread** (one dictionary at a time), not via parallel subagents: an earlier attempt that fanned out ~26 background OCR agents at once failed wholesale — long vision turns died on "Connection closed", the burst tripped a 403 auth/concurrency ceiling, and the flood of scan downloads temporarily **IP-blocked us at sanskrit-lexicon.uni-koeln.de**. Lesson: OCR these gently and sequentially, never in a large parallel burst.

**Cost.** 2 pages, main-thread native-resolution cropping. The title page is large type (read from a thumbnail + native-res crops of the imprint); the Abbreviations page is dense (a two-column English list + a clipped/torn Devanāgarī table) and dominated the effort — ~30 native-res crop reads.

**Technical lessons (reusable):** (1) The scans are 3540×4960 `.jpg`; crop to ≤1900 px and never upscale past 2000. (2) The leftmost Devanāgarī abbreviation column sits in the binding and is physically cut off — unrecoverable, marked `[?]` rather than invented. (3) A binding tear crosses the right English column and the Devanāgarī table; native crops still resolve the text. (4) Thumbnail reads mis-rendered "Parasmaipada"/"Penultimate" as "Paramaipada"/"Penultinate" — native crops corrected them.

</details>

## Timeline

| Period | Activity |
|---|---|
| 2025 | Repository activity begins (first tracked issues) |
| 2026-05 | Issue taxonomy, citation metadata, documentation |
| 2026-06 | Front-matter OCR + EN/RU translation of the prefaces (`prefaces/`) |

## Projects & Milestones

| Milestone | Open | Closed | Total |
|---|---|---|---|
| Dictionary to Book | 0 | 0 | 0 |
| Digitization Quality | 1 | 0 | 1 |
| Structured Data | 1 | 1 | 2 |
| Major Enhancements | 1 | 0 | 1 |
| **Total** | **3** | **1** | **4** |

```mermaid
pie showData
  title SHS issues by milestone
  "Digitization Quality" : 1
  "Structured Data" : 2
  "Major Enhancements" : 1
```

## Issues

```mermaid
pie showData
  title SHS issues by type
  "content-enhancement" : 1
  "question" : 1
  "markup" : 1
  "encoding" : 1
```

### Open

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| 1 | EOL hyphen | encoding | minor | Digitization Quality |
| 3 | Questions for Andhrabharati | question | minor | Structured Data |
| 4 | docs-pass: SHS documentation review | content-enhancement | medium | Major Enhancements |

### Solved

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| 2 | [markup] Minor shs.txt Markup Oddities | markup | minor | Structured Data |

## Labels

### Type labels

| Label | Meaning |
|---|---|
| `link-target` | Click-throughs from `<ls>` abbreviations to scanned PDF pages |
| `link-splitting` | Splitting combined `SOURCE N,N` refs into per-page links |
| `markup` | Normalising XML tag content |
| `text-correction` | Corrections to English/Sanskrit definitions or headwords |
| `content-enhancement` | New material or structural additions beyond correction |
| `encoding` | SLP1/IAST transcoding, character normalisation |
| `scan-quality` | Replacing blurry/skewed/missing scan pages |
| `bug` | Broken links, XML errors, broken downloads |
| `question` | Scholarly questions requiring research |

### Severity labels

| Label | Meaning |
|---|---|
| `minor` | Targeted fix — a handful of lines or a single file |
| `medium` | Standard unit of work — one batch of corrections |
| `hard` | Large effort spanning many sources or files |

## Contributors

| Contributor | Commits |
|---|---|
| drdhaval2785 | 14 |
| gasyoun (Mārcis Gasūns) | 2 |
| funderburkjim | 2 |

## Source

- **Author**: Vidyāsāgara, Kulapati Jibananda
- **Title**: *Shabda-Sagara, or A Comprehensive Sanscrit-English Dictionary*
- **Place / Publisher**: Calcutta
- **Year(s)**: 1900
- **Language pair**: Sanskrit → English
- **Size (CDSL headword index)**: 46,730 entries
- **License (digital edition)**: CC BY-SA 4.0
- See [CITATION.cff](CITATION.cff) for machine-readable citation.

## Encoding

- UTF-8 (NFC) throughout.
- Sanskrit text in SLP1 transliteration, wrapped in `{#…#}`; English gloss / italic display text in `{%…%}`.
- Devanāgarī and IAST display forms are generated at display time, not stored in the source.

## How it works

```mermaid
flowchart LR
  S["Print scan"] -->|keyboarding| O["csl-orig/v02/shs/shs.txt"]
  O -->|updateByLine.py| C["change_*.txt corrections"]
  C --> O
  O -->|csl-pywork build| X["shs.xml"]
  X --> A["csl-app web display"]
```

---
*Issue taxonomy and documentation per the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md).*
