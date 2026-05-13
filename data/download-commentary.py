"""
Download Matthew Henry's Concise Commentary (MHCC) from CCEL
and convert to per-book JSON files for the OpenBible-TV Roku app.

Source: https://ccel.org/ccel/henry/mhcc (Public Domain)
Output: roku/src/data/commentary/{abbrev}.json
Format: {"1": "Chapter 1 commentary text...", "2": "Chapter 2 commentary text..."}

Usage: python download-commentary.py
"""

import json
import os
import re
import time
import requests
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------
# Book metadata: abbrev -> (display_name, ccel_section_num, chapter_count)
# ccel_section_num: actual CCEL MHCC section (from TOC at mhcc.toc.html)
# Section 0 = book NOT included in CCEL MHCC (9 minor prophets missing)
# Note: 2 Kings/2 Chronicles start from ch.2 in MHCC (ch.1 commentary absent)
# -----------------------------------------------------------------------
BOOKS = [
    ("gn",   "Genesis",          2,  50),  # ii
    ("ex",   "Exodus",           3,  40),  # iii
    ("lv",   "Leviticus",        4,  27),  # iv
    ("nm",   "Numbers",          5,  36),  # v
    ("dt",   "Deuteronomy",      6,  34),  # vi
    ("js",   "Joshua",           7,  24),  # vii
    ("jdg",  "Judges",           8,  21),  # viii
    ("rt",   "Ruth",             9,   4),  # ix
    ("1sm",  "1 Samuel",        10,  31),  # x
    ("2sm",  "2 Samuel",        11,  24),  # xi
    ("1kgs", "1 Kings",         12,  22),  # xii
    ("2kgs", "2 Kings",         13,  25),  # xiii (starts at ch.2)
    ("1ch",  "1 Chronicles",    14,  29),  # xiv
    ("2ch",  "2 Chronicles",    15,  36),  # xv (starts at ch.2)
    ("ezr",  "Ezra",            16,  10),  # xvi
    ("ne",   "Nehemiah",        17,  13),  # xvii
    ("est",  "Esther",          18,  10),  # xviii
    ("jb",   "Job",             19,  42),  # xix
    ("ps",   "Psalms",          20, 150),  # xx
    ("prv",  "Proverbs",        21,  31),  # xxi
    ("ec",   "Ecclesiastes",    22,  12),  # xxii
    ("sg",   "Song of Solomon", 23,   8),  # xxiii
    ("is",   "Isaiah",          24,  66),  # xxiv
    ("jr",   "Jeremiah",        25,  52),  # xxv
    ("lm",   "Lamentations",    26,   5),  # xxvi
    ("ez",   "Ezekiel",         27,  48),  # xxvii
    ("dn",   "Daniel",          28,  12),  # xxviii
    ("hs",   "Hosea",           29,  14),  # xxix
    ("jl",   "Joel",            30,   3),  # xxx
    ("am",   "Amos",             0,   9),  # MISSING from CCEL MHCC
    ("ob",   "Obadiah",          0,   1),  # MISSING from CCEL MHCC
    ("jon",  "Jonah",            0,   4),  # MISSING from CCEL MHCC
    ("mc",   "Micah",            0,   7),  # MISSING from CCEL MHCC
    ("na",   "Nahum",            0,   3),  # MISSING from CCEL MHCC
    ("hbk",  "Habakkuk",         0,   3),  # MISSING from CCEL MHCC
    ("zp",   "Zephaniah",        0,   3),  # MISSING from CCEL MHCC
    ("hg",   "Haggai",           0,   2),  # MISSING from CCEL MHCC
    ("zc",   "Zechariah",        0,  14),  # MISSING from CCEL MHCC
    ("ml",   "Malachi",         31,   4),  # xxxi
    ("mt",   "Matthew",         32,  28),  # xxxii
    ("mk",   "Mark",            33,  16),  # xxxiii
    ("lk",   "Luke",            34,  24),  # xxxiv
    ("jn",   "John",            35,  21),  # xxxv
    ("act",  "Acts",            36,  28),  # xxxvi
    ("rm",   "Romans",          37,  16),  # xxxvii
    ("1co",  "1 Corinthians",   38,  16),  # xxxviii
    ("2co",  "2 Corinthians",   39,  13),  # xxxix
    ("gl",   "Galatians",       40,   6),  # xl
    ("eph",  "Ephesians",       41,   6),  # xli
    ("ph",   "Philippians",     42,   4),  # xlii
    ("cl",   "Colossians",      43,   4),  # xliii
    ("1ts",  "1 Thessalonians", 44,   5),  # xliv
    ("2ts",  "2 Thessalonians", 45,   3),  # xlv
    ("1tm",  "1 Timothy",       46,   6),  # xlvi
    ("2tm",  "2 Timothy",       47,   4),  # xlvii
    ("tt",   "Titus",           48,   3),  # xlviii
    ("phm",  "Philemon",        49,   1),  # xlix
    ("hb",   "Hebrews",         50,  13),  # l
    ("jms",  "James",           51,   5),  # li
    ("1pt",  "1 Peter",         52,   5),  # lii
    ("2pt",  "2 Peter",         53,   3),  # liii
    ("1jn",  "1 John",          54,   5),  # liv
    ("2jn",  "2 John",          55,   1),  # lv
    ("3jn",  "3 John",          56,   1),  # lvi
    ("jd",   "Jude",            57,   1),  # lvii
    ("rv",   "Revelation",      58,  22),  # lviii
]


