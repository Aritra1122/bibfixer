import re
import requests
import xml.etree.ElementTree as ET

def split_reference_entries(ref_section_text):
    entries = re.findall(r"\[\d+\]\s*(.*?)(?=\n\[\d+\]|\Z)", ref_section_text, re.DOTALL)
    if not entries:
        entries = re.split(r'\n(?=\s*\d+\.|\s*•)', ref_section_text)
    return [re.sub(r'\s+', ' ', ref.strip()) for ref in entries if len(ref.strip()) > 30]

def parse_single_citation(citation):
    response = requests.post(
        "http://localhost:8070/api/processCitation",
        data={"citations": citation, "consolidateCitations": "1"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    if response.status_code != 200:
        print(f"❌ Failed on: {citation[:60]}...")
        return None
    return response.text

def extract_fields_from_biblStruct(xml_string):
    root = ET.fromstring(f"<root>{xml_string}</root>")
    entries = []
    for bibl in root.findall("biblStruct"):
        data = {}
        title_elem = bibl.find(".//analytic/title[@level='a']")
        data["title"] = title_elem.text.strip() if title_elem is not None and title_elem.text else None
        authors = []
        for author in bibl.findall(".//analytic/author"):
            pers_name = author.find(".//persName")
            if pers_name is not None:
                forename = pers_name.findtext("forename", default="").strip()
                surname = pers_name.findtext("surname", default="").strip()
                full_name = f"{forename} {surname}".strip()
                if full_name:
                    authors.append(full_name)
            else:
                org_name = author.findtext(".//orgName")
                if org_name:
                    authors.append(org_name.strip())
        data["authors"] = "; ".join(authors) if authors else None
        journal = bibl.find(".//monogr/title[@level='j']")
        data["journal"] = journal.text.strip() if journal is not None and journal.text else None
        volume = bibl.find(".//monogr/imprint/biblScope[@unit='volume']")
        data["volume"] = volume.text.strip() if volume is not None and volume.text else None
        page = bibl.find(".//monogr/imprint/biblScope[@unit='page']")
        data["pages"] = page.text.strip() if page is not None and page.text else None
        date = bibl.find(".//monogr/imprint/date[@type='published']")
        data["year"] = date.attrib["when"].split(".")[0].strip() if date is not None and "when" in date.attrib else None
        note = bibl.find(".//note")
        data["note"] = note.text.strip() if note is not None else None
        doi_elem = bibl.find(".//idno[@type='DOI']")
        data["doi"] = doi_elem.text.strip() if doi_elem is not None and doi_elem.text else None
        entries.append(data)
    return entries
