# OpenBible-TV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Roku](https://img.shields.io/badge/Platform-Roku-blue.svg)](https://developer.roku.com/)
[![BrighterScript](https://img.shields.io/badge/Language-BrighterScript-FF4500.svg)](https://github.com/rokucommunity/brighterscript)
[![GitHub stars](https://img.shields.io/github/stars/johnbpdx/OpenBible-TV.svg)](https://github.com/johnbpdx/OpenBible-TV/stargazers)

**Open-source Bible study app for Roku (and other smart TVs)** featuring public-domain Bible translations, classic commentaries, **AI-generated discussion questions**, trivia games, and a dedicated kids' mode.

Built with love for small groups, families, and personal devotion. Designed to be simple to use with a TV remote.

*(Screenshots will be added as development progresses)*

---

## ✨ Features

- 📖 **World English Bible (WEB)** — all 66 books bundled as offline JSON (public domain / CC0)
- 📚 **Full navigation** — Book list → Chapter grid → Verse reader
- ◄ ► **Chapter navigation** — Left/Right arrow keys jump to previous/next chapter without leaving the reader
- 🔍 **Study Panel** — press OK on any verse to open a dedicated study overlay with the verse text and commentary section
- 📝 **Matthew Henry Commentary** — framework in place, full data coming in a future update
- 🤖 **AI-powered discussion questions** — planned for future update
- 🎮 **Interactive Trivia Game** — planned for future update
- 👨‍👩‍👧 **Kids Mode** — planned for future update
- 🔄 Fully offline — all Bible text bundled in the package, no internet required
- 📱 Clean, remote-friendly interface designed for living-room use

---

## 🚀 Quick Start (Development)

### Prerequisites

- Roku device with [Developer Mode enabled](https://developer.roku.com/docs/developer-program/getting-started/developer-setup.md)
- [VS Code](https://code.visualstudio.com/) with the [BrightScript Language extension](https://marketplace.visualstudio.com/items?itemName=RokuCommunity.brightscript)
- [Node.js](https://nodejs.org/) (for BrighterScript build toolchain)
- Your Roku's local IP address and developer password

### Setup

```bash
git clone https://github.com/johnbpdx/OpenBible-TV.git
cd OpenBible-TV

# Install BrighterScript build tools
npm install -g brighterscript
```

### Configure credentials

Copy `.env.example` to `.env` and fill in your Roku's details:

```bash
cp .env.example .env
```

```env
ROKU_HOST=192.168.x.x       # Your Roku's local IP (Settings > Network > About)
ROKU_PASSWORD=yourpassword  # Set when enabling Developer Mode
```

> `.env` is gitignored and will never be committed.

### Build & Deploy

```powershell
cd roku
.\deploy.ps1
```

This builds the BrighterScript source and sideloads the `.zip` directly to your Roku in one step.

### Download Bible Data

The 66 WEB Bible JSON files are committed to the repo under `roku/src/data/books/`. If you ever need to regenerate them:

```powershell
cd data
.\download-web-bible.ps1
```

This fetches all 66 books from [TehShrike/world-english-bible](https://github.com/TehShrike/world-english-bible) and writes them to `roku/src/data/books/{abbrev}.json`.

### VS Code F5 Deploy

Open the workspace, ensure the BrightScript Language extension is installed, and press **F5**. The `launch.json` (gitignored) handles the rest.

---

## 📁 Project Structure

```
OpenBible-TV/
├── roku/
│   ├── src/
│   │   ├── manifest                      # Roku app manifest
│   │   ├── source/
│   │   │   └── main.bs                   # App entry point
│   │   ├── components/
│   │   │   ├── HomeScene/                # Title/splash screen (extends Scene)
│   │   │   │   ├── HomeScene.xml
│   │   │   │   └── HomeScene.bs
│   │   │   ├── BookListScene/            # 66-book scrollable grid (extends Group)
│   │   │   │   ├── BookListScene.xml
│   │   │   │   ├── BookListScene.bs
│   │   │   │   ├── BookItem.xml          # Custom grid cell — book name + OT/NT color
│   │   │   │   └── BookItem.bs
│   │   │   ├── ChapterListScene/         # Chapter number grid (extends Group)
│   │   │   │   ├── ChapterListScene.xml
│   │   │   │   ├── ChapterListScene.bs
│   │   │   │   ├── ChapterItem.xml       # Custom grid cell — chapter number
│   │   │   │   └── ChapterItem.bs
│   │   │   └── VerseView/               # Chapter reading screen (extends Group)
│   │   │       ├── VerseView.xml
│   │   │       ├── VerseView.bs
│   │   │       ├── VerseItem.xml         # Scrollable verse row — number + wrapped text
│   │   │       ├── VerseItem.bs
│   │   │       ├── StudyPanel.xml        # Verse study overlay with commentary
│   │   │       └── StudyPanel.bs
│   │   └── data/
│   │       └── books/                    # 66 WEB Bible JSON files (bundled in package)
│   │           ├── gn.json               # Genesis
│   │           ├── ex.json               # Exodus
│   │           └── ...                   # All 66 books
│   ├── bsconfig.json                     # BrighterScript build config
│   └── deploy.ps1                        # One-step build + deploy script
├── data/
│   └── download-web-bible.ps1            # Script to regenerate Bible JSON from source
├── backend/                              # Future: AI discussion questions API
├── docs/                                 # GitHub Pages site (privacy, terms, learn more)
├── .env.example                          # Credential template (copy to .env)
└── README.md
```

---

## � Installing the Beta App on Your Roku

If someone has shared a beta channel code with you, here's how to install it:

1. On a computer or phone, go to [my.roku.com](https://my.roku.com) and log in with your Roku account.
2. Go to **Manage account** → **Add channel with a code** (may also appear as **Add beta channel**).
3. Enter the code you were given and click **Add Channel**.
   > You'll see a warning that the channel hasn't been certified — this is normal for beta/developer apps. Click through to confirm.
4. On your Roku, go to **Settings → System → System update → Check now** (or wait up to 30 minutes for it to appear automatically).
5. The app will appear on your Roku home screen.

---

## �🗺️ Roadmap

| Status | Feature |
|--------|---------|
| ✅ | App loads and displays on Roku |
| ✅ | Scrollable 6-column book list — all 66 books (OT + NT color coded) |
| ✅ | One-step build & deploy script |
| ✅ | All 66 WEB Bible books bundled as offline JSON |
| ✅ | Chapter grid — 10-column number picker per book |
| ✅ | Verse reader — scrollable chapter view with wrapped verse text |
| ✅ | Left/Right remote navigation between chapters |
| ✅ | Study Panel overlay — verse + commentary section on OK press |
| ✅ | Hint bar — on-screen remote button guide |
| 🔲 | Matthew Henry Commentary data bundled |
| 🔲 | AI-generated discussion questions |
| 🔲 | Trivia game mode |
| 🔲 | Kids mode |
| 🔲 | Multiple translations |
| 🔲 | Roku Channel Store submission |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions welcome — Bible data, UI improvements, platform ports, and beyond.

---

## 📄 License

MIT — see [LICENSE](LICENSE). Bible translations used are in the public domain.

- [VS Code](https://code.visualstudio.com/) + [BrighterScript extension](https://marketplace.visualstudio.com/items?itemName=RokuCommunity.brightscript)
- Roku IP address and developer password

### Setup

```bash
git clone https://github.com/johnbpdx/OpenBible-TV.git
cd OpenBible-TV

# Install tools (optional but recommended)
npm install -g @rokucommunity/bs
