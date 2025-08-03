# Known Bugs & Issues

## 2025-08-02

### 🐞 1. Metadata Extraction Failure  

For some citations, the parsed output contains `None` for all or some of the major fields (`authors`, `title`, `DOI`, `journal`, etc.), even though the citation is clearly present in the paper.


**Sample Output:**

```json
{
  "authors": null,
  "doi": null,
  "journal": null,
  "note": "INSPIRE",
  "pages": null,
  "title": null,
  "volume": null,
  "year": null
}
```
Suspected Cause: GROBID misinterpretation or failure of metadata fetch from citation APIs.

### 🐞 2. Citation Block Misidentification  
When extracting references from a paper with 78 citations, the tool extracted 79 — the first "citation" was actually a large chunk of the paper body text.  
- Effect: This falsely increases the citation count and pollutes BibTeX.  
- Cause: Improper reference block boundary detection during parsing.

**🔍 Preview of First 3 References:**

```text
1. , masses [11–16] and spins [16–18], the redshift dependence of the BH merger rate...  
2. LIGO Scientific and Virgo collaborations, Observation of Gravitational Waves...  
3. LIGO Scientific and Virgo collaborations, GW151226: Observation of Gravitational Waves...
```

⚠️ Internet search only succeeds when the parser correctly extracts the title.

```markdown
================================================================================

📘 Entry 25: New constraints on primordial black holes abundance from femtolensing of gamma-ray bursts
✅ BibTeX Found.

================================================================================

❌ Entry 26: No title found.

📘 Entry 27: Femtolensing by dark matter revisited
✅ BibTeX Found.

================================================================================
```
For entries like 26, where parsing fails, the search also fails — proving the issue lies in extraction, not in missing data.

### 🐞 3. Deduplication Logic Failure  
The deduplication algorithm falsely flags distinct citations as duplicates, even in published papers.  
- Consequence: Unique references get removed or misgrouped.  
- Status: Needs complete rework or disabling.

**🧪 Console Log Preview:**
```text
Total extracted entries from temporary file: 64  
Number of unique entries after de-duplication: 58  
```

### 🐞 4. Unknown GROBID Token Limit  
GROBID might have a token/character limit when parsing large blocks of citations, but its exact threshold is unknown.  
- Effect: Some citations may be silently skipped or incomplete without warning.  
- Next Step: Benchmark token tolerance and build token-aware batching.
---

