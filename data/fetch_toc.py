import requests
from bs4 import BeautifulSoup

sess = requests.Session()
sess.headers['User-Agent'] = 'OpenBible-TV/1.0'
r = sess.get('https://ccel.org/ccel/henry/mhcc/mhcc.toc.html', timeout=20)
soup = BeautifulSoup(r.text, 'html.parser')
links = [a for a in soup.find_all('a', href=True)]
print('TOC links:')
for link in links:
    href = str(link.get('href', ''))
    txt = link.get_text(strip=True)
    if href and txt and 'mhcc.' in href:
        print(f"{href:50s} -> {txt[:40]}")
