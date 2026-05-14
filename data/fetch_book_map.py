"""Fetch MHCC TOC and extract the book-to-section mapping."""
import requests, re
from bs4 import BeautifulSoup

sess = requests.Session()
sess.headers['User-Agent'] = 'OpenBible-TV/1.0'
r = sess.get('https://ccel.org/ccel/henry/mhcc/mhcc.toc.html', timeout=30)
soup = BeautifulSoup(r.text, 'html.parser')

# Find all links that point to book-level pages (e.g., mhcc.ii.html, mhcc.xlv.html)
# These are links WITHOUT a third segment (no chapter number)
book_links = {}
for a in soup.find_all('a', href=True):
    href = str(a.get('href', ''))
    txt = a.get_text(strip=True)
    # Match book-level URLs: mhcc.{roman}.html (exactly two dot-segments)
    m = re.match(r'mhcc\.([ivxlcdm]+)\.html$', href)
    if m and txt and txt not in ('', 'Prev', 'Next', 'Concise Comm on the Bible'):
        roman = m.group(1)
        if roman not in book_links:
            book_links[roman] = txt

print("Book -> Section mapping:")
for roman, name in book_links.items():
    print(f"  {roman:10s} -> {name}")
print(f"\nTotal: {len(book_links)} books")
