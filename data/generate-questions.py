"""
Generate AI discussion questions for each Bible chapter using xAI (Grok).

Output: roku/src/data/questions/{abbrev}.json
Format: {"1": ["Question 1", "Question 2", "Question 3"], "2": [...], ...}

Questions follow the OIA model (Observation / Interpretation / Application)
and are grounded in orthodox, evangelical Christian doctrine.

Usage:
    python data/generate-questions.py
    python data/generate-questions.py --book jhn        # single book
    python data/generate-questions.py --model grok-3    # use full Grok 3

Requires XAI_API_KEY in .env file at project root.
Resume-safe: skips books whose output file already exists and is complete.
"""

import argparse
import json
import os
import time
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

XAI_BASE_URL = "https://api.x.ai/v1"
DEFAULT_MODEL = "grok-3-mini"
SLEEP_BETWEEN_REQUESTS = 0.5   # seconds — adjust if you hit rate limits

BOOKS_DIR  = "roku/src/data/books"
OUTPUT_DIR = "roku/src/data/questions"

# (abbrev, display_name, chapter_count)
BOOKS = [
    ("gn",   "Genesis",           50),
    ("ex",   "Exodus",            40),
    ("lv",   "Leviticus",         27),
    ("nm",   "Numbers",           36),
    ("dt",   "Deuteronomy",       34),
    ("js",   "Joshua",            24),
    ("jdg",  "Judges",            21),
    ("rt",   "Ruth",               4),
    ("1sm",  "1 Samuel",          31),
    ("2sm",  "2 Samuel",          24),
    ("1kgs", "1 Kings",           22),
    ("2kgs", "2 Kings",           25),
    ("1ch",  "1 Chronicles",      29),
    ("2ch",  "2 Chronicles",      36),
    ("ezr",  "Ezra",              10),
    ("ne",   "Nehemiah",          13),
    ("est",  "Esther",            10),
    ("jb",   "Job",               42),
    ("ps",   "Psalms",           150),
    ("prv",  "Proverbs",          31),
    ("ec",   "Ecclesiastes",      12),
    ("sg",   "Song of Solomon",    8),
    ("is",   "Isaiah",            66),
    ("jr",   "Jeremiah",          52),
    ("lm",   "Lamentations",       5),
    ("ez",   "Ezekiel",           48),
    ("dn",   "Daniel",            12),
    ("hs",   "Hosea",             14),
    ("jl",   "Joel",               3),
    ("am",   "Amos",               9),
    ("ob",   "Obadiah",            1),
    ("jon",  "Jonah",              4),
    ("mc",   "Micah",              7),
    ("na",   "Nahum",              3),
    ("hbk",  "Habakkuk",           3),
    ("zp",   "Zephaniah",          3),
    ("hg",   "Haggai",             2),
    ("zc",   "Zechariah",         14),
    ("ml",   "Malachi",            4),
    ("mt",   "Matthew",           28),
    ("mk",   "Mark",              16),
    ("lk",   "Luke",              24),
    ("jn",   "John",              21),
    ("act",  "Acts",              28),
    ("rm",   "Romans",            16),
    ("1co",  "1 Corinthians",     16),
    ("2co",  "2 Corinthians",     13),
    ("gl",   "Galatians",          6),
    ("eph",  "Ephesians",          6),
    ("ph",   "Philippians",        4),
    ("cl",   "Colossians",         4),
    ("1ts",  "1 Thessalonians",    5),
    ("2ts",  "2 Thessalonians",    3),
    ("1tm",  "1 Timothy",          6),
    ("2tm",  "2 Timothy",          4),
    ("tt",   "Titus",              3),
    ("phm",  "Philemon",           1),
    ("hb",   "Hebrews",           13),
    ("jms",  "James",              5),
    ("1pt",  "1 Peter",            5),
    ("2pt",  "2 Peter",            3),
    ("1jn",  "1 John",             5),
    ("2jn",  "2 John",             1),
    ("3jn",  "3 John",             1),
    ("jd",   "Jude",               1),
    ("rv",   "Revelation",        22),
]

