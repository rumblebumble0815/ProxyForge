import tkinter as tk
from tkinter import messagebox, ttk, colorchooser, filedialog, scrolledtext
from PIL import Image, ImageDraw, ImageGrab, ImageTk
import requests
import threading
import os
import io
import time
import shutil
import re
import json

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════

CONFIG_FILE = "mtg_proxy_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(data: dict):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Config save error: {e}")

# ══════════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════════

TRANSLATIONS = {
    "en": {
        "title":               "ProxyForge",
        "subtitle":            "Decklist → Download → Export Proxy Sheets",
        "deck_frame":          "🃏 Deck",
        "deck_name":           "Deck Name:",
        "path_hint":           "→ Path: (set base path in ⚙️)",
        "tab_decklist":        "🌐 Decklist",
        "tab_clipboard":       "📋 Clipboard",
        "decklist_label":      "Decklist (e.g. '9 Swamp' or '1 Brainstorm'):",
        "btn_download":        "📥 Download",
        "btn_load_export":     "⚡ Load & Auto-Export",
        "btn_cancel":          "⛔ Cancel",
        "log_label":           "Download Log:",
        "preview_check":       "👁 Preview",
        "btn_export":          "🚀 Export Proxy Sheets!",
        "status_ready":        "Ready – ⚙️ for Settings",
        "clipboard_btn":       "Card {n}: Clipboard →",
        "clipboard_done":      "Card {n}: ✓",
        "settings_title":      "⚙️ Settings",
        "settings_header":     "⚙️ Settings",
        "base_path":           "📁 Base Path:",
        "base_path_hint":      "e.g. D:/Decks  (no special chars in path!)",
        "apis_header":         "🔌 APIs:",
        "default_api":         "Default API:",
        "active_apis":         "Active APIs (queried in order)",
        "manual_fb_frame":     "🖼 Manual Fallback",
        "manual_fb_enable":    "  Enable",
        "manual_fb_desc":      "If active: When a card is not found\nin a language, a popup opens.\nYou can add the card manually via\nscreenshot (Win+Shift+S) or skip it.",
        "api_interval":        "⏱ API Interval:",
        "api_interval_hint":   "0=max(⚠️)  |  100=recommended  |  500+=safe",
        "dl_limit":            "📶 Download Limit:",
        "dl_limit_hint":       "1.0=~125KB/s  |  10.0=~1.25MB/s",
        "languages_header":    "🌍 Card Languages:",
        "lang_default":        "Default:",
        "lang_extra":          "Additional:",
        "cut_color":           "🎨 Cut Color:",
        "choose_color":        "  Choose Color  ",
        "border_width":        "📏 Border Width:",
        "export_formats":      "📂 Export Formats:",
        "btn_save_close":      "✅ Save & Close",
        "ui_language":         "🗣 UI Language:",
        "manual_title":        "🖼 Add Card Manually",
        "manual_header":       "⚠️ Card not found automatically",
        "manual_card":         "🃏 Card:   ",
        "manual_lang":         "🌍 Language: ",
        "manual_api":          "🔌 API:     ",
        "manual_guide":        "How to:\n1. Open a browser and search for the card\n2. Press  Win + Shift + S  for a screenshot\n3. Click  '📋 Load from Clipboard'\n4. Check preview → '✅ Use Image'",
        "manual_no_img":       "[ No image loaded yet ]",
        "btn_clipboard_load":  "📋 Load from Clipboard",
        "btn_use":             "✅ Use Image",
        "btn_skip":            "⏭ Skip",
        "no_image_warn":       "No image in clipboard!\nPlease use Win+Shift+S.",
        "warn_no_path":        "No Base Path",
        "warn_no_path_msg":    "Please set base path in ⚙️!",
        "warn_no_deck":        "No Deck Name",
        "warn_no_deck_msg":    "Please enter a deck name!",
        "warn_no_api":         "No API",
        "warn_no_api_msg":     "Please activate at least one API!",
        "warn_no_format":      "No Format",
        "warn_no_format_msg":  "Please select a format in ⚙️!",
        "warn_empty":          "Empty",
        "warn_empty_msg":      "No cards in the list!",
        "warn_no_images":      "No Images",
        "warn_no_images_msg":  "Load cards via Download or Clipboard first!",
        "export_done_title":   "✅ Export complete!",
        "export_done_msg":     "✅ {n} proxy sheet(s)!\nFormats: {f}\n\nFolder structure:\n{s}\n\ntmp/ deleted ✓",
        "status_exported":     "✅ {n} sheets saved in '{d}'",
        "status_ready_dl":     "✅ {n} cards ready → export!",
        "tmp_deleted":         "🗑 tmp/ deleted.",
        "scryfall_info":       "✅ Always searches in English\nFlow: Name(EN) → oracle_id → prints+lang:XX → image\nFallback to EN if language not available",
        "mtgio_info":          "✅ No key  |  5000 Req/h\nFlow: Name(EN) → multiverseid → foreignNames → Gatherer\nName fallback if ID language missing\nScryfall fallback as last resort",
        "path_structure":      "→ Structure: {b}/{d}/[API]/[lang]/proxy_01.jpg\n   Active APIs: {a}",
        "path_no_api":         "→ No API selected!",
        "path_apis_only":      "→ APIs: {a}",
        "lang_info":           "→ Download: {l}",
        "path_no_deck":        "→ Base: {b}  |  Deck name missing",
        "config_saved":        "💾 Settings saved.",
    },
    "de": {
        "title":               "ProxyForge",
        "subtitle":            "Deckliste → Download → Proxy-Blätter exportieren",
        "deck_frame":          "🃏 Deck",
        "deck_name":           "Deckname:",
        "path_hint":           "→ Pfad: (Basis-Pfad in ⚙️ setzen)",
        "tab_decklist":        "🌐 Deckliste",
        "tab_clipboard":       "📋 Clipboard",
        "decklist_label":      "Deckliste (z.B. '9 Swamp' oder '1 Brainstorm'):",
        "btn_download":        "📥 Herunterladen",
        "btn_load_export":     "⚡ Laden & Auto-Export",
        "btn_cancel":          "⛔ Abbrechen",
        "log_label":           "Download-Log:",
        "preview_check":       "👁 Vorschau",
        "btn_export":          "🚀 Proxy-Blätter exportieren!",
        "status_ready":        "Bereit – ⚙️ für Einstellungen",
        "clipboard_btn":       "Karte {n}: Clipboard →",
        "clipboard_done":      "Karte {n}: ✓",
        "settings_title":      "⚙️ Einstellungen",
        "settings_header":     "⚙️ Einstellungen",
        "base_path":           "📁 Basis-Pfad:",
        "base_path_hint":      "z.B. D:/Decks  (keine Sonderzeichen im Pfad!)",
        "apis_header":         "🔌 APIs:",
        "default_api":         "Standard-API:",
        "active_apis":         "Aktive APIs (werden nacheinander abgefragt)",
        "manual_fb_frame":     "🖼 Manueller Fallback",
        "manual_fb_enable":    "  Aktivieren",
        "manual_fb_desc":      "Wenn aktiv: Wird eine Karte in einer Sprache\nnicht gefunden, öffnet sich ein Popup-Fenster.\nDu kannst die Karte dann per Screenshot\n(Win+Shift+S) manuell hinzufügen oder überspringen.",
        "api_interval":        "⏱ API-Intervall:",
        "api_interval_hint":   "0=max(⚠️)  |  100=empfohlen  |  500+=sicher",
        "dl_limit":            "📶 Download-Limit:",
        "dl_limit_hint":       "1.0=~125KB/s  |  10.0=~1.25MB/s",
        "languages_header":    "🌍 Karten-Sprachen:",
        "lang_default":        "Standard:",
        "lang_extra":          "Weitere:",
        "cut_color":           "🎨 Schnittfarbe:",
        "choose_color":        "  Farbe wählen  ",
        "border_width":        "📏 Randbreite:",
        "export_formats":      "📂 Export-Formate:",
        "btn_save_close":      "✅ Speichern & Schließen",
        "ui_language":         "🗣 UI-Sprache:",
        "manual_title":        "🖼 Karte manuell hinzufügen",
        "manual_header":       "⚠️ Karte nicht automatisch gefunden",
        "manual_card":         "🃏 Karte:   ",
        "manual_lang":         "🌍 Sprache: ",
        "manual_api":          "🔌 API:     ",
        "manual_guide":        "So gehts:\n1. Öffne einen Browser und suche die Karte\n2. Drücke  Win + Shift + S  für einen Screenshot\n3. Klicke auf  '📋 Aus Clipboard laden'\n4. Vorschau prüfen → '✅ Übernehmen'",
        "manual_no_img":       "[ Noch kein Bild geladen ]",
        "btn_clipboard_load":  "📋 Aus Clipboard laden",
        "btn_use":             "✅ Übernehmen",
        "btn_skip":            "⏭ Überspringen",
        "no_image_warn":       "Kein Bild im Clipboard!\nBitte Win+Shift+S nutzen.",
        "warn_no_path":        "Kein Basis-Pfad",
        "warn_no_path_msg":    "Bitte Basis-Pfad in ⚙️ setzen!",
        "warn_no_deck":        "Kein Deckname",
        "warn_no_deck_msg":    "Bitte Decknamen eingeben!",
        "warn_no_api":         "Keine API",
        "warn_no_api_msg":     "Bitte mindestens eine API aktivieren!",
        "warn_no_format":      "Kein Format",
        "warn_no_format_msg":  "Bitte Format in ⚙️ wählen!",
        "warn_empty":          "Leer",
        "warn_empty_msg":      "Keine Karten in der Liste!",
        "warn_no_images":      "Keine Bilder",
        "warn_no_images_msg":  "Lade erst Karten per Download oder Clipboard!",
        "export_done_title":   "✅ Export fertig!",
        "export_done_msg":     "✅ {n} Proxy-Blatt/-Blätter!\nFormate: {f}\n\nOrdnerstruktur:\n{s}\n\ntmp/ gelöscht ✓",
        "status_exported":     "✅ {n} Blätter in '{d}' gespeichert",
        "status_ready_dl":     "✅ {n} Karten bereit → exportieren!",
        "tmp_deleted":         "🗑 tmp/ gelöscht.",
        "scryfall_info":       "✅ Sucht immer auf Englisch\nAblauf: Name(EN) → oracle_id → prints+lang:XX → Bild\nFallback auf EN wenn Sprache nicht verfügbar",
        "mtgio_info":          "✅ Kein Key  |  5000 Req/h\nAblauf: Name(EN) → multiverseid → foreignNames → Gatherer\nName-Fallback wenn ID-Sprache fehlt\nScryfall-Fallback als letzter Ausweg",
        "path_structure":      "→ Struktur: {b}/{d}/[API]/[sprache]/proxy_01.jpg\n   Aktive APIs: {a}",
        "path_no_api":         "→ Keine API ausgewählt!",
        "path_apis_only":      "→ APIs: {a}",
        "lang_info":           "→ Download: {l}",
        "path_no_deck":        "→ Basis: {b}  |  Deckname fehlt",
        "config_saved":        "💾 Einstellungen gespeichert.",
    }
}

