import fitz
import re

def extract_references_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    ref_text = ""
    ref_started = False
    headings = ["References", "Bibliography", "Works Cited", "Citations"]

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        lines = page.get_text().split('\n')

        for line in lines:
            if ref_started:
                ref_text += line + "\n"
            else:
                for heading in headings:
                    if re.search(r"\b" + re.escape(heading) + r"\b", line, re.IGNORECASE):
                        ref_started = True
                        ref_text += line + "\n"
                        break
    return ref_text.strip()