SYSTEM_PROMPT = """You are a Bible study guide writer for an evangelical Christian TV app.
Your task is to write exactly 3 discussion questions for a Bible chapter.

Guidelines:
- Write one question of each type: Observation, Interpretation, Application.
  - Observation: "What does the text say?" — factual, answerable from the passage alone.
  - Interpretation: "What does it mean?" — historical/literary context, how it fits the whole Bible.
  - Application: "How does this apply to a Christian today?" — practical, personal, action-oriented.
- Keep each question under 120 characters.
- Do NOT number the questions.
- Base every question directly on the passage text provided — no question should require knowledge beyond what is written.
- Questions must be consistent with orthodox, evangelical Christian doctrine: the authority of Scripture, salvation by grace through faith in Christ alone, and the historic creeds.
- Avoid theologically divisive topics (baptism mode, eschatological timelines, charismatic gifts debates).
- Assume the reader believes the Bible is true and authoritative.
- Use plain, clear English — this will appear on a TV screen.

Return ONLY a JSON array of exactly 3 strings. No explanation, no numbering, no markdown.
Example: ["What does Paul say...", "Why does he contrast...", "How can you apply..."]"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    env = {}
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip()
    return env


def build_passage_text(chapter_data, book_name, chapter_num):
    """Concatenate all verses into a readable passage string."""
    lines = [f"{book_name} {chapter_num}"]
    for v in chapter_data["verses"]:
        lines.append(f"[{v['verse']}] {v['text']}")
    return "\n".join(lines)


def generate_questions(api_key, model, passage_text):
    """Call xAI and return a list of 3 question strings."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": passage_text},
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    for attempt in range(3):
        try:
            resp = requests.post(
                f"{XAI_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=90,
            )
            resp.raise_for_status()
            break
        except requests.exceptions.ReadTimeout:
            if attempt < 2:
                print(f"    [TIMEOUT] attempt {attempt + 1}, retrying...")
                import time; time.sleep(5)
            else:
                raise

    content = resp.json()["choices"][0]["message"]["content"].strip()

    # Strip markdown code fences if the model wraps in ```json ... ```
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    questions = json.loads(content)
    if not isinstance(questions, list) or len(questions) != 3:
        raise ValueError(f"Unexpected response format: {content}")
    return [str(q) for q in questions]


def output_path(abbrev):
    return os.path.join(OUTPUT_DIR, f"{abbrev}.json")


def is_complete(abbrev, expected_chapters):
    path = output_path(abbrev)
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return len(data) >= expected_chapters


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_book(api_key, model, abbrev, book_name, chapter_count):
    book_path = os.path.join(BOOKS_DIR, f"{abbrev}.json")
    if not os.path.exists(book_path):
        print(f"  [SKIP] {book_name}: no Bible JSON at {book_path}")
        return

    with open(book_path, encoding="utf-8") as f:
        bible_data = json.load(f)

    chapters = bible_data["chapters"]
    result = {}

    # Load partial progress if file exists
    out_path = output_path(abbrev)
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            result = json.load(f)

    for ch in chapters:
        ch_num = str(ch["chapter"])
        if ch_num in result:
            continue  # already done

        passage = build_passage_text(ch, book_name, ch["chapter"])
        try:
            questions = generate_questions(api_key, model, passage)
            result[ch_num] = questions
            print(f"  Chapter {ch_num}: {questions[0][:60]}...")
        except Exception as e:
            print(f"  [ERROR] Chapter {ch_num}: {e}")
            # Save progress so far before propagating
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            raise

        # Save after each chapter (resume-safe)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"  Done — {len(result)} chapters saved.")


def main():
    parser = argparse.ArgumentParser(description="Generate AI discussion questions for each Bible chapter.")
    parser.add_argument("--book", help="Process only this book abbreviation (e.g. jhn)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"xAI model name (default: {DEFAULT_MODEL})")
    parser.add_argument("--force", action="store_true", help="Regenerate even if output file exists")
    args = parser.parse_args()

    env = load_env()
    api_key = env.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
    if not api_key:
        raise SystemExit("ERROR: XAI_API_KEY not found in .env or environment.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    books_to_process = BOOKS
    if args.book:
        books_to_process = [b for b in BOOKS if b[0] == args.book]
        if not books_to_process:
            raise SystemExit(f"ERROR: Unknown book abbreviation '{args.book}'")

    total = len(books_to_process)
    for i, (abbrev, book_name, chapter_count) in enumerate(books_to_process, 1):
        print(f"[{i}/{total}] {book_name} ({abbrev}, {chapter_count} chapters)")
        if not args.force and is_complete(abbrev, chapter_count):
            print("  Already complete — skipping.")
            continue
        process_book(api_key, args.model, abbrev, book_name, chapter_count)

    print("\nAll done.")


if __name__ == "__main__":
    main()