CARD_LANGUAGES = {
    "English (en)":             "en",
    "German (de)":              "de",
    "French (fr)":              "fr",
    "Spanish (es)":             "es",
    "Italian (it)":             "it",
    "Portuguese (pt)":          "pt",
    "Japanese (ja)":            "ja",
    "Korean (ko)":              "ko",
    "Russian (ru)":             "ru",
    "Chinese Simplified (zhs)": "zhs",
    "Chinese Traditional (zht)":"zht",
}

MTGIO_LANGUAGES = {
    "en":  "English",
    "de":  "German",
    "fr":  "French",
    "es":  "Spanish",
    "it":  "Italian",
    "pt":  "Portuguese (Brazil)",
    "ja":  "Japanese",
    "ko":  "Korean",
    "ru":  "Russian",
    "zhs": "Chinese Simplified",
    "zht": "Chinese Traditional",
}

APIS = {
    "Scryfall":   {"desc_en": "Free, no key required",               "needs_key": False},
    "MTG.io":     {"desc_en": "magicthegathering.io – Name→ID→Lang", "needs_key": False},
    "Scrydex":    {"desc_en": "Scryfall mirror, no key required",     "needs_key": False},
    "Cardmarket": {"desc_en": "Requires App-Token & Secret",          "needs_key": True},
}

UI_LANGUAGES = {"English": "en", "Deutsch": "de"}


def safe_path(name):
    name = name.strip()
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    name = re.sub(r'_+', '_', name)
    return name


def t(key, lang, **kwargs):
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text


# ══════════════════════════════════════════════════════════════
#  MANUAL FALLBACK DIALOG
# ══════════════════════════════════════════════════════════════

