"""Quick test: download 3 chapters from Genesis, John, and Malachi."""
import json, os, re, time, requests
from bs4 import BeautifulSoup

def to_roman(n):
    val  = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    syms = ['m','cm','d','cd','c','xc','l','xl','x','ix','v','iv','i']
    r = ''
    for i in range(len(val)):
        while n >= val[i]:
            r += syms[i]; n -= val[i]
    return r

def fetch_chapter(session, book_section, chapter_num):
    url = f'https://ccel.org/ccel/henry/mhcc/mhcc.{to_roman(book_section)}.{to_roman(chapter_num)}.html'
    try:
        resp = session.get(url, timeout=30)
        if resp.status_code == 404: return None
        resp.raise_for_status()
    except Exception as e:
        print(f'    ERROR: {e}'); return None
    soup = BeautifulSoup(resp.text, 'html.parser')
    h3s = soup.find_all('h3')
    if not h3s: return None
    sections = []
    for h3 in h3s:
        raw = h3.get_text(strip=True)
        label = re.sub(r'^(Verses?)', r'\1 ', raw)
        label = re.sub(r',', ', ', label)
        label = re.sub(r'\s+', ' ', label).strip()
        paras = []
        node = h3.find_next_sibling()
        while node and node.name != 'h3':
            if node.name == 'p':
                t = node.get_text(separator=' ', strip=True)
                if t and len(t) > 30 and 'close the reader' not in t.lower():
                    paras.append(t)
            node = node.find_next_sibling()
        if paras:
            sections.append(label + ': ' + ' '.join(paras))
    result = '\n'.join(sections).strip()
    return result if len(result) > 50 else None

sess = requests.Session()
sess.headers['User-Agent'] = 'OpenBible-TV/1.0'

# Test a few chapters
tests = [
    ("Genesis",    2, [1, 2, 3]),
    ("John",      35, [1, 3, 21]),
    ("Malachi",   31, [1, 2, 3, 4]),
    ("Revelation",58, [1, 22]),
]

for book_name, section, chapters in tests:
    print(f'\n=== {book_name} (section {section}) ===')
    for ch in chapters:
        text = fetch_chapter(sess, section, ch)
        if text:
            print(f'  Ch {ch}: {len(text)} chars -- preview: {text[:80]}...')
        else:
            print(f'  Ch {ch}: NOT FOUND')
        time.sleep(0.5)