def to_roman(n: int) -> str:
    """Convert integer to lowercase Roman numeral."""
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ['m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i']
    result = ''
    for i in range(len(val)):
        while n >= val[i]:
            result += syms[i]
            n -= val[i]
    return result


def fetch_chapter(session: requests.Session, book_section: int, chapter_num: int) -> str | None:
    """Fetch and parse commentary text for one chapter from CCEL.

    CCEL page structure:
      - h3 elements = verse range headers (e.g. "Verses1,2", "Verses3-5", "Verse31")
      - p elements immediately following each h3 = the commentary paragraphs
    We collect all h3+p groups and concatenate them into one chapter commentary string.
    """
    book_roman = to_roman(book_section)
    chap_roman = to_roman(chapter_num)
    url = f"https://ccel.org/ccel/henry/mhcc/mhcc.{book_roman}.{chap_roman}.html"

    try:
        resp = session.get(url, timeout=30)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"    ERROR fetching {url}: {e}")
        return None

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Each h3 = verse range label, followed by 1+ <p> siblings = commentary
    h3_elements = soup.find_all('h3')
    if not h3_elements:
        return None

    sections = []
    for h3 in h3_elements:
        # Format the verse label — CCEL omits spaces e.g. "Verses1,2" -> "Verses 1, 2"
        raw_label = h3.get_text(strip=True)
        # Insert space after "Verse" / "Verses"
        label = re.sub(r'^(Verses?)', r'\1 ', raw_label)
        label = re.sub(r',', ', ', label)
        label = re.sub(r'\s+', ' ', label).strip()

        # Collect p siblings until the next h3
        para_texts = []
        node = h3.find_next_sibling()
        while node and node.name != 'h3':
            if node.name == 'p':
                t = node.get_text(separator=' ', strip=True)
                # Skip very short / nav snippets
                if t and len(t) > 30 and 'close the reader' not in t.lower():
                    para_texts.append(t)
            node = node.find_next_sibling()

        if para_texts:
            combined = ' '.join(para_texts)
            sections.append(f"{label}: {combined}")

    result = '\n'.join(sections).strip()
    return result if len(result) > 50 else None


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, '..', 'roku', 'src', 'data', 'commentary')
    os.makedirs(out_dir, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'OpenBible-TV/1.0 (open-source Roku Bible app; github.com/johnbpdx/OpenBible-TV)'
    })

    total_books = len(BOOKS)

    for book_idx, (abbrev, name, section_num, chapter_count) in enumerate(BOOKS, 1):
        out_file = os.path.join(out_dir, f"{abbrev}.json")

        # Skip if already downloaded
        if os.path.exists(out_file):
            print(f"[{book_idx}/{total_books}] {name} — already exists, skipping")
            continue

        print(f"[{book_idx}/{total_books}] {name} ({chapter_count} chapters)...")
        book_data = {}

        if section_num == 0:
            # Book not in CCEL MHCC — write empty chapters
            print(f"  -> Not available in CCEL MHCC, writing empty file")
            for ch in range(1, chapter_count + 1):
                book_data[str(ch)] = ""
        else:
            for ch in range(1, chapter_count + 1):
                text = fetch_chapter(session, section_num, ch)
                if text:
                    book_data[str(ch)] = text
                    print(f"  Ch {ch}: {len(text)} chars")
                else:
                    book_data[str(ch)] = ""
                    print(f"  Ch {ch}: not found")

                # Be polite — short delay between requests
                time.sleep(0.5)

        # Write JSON
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, ensure_ascii=False, separators=(',', ':'))

        print(f"  -> Saved {out_file}")
        # Extra delay between books
        time.sleep(1)

    print("\nDone. Commentary JSON files written to roku/src/data/commentary/")
    print("\nFile sizes:")
    for abbrev, name, _, _ in BOOKS:
        fp = os.path.join(out_dir, f"{abbrev}.json")
        if os.path.exists(fp):
            size = os.path.getsize(fp)
            print(f"  {abbrev}.json: {size:,} bytes")


if __name__ == '__main__':
    main()
