from src.setup_grobid import wait_for_grobid
from src.extract_refs import extract_references_from_pdf
from src.parse_refs import split_reference_entries, parse_single_citation, extract_fields_from_biblStruct
from src.fetch_bibtex import find_bibtex
from src.deduplicate import save_and_deduplicate_bibtex

# Step 1: Start Grobid
wait_for_grobid()

# Step 2: Upload & extract references (replace this with actual PDF path in non-colab)
ref_text = extract_references_from_pdf("sample.pdf")

# Step 3: Split and parse
ref_entries = split_reference_entries(ref_text)
xml_all = "\n".join([parse_single_citation(ref) for ref in ref_entries if ref])
results = extract_fields_from_biblStruct(xml_all)

# Step 4: Fetch BibTeX entries
bib_entries = []
for entry in results:
    title = entry.get("title")
    if not title:
        continue
    bib = find_bibtex(title)
    if bib:
        bib_entries.append(bib)

# Step 5: Save + deduplicate
save_and_deduplicate_bibtex(bib_entries)
