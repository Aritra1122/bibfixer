import requests
import urllib.parse
import xml.etree.ElementTree as ET

def get_doi_from_crossref(title):
    url = "https://api.crossref.org/works"
    params = {"query.bibliographic": title, "rows": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        items = response.json().get("message", {}).get("items", [])
        if items:
            return items[0].get("DOI")
    return None

def get_bibtex_from_doi(doi):
    headers = {"Accept": "application/x-bibtex"}
    url = f"https://doi.org/{urllib.parse.quote(doi)}"
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

def get_bibtex_from_arxiv(title):
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": f"all:{title}", "start": 0, "max_results": 1}
    response = requests.get(url, params=params)
    if "http://arxiv.org/abs/" in response.text:
        root = ET.fromstring(response.content)
        ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
        entry = root.find("arxiv:entry", ns)
        if entry is not None:
            arxiv_id = entry.find("arxiv:id", ns)
            if arxiv_id is not None:
                arxiv_id = arxiv_id.text.strip()
                return f"@misc{{{arxiv_id},\n  title={{ {title} }},\n  eprint={{arXiv:{arxiv_id}}},\n  archivePrefix={{arXiv}},\n}}"
    return None

def get_bibtex_from_semantic(title):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": title, "limit": 1, "fields": "title,externalIds"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            paper = data["data"][0]
            doi = paper.get("externalIds", {}).get("DOI")
            if doi:
                return get_bibtex_from_doi(doi)
    return None

def get_bibtex_from_inspire(title):
    url = "https://inspirehep.net/api/literature"
    params = {"q": title, "size": 1, "format": "bibtex"}
    response = requests.get(url, params=params)
    if response.status_code == 200 and "@article" in response.text:
        return response.text.strip()
    return None

def find_bibtex(title):
    doi = get_doi_from_crossref(title)
    if doi:
        bib = get_bibtex_from_doi(doi)
        if bib:
            return bib
    for fetch_func in [get_bibtex_from_semantic, get_bibtex_from_arxiv, get_bibtex_from_inspire]:
        bib = fetch_func(title)
        if bib:
            return bib
    return None
