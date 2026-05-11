# OpenBible-TV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Roku](https://img.shields.io/badge/Platform-Roku-blue.svg)](https://developer.roku.com/)
[![BrighterScript](https://img.shields.io/badge/Language-BrighterScript-FF4500.svg)](https://github.com/rokucommunity/brighterscript)
[![GitHub stars](https://img.shields.io/github/stars/johnbpdx/OpenBible-TV.svg)](https://github.com/johnbpdx/OpenBible-TV/stargazers)

**Open-source Bible study app for Roku (and other smart TVs)** featuring public-domain Bible translations, classic commentaries, **AI-generated discussion questions**, trivia games, and a dedicated kids' mode.

Built with love for small groups, families, and personal devotion. Designed to be simple to use with a TV remote.

![Screenshot of reading screen](screenshots/reading-screen.png)  
*(Screenshots will be added as development progresses)*

## ✨ Features

- 📖 **Multiple public-domain Bible translations** (KJV, WEB, ASV, and more)
- 📝 **Matthew Henry Commentary** (full public-domain text) with easy toggling
- 🤖 **AI-powered discussion questions** — 4–5 thoughtful group questions generated on demand
- 🎮 **Interactive Trivia Game** with multiple choice questions
- 👨‍👩‍👧 **Kids Mode** — simplified language, activities, and fun visuals
- 🔄 Offline support (bundled Bible data)
- 📱 Clean, remote-friendly interface built for living-room use
- 🌍 Extensible — easy to add more translations, commentaries, or languages

## 🚀 Quick Start (Development)

### Prerequisites
- Roku device with [Developer Mode enabled](https://developer.roku.com/docs/developer-program/getting-started/developer-setup.md)
- [VS Code](https://code.visualstudio.com/) + [BrighterScript extension](https://marketplace.visualstudio.com/items?itemName=RokuCommunity.brightscript)
- Roku IP address and developer password

### Setup

```bash
git clone https://github.com/johnbpdx/OpenBible-TV.git
cd OpenBible-TV

# Install tools (optional but recommended)
npm install -g @rokucommunity/bs
