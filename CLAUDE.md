# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SHS** is the corrections and research repository for the Cologne digitization of Tara Nath Tarkavachaspati's *Shabda-Sagara* (Sanskrit-English dictionary, 1900). The canonical source lives in `csl-orig/v02/shs/shs.txt`.

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/SHS/issues).

## Common Commands

### Apply line-level corrections (standard pattern)
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh shs ../../SHSScan/2020
sh xmlchk_xampp.sh shs
```

## Dependencies

- **Python 3**
- **shs.txt** — in `$BASE/cologne/csl-orig/v02/shs/shs.txt`
