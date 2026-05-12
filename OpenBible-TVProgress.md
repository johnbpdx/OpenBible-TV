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

### Core Code Foundation
- ✅ `main.bs` — app entry point with `scene.setFocus(true)` (required for key events)
- ✅ `HomeScene` — title screen, navigates to BookListScene on OK
- ✅ `BookListScene` — scrollable 6-column grid of all 66 books (OT + NT)
- ✅ `BookItem` — custom grid item component with OT/NT color coding and focus highlight
- ✅ Testament label updates dynamically as user scrolls through grid
- ✅ Back button returns from BookListScene to HomeScene

### Bug Fixes Applied
- `bsconfig.json` `rootDir` was `"."` instead of `"src"` — nothing compiled into package
- `manifest` relocated from `roku/` to `roku/src/` to match `rootDir`
- Removed broken `<script>` tags from all XML components (redundant with `autoImportComponentScript`)
- Added `ui_resolutions=fhd` to manifest (was defaulting to 720p with 1080p coordinates)
- `BookListScene` changed from `extends="Scene"` to `extends="Group"` (only one Scene per channel)
- Removed `cornerRadius` from `Rectangle` nodes (attribute does not exist in SceneGraph)
- Replaced two separate OT/NT `MarkupGrid`s with one scrollable grid (old layout overflowed screen)
- Removed redundant `bookName` custom field — `node.title` sufficient
- Fixed cross-grid focus navigation (was using unreliable key intercept; now single grid + observer)

### Documentation
- ✅ README with full setup guide, project structure, and roadmap
- ✅ `.env.example` with credential setup instructions
- ✅ This progress tracking file

## 🔄 Current Status

**Working on physical Roku:**
- HomeScene title screen displays correctly
- Press OK → BookListScene opens with all 66 books in scrollable grid
- OT books (dark slate) and NT books (dark blue) visually distinct
- Focused book highlights in bright blue
- Testament label ("OLD TESTAMENT" / "NEW TESTAMENT") updates as you scroll
- Back button returns to HomeScene

## 🚧 Next Priority Tasks

1. **Chapter picker** — after selecting a book, show list of chapters
2. **Verse/reading view** — display actual scripture text (bundle KJV JSON)
3. **Bible data** — source and bundle public-domain KJV or WEB as JSON
4. **Key Features** (later)
   - Toggleable Matthew Henry commentary
   - AI-generated discussion questions (backend)
   - Trivia game
   - Kids mode

---

**This document will be kept updated** as we make progress.

