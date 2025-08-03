import tempfile
import os

def save_and_deduplicate_bibtex(entries, bib_filename="unique_references.bib", txt_filename="unique_references.txt"):
    # Save all to temp file
    temp_bibtex_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
    for entry in entries:
        if entry.strip():
            temp_bibtex_file.write(entry.strip())
            temp_bibtex_file.write("\n" + "="*80 + "\n")
    temp_bibtex_file.close()

    temp_path = temp_bibtex_file.name
    print(f"📁 Temp BibTeX written to: {temp_path}")

    # Read and deduplicate
    with open(temp_path, 'r', encoding='utf-8') as f:
        all = f.read()
    parts = all.split("\n" + "="*80 + "\n")
    unique = list(set(p.strip() for p in parts if p.strip()))

    # Save .bib
    with open(bib_filename, 'w', encoding='utf-8') as f:
        for e in unique:
            f.write(e + "\n\n")
    print(f"✅ Saved {len(unique)} unique entries to {bib_filename}")

    # Save .txt
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for e in unique:
            f.write(e + "\n---\n")
    print(f"✅ Saved {len(unique)} unique entries to {txt_filename}")

    # Cleanup
    os.remove(temp_path)
    print(f"🧹 Temp file cleaned up.")
