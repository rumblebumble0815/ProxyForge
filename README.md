# 🎴 ProxyForge (MTG Proxy Generator)

A desktop GUI tool for automatically downloading and printing
Magic: The Gathering proxy cards — no command line required.

---

## 📋 Requirements

- Python 3.10+
- pip install pillow requests

---

## 🚀 Quick Start

1. Run:  python mtg_proxy.py
2. Open ⚙️ Settings → set Base Path + select API
3. Enter your decklist
4. Click 📥 Download → 🚀 Export Proxy Sheets!

---

## 🌐 Decklist Tab

Enter your cards in standard format:

  4 Lightning Bolt
  1 Brainstorm
  9 Island

- One card per line, number prefix is optional
- Supports any number of copies
- 🗑 button clears the list instantly
- 📥 Download  — fetches all card images via the selected APIs
- ⚡ Load & Auto-Export  — downloads AND exports in one click
- ⛔ Cancel  — stops a running download at any time
- Live progress bar with speed (cards/min) and ETA display
- Color-coded download log (dark terminal style)

---

## 📋 Clipboard Tab

Manually add card images without downloading:

1. Take a screenshot (Win + Shift + S on Windows)
2. Click one of the 4 "Card N: Clipboard →" buttons
3. The image is loaded directly from your clipboard
4. Repeat for all 4 slots
5. Export via 🚀 Export Proxy Sheets!

Useful for cards not found by any API.

---

## 👁 Preview

Toggle the live preview panel to see how your
proxy sheet will look before exporting:

- Shows all 4 card slots in the correct layout
- Reflects current cut color and border width
- Updates instantly when cards or settings change

---

## 🚀 Export Proxy Sheets

Generates print-ready proxy sheets at 300 DPI:

- Page size: 13 × 18 cm (fits standard home printers)
- 4 cards per sheet (2 × 2 grid)
- Cards are auto-scaled to fit their slot
- If fewer than 4 cards: last card is repeated to fill
- Supported formats: PNG, JPEG, PDF (select in ⚙️)
- Output folder structure:
  [Base Path]/[Deck Name]/[API]/[Language]/proxy_01.jpg
                                           proxy_02.jpg
                                           ...
- tmp/ folder is automatically deleted after export

---

## ⚙️ Settings

All settings are saved automatically to
mtg_proxy_config.json on close and reloaded on startup.

### 🗣 UI Language
  Switch between English and Deutsch at any time.
  Takes effect immediately without restart.

### 📁 Base Path
  The root folder where all deck exports are saved.
  Use the 📂 button to browse for a folder.
  Example: D:/Decks

### 🔌 APIs
  Choose which APIs to use for downloading card images.
  Multiple APIs can be active at the same time —
  they are queried one after the other.

  | API         | Key needed | Notes                              |
  |-------------|------------|------------------------------------|
  | Scryfall    | No         | Best quality, recommended default  |
  | MTG.io      | No         | 5000 requests/hour                 |
  | Scrydex     | No         | Scryfall mirror                    |
  | Cardmarket  | Yes        | Requires OAuth app credentials     |

  Scryfall download flow:
    English name → oracle_id → language filter → image
    Falls back to English if the language is unavailable.

  MTG.io download flow:
    English name → multiverseid → foreignNames → Gatherer image
    Falls back to name-search, then Scryfall as last resort.

### 🖼 Manual Fallback
  When enabled: if a card cannot be found automatically,
  a popup dialog opens. You can then:
  - Take a screenshot (Win + Shift + S)
  - Click "Load from Clipboard" to load it
  - Click "Use Image" to add it to the download queue
  - Or click "Skip" to leave that card out

### ⏱ API Interval
  Delay in milliseconds between each API request.
  - 0 ms   = maximum speed (may trigger rate limits)
  - 100 ms = recommended
  - 500 ms = safe for all APIs

### 📶 Download Limit
  Throttle the download speed in Mbit/s.
  - 1.0 Mbit/s  ≈ 125 KB/s
  - 10.0 Mbit/s ≈ 1.25 MB/s
  Set to a high value to disable throttling effectively.

### 🌍 Card Languages
  - Default language: used for all cards by default
  - Additional languages: download the same cards in
    multiple languages simultaneously
  - Each language gets its own subfolder in the output

  Supported languages:
    English, German, French, Spanish, Italian,
    Portuguese, Japanese, Korean, Russian,
    Chinese Simplified, Chinese Traditional

### 🎨 Cut Color
  The color of the border / cut marks between cards.
  Default: green (#00AA00)
  Click "Choose Color" to open the color picker.

### 📏 Border Width
  Thickness of the cut border in pixels (2–20 px).
  Adjust with the slider. Affects all future exports.

### 📂 Export Formats
  Choose one or more output formats:
  - PNG  — lossless, large file size
  - JPEG — smaller file size, 95% quality, includes DPI
  - PDF  — ready for print shops

---

## 💾 Config File

All settings are stored in:
  mtg_proxy_config.json

This file is created automatically next to the script.
You can delete it to reset all settings to default.

---

## 📁 Output Structure

  D:/Decks/
  └── Hakbal_An_Exploration_of_Merfolk/
      ├── Scryfall/
      │   ├── en/
      │   │   ├── proxy_01.jpg
      │   │   └── proxy_02.jpg
      │   └── de/
      │       ├── proxy_01.jpg
      │       └── proxy_02.jpg
      └── MTG.io/
          └── en/
              └── proxy_01.jpg

---

## ⚠️ Notes

- Deck names with special characters (: / \ * ? " < > |)
  are automatically sanitized for Windows compatibility
- The tmp/ folder is used as a download cache during
  export and is deleted automatically afterwards
- Proxy cards are for personal use only —
  do not use them in official tournaments

---
