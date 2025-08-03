import os
from src.setup_grobid import wait_for_grobid
from src.extract_refs import extract_references_from_pdf
from src.parse_refs import split_reference_entries, parse_single_citation, extract_fields_from_biblStruct
from src.fetch_bibtex import find_bibtex
from src.deduplicate import save_and_deduplicate_bibtex

def main():
    # === Step 1: Start Grobid ===
    print("⚙️ Starting Grobid...")
    wait_for_grobid()

    # === Step 2: Upload & extract references ===
    pdf_path = "sample.pdf"  # Replace with path to your actual PDF

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF file '{pdf_path}' not found. Please provide a valid path.")

    print(f"📄 Extracting references from {pdf_path}...")
    ref_text = extract_references_from_pdf(pdf_path)

    # === Step 3: Split and parse references ===
    ref_entries = split_reference_entries(ref_text)
    print(f"🔍 Total references found: {len(ref_entries)}")

    print("📤 Sending to Grobid for parsing...")
    xml_all = "\n".join([parse_single_citation(ref) for ref in ref_entries if ref])
    results = extract_fields_from_biblStruct(xml_all)
    print(f"✅ Parsed {len(results)} structured entries.")

    # === Step 4: Fetch BibTeX entries ===
    print("🔁 Fetching BibTeX entries...")
    bib_entries = []
    for i, entry in enumerate(results, 1):
        title = entry.get("title")
        if not title:
            print(f"⚠️ Entry {i}: No title found.")
            continue

        print(f"📘 ({i}/{len(results)}) Searching BibTeX for: {title}")
        bib = find_bibtex(title)
        if bib:
            print("   ✅ BibTeX found.")
            bib_entries.append(bib)
        else:
            print("   🚫 BibTeX not found.")

    # === Step 5: Save and deduplicate ===
    print("💾 Saving and deduplicating BibTeX entries...")
    save_and_deduplicate_bibtex(bib_entries)
    print("🎉 Done.")

if __name__ == "__main__":
    main()
