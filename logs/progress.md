# 🧪 Progress Log — CitationCleaner
Tracking development progress of the reference extraction and BibTeX generation tool.

---

### 📅 August 2, 2025

#### ✅ Grobid Server Automation
- Installed Grobid via shell commands inside Colab
- Added `wait_for_grobid()` to automatically pause until the server is ready

#### ✅ PDF Parsing & Reference Extraction
- Used PyMuPDF to extract text from uploaded PDFs
- Implemented logic to detect start of references using keywords:
  `References`, `Bibliography`, `Works Cited`, `Citations`

#### ✅ Reference Entry Splitting (Flexible)
- Supported both `[n]`-style and `1.` or `•` bullet style splitting
- Cleaned and filtered entries based on length and spacing

#### ✅ Citation Structuring via Grobid
- Sent each entry to Grobid `/processCitation` API
- Parsed structured XML data fields:
  - Title
  - Authors (with org/personal support)
  - Journal, Volume, Pages, Year, DOI

#### ✅ BibTeX Fetching Pipeline
- Integrated search-based BibTeX fetching using:
  - CrossRef
  - Semantic Scholar
  - arXiv
  - InspireHEP
- All done via title-based search

#### ✅ BibTeX Deduplication and Output
- Saved BibTeX entries to a temp `.txt` file
- Removed duplicates using Python `set()`
- Output to:
  - `unique_references.bib` for LaTeX
  - `unique_references.txt` for reading

#### ✅ Auto File Download in Colab
- Added `files.download()` to let user retrieve results directly

---
