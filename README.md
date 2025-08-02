# bibfixer

A Python tool for extracting references from research papers (PDF) and generating clean BibTeX files using AI-assisted citation parsing and trusted metadata sources.

## 🔧 Features
- Extracts the reference section from uploaded PDFs
- Parses citations using GROBID
- Fetches BibTeX from Crossref, arXiv, Semantic Scholar, and INSPIRE-HEP
- Deduplicates and validates references
- Outputs a cleaned `.bib` file

## ⚙️ How It Works
1. Upload a research paper (PDF)
2. Extract the references section
3. Parse each citation using GROBID
4. Search for matching BibTeX entries using the parsed title
5. Save the final structured `.bib` file

## 🛠️ Dependencies
- Python 3
- PyMuPDF
- GROBID server (running locally or via Docker)
- `requests`, `re`, `xml.etree`

## 🚧 Known Limitations
- **GROBID token limit** may skip long entries
- **Metadata Extraction Failure** for some malformed citations
- **Citation Block Misidentification**: full paper body may be misparsed as a citation
- Occasional false positives and duplicate detection errors
- Requires internet for metadata lookup
- No GUI (yet) — CLI/Colab-based interface only

## 💻 Installation
This project currently runs in Google Colab.

> 🛠 A proper installation/setup guide will be added once a standalone version is finalized.

## 📌 Demo
Run it on [Google Colab](https://colab.research.google.com/drive/1eimeMU1geWOS94y3Vx8hnUZ5wZIWMd-e?usp=sharing)

---

## ✍️ Author
**Aritra Basak**  
Physics student · Creative technologist · Poetic glitch hunter  
[GitHub](https://github.com/Aritra1122) · [LinkedIn](https://www.linkedin.com/in/aritra-basak-6090b127a)

## 📝 License
MIT
