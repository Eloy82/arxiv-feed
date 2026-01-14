import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

AUTHOR_QUERY = 'au:"de Lera Acedo"'
MAX_RESULTS = 10

url = (
    "https://export.arxiv.org/api/query?"
    + urllib.parse.urlencode({
        "search_query": AUTHOR_QUERY,
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
)

xml_text = urllib.request.urlopen(url).read().decode("utf-8")

ns = {"a": "http://www.w3.org/2005/Atom"}
root = ET.fromstring(xml_text)

papers = []
for entry in root.findall("a:entry", ns):
    title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
    link = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
    published = (entry.findtext("a:published", default="", namespaces=ns) or "")[:10]

    authors = []
    for author in entry.findall("a:author", ns):
        name = author.findtext("a:name", default="", namespaces=ns)
        if name:
            authors.append(name.strip())

    papers.append({
        "title": title,
        "link": link,
        "published": published,
        "authors": ", ".join(authors),
    })

# Write JS file that can be loaded via <script src="..."> (no CORS issues)
payload = "window.ARXIV_PAPERS = " + json.dumps(papers, ensure_ascii=False) + ";"
with open("papers.js", "w", encoding="utf-8") as f:
    f.write(payload)

print(f"Wrote {len(papers)} papers to papers.js")
