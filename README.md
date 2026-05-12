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

- 📖 **Multiple public-domain Bible translations** (KJV, WEB, ASV, and more)
- 📝 **Matthew Henry Commentary** (full public-domain text) with easy toggling
- 🤖 **AI-powered discussion questions** — 4–5 thoughtful group questions generated on demand
- 🎮 **Interactive Trivia Game** with multiple choice questions
- 👨‍👩‍👧 **Kids Mode** — simplified language, activities, and fun visuals
- 🔄 Offline support (bundled Bible data)
- 📱 Clean, remote-friendly interface built for living-room use
- 🌍 Extensible — easy to add more translations, commentaries, or languages

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

### VS Code F5 Deploy

Open the workspace, ensure the BrightScript Language extension is installed, and press **F5**. The `launch.json` (gitignored) handles the rest.

---

## 📁 Project Structure

```
OpenBible-TV/
├── roku/
│   ├── src/
│   │   ├── manifest                  # Roku app manifest
│   │   ├── source/
│   │   │   └── main.bs               # App entry point
│   │   └── components/
│   │       ├── HomeScene/            # Title/splash screen
│   │       └── BookListScene/        # Scrollable grid of all 66 books
│   ├── bsconfig.json                 # BrighterScript build config
│   └── deploy.ps1                    # One-step build + deploy script
├── backend/                          # Future: AI discussion questions API
├── data/                             # Future: Bible JSON data
├── docs/                             # Additional documentation
├── .env.example                      # Credential template (copy to .env)
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
| ✅ | Scrollable book list — all 66 books (OT + NT) |
| ✅ | One-step build & deploy script |
| 🔄 | Chapter/verse picker |
| 🔄 | Bible text display (KJV — bundled JSON) |
| 🔲 | Matthew Henry Commentary toggle |
| 🔲 | AI-generated discussion questions |
| 🔲 | Trivia game mode |
| 🔲 | Kids mode |
| 🔲 | Multiple translations |

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
