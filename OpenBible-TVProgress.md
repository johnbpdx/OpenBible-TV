# Project Progress & Status

**Project:** OpenBible-TV  
**Last Updated:** May 12, 2026

## ✅ What We've Completed

### Project Setup & Professional Structure
- ✅ Created professional GitHub repository (`johnbpdx/OpenBible-TV`)
- ✅ Added `README.md`, `CONTRIBUTING.md`, `.gitignore`
- ✅ Set up proper folder structure following RokuCommunity best practices
- ✅ Configured `bsconfig.json` and `manifest`
- ✅ Initialized Git with proper commits and pushed to GitHub

### Roku Development Environment
- ✅ Enabled Developer Mode on Roku
- ✅ Installed BrighterScript toolchain
- ✅ Created VS Code debug configuration (`launch.json` — gitignored)
- ✅ Created `deploy.ps1` — one-step build + sideload script
- ✅ Credentials secured in `.env` (gitignored); `.env.example` committed as template
- ✅ App deploys and runs on physical Roku device

### Bible Data
- ✅ Sourced World English Bible (WEB) from [TehShrike/world-english-bible](https://github.com/TehShrike/world-english-bible) — public domain / CC0
- ✅ `data/download-web-bible.ps1` — PowerShell script to download all 66 books from TehShrike's GitHub raw JSON
- ✅ All 66 WEB Bible books downloaded and verified, stored as `roku/src/data/books/{abbrev}.json`
- ✅ `bsconfig.json` updated to bundle `data/**/*` into the Roku package
- ✅ JSON format: `{"book": "...", "abbrev": "...", "chapters": [{"chapter": 1, "verses": [{"verse": 1, "text": "..."}]}]}`
- ✅ Verified: John 3:16, Psalm 23, Genesis 1:1 all correct. Psalms has 151 chapters (Psalm 151 in WEB).

### Navigation: HomeScene → BookListScene → ChapterListScene → VerseView
- ✅ `HomeScene` — title screen, navigates to BookListScene on OK press
- ✅ `BookListScene` — scrollable 6-column MarkupGrid of all 66 books
  - OT books (dark slate `#1e293b`) and NT books (dark blue `#1e3a5f`) visually distinct
  - Focused book highlights in bright blue `#3b82f6`
  - `BookItem` custom grid component with OT/NT color coding
  - Sets both `selectedBook` (title) and `selectedBookAbbrev` (abbreviation) on OK
  - `titleToAbbrev()` maps all 66 book titles to their file abbreviations
  - Back button returns to HomeScene
- ✅ `ChapterListScene` — 10-column chapter number grid
  - Reads bundled JSON to determine chapter count dynamically
  - `ChapterItem` custom grid component with blue focus highlight
  - Navigates to VerseView on OK; Back returns to BookListScene
- ✅ `VerseView` — full chapter reading screen
  - Loads all verses from bundled JSON for the selected chapter
  - `VerseItem` rows: blue verse number on left, wrapped text on right
  - Compact header (75px) showing "Book — Chapter N"
  - **Left/Right arrow keys** navigate to previous/next chapter without leaving the reader
  - **OK** opens the StudyPanel overlay for the focused verse
  - **Back** returns to ChapterListScene
  - Hint bar at bottom: `< Prev Ch   Up/Dn Scroll   OK Study Verse   Next Ch >   Back`
- ✅ `StudyPanel` — verse study overlay
  - Dims the reading screen behind it
  - Shows verse reference (e.g. "John 3:16") in blue accent
  - Displays verse text large with curly quotes
  - Commentary section with placeholder text (Matthew Henry data planned)
  - Back closes overlay and returns focus to verse list

### GitHub Pages Documentation Site
- ✅ `docs/` — Jekyll Cayman theme site at `https://johnbpdx.github.io/OpenBible-TV/`
- ✅ `docs/index.md` — project home / learn more page
- ✅ `docs/privacy-policy.md` — privacy policy (required for Roku Channel Store)
- ✅ `docs/terms-of-use.md` — terms of use
- ✅ `docs/_config.yml` — Jekyll configuration

### Bug Fixes Applied
- `bsconfig.json` `rootDir` was `"."` instead of `"src"` — nothing compiled into package
- `manifest` relocated from `roku/` to `roku/src/` to match `rootDir`
- Removed broken `<script>` tags from all XML components (redundant with `autoImportComponentScript`)
- Added `ui_resolutions=fhd` to manifest (was defaulting to 720p with 1080p coordinates)
- `BookListScene` changed from `extends="Scene"` to `extends="Group"` (only one Scene per channel)
- Removed `cornerRadius` from `Rectangle` nodes (attribute does not exist in SceneGraph)
- Replaced two separate OT/NT `MarkupGrid`s with one scrollable grid (old layout overflowed screen)
- Fixed `next` reserved keyword in BrightScript — renamed to `newChapter`
- Unicode arrow symbols in hint bar replaced with plain ASCII (Roku font doesn't support them)

---

## 🔄 Current Status

**Working on physical Roku (verified on device):**
- HomeScene title screen displays correctly
- OK → BookListScene: all 66 books in scrollable 6-column grid, OT/NT color coded
- OK on book → ChapterListScene: 10-column chapter number grid, chapter count from JSON
- OK on chapter → VerseView: all verses for the chapter, scrollable
- Left/Right in VerseView: navigates between chapters in place
- OK on verse → StudyPanel overlay: verse text + commentary placeholder
- Back at each level returns to the previous screen correctly
- Hint bar visible at bottom of VerseView

---

## 🚧 Next Priority Tasks

1. **Matthew Henry Commentary data** — source, parse, and bundle per-verse commentary text
2. **Roku Channel Store static analysis warnings** — bump manifest version, add memory monitoring API calls
3. **AI-generated discussion questions** — backend API or on-device model
4. **Trivia game mode**
5. **Kids mode**
6. **Multiple Bible translations**

---

**This document will be kept updated** as we make progress.