class ManualCardDialog:
    def __init__(self, parent, card_name, lang_code, api_name, ui_lang):
        self.result = None
        self._img   = None
        self._lang  = ui_lang

        self.win = tk.Toplevel(parent)
        self.win.title(t("manual_title", ui_lang))
        self.win.geometry("480x400")
        self.win.resizable(False, False)
        self.win.grab_set()
        self.win.focus_force()

        main = tk.Frame(self.win, padx=20, pady=15)
        main.pack(fill="both", expand=True)

        tk.Label(main, text=t("manual_header", ui_lang),
                 font=("Arial", 13, "bold"), fg="#c62828").pack(pady=(0, 8))

        info = tk.Frame(main, bg="#fff8e1", relief="solid", bd=1)
        info.pack(fill="x", pady=6)
        tk.Label(info,
                 text=(t("manual_card", ui_lang) + card_name + "\n" +
                       t("manual_lang", ui_lang) + lang_code.upper() + "\n" +
                       t("manual_api",  ui_lang) + api_name),
                 font=("Courier", 11), bg="#fff8e1",
                 justify="left").pack(padx=12, pady=8)

        tk.Label(main, text=t("manual_guide", ui_lang),
                 font=("Arial", 10), justify="left",
                 fg="#424242").pack(anchor="w", pady=8)

        self.preview = tk.Label(main,
                                text=t("manual_no_img", ui_lang),
                                bg="#eceff1", relief="sunken",
                                width=30, height=5,
                                font=("Arial", 9), fg="gray")
        self.preview.pack(pady=6)

        btns = tk.Frame(main)
        btns.pack(fill="x", pady=8)

        tk.Button(btns, text=t("btn_clipboard_load", ui_lang),
                  command=self._load_clipboard,
                  bg="#1565c0", fg="white",
                  font=("Arial", 11, "bold"),
                  width=20).pack(side="left", padx=(0, 6))

        self.btn_use = tk.Button(
            btns, text=t("btn_use", ui_lang),
            command=self._use,
            bg="#4caf50", fg="white",
            font=("Arial", 11, "bold"),
            width=14, state="disabled")
        self.btn_use.pack(side="left", padx=6)

        tk.Button(btns, text=t("btn_skip", ui_lang),
                  command=self._skip,
                  bg="#757575", fg="white",
                  font=("Arial", 11),
                  width=12).pack(side="right")

    def _load_clipboard(self):
        try:
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image) and img.size[0] > 10:
                self._img = img.copy().convert("RGB")
                thumb = self._img.copy()
                thumb.thumbnail((250, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(thumb)
                self.preview.config(image=photo, text="", bg="white")
                self.preview.image = photo
                self.btn_use.config(state="normal")
            else:
                messagebox.showwarning(
                    "⚠️", t("no_image_warn", self._lang),
                    parent=self.win)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.win)

    def _use(self):
        if self._img:
            self.result = self._img
        self.win.destroy()

    def _skip(self):
        self.result = None
        self.win.destroy()

    def wait(self):
        self.win.wait_window()
        return self.result


# ══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════

class MTGProxyGUI:
    def __init__(self, root):
        self.root = root

        # ── Defaults ──────────────────────────────────────────
        self.ui_lang        = tk.StringVar(value="en")
        self.dpi            = 300
        self.border_px      = 8
        self.cut_color      = "#00AA00"
        self.tmp_dir        = "tmp"

        self.api_interval   = tk.IntVar(value=100)
        self.dl_limit_mbit  = tk.DoubleVar(value=1.0)
        self.base_path      = tk.StringVar(value="")
        self.deck_name      = tk.StringVar(value="")
        self.default_lang   = tk.StringVar(value="en")
        self.default_api    = tk.StringVar(value="Scryfall")

        self.active_apis    = {n: tk.BooleanVar(value=(n == "Scryfall"))
                               for n in APIS}
        self.api_keys       = {
            "Cardmarket_app_token":     tk.StringVar(value=""),
            "Cardmarket_app_secret":    tk.StringVar(value=""),
            "Cardmarket_access_token":  tk.StringVar(value=""),
            "Cardmarket_access_secret": tk.StringVar(value=""),
        }
        self.lang_vars      = {code: tk.BooleanVar(value=False)
                               for code in CARD_LANGUAGES.values()}
        self.extra_langs    = []
        self.manual_fb      = tk.BooleanVar(value=False)
        self.card_images    = [None] * 4
        self.downloaded     = {}
        self.export_png     = tk.BooleanVar(value=False)
        self.export_jpg     = tk.BooleanVar(value=True)
        self.export_pdf     = tk.BooleanVar(value=False)
        self.preview_active = tk.BooleanVar(value=False)
        self._cancel_dl     = False
        self._manual_event  = threading.Event()
        self._manual_result = None

        # ── Load config ───────────────────────────────────────
        self._load_config()

        # ── Build UI ──────────────────────────────────────────
        self._build_ui()

        self.ui_lang.trace_add("write", self._on_lang_change)

    # ══════════════════════════════════════════════════════════
    #  CONFIG LOAD / SAVE
    # ══════════════════════════════════════════════════════════

    def _load_config(self):
        cfg = load_config()
        if not cfg:
            return

        self.ui_lang.set(       cfg.get("ui_lang",       "en"))
        self.base_path.set(     cfg.get("base_path",     ""))
        self.deck_name.set(     cfg.get("deck_name",     ""))
        self.default_lang.set(  cfg.get("default_lang",  "en"))
        self.default_api.set(   cfg.get("default_api",   "Scryfall"))
        self.cut_color =         cfg.get("cut_color",     "#00AA00")
        self.border_px =         cfg.get("border_px",     8)
        self.api_interval.set(  cfg.get("api_interval",  100))
        self.dl_limit_mbit.set( cfg.get("dl_limit_mbit", 1.0))
        self.manual_fb.set(     cfg.get("manual_fb",     False))
        self.export_png.set(    cfg.get("export_png",    False))
        self.export_jpg.set(    cfg.get("export_jpg",    True))
        self.export_pdf.set(    cfg.get("export_pdf",    False))

        saved_apis = cfg.get("active_apis", {})
        for api_name in APIS:
            self.active_apis[api_name].set(
                saved_apis.get(api_name, api_name == "Scryfall"))

        saved_keys = cfg.get("api_keys", {})
        for key in self.api_keys:
            self.api_keys[key].set(saved_keys.get(key, ""))

        saved_langs = cfg.get("lang_vars", {})
        for code in self.lang_vars:
            self.lang_vars[code].set(saved_langs.get(code, False))

        self.extra_langs = cfg.get("extra_langs", [])

    def _save_config(self):
        save_config({
            "ui_lang":       self.ui_lang.get(),
            "base_path":     self.base_path.get(),
            "deck_name":     self.deck_name.get(),
            "default_lang":  self.default_lang.get(),
            "default_api":   self.default_api.get(),
            "cut_color":     self.cut_color,
            "border_px":     self.border_px,
            "api_interval":  self.api_interval.get(),
            "dl_limit_mbit": self.dl_limit_mbit.get(),
            "manual_fb":     self.manual_fb.get(),
            "export_png":    self.export_png.get(),
            "export_jpg":    self.export_jpg.get(),
            "export_pdf":    self.export_pdf.get(),
            "active_apis":   {n: v.get() for n, v in self.active_apis.items()},
            "api_keys":      {k: v.get() for k, v in self.api_keys.items()},
            "lang_vars":     {c: v.get() for c, v in self.lang_vars.items()},
            "extra_langs":   self.extra_langs,
        })

    # ══════════════════════════════════════════════════════════
    #  LANGUAGE
    # ══════════════════════════════════════════════════════════

    def _on_lang_change(self, *args):
        self._refresh_main_labels()

    def _refresh_main_labels(self):
        lang = self.ui_lang.get()
        self.root.title(t("title", lang))
        try:
            self.lbl_subtitle.config(text=t("subtitle", lang))
            self.lbl_deck_name.config(text=t("deck_name", lang))
            self.frame_deck.config(text=t("deck_frame", lang))
            self.lbl_decklist.config(text=t("decklist_label", lang))
            self.btn_download_main.config(text=t("btn_download", lang))
            self.btn_load_export.config(text=t("btn_load_export", lang))
            self.btn_cancel.config(text=t("btn_cancel", lang))
            self.lbl_log.config(text=t("log_label", lang))
            self.chk_preview.config(text=t("preview_check", lang))
            self.btn_export_main.config(text=t("btn_export", lang))
            self.notebook.tab(0, text=t("tab_decklist", lang))
            self.notebook.tab(1, text=t("tab_clipboard", lang))
            for i, btn in enumerate(self.clipboard_buttons):
                if "✓" not in btn.cget("text"):
                    btn.config(text=t("clipboard_btn", lang, n=i+1))
            self._update_path_preview()
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════
    #  BUILD MAIN UI
    # ══════════════════════════════════════════════════════════

    def _build_ui(self):
        lang = self.ui_lang.get()
        self.root.title(t("title", lang))
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{int(sw*0.55)}x{int(sh*0.75)}")
        self.root.minsize(650, 550)

        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=1)

        # Title
        frame_title = tk.Frame(main)
        frame_title.pack(fill="x", pady=(0, 5))
        frame_title.columnconfigure(0, weight=1)
        tk.Label(frame_title, text="🎴 ProxyForge",
                 font=("Arial", 15, "bold"), fg="#2e7d32").grid(
                 row=0, column=0, sticky="w")
        tk.Button(frame_title, text="⚙️",
                  command=self._open_settings,
                  font=("Arial", 14), width=3,
                  relief="flat", bg="#f0f0f0",
                  cursor="hand2").grid(row=0, column=1, sticky="e", padx=5)

        self.lbl_subtitle = tk.Label(
            main, text=t("subtitle", lang),
            font=("Arial", 10), fg="gray")
        self.lbl_subtitle.pack(anchor="w")

        # Deck frame
        self.frame_deck = tk.LabelFrame(
            main, text=t("deck_frame", lang),
            font=("Arial", 10, "bold"), padx=10, pady=6)
        self.frame_deck.pack(fill="x", pady=6)
        self.frame_deck.columnconfigure(1, weight=1)

        self.lbl_deck_name = tk.Label(
            self.frame_deck, text=t("deck_name", lang),
            font=("Arial", 10))
        self.lbl_deck_name.grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(self.frame_deck, textvariable=self.deck_name,
                 font=("Arial", 10)).grid(
                 row=0, column=1, sticky="ew", padx=5)

        self.lbl_path_preview = tk.Label(
            self.frame_deck,
            text=t("path_hint", lang),
            font=("Arial", 9, "italic"), fg="gray")
        self.lbl_path_preview.grid(
            row=1, column=0, columnspan=2, sticky="w", pady=2)

        self.base_path.trace_add("write", self._update_path_preview)
        self.deck_name.trace_add("write", self._update_path_preview)
        self.default_api.trace_add("write", self._update_path_preview)

        # Notebook
        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="x", pady=6)

        # Tab: Decklist
        tab_dl = tk.Frame(self.notebook, padx=10, pady=8)
        self.notebook.add(tab_dl, text=t("tab_decklist", lang))

        self.lbl_decklist = tk.Label(
            tab_dl, text=t("decklist_label", lang),
            font=("Arial", 10, "bold"))
        self.lbl_decklist.pack(anchor="w")

        self.deck_input = scrolledtext.ScrolledText(
            tab_dl, height=5, font=("Courier", 10))
        self.deck_input.pack(fill="x", pady=4)
        self.deck_input.insert("1.0",
            "1 Octavia, Living Thesis\n1 Brainstorm\n1 Ponder\n1 Windfall")

        frame_btns = tk.Frame(tab_dl)
        frame_btns.pack(fill="x", pady=4)

        self.btn_download_main = tk.Button(
            frame_btns, text=t("btn_download", lang),
            command=self._start_download,
            bg="#1565c0", fg="white",
            font=("Arial", 11, "bold"), width=15)
        self.btn_download_main.pack(side="left", padx=(0, 4))

        self.btn_load_export = tk.Button(
            frame_btns, text=t("btn_load_export", lang),
            command=self._load_and_export,
            bg="#e65100", fg="white",
            font=("Arial", 11, "bold"), width=20)
        self.btn_load_export.pack(side="left", padx=4)

        self.btn_cancel = tk.Button(
            frame_btns, text=t("btn_cancel", lang),
            command=self._cancel_download,
            bg="#c62828", fg="white",
            font=("Arial", 11, "bold"),
            width=12, state="disabled")
        self.btn_cancel.pack(side="left", padx=4)

        tk.Button(frame_btns, text="🗑",
                  command=lambda: self.deck_input.delete("1.0", tk.END),
                  font=("Arial", 11), width=3).pack(side="right")

        frame_bar = tk.Frame(tab_dl)
        frame_bar.pack(fill="x", pady=(4, 0))
        self.dl_progress = ttk.Progressbar(frame_bar, mode='determinate')
        self.dl_progress.pack(side="left", fill="x",
                               expand=True, padx=(0, 8))
        self.lbl_speed = tk.Label(
            frame_bar, text="⚡ --",
            font=("Courier", 10, "bold"),
            fg="#1565c0", width=14, anchor="w")
        self.lbl_speed.pack(side="left")
        self.lbl_eta = tk.Label(
            frame_bar, text="ETA: --",
            font=("Courier", 10), fg="gray",
            width=10, anchor="w")
        self.lbl_eta.pack(side="left")

        self.lbl_log = tk.Label(
            tab_dl, text=t("log_label", lang),
            font=("Arial", 10, "bold"))
        self.lbl_log.pack(anchor="w", pady=(4, 0))

        self.log = scrolledtext.ScrolledText(
            tab_dl, height=4, font=("Courier", 9),
            state="disabled", bg="#1e1e1e", fg="#00ff00")
        self.log.pack(fill="x")

        # Tab: Clipboard
        tab_cb = tk.Frame(self.notebook, padx=10, pady=8)
        self.notebook.add(tab_cb, text=t("tab_clipboard", lang))

        self.clipboard_buttons = []
        for i in range(4):
            btn = tk.Button(tab_cb,
                            text=t("clipboard_btn", lang, n=i+1),
                            command=lambda n=i: self._load_clipboard(n),
                            width=22, height=1,
                            bg="#e8f5e8", font=("Arial", 10))
            btn.grid(row=i//2, column=i%2,
                     padx=8, pady=4, sticky="ew")
            tab_cb.columnconfigure(i%2, weight=1)
            self.clipboard_buttons.append(btn)

        # Preview
        frame_prev = tk.Frame(main)
        frame_prev.pack(fill="x")
        self.chk_preview = tk.Checkbutton(
            frame_prev, text=t("preview_check", lang),
            variable=self.preview_active,
            command=self._toggle_preview,
            font=("Arial", 10, "bold"))
        self.chk_preview.pack(side="left")

        self.preview_frame = tk.Frame(main, relief="sunken", bd=2)
        self.preview_canvas = tk.Canvas(
            self.preview_frame, bg="white", height=200)
        self.preview_canvas.pack(fill="both", expand=True)

        self.export_progress = ttk.Progressbar(main, mode='determinate')
        self.export_progress.pack(fill="x", pady=4)

        self.btn_export_main = tk.Button(
            main, text=t("btn_export", lang),
            command=self._export_all,
            bg="#4caf50", fg="white",
            font=("Arial", 13, "bold"), height=2)
        self.btn_export_main.pack(fill="x", pady=4)

        self.lbl_status = tk.Label(
            main, text=t("status_ready", lang),
            font=("Arial", 10), fg="#1976d2")
        self.lbl_status.pack(pady=2)

        # ── Save & close on window X ───────────────────────────
        def _on_app_close():
            self._save_config()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", _on_app_close)

    # ══════════════════════════════════════════════════════════
    #  SETTINGS WINDOW
    # ══════════════════════════════════════════════════════════

    def _open_settings(self):
        lang = self.ui_lang.get()
        win = tk.Toplevel(self.root)
        win.title(t("settings_title", lang))
        win.geometry("580x940")
        win.resizable(False, False)
        win.grab_set()

        canvas = tk.Canvas(win)
        sb = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        sf = tk.Frame(canvas, padx=20, pady=15)
        cw = canvas.create_window((0, 0), window=sf, anchor="nw")

        sf.bind("<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(cw, width=e.width))

        def _scroll(e):
            try:
                canvas.yview_scroll(-1*(e.delta//120), "units")
            except tk.TclError:
                pass

        win.bind("<MouseWheel>", _scroll)

        def _close():
            self._save_config()
            win.unbind("<MouseWheel>")
            win.destroy()
            self._refresh_main_labels()
            self.lbl_status.config(
                text=t("config_saved", self.ui_lang.get()),
                fg="#2e7d32")

        win.protocol("WM_DELETE_WINDOW", _close)

        sf.columnconfigure(1, weight=1)
        row = 0

        tk.Label(sf, text=t("settings_header", lang),
                 font=("Arial", 13, "bold"), fg="#2e7d32").grid(
                 row=row, column=0, columnspan=3,
                 sticky="w", pady=(0, 12))
        row += 1

        # ── UI Language ────────────────────────────────────────
        tk.Label(sf, text=t("ui_language", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, sticky="w", pady=5)
        f_ul = tk.Frame(sf)
        f_ul.grid(row=row, column=1, columnspan=2, sticky="w")
        for ui_name, ui_code in UI_LANGUAGES.items():
            tk.Radiobutton(f_ul, text=ui_name,
                           variable=self.ui_lang,
                           value=ui_code,
                           font=("Arial", 11)).pack(side="left", padx=8)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── Base Path ──────────────────────────────────────────
        tk.Label(sf, text=t("base_path", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, sticky="w", pady=5)
        tk.Entry(sf, textvariable=self.base_path,
                 font=("Arial", 10)).grid(
                 row=row, column=1, sticky="ew", padx=8)
        tk.Button(sf, text="📂",
                  command=self._choose_base_path,
                  font=("Arial", 10), width=3).grid(row=row, column=2)
        row += 1
        tk.Label(sf, text=t("base_path_hint", lang),
                 font=("Arial", 9), fg="gray").grid(
                 row=row, column=1, sticky="w", padx=8)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── APIs ───────────────────────────────────────────────
        tk.Label(sf, text=t("apis_header", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, columnspan=3,
                 sticky="w", pady=(0, 5))
        row += 1

        tk.Label(sf, text=t("default_api", lang),
                 font=("Arial", 10)).grid(
                 row=row, column=0, sticky="w", pady=4)
        ttk.Combobox(sf, values=list(APIS.keys()),
                     textvariable=self.default_api,
                     state="readonly", width=20,
                     font=("Arial", 10)).grid(
                     row=row, column=1, sticky="w", padx=8, pady=4)
        row += 1

        frame_apis = tk.LabelFrame(
            sf, text=t("active_apis", lang),
            font=("Arial", 9), padx=8, pady=6)
        frame_apis.grid(row=row, column=0, columnspan=3,
                         sticky="ew", padx=5, pady=4)
        row += 1

        for api_name, api_info in APIS.items():
            f = tk.Frame(frame_apis)
            f.pack(fill="x", pady=3)
            f.columnconfigure(1, weight=1)

            tk.Checkbutton(f, text=f"  {api_name}",
                            variable=self.active_apis[api_name],
                            font=("Arial", 10, "bold")).grid(
                            row=0, column=0, sticky="w")
            tk.Label(f, text=api_info["desc_en"],
                     font=("Arial", 9), fg="gray").grid(
                     row=0, column=1, sticky="w", padx=10)

            if api_name == "Scryfall":
                ib = tk.Frame(f, bg="#e3f2fd", relief="solid", bd=1)
                ib.grid(row=1, column=0, columnspan=3,
                         sticky="ew", padx=15, pady=4)
                tk.Label(ib, text=t("scryfall_info", lang),
                         font=("Arial", 8), fg="#1565c0",
                         bg="#e3f2fd", justify="left").pack(
                         padx=6, pady=4, anchor="w")

            if api_name == "MTG.io":
                ib = tk.Frame(f, bg="#e8f5e9", relief="solid", bd=1)
                ib.grid(row=1, column=0, columnspan=3,
                         sticky="ew", padx=15, pady=4)
                tk.Label(ib, text=t("mtgio_info", lang),
                         font=("Arial", 8), fg="#2e7d32",
                         bg="#e8f5e9", justify="left").pack(
                         padx=6, pady=4, anchor="w")

            if api_name == "Cardmarket":
                kf = tk.Frame(f, bg="#fff8e1", relief="solid", bd=1)
                kf.grid(row=1, column=0, columnspan=3,
                         sticky="ew", padx=15, pady=4)
                kf.columnconfigure(1, weight=1)
                for r_idx, (lbl, key) in enumerate([
                    ("App Token:",     "Cardmarket_app_token"),
                    ("App Secret:",    "Cardmarket_app_secret"),
                    ("Access Token:",  "Cardmarket_access_token"),
                    ("Access Secret:", "Cardmarket_access_secret"),
                ]):
                    tk.Label(kf, text=lbl, font=("Arial", 9),
                             bg="#fff8e1").grid(
                             row=r_idx, column=0, sticky="w", padx=5, pady=2)
                    tk.Entry(kf, textvariable=self.api_keys[key],
                             font=("Arial", 9), show="*", width=28).grid(
                             row=r_idx, column=1, sticky="ew", padx=5, pady=2)
                tk.Label(kf,
                         text="⚠️ cardmarket.com/en/Magic/Account/API",
                         font=("Arial", 8), fg="#e65100",
                         bg="#fff8e1").grid(
                         row=4, column=0, columnspan=2,
                         sticky="w", padx=5, pady=4)

        self.lbl_api_path = tk.Label(
            sf, text=self._get_api_path_info(),
            font=("Arial", 9, "italic"), fg="#1565c0",
            wraplength=500, justify="left")
        self.lbl_api_path.grid(row=row, column=0, columnspan=3,
                                sticky="w", padx=5, pady=4)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── Manual Fallback ────────────────────────────────────
        frame_mf = tk.LabelFrame(
            sf, text=t("manual_fb_frame", lang),
            font=("Arial", 10, "bold"), padx=10, pady=8)
        frame_mf.grid(row=row, column=0, columnspan=3,
                       sticky="ew", padx=5, pady=6)

        tk.Checkbutton(frame_mf,
                       text=t("manual_fb_enable", lang),
                       variable=self.manual_fb,
                       font=("Arial", 11, "bold"),
                       fg="#c62828").grid(
                       row=0, column=0, columnspan=2, sticky="w", pady=4)
        tk.Label(frame_mf, text=t("manual_fb_desc", lang),
                 font=("Arial", 9), fg="#424242",
                 justify="left").grid(
                 row=1, column=0, columnspan=2,
                 sticky="w", padx=5, pady=4)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── API Interval ───────────────────────────────────────
        tk.Label(sf, text=t("api_interval", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, sticky="w", pady=5)
        f_int = tk.Frame(sf)
        f_int.grid(row=row, column=1, columnspan=2, sticky="w")
        vcmd_int = (win.register(self._val_int), '%P')
        tk.Spinbox(f_int, from_=0, to=5000,
                   textvariable=self.api_interval,
                   width=7, font=("Arial", 11),
                   validate="key", validatecommand=vcmd_int).pack(side="left")
        tk.Label(f_int, text="ms", font=("Arial", 11),
                 fg="gray").pack(side="left", padx=4)
        row += 1
        tk.Label(sf, text=t("api_interval_hint", lang),
                 font=("Arial", 9), fg="gray").grid(
                 row=row, column=0, columnspan=3, sticky="w", padx=5)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── Download Limit ─────────────────────────────────────
        tk.Label(sf, text=t("dl_limit", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, sticky="w", pady=5)
        f_dl = tk.Frame(sf)
        f_dl.grid(row=row, column=1, columnspan=2, sticky="w")
        vcmd_float = (win.register(self._val_float), '%P')
        tk.Spinbox(f_dl, from_=0.1, to=1000.0, increment=0.5,
                   textvariable=self.dl_limit_mbit,
                   width=7, font=("Arial", 11), format="%.1f",
                   validate="key", validatecommand=vcmd_float).pack(side="left")
        tk.Label(f_dl, text="Mbit/s", font=("Arial", 11),
                 fg="gray").pack(side="left", padx=4)
        row += 1
        tk.Label(sf, text=t("dl_limit_hint", lang),
                 font=("Arial", 9), fg="gray").grid(
                 row=row, column=0, columnspan=3, sticky="w", padx=5)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── Card Languages ─────────────────────────────────────
        tk.Label(sf, text=t("languages_header", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, columnspan=3,
                 sticky="w", pady=(0, 5))
        row += 1

        tk.Label(sf, text=t("lang_default", lang),
                 font=("Arial", 10)).grid(
                 row=row, column=0, sticky="w", pady=4)
        lang_names  = list(CARD_LANGUAGES.keys())
        lang_values = list(CARD_LANGUAGES.values())
        cur_idx = (lang_values.index(self.default_lang.get())
                   if self.default_lang.get() in lang_values else 0)
        self.combo_card_lang = ttk.Combobox(
            sf, values=lang_names,
            state="readonly", width=24, font=("Arial", 10))
        self.combo_card_lang.current(cur_idx)
        self.combo_card_lang.grid(row=row, column=1, columnspan=2,
                                   sticky="w", padx=8, pady=4)
        self.combo_card_lang.bind("<<ComboboxSelected>>",
                                   self._on_card_lang_change)
        row += 1

        tk.Label(sf, text=t("lang_extra", lang),
                 font=("Arial", 10)).grid(
                 row=row, column=0, sticky="nw", pady=4)
        frame_lc = tk.Frame(sf, relief="sunken", bd=1)
        frame_lc.grid(row=row, column=1, columnspan=2,
                       sticky="ew", padx=8, pady=4)
        for idx, lname in enumerate(lang_names):
            code = CARD_LANGUAGES[lname]
            tk.Checkbutton(frame_lc, text=lname,
                            variable=self.lang_vars[code],
                            command=self._on_extra_lang_change,
                            font=("Arial", 10), anchor="w").grid(
                            row=idx//2, column=idx%2,
                            sticky="w", padx=8, pady=1)
        row += 1

        self.lbl_lang_info = tk.Label(
            sf, text=self._get_lang_info(),
            font=("Arial", 9, "italic"), fg="#1565c0")
        self.lbl_lang_info.grid(row=row, column=0, columnspan=3,
                                 sticky="w", padx=5, pady=4)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── Cut Color ──────────────────────────────────────────
        tk.Label(sf, text=t("cut_color", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, sticky="w", pady=5)
        f_col = tk.Frame(sf)
        f_col.grid(row=row, column=1, columnspan=2, sticky="w")
        self.btn_color = tk.Button(
            f_col, text=t("choose_color", lang),
            command=lambda: self._choose_color(win),
            bg=self.cut_color, fg="white",
            font=("Arial", 10, "bold"))
        self.btn_color.pack(side="left", padx=5)
        self.lbl_color = tk.Label(
            f_col, text=self.cut_color,
            font=("Arial", 10), fg=self.cut_color)
        self.lbl_color.pack(side="left", padx=10)
        row += 1

        # ── Border Width ───────────────────────────────────────
        tk.Label(sf, text=t("border_width", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, sticky="w", pady=5)
        f_brd = tk.Frame(sf)
        f_brd.grid(row=row, column=1, columnspan=2, sticky="ew")
        self.slider_border = tk.Scale(
            f_brd, from_=2, to=20,
            orient=tk.HORIZONTAL,
            command=self._on_border_change,
            showvalue=False, bg="white", length=180)
        self.slider_border.set(self.border_px)
        self.slider_border.pack(side="left")
        self.lbl_border = tk.Label(
            f_brd, text=f"{self.border_px}px",
            font=("Arial", 10), width=5)
        self.lbl_border.pack(side="left", padx=5)
        row += 1

        ttk.Separator(sf, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        # ── Export Formats ─────────────────────────────────────
        tk.Label(sf, text=t("export_formats", lang),
                 font=("Arial", 11, "bold")).grid(
                 row=row, column=0, sticky="w", pady=5)
        f_fmt = tk.Frame(sf)
        f_fmt.grid(row=row, column=1, columnspan=2, sticky="w")
        tk.Checkbutton(f_fmt, text="PNG",
                       variable=self.export_png,
                       font=("Arial", 10)).pack(side="left", padx=5)
        tk.Checkbutton(f_fmt, text="JPEG",
                       variable=self.export_jpg,
                       font=("Arial", 10)).pack(side="left", padx=5)
        tk.Checkbutton(f_fmt, text="PDF",
                       variable=self.export_pdf,
                       font=("Arial", 10)).pack(side="left", padx=5)
        row += 1

        # ── Save & Close button ────────────────────────────────
        tk.Button(sf, text=t("btn_save_close", lang),
                  command=_close,
                  bg="#4caf50", fg="white",
                  font=("Arial", 11, "bold"),
                  width=22).grid(row=row, column=0,
                                  columnspan=3, pady=12)

    # ══════════════════════════════════════════════════════════
    #  CALLBACKS / HELPERS
    # ══════════════════════════════════════════════════════════

    def _val_int(self, v):
        return v == "" or v.isdigit()

    def _val_float(self, v):
        if v in ("", "."):
            return True
        try:
            float(v)
            return True
        except ValueError:
            return False

    def _get_api_path_info(self):
        lang   = self.ui_lang.get()
        active = [n for n, v in self.active_apis.items() if v.get()]
        base   = self.base_path.get().strip()
        deck   = safe_path(self.deck_name.get().strip())
        if not active:
            return t("path_no_api", lang)
        if base and deck:
            return t("path_structure", lang,
                     b=base, d=deck, a=', '.join(active))
        return t("path_apis_only", lang, a=', '.join(active))

    def _get_lang_info(self):
        lang = self.ui_lang.get()
        all_langs = [self.default_lang.get()] + [
            s for s in self.extra_langs
            if s != self.default_lang.get()
        ]
        inv = {v: k for k, v in CARD_LANGUAGES.items()}
        return t("lang_info", lang,
                 l=', '.join(inv.get(s, s) for s in all_langs))

    def _update_path_preview(self, *args):
        lang   = self.ui_lang.get()
        base   = self.base_path.get().strip()
        name   = safe_path(self.deck_name.get().strip())
        active = [n for n, v in self.active_apis.items() if v.get()]
        try:
            if base and name and active:
                self.lbl_path_preview.config(
                    text=f"→ {base}/{name}/[API]/[lang]/",
                    fg="#2e7d32")
            elif base:
                self.lbl_path_preview.config(
                    text=t("path_no_deck", lang, b=base), fg="orange")
            else:
                self.lbl_path_preview.config(
                    text=t("path_hint", lang), fg="gray")
        except Exception:
            pass

    def _choose_base_path(self):
        path = filedialog.askdirectory(title="Base Folder")
        if path:
            self.base_path.set(path)

    def _choose_color(self, parent=None):
        color = colorchooser.askcolor(
            title="Cut Color", parent=parent)[1]
        if color:
            self.cut_color = color
            if hasattr(self, 'btn_color'):
                self.btn_color.config(bg=color)
                self.lbl_color.config(text=color, fg=color)
            if self.preview_active.get():
                self._draw_preview()

    def _on_border_change(self, value):
        self.border_px = int(float(value))
        if hasattr(self, 'lbl_border'):
            self.lbl_border.config(text=f"{self.border_px}px")
        if self.preview_active.get():
            self._draw_preview()

    def _on_card_lang_change(self, event=None):
        sel = self.combo_card_lang.get()
        self.default_lang.set(CARD_LANGUAGES[sel])
        self.lang_vars[CARD_LANGUAGES[sel]].set(False)
        self._on_extra_lang_change()
        if hasattr(self, 'lbl_lang_info'):
            self.lbl_lang_info.config(text=self._get_lang_info())

    def _on_extra_lang_change(self):
        default = self.default_lang.get()
        self.extra_langs = [
            code for code, var in self.lang_vars.items()
            if var.get() and code != default
        ]
        if hasattr(self, 'lbl_lang_info'):
            self.lbl_lang_info.config(text=self._get_lang_info())

    def _log(self, text):
        self.log.config(state="normal")
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.config(state="disabled")
        self.root.update_idletasks()

    def _toggle_preview(self):
        if self.preview_active.get():
            self.preview_frame.pack(
                fill="x", pady=4, before=self.lbl_status)
            self._draw_preview()
        else:
            self.preview_frame.pack_forget()

    def _cancel_download(self):
        self._cancel_dl = True
        self._log("⛔ Cancelled by user.")
        self.btn_cancel.config(state="disabled")
        self.lbl_speed.config(text="⛔ Cancelled")
        self.lbl_eta.config(text="")
        self._manual_event.set()

    # ══════════════════════════════════════════════════════════
    #  MANUAL FALLBACK THREAD SYNC
    # ══════════════════════════════════════════════════════════

    def _open_manual_dialog(self, card, lang_code, api_name):
        self._manual_result = None
        self._manual_event.clear()

        def _open():
            dlg = ManualCardDialog(
                self.root, card, lang_code, api_name,
                self.ui_lang.get())
            result = dlg.wait()
            self._manual_result = result
            self._manual_event.set()

        self.root.after(0, _open)
        self._manual_event.wait()
        return self._manual_result

    # ══════════════════════════════════════════════════════════
    #  API ADAPTERS
    # ══════════════════════════════════════════════════════════

    def _download_image(self, url):
        try:
            limit_mbit    = self.dl_limit_mbit.get()
            limit_bytes_s = (limit_mbit * 1_000_000 / 8
                             if limit_mbit > 0 else None)
            r = requests.get(url, timeout=15, stream=True)
            if r.status_code != 200:
                return None
            chunks = []
            for chunk in r.iter_content(chunk_size=4096):
                if self._cancel_dl:
                    return None
                if chunk:
                    chunks.append(chunk)
                    if limit_bytes_s:
                        time.sleep(len(chunk) / limit_bytes_s)
            return Image.open(
                io.BytesIO(b"".join(chunks))).convert("RGB")
        except:
            return None

    def _fetch_scryfall(self, name, lang="en"):
        try:
            url = (f"https://api.scryfall.com/cards/named"
                   f"?exact={requests.utils.quote(name)}&lang=en")
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                url = (f"https://api.scryfall.com/cards/named"
                       f"?fuzzy={requests.utils.quote(name)}&lang=en")
                r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return None, False

            data = r.json()
            en_url = None
            if "image_uris" in data:
                en_url = data["image_uris"]["normal"]
            elif "card_faces" in data:
                en_url = data["card_faces"][0]["image_uris"]["normal"]

            if lang == "en":
                if en_url:
                    return self._download_image(en_url), True
                return None, False

            oracle_id = data.get("oracle_id", "")
            if oracle_id:
                lang_url = (
                    f"https://api.scryfall.com/cards/search"
                    f"?q=oracle_id%3A{oracle_id}+lang%3A{lang}"
                    f"&unique=prints&order=released&dir=asc")
                r2 = requests.get(lang_url, timeout=10)
                if r2.status_code == 200:
                    cards = r2.json().get("data", [])
                    if cards:
                        card_l = cards[-1]
                        img_url = None
                        if "image_uris" in card_l:
                            img_url = card_l["image_uris"]["normal"]
                        elif "card_faces" in card_l:
                            img_url = card_l["card_faces"][0][
                                "image_uris"]["normal"]
                        if img_url:
                            img = self._download_image(img_url)
                            if img:
                                self._log(
                                    f"  🌍 Scryfall [{lang}]: "
                                    f"'{card_l.get('printed_name') or card_l.get('name')}' "
                                    f"({card_l.get('set','').upper()} "
                                    f"{card_l.get('collector_number','')})")
                                return img, True

                self._log(
                    f"  ⚠️ Scryfall: '{name}' not in [{lang}] → EN fallback")

            if en_url:
                img = self._download_image(en_url)
                if img:
                    return img, False

            return None, False

        except Exception as e:
            self._log(f"  ✗ Scryfall error: {e}")
            return None, False

    def _fetch_mtgio(self, name, lang="en"):
        try:
            url = (f"https://api.magicthegathering.io/v1/cards"
                   f"?name=%22{requests.utils.quote(name)}%22"
                   f"&contains=imageUrl&pageSize=5")
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                self._log(f"  ✗ MTG.io HTTP {r.status_code} → Scryfall")
                return self._fetch_scryfall(name, lang)

            cards = r.json().get("cards", [])
            if not cards:
                self._log(f"  ✗ MTG.io: '{name}' not found → Scryfall")
                return self._fetch_scryfall(name, lang)

            card = next(
                (c for c in cards
                 if c.get("name", "").lower() == name.lower()),
                cards[0])
            mv_en   = card.get("multiverseid")
            foreign = card.get("foreignNames", [])

            self._log(
                f"  ✓ MTG.io: '{card.get('name')}' "
                f"(id={mv_en}, {len(foreign)} languages)")

            if lang == "en":
                img_url = card.get("imageUrl")
                if img_url:
                    img = self._download_image(img_url)
                    if img:
                        return img, True
                if mv_en:
                    img = self._download_image(
                        f"https://gatherer.wizards.com/Handlers/"
                        f"Image.ashx?multiverseid={mv_en}&type=card")
                    if img:
                        return img, True
            else:
                target = MTGIO_LANGUAGES.get(lang, "")
                entry  = next(
                    (f for f in foreign
                     if f.get("language", "").lower() == target.lower()),
                    None)

                if entry and entry.get("multiverseid"):
                    mv_id = entry["multiverseid"]
                    self._log(
                        f"  🌍 MTG.io [{lang}]: id={mv_id} "
                        f"'{entry.get('name', '')}'")
                    img = self._download_image(
                        f"https://gatherer.wizards.com/Handlers/"
                        f"Image.ashx?multiverseid={mv_id}&type=card")
                    if img:
                        return img, True
                    self._log(f"  ⚠️ Gatherer image unavailable")

                if entry and entry.get("name"):
                    fname = entry["name"]
                    self._log(f"  🔄 Name fallback: '{fname}'...")
                    url2 = (
                        f"https://api.magicthegathering.io/v1/cards"
                        f"?name=%22{requests.utils.quote(fname)}%22"
                        f"&contains=imageUrl&pageSize=3")
                    r2 = requests.get(url2, timeout=10)
                    if r2.status_code == 200:
                        for c2 in r2.json().get("cards", []):
                            iu = c2.get("imageUrl")
                            if iu:
                                img = self._download_image(iu)
                                if img:
                                    self._log(f"  ✓ Name fallback OK")
                                    return img, True
                            mv2 = c2.get("multiverseid")
                            if mv2:
                                img = self._download_image(
                                    f"https://gatherer.wizards.com/"
                                    f"Handlers/Image.ashx"
                                    f"?multiverseid={mv2}&type=card")
                                if img:
                                    self._log(f"  ✓ Name fallback (Gatherer)")
                                    return img, True
                    self._log(f"  ✗ Name fallback failed → Scryfall")
                else:
                    self._log(
                        f"  ⚠️ [{lang}] not in foreignNames → Scryfall")

            return self._fetch_scryfall(name, lang)

        except Exception as e:
            self._log(f"  ✗ MTG.io: {e} → Scryfall")
            return self._fetch_scryfall(name, lang)

    def _fetch_scrydex(self, name, lang="en"):
        try:
            url = (f"https://api.scrydex.com/cards/named"
                   f"?exact={requests.utils.quote(name)}&lang={lang}")
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                url = (f"https://api.scrydex.com/cards/named"
                       f"?fuzzy={requests.utils.quote(name)}")
                r = requests.get(url, timeout=10)
            if r.status_code != 200:
                self._log(f"  ↩ Scrydex → Scryfall: {name}")
                return self._fetch_scryfall(name, lang)
            data       = r.json()
            found_lang = data.get("lang", "en")
            img_url    = None
            if "image_uris" in data:
                img_url = data["image_uris"]["normal"]
            elif "card_faces" in data:
                img_url = data["card_faces"][0]["image_uris"]["normal"]
            if not img_url:
                return None, False
            return self._download_image(img_url), (found_lang == lang)
        except:
            return self._fetch_scryfall(name, lang)

    def _fetch_cardmarket(self, name, lang="en"):
        import hmac, hashlib, base64, urllib.parse, random, string

        app_token  = self.api_keys["Cardmarket_app_token"].get().strip()
        app_secret = self.api_keys["Cardmarket_app_secret"].get().strip()

        if not app_token or not app_secret:
            self._log(f"  ⚠️ Cardmarket: No key → Scryfall")
            return self._fetch_scryfall(name, lang)

        try:
            search_url = (
                f"https://api.cardmarket.com/ws/v2.0/products/find"
                f"?search={requests.utils.quote(name)}"
                f"&exact=false&idGame=1&idLanguage=1")
            ts    = str(int(time.time()))
            nonce = ''.join(random.choices(
                string.ascii_lowercase + string.digits, k=16))
            params = {
                "oauth_consumer_key":     app_token,
                "oauth_nonce":            nonce,
                "oauth_signature_method": "HMAC-SHA1",
                "oauth_timestamp":        ts,
                "oauth_token": self.api_keys[
                    "Cardmarket_access_token"].get().strip(),
                "oauth_version": "1.0",
            }
            base = "&".join([
                "GET",
                urllib.parse.quote(search_url.split("?")[0], safe=""),
                urllib.parse.quote("&".join(
                    f"{k}={v}" for k, v in sorted(params.items())
                ), safe="")
            ])
            sk  = (urllib.parse.quote(app_secret, safe="") + "&" +
                   urllib.parse.quote(
                       self.api_keys["Cardmarket_access_secret"].get().strip(),
                       safe=""))
            sig = base64.b64encode(
                hmac.new(sk.encode(), base.encode(),
                          hashlib.sha1).digest()).decode()
            params["oauth_signature"] = sig
            auth = "OAuth " + ", ".join(
                f'{k}="{urllib.parse.quote(v, safe="")}"'
                for k, v in params.items())
            r = requests.get(search_url,
                             headers={"Authorization": auth},
                             timeout=10)
            self._log(f"  Cardmarket: HTTP {r.status_code} '{name}'")
        except Exception as e:
            self._log(f"  ✗ Cardmarket: {e}")

        return self._fetch_scryfall(name, lang)

    def _fetch_for_api(self, api_name, card, lang):
        if api_name == "Scryfall":
            return self._fetch_scryfall(card, lang)
        elif api_name == "MTG.io":
            return self._fetch_mtgio(card, lang)
        elif api_name == "Scrydex":
            return self._fetch_scrydex(card, lang)
        elif api_name == "Cardmarket":
            return self._fetch_cardmarket(card, lang)
        return None, False

    # ══════════════════════════════════════════════════════════
    #  DOWNLOAD
    # ══════════════════════════════════════════════════════════

    def _parse_decklist(self):
        text  = self.deck_input.get("1.0", tk.END).strip()
        cards = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 1)
            if parts[0].isdigit() and len(parts) > 1:
                name  = parts[1].strip()
                count = int(parts[0])
            else:
                name  = line
                count = 1
            for _ in range(count):
                cards.append(name)
        return cards

    def _start_download(self):
        self._cancel_dl = False
        threading.Thread(
            target=self._download_thread,
            kwargs={"auto_export": False},
            daemon=True).start()

    def _load_and_export(self):
        lang   = self.ui_lang.get()
        base   = self.base_path.get().strip()
        name   = self.deck_name.get().strip()
        active = [n for n, v in self.active_apis.items() if v.get()]
        if not base or not os.path.isdir(base):
            messagebox.showwarning(
                t("warn_no_path", lang), t("warn_no_path_msg", lang))
            return
        if not name:
            messagebox.showwarning(
                t("warn_no_deck", lang), t("warn_no_deck_msg", lang))
            return
        if not active:
            messagebox.showwarning(
                t("warn_no_api", lang), t("warn_no_api_msg", lang))
            return
        if not (self.export_png.get() or self.export_jpg.get()
                or self.export_pdf.get()):
            messagebox.showwarning(
                t("warn_no_format", lang), t("warn_no_format_msg", lang))
            return
        self._cancel_dl = False
        threading.Thread(
            target=self._download_thread,
            kwargs={"auto_export": True},
            daemon=True).start()

    def _download_thread(self, auto_export=False):
        lang  = self.ui_lang.get()
        cards = self._parse_decklist()
        if not cards:
            messagebox.showwarning(
                t("warn_empty", lang), t("warn_empty_msg", lang))
            return

        active_apis = [n for n, v in self.active_apis.items() if v.get()]
        if not active_apis:
            messagebox.showwarning(
                t("warn_no_api", lang), t("warn_no_api_msg", lang))
            return

        self.root.after(0, lambda: self.btn_cancel.config(state="normal"))
        self.root.after(0, lambda: self.dl_progress.config(value=0))
        os.makedirs(self.tmp_dir, exist_ok=True)

        def_lang   = self.default_lang.get()
        all_langs  = [def_lang] + [
            s for s in self.extra_langs if s != def_lang]
        unique     = list(dict.fromkeys(cards))
        total      = len(unique) * len(all_langs) * len(active_apis)
        interval_s = self.api_interval.get() / 1000.0

        self._log(
            f"▶ {len(unique)} × {len(all_langs)} lang(s) "
            f"× {len(active_apis)} API(s) = {total} downloads\n"
            f"⏱ {self.api_interval.get()} ms  |  "
            f"📶 {self.dl_limit_mbit.get():.1f} Mbit/s\n"
            f"🔌 {', '.join(active_apis)}"
            + ("  |  🖼 Manual FB ON"
               if self.manual_fb.get() else "") + "\n")

        cache = {api: {c: {} for c in unique} for api in active_apis}
        done  = 0
        times = []

        for api_name in active_apis:
            if self._cancel_dl:
                break
            self._log(f"\n── {api_name} ──────────────")

            for card in unique:
                if self._cancel_dl:
                    break
                safe = re.sub(r'[\\/:*?"<>|]', '_', card.strip())
                safe = re.sub(r'_+', '_', safe)

                for card_lang in all_langs:
                    if self._cancel_dl:
                        break
                    tmp_path = os.path.join(
                        self.tmp_dir,
                        f"{api_name}_{safe}_{card_lang}.jpg")
                    t_start = time.time()

                    if os.path.exists(tmp_path):
                        cache[api_name][card][card_lang] = tmp_path
                        done += 1
                        self._log(
                            f"⏭ [{done}/{total}] "
                            f"{card} [{card_lang}] (cached)")
                    else:
                        img, found = self._fetch_for_api(
                            api_name, card, card_lang)
                        t_dur = time.time() - t_start
                        times.append(t_dur)
                        if len(times) > 8:
                            times.pop(0)

                        if (img is None or not found) and \
                                self.manual_fb.get() and \
                                not self._cancel_dl:
                            reason = ("not found"
                                      if img is None
                                      else "EN fallback only")
                            self._log(
                                f"  🖼 Manual fallback ({reason}): "
                                f"'{card}' [{card_lang}]...")
                            manual = self._open_manual_dialog(
                                card, card_lang, api_name)
                            if manual:
                                img   = manual
                                found = True
                                self._log(f"  ✅ Added manually!")
                            else:
                                self._log(f"  ⏭ Skipped.")

                        if img:
                            img.save(tmp_path, "JPEG", quality=95)
                            cache[api_name][card][card_lang] = tmp_path
                            done += 1
                            flag = "✓" if found else "→EN"
                            self._log(
                                f"✓ [{done}/{total}] "
                                f"{card} [{card_lang}] [{flag}] "
                                f"({t_dur:.2f}s)")
                        else:
                            done += 1
                            self._log(
                                f"✗ [{done}/{total}] "
                                f"{card} [{card_lang}] skipped")

                    if times:
                        avg = sum(times) / len(times)
                        eta = avg * (total - done)
                        kpm = 60 / avg if avg > 0 else 0

                        def upd(p=done, g=total, km=kpm, et=eta):
                            self.dl_progress['value'] = (p/g)*100
                            self.lbl_speed.config(
                                text=f"⚡ {km:.1f} c/min")
                            m, s = divmod(int(et), 60)
                            self.lbl_eta.config(
                                text=f"ETA: {m:02d}:{s:02d}")
                        self.root.after(0, upd)

                    time.sleep(interval_s)

        self.downloaded = {
            api: [cache[api][c] for c in cards
                  if c in cache[api] and cache[api][c]]
            for api in active_apis
        }
        total_dl = sum(len(v) for v in self.downloaded.values())
        self._log(f"\n✅ Done | {done}/{total} | {total_dl} entries")

        def _done():
            self.btn_cancel.config(state="disabled")
            self.dl_progress['value'] = 100
            self.lbl_speed.config(text="✅ Done", fg="#2e7d32")
            self.lbl_eta.config(text="")
            self.lbl_status.config(
                text=t("status_ready_dl",
                       self.ui_lang.get(), n=total_dl),
                fg="green")
        self.root.after(0, _done)

        if auto_export and not self._cancel_dl:
            self.root.after(0, self._export_all)

    # ══════════════════════════════════════════════════════════
    #  CLIPBOARD
    # ══════════════════════════════════════════════════════════

    def _load_clipboard(self, nr):
        lang = self.ui_lang.get()
        try:
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image) and img.size[0] > 10:
                self.card_images[nr] = img.copy()
                self.clipboard_buttons[nr].config(
                    text=t("clipboard_done", lang, n=nr+1),
                    bg="#c8e6c9")
                if self.preview_active.get():
                    self._draw_preview()
            else:
                messagebox.showwarning("⚠️", t("no_image_warn", lang))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ══════════════════════════════════════════════════════════
    #  PREVIEW
    # ══════════════════════════════════════════════════════════

    def _draw_preview(self):
        canvas = self.preview_canvas
        canvas.delete("all")
        canvas.update_idletasks()
        vw = max(canvas.winfo_width(), 600)
        vh = 200
        prev = Image.new('RGB', (vw, vh), self.cut_color)
        draw = ImageDraw.Draw(prev)
        s  = max(4, self.border_px)
        iw = (vw - 3*s) // 2
        ih = (vh - 3*s) // 2
        for i, (x, y) in enumerate([
            (s, s), (vw-s-iw, s),
            (s, vh-s-ih), (vw-s-iw, vh-s-ih)
        ]):
            draw.rectangle([x, y, x+iw, y+ih], fill="white")
            if self.card_images[i]:
                prev.paste(
                    self.card_images[i].resize(
                        (iw, ih), Image.Resampling.LANCZOS),
                    (x, y))
        photo = ImageTk.PhotoImage(prev)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.image = photo

    # ══════════════════════════════════════════════════════════
    #  BUILD PROXY PAGE
    # ══════════════════════════════════════════════════════════

    def _make_proxy_page(self, four_images):
        cm2in = 1 / 2.54
        pw = int(13 * cm2in * self.dpi)
        ph = int(18 * cm2in * self.dpi)
        s  = self.border_px
        iw = (pw - 3*s) // 2
        ih = (ph - 3*s) // 2
        page = Image.new('RGB', (pw, ph), self.cut_color)
        draw = ImageDraw.Draw(page)
        for i, (x, y) in enumerate([
            (s, s), (pw-s-iw, s),
            (s, ph-s-ih), (pw-s-iw, ph-s-ih)
        ]):
            draw.rectangle([x, y, x+iw, y+ih], fill='white')
            if four_images[i]:
                page.paste(
                    four_images[i].resize(
                        (iw, ih), Image.Resampling.LANCZOS),
                    (x, y))
        return page

    # ══════════════════════════════════════════════════════════
    #  EXPORT
    # ══════════════════════════════════════════════════════════

    def _save_page(self, page, folder, filename):
        if self.export_png.get():
            page.save(os.path.join(folder, f"{filename}.png"))
        if self.export_jpg.get():
            page.save(os.path.join(folder, f"{filename}.jpg"),
                      'JPEG', quality=95, dpi=(self.dpi, self.dpi))
        if self.export_pdf.get():
            page.save(os.path.join(folder, f"{filename}.pdf"),
                      'PDF', resolution=self.dpi)

    def _export_all(self):
        lang = self.ui_lang.get()
        base = self.base_path.get().strip()
        name = self.deck_name.get().strip()

        if not base or not os.path.isdir(base):
            messagebox.showwarning(
                t("warn_no_path", lang), t("warn_no_path_msg", lang))
            return
        if not name:
            messagebox.showwarning(
                t("warn_no_deck", lang), t("warn_no_deck_msg", lang))
            return
        if not (self.export_png.get() or self.export_jpg.get()
                or self.export_pdf.get()):
            messagebox.showwarning(
                t("warn_no_format", lang), t("warn_no_format_msg", lang))
            return

        name_safe   = safe_path(name)
        deck_folder = os.path.join(base, name_safe)
        def_lang    = self.default_lang.get()
        all_langs   = [def_lang] + [
            s for s in self.extra_langs if s != def_lang]
        active_apis  = [n for n, v in self.active_apis.items() if v.get()]
        total_sheets = 0
        formats_used = []

        if self.downloaded:
            for api_name, card_list in self.downloaded.items():
                if not card_list:
                    continue
                for card_lang in all_langs:
                    out_dir = os.path.join(
                        deck_folder, api_name, card_lang)
                    os.makedirs(out_dir, exist_ok=True)

                    images = []
                    for cd in card_list:
                        p = (cd.get(card_lang) or
                             cd.get(def_lang) or
                             next(iter(cd.values()), None))
                        if p:
                            try:
                                images.append(
                                    Image.open(p).convert("RGB"))
                            except:
                                pass

                    if not images:
                        continue

                    for i in range(0, len(images), 4):
                        group = images[i:i+4]
                        while len(group) < 4:
                            group.append(group[-1])
                        page  = self._make_proxy_page(group)
                        fname = f"proxy_{(i//4)+1:02d}"
                        self._save_page(page, out_dir, fname)
                        total_sheets += 1
                        for fmt in (
                            (["PNG"]  if self.export_png.get() else []) +
                            (["JPEG"] if self.export_jpg.get() else []) +
                            (["PDF"]  if self.export_pdf.get() else [])
                        ):
                            if fmt not in formats_used:
                                formats_used.append(fmt)
                        self.export_progress['value'] = min(
                            90, self.export_progress['value'] + 2)
                        self.root.update_idletasks()
        else:
            active_api = self.default_api.get()
            out_dir    = os.path.join(deck_folder, active_api, def_lang)
            os.makedirs(out_dir, exist_ok=True)
            imgs = [b for b in self.card_images if b is not None]
            if len(imgs) < 4:
                messagebox.showwarning(
                    t("warn_no_images", lang),
                    t("warn_no_images_msg", lang))
                return
            for i in range(0, len(imgs), 4):
                group = imgs[i:i+4]
                while len(group) < 4:
                    group.append(group[-1])
                page  = self._make_proxy_page(group)
                fname = f"proxy_{(i//4)+1:02d}"
                self._save_page(page, out_dir, fname)
                total_sheets += 1
            for fmt in (
                (["PNG"]  if self.export_png.get() else []) +
                (["JPEG"] if self.export_jpg.get() else []) +
                (["PDF"]  if self.export_pdf.get() else [])
            ):
                if fmt not in formats_used:
                    formats_used.append(fmt)

        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
            self._log(t("tmp_deleted", lang))

        self.export_progress['value'] = 100
        structure = "\n".join(
            f"  📁 {deck_folder}/{api}/{l}"
            for api in active_apis
            for l in all_langs
        )
        messagebox.showinfo(
            t("export_done_title", lang),
            t("export_done_msg", lang,
              n=total_sheets,
              f=', '.join(formats_used),
              s=structure))

        self.lbl_status.config(
            text=t("status_exported", lang,
                   n=total_sheets, d=name_safe),
            fg="green")

        self.card_images = [None] * 4
        self.downloaded  = {}
        for i, btn in enumerate(self.clipboard_buttons):
            btn.config(
                text=t("clipboard_btn", lang, n=i+1),
                bg="#e8f5e8")
        self.export_progress['value'] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = MTGProxyGUI(root)
    root.mainloop()
