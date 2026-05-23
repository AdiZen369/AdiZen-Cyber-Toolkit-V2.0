"""
AdiZenWorks Cybersecurity Toolkit V2.0 — Desktop GUI
Brand: Burgundy · Crimson · Deep Space Black · Pearl White
Author: AdiZenWorks Inc.
"""

import sys
import os
import json
import threading
from pathlib import Path

# Fix imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font as tkfont

try:
    import adizenports
    import adizenheaders
    import adizenhash
    import adizenai
    import adizenmapper
    import adizenspider
    import adizensqli
    import adizenxss
    import adizendns
    import adizenssl
    import adizenpassword
    import adizensubdomain
    import adizencve
    import adizenrevshell
    import adizensecurity
    MODULES_OK = True
except ImportError as e:
    MODULES_OK = False
    IMPORT_ERROR = str(e)


# ── BRAND COLORS ──────────────────────────────────────────────
C = {
    "bg":       "#080808",   # deep space black
    "bg2":      "#0f0f0f",
    "bg3":      "#161616",
    "bg4":      "#1e0808",   # burgundy-tinted dark
    "burgundy": "#6d0a1b",
    "crimson":  "#cc0000",
    "crimson2": "#ff2222",
    "crimson3": "#8b0000",
    "pearl":    "#e8e4dc",
    "pearl2":   "rgba(232,228,220,0.6)",
    "muted":    "#887878",
    "border":   "#2a0a0a",
    "border2":  "#3a0000",
    "success":  "#00cc55",
    "warn":     "#cc8800",
}

CONFIG_PATH = project_root / "adizen_config.json"


def load_config():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return {}


def save_config(data):
    try:
        existing = load_config()
        existing.update(data)
        CONFIG_PATH.write_text(json.dumps(existing, indent=2))
    except Exception:
        pass


class AdiZenDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AdiZenWorks Cybersecurity Toolkit V2.0 — 15 Tools")
        self.root.geometry("1320x860")
        self.root.minsize(1100, 720)
        self.root.configure(bg=C["bg"])

        # Window icon + header logo
        self._logo_img = None
        # Try to load logo for header (42px pre-scaled preferred)
        logo_candidates = [
            project_root / "web" / "static" / "assets" / "logo_header.png",
            project_root / "web" / "static" / "assets" / "logo_small.png",
            project_root / "web" / "static" / "assets" / "logo.png",
            project_root / "assets" / "logo.png",
        ]
        for logo_path in logo_candidates:
            if logo_path.exists():
                try:
                    img = tk.PhotoImage(file=str(logo_path))
                    if img.width() > 48:
                        factor = max(1, img.width() // 42)
                        img = img.subsample(factor, factor)
                    self._logo_img = img
                    break
                except Exception:
                    pass

        # Window icon (use full-res logo)
        icon_paths = [
            project_root / "web" / "static" / "assets" / "logo.png",
            project_root / "assets" / "logo.png",
        ]
        for p in icon_paths:
            if p.exists():
                try:
                    ico = tk.PhotoImage(file=str(p))
                    self.root.iconphoto(True, ico)
                    break
                except Exception:
                    pass

        self.ai_config = load_config().get("ai", {})
        self._build_ui()

        if not MODULES_OK:
            self.log(f"[ERROR] Module import failed: {IMPORT_ERROR}", "err")

    def _build_ui(self):
        # ── HEADER BAR
        header = tk.Frame(self.root, bg=C["bg2"], height=60)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # Left: brand (logo + text)
        left_hdr = tk.Frame(header, bg=C["bg2"])
        left_hdr.pack(side=tk.LEFT, padx=20, pady=8)

        # Logo in header
        if self._logo_img:
            logo_lbl = tk.Label(left_hdr, image=self._logo_img, bg=C["bg2"], bd=0)
            logo_lbl.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            left_hdr, text="AdiZenWorks",
            bg=C["bg2"], fg=C["pearl"],
            font=("Segoe UI", 16, "bold")
        ).pack(side=tk.LEFT)

        tk.Label(
            left_hdr, text="  Cybersecurity Toolkit V2.0  •  15 Tools",
            bg=C["bg2"], fg=C["muted"],
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT)

        # Right: status
        right_hdr = tk.Frame(header, bg=C["bg2"])
        right_hdr.pack(side=tk.RIGHT, padx=20)

        self.status_label = tk.Label(
            right_hdr, text="● READY",
            bg=C["bg2"], fg=C["success"],
            font=("Consolas", 9)
        )
        self.status_label.pack(side=tk.RIGHT)

        # Crimson header line
        tk.Frame(self.root, bg=C["crimson"], height=2).pack(fill=tk.X)

        # ── MAIN BODY (sidebar + content)
        body = tk.Frame(self.root, bg=C["bg"])
        body.pack(fill=tk.BOTH, expand=True)

        # ── SIDEBAR
        sidebar = tk.Frame(body, bg=C["bg2"], width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Frame(sidebar, bg=C["border"], height=1).pack(fill=tk.X)

        nav_items = [
            ("🔌", "Port Scanner",      "ports"),
            ("🛡", "Headers Check",     "headers"),
            ("🔐", "Hash Generator",    "hash"),
            ("💥", "XSS Scanner",       "xss"),
            ("💉", "SQLi Scanner",      "sqli"),
            ("🗺", "Network Mapper",    "mapper"),
            ("🕷", "Web Spider",        "spider"),
            ("🌐", "DNS Lookup",        "dns"),
            ("🔒", "SSL Inspector",     "ssl"),
            ("🔑", "Password Strength", "password"),
            ("🔎", "Subdomain Enum",    "subdomain"),
            ("📋", "CVE Search",        "cve"),
            ("💻", "Shell Detector",    "revshell"),
            ("🛡️", "Security Audit",   "security"),
            ("🤖", "AI Analyst",        "ai"),
            ("⚙", "AI / BYOK Config",  "config"),
        ]

        self.nav_buttons = {}
        self.active_tool = tk.StringVar(value="ports")

        for ico, label, key in nav_items:
            btn = tk.Button(
                sidebar,
                text=f"  {ico}  {label}",
                bg=C["bg2"], fg=C["muted"],
                font=("Segoe UI", 9),
                anchor="w",
                relief=tk.FLAT,
                bd=0,
                padx=8, pady=10,
                cursor="hand2",
                command=lambda k=key: self.show_tool(k)
            )
            btn.pack(fill=tk.X)

            def on_enter(e, b=btn):
                if self.active_tool.get() != b.cget("text").strip().split("  ")[-1]:
                    b.configure(bg=C["bg3"], fg=C["pearl"])

            def on_leave(e, b=btn, k=key):
                if self.active_tool.get() != k:
                    b.configure(bg=C["bg2"], fg=C["muted"])

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            self.nav_buttons[key] = btn
            tk.Frame(sidebar, bg=C["border"], height=1).pack(fill=tk.X)

        # Sidebar bottom — version
        tk.Label(
            sidebar, text="v2.0  •  15 Tools  •  AdiZenWorks",
            bg=C["bg2"], fg="#333",
            font=("Consolas", 7)
        ).pack(side=tk.BOTTOM, pady=8)

        # ── CONTENT AREA
        self.content = tk.Frame(body, bg=C["bg"])
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ── LOG BAR at bottom
        log_frame = tk.Frame(self.root, bg=C["bg2"], height=130)
        log_frame.pack(fill=tk.X, side=tk.BOTTOM)
        log_frame.pack_propagate(False)
        tk.Frame(log_frame, bg=C["crimson3"], height=1).pack(fill=tk.X)

        log_header = tk.Frame(log_frame, bg=C["bg2"])
        log_header.pack(fill=tk.X, padx=12, pady=(6, 2))

        tk.Label(
            log_header, text="ACTIVITY LOG",
            bg=C["bg2"], fg=C["crimson"],
            font=("Consolas", 8, "bold")
        ).pack(side=tk.LEFT)

        tk.Button(
            log_header, text="Clear",
            bg=C["bg2"], fg=C["muted"],
            font=("Consolas", 7),
            relief=tk.FLAT, bd=0,
            cursor="hand2",
            command=lambda: self.log_box.delete(1.0, tk.END)
        ).pack(side=tk.RIGHT)

        self.log_box = tk.Text(
            log_frame,
            bg=C["bg"], fg="#555",
            font=("Consolas", 8),
            relief=tk.FLAT,
            height=5,
            wrap=tk.WORD,
            state=tk.NORMAL
        )
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))

        self.log_box.tag_config("ok",   foreground=C["success"])
        self.log_box.tag_config("err",  foreground=C["crimson2"])
        self.log_box.tag_config("warn", foreground=C["warn"])
        self.log_box.tag_config("info", foreground="#4488ff")
        self.log_box.tag_config("ts",   foreground="#333")

        # Show default tool
        self.show_tool("ports")
        self.log("[SYSTEM] AdiZenWorks Desktop initialized", "info")
        self.log("[SYSTEM] UI ready — awaiting operator commands", "ok")

    # ── LOG ───────────────────────────────────────────────────
    def log(self, msg, tag=""):
        import datetime
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"[{ts}] ", "ts")
        self.log_box.insert(tk.END, f"{msg}\n", tag or "")
        self.log_box.see(tk.END)

    def set_status(self, text, color=None):
        self.status_label.config(
            text=text,
            fg=color or C["success"]
        )

    # ── NAVIGATION ────────────────────────────────────────────
    def show_tool(self, key):
        self.active_tool.set(key)

        # Update sidebar highlight
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(bg=C["bg4"], fg=C["pearl"], relief=tk.FLAT)
                # Add left accent
                btn.configure(padx=12)
            else:
                btn.configure(bg=C["bg2"], fg=C["muted"], padx=8)

        # Clear content
        for w in self.content.winfo_children():
            w.destroy()

        # Draw tool panel
        panels = {
            "ports":    self._panel_ports,
            "headers":  self._panel_headers,
            "hash":     self._panel_hash,
            "xss":      self._panel_xss,
            "sqli":     self._panel_sqli,
            "mapper":   self._panel_mapper,
            "spider":   self._panel_spider,
            "dns":      self._panel_dns,
            "ssl":      self._panel_ssl,
            "password": self._panel_password,
            "subdomain": self._panel_subdomain,
            "cve":      self._panel_cve,
            "revshell": self._panel_revshell,
            "security": self._panel_security,
            "ai":       self._panel_ai,
            "config":   self._panel_config,
        }
        if key in panels:
            panels[key]()

    # ── HELPER WIDGETS ────────────────────────────────────────
    def _panel_header(self, parent, icon, title):
        hdr = tk.Frame(parent, bg=C["bg"])
        hdr.pack(fill=tk.X, padx=24, pady=(20, 4))

        tk.Label(
            hdr, text=f"{icon}  {title}",
            bg=C["bg"], fg=C["pearl"],
            font=("Segoe UI", 15, "bold")
        ).pack(side=tk.LEFT)

        # Crimson underline
        tk.Frame(parent, bg=C["crimson3"], height=1).pack(fill=tk.X, padx=24, pady=(2, 16))

    def _labeled_entry(self, parent, label, default="", show=None):
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(
            row, text=label.upper(),
            bg=C["bg"], fg=C["muted"],
            font=("Consolas", 7)
        ).pack(anchor=tk.W)
        kwargs = dict(
            bg=C["bg3"], fg=C["pearl"],
            insertbackground=C["pearl"],
            relief=tk.FLAT, bd=0,
            font=("Segoe UI", 10),
            highlightthickness=1,
            highlightbackground=C["border2"],
            highlightcolor=C["crimson"],
        )
        if show:
            kwargs["show"] = show
        entry = tk.Entry(row, **kwargs)
        entry.pack(fill=tk.X, ipady=7, pady=2)
        if default:
            entry.insert(0, default)
        return entry

    def _labeled_combo(self, parent, label, options, default=0):
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(
            row, text=label.upper(),
            bg=C["bg"], fg=C["muted"],
            font=("Consolas", 7)
        ).pack(anchor=tk.W)
        var = tk.StringVar(value=options[default])
        combo = ttk.Combobox(row, textvariable=var, values=options, state="readonly")
        combo.pack(fill=tk.X, pady=2)
        return var

    def _results_box(self, parent):
        frame = tk.Frame(parent, bg=C["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=(8, 4))
        tk.Label(
            frame, text="OUTPUT",
            bg=C["bg"], fg=C["muted"],
            font=("Consolas", 7)
        ).pack(anchor=tk.W)
        box = scrolledtext.ScrolledText(
            frame,
            bg="#050505", fg="#777",
            font=("Consolas", 9),
            relief=tk.FLAT,
            wrap=tk.WORD,
            highlightthickness=1,
            highlightbackground=C["border"],
            highlightcolor=C["crimson3"],
        )
        box.pack(fill=tk.BOTH, expand=True, pady=2)
        box.tag_config("ok",   foreground=C["success"])
        box.tag_config("err",  foreground=C["crimson2"])
        box.tag_config("warn", foreground=C["warn"])
        box.tag_config("info", foreground="#4488ff")
        box.tag_config("head", foreground=C["crimson"], font=("Consolas", 9, "bold"))
        return box

    def _btn_row(self, parent):
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill=tk.X, padx=24, pady=(10, 4))
        return row

    def _primary_btn(self, parent, text, cmd):
        btn = tk.Button(
            parent, text=text,
            bg=C["crimson3"], fg=C["pearl"],
            activebackground=C["crimson"],
            activeforeground=C["pearl"],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT, bd=0,
            padx=18, pady=8,
            cursor="hand2",
            command=cmd
        )
        btn.pack(side=tk.LEFT, padx=(0, 8))

        def on_enter(e): btn.configure(bg=C["crimson"])
        def on_leave(e): btn.configure(bg=C["crimson3"])
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _secondary_btn(self, parent, text, cmd):
        btn = tk.Button(
            parent, text=text,
            bg=C["bg3"], fg=C["muted"],
            activebackground=C["bg4"],
            activeforeground=C["pearl"],
            font=("Segoe UI", 9),
            relief=tk.FLAT, bd=0,
            padx=14, pady=8,
            cursor="hand2",
            command=cmd
        )
        btn.pack(side=tk.LEFT, padx=(0, 8))
        return btn

    def _write_result(self, box, text, tag=""):
        box.config(state=tk.NORMAL)
        box.delete(1.0, tk.END)
        box.insert(tk.END, text, tag)

    def _append_result(self, box, text, tag=""):
        box.config(state=tk.NORMAL)
        box.insert(tk.END, text, tag)
        box.see(tk.END)

    def _run_threaded(self, fn, *args):
        """Run fn(*args) in a background thread."""
        t = threading.Thread(target=fn, args=args, daemon=True)
        t.start()

    # ── TOOL PANELS ───────────────────────────────────────────

    def _panel_ports(self):
        self._panel_header(self.content, "🔌", "Port Scanner")
        target_e = self._labeled_entry(self.content, "Target Host / IP", "192.168.1.1")
        range_e  = self._labeled_entry(self.content, "Port Range", "1-1000")
        box = self._results_box(self.content)

        def run():
            target = target_e.get().strip()
            r      = range_e.get().strip() or "1-1000"
            if not target:
                messagebox.showerror("Error", "Enter a target host.")
                return
            self._write_result(box, f"[+] Scanning {target} ports {r}...\n")
            self.log(f"Port scan: {target} [{r}]", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizenports.scan_ports(target, r)
                import json as j
                self._append_result(box, j.dumps(results, indent=2), "ok")
                self.log(f"Port scan complete: {target}", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"Port scan error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Start Scan", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_headers(self):
        self._panel_header(self.content, "🛡", "Security Headers Check")
        url_e = self._labeled_entry(self.content, "Target URL", "https://example.com")
        box = self._results_box(self.content)

        def run():
            url = url_e.get().strip()
            if not url:
                messagebox.showerror("Error", "Enter a URL.")
                return
            self._write_result(box, f"[+] Inspecting headers: {url}\n")
            self.log(f"Header check: {url}", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizenheaders.inspect_headers(url)
                import json as j
                self._append_result(box, j.dumps(results, indent=2), "ok")
                self.log(f"Header check complete: {url}", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"Header error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Inspect Headers", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_hash(self):
        self._panel_header(self.content, "🔐", "Hash Generator")
        text_e = self._labeled_entry(self.content, "Input Text", "Enter text to hash...")
        algo_var = self._labeled_combo(self.content, "Algorithm",
            ["sha256","sha512","sha1","md5","sha3_256","blake2b"], 0)
        box = self._results_box(self.content)

        def run():
            text = text_e.get().strip()
            algo = algo_var.get()
            if not text:
                messagebox.showerror("Error", "Enter text to hash.")
                return
            try:
                results = adizenhash.generate_hash(text, algo)
                import json as j
                self._write_result(box, j.dumps(results, indent=2), "ok")
                self.log(f"Hash generated [{algo.upper()}]", "ok")
            except Exception as e:
                self._write_result(box, f"[ERROR] {e}", "err")
                self.log(f"Hash error: {e}", "err")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Generate Hash", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_xss(self):
        self._panel_header(self.content, "💥", "XSS Scanner")
        url_e = self._labeled_entry(self.content, "Target URL", "https://target.com/search?q=test")
        box = self._results_box(self.content)

        def run():
            url = url_e.get().strip()
            if not url:
                messagebox.showerror("Error", "Enter a URL.")
                return
            self._write_result(box, f"[+] Scanning {url} for XSS...\n")
            self.log(f"XSS scan: {url}", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizenxss.scan_xss(url)
                import json as j
                self._append_result(box, j.dumps(results, indent=2),
                    "warn" if results.get("vulnerabilities") else "ok")
                count = len(results.get("vulnerabilities", []))
                if count:
                    self.log(f"⚠ {count} XSS vulnerabilities found on {url}", "warn")
                else:
                    self.log(f"No XSS vulnerabilities on {url}", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"XSS error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Scan for XSS", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_sqli(self):
        self._panel_header(self.content, "💉", "SQL Injection Scanner")
        url_e = self._labeled_entry(self.content, "Target URL", "https://target.com/login?id=1")
        box = self._results_box(self.content)

        def run():
            url = url_e.get().strip()
            if not url:
                messagebox.showerror("Error", "Enter a URL.")
                return
            self._write_result(box, f"[+] Scanning {url} for SQL Injection...\n")
            self.log(f"SQLi scan: {url}", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizensqli.scan_sqli(url)
                import json as j
                self._append_result(box, j.dumps(results, indent=2),
                    "warn" if results.get("vulnerabilities") else "ok")
                count = len(results.get("vulnerabilities", []))
                if count:
                    self.log(f"⚠ {count} SQLi vulnerabilities found on {url}", "warn")
                else:
                    self.log(f"No SQLi vulnerabilities on {url}", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"SQLi error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Scan for SQLi", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_mapper(self):
        self._panel_header(self.content, "🗺", "Network Mapper")
        target_e = self._labeled_entry(self.content, "Target Network / Host", "192.168.1.0/24")
        box = self._results_box(self.content)

        def run():
            target = target_e.get().strip()
            if not target:
                messagebox.showerror("Error", "Enter a target.")
                return
            self._write_result(box, f"[+] Mapping network: {target}\n")
            self.log(f"Network map: {target}", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizenmapper.map_network(target)
                import json as j
                self._append_result(box, j.dumps(results, indent=2), "ok")
                self.log(f"Network mapping complete: {target}", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"Mapper error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Map Network", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_spider(self):
        self._panel_header(self.content, "🕷", "Web Spider")
        url_e   = self._labeled_entry(self.content, "Target URL", "https://example.com")
        depth_e = self._labeled_entry(self.content, "Crawl Depth (1-5)", "2")
        box = self._results_box(self.content)

        def run():
            url   = url_e.get().strip()
            depth = int(depth_e.get().strip() or "2")
            if not url:
                messagebox.showerror("Error", "Enter a URL.")
                return
            self._write_result(box, f"[+] Spidering {url} (depth {depth})...\n")
            self.log(f"Web spider: {url} depth {depth}", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizenspider.spider_website(url, depth)
                import json as j
                self._append_result(box, j.dumps(results, indent=2), "ok")
                count = len(results.get("urls", []))
                self.log(f"Spider found {count} URLs on {url}", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"Spider error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Start Spider", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    # ── TOOL 9: DNS LOOKUP ────────────────────────────────────
    def _panel_dns(self):
        self._panel_header(self.content, "🌐", "DNS Lookup")
        domain_e = self._labeled_entry(self.content, "Domain", "example.com")
        box = self._results_box(self.content)

        def run():
            domain = domain_e.get().strip()
            if not domain:
                messagebox.showerror("Error", "Enter a domain.")
                return
            self._write_result(box, f"[+] Looking up DNS records for {domain}...\n")
            self.log(f"DNS lookup: {domain}", "info")
            self.set_status("● RESOLVING", C["warn"])
            try:
                results = adizendns.dns_lookup(domain)
                import json as j
                self._append_result(box, "\n")
                records = results.get("records", {})
                if records:
                    for rtype, values in records.items():
                        self._append_result(box, f"  ── {rtype} ──\n", "head")
                        for v in values:
                            self._append_result(box, f"    {v}\n", "ok")
                else:
                    self._append_result(box, "  No records found\n", "warn")
                if results.get("errors"):
                    for err in results["errors"]:
                        self._append_result(box, f"\n  [!] {err}\n", "err")
                self._append_result(box, f"\n  Total records: {results.get('total_records', 0)}\n", "info")
                self.log(f"DNS lookup complete: {results.get('total_records', 0)} records", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"DNS error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Lookup DNS", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    # ── TOOL 10: SSL/TLS INSPECTOR ───────────────────────────
    def _panel_ssl(self):
        self._panel_header(self.content, "🔒", "SSL / TLS Inspector")
        host_e = self._labeled_entry(self.content, "Hostname", "example.com")
        port_e = self._labeled_entry(self.content, "Port", "443")
        box = self._results_box(self.content)

        def run():
            host = host_e.get().strip()
            try:
                port = int(port_e.get().strip() or "443")
            except ValueError:
                port = 443
            if not host:
                messagebox.showerror("Error", "Enter a hostname.")
                return
            self._write_result(box, f"[+] Inspecting SSL/TLS for {host}:{port}...\n")
            self.log(f"SSL inspect: {host}:{port}", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizenssl.inspect_ssl(host, port)
                self._append_result(box, "\n")
                status = results.get("status", "unknown")
                tag = "ok" if "VALID" in status else "warn" if "WARNING" in status else "err"
                self._append_result(box, f"  Status:       {status}\n", tag)
                self._append_result(box, f"  Rating:       {results.get('rating', 'N/A')}\n", tag)

                cert = results.get("certificate", {})
                if cert:
                    self._append_result(box, "\n  ── Certificate ──\n", "head")
                    self._append_result(box, f"    Common Name:  {cert.get('common_name', 'N/A')}\n")
                    self._append_result(box, f"    Org:          {cert.get('org', 'N/A')}\n")
                    self._append_result(box, f"    Issuer:       {cert.get('issuer_org', 'N/A')}\n")
                    self._append_result(box, f"    Serial:       {cert.get('serial_number', 'N/A')}\n")

                val = results.get("validity", {})
                if val:
                    self._append_result(box, "\n  ── Validity ──\n", "head")
                    self._append_result(box, f"    Not Before:   {val.get('not_before', 'N/A')}\n")
                    self._append_result(box, f"    Not After:    {val.get('not_after', 'N/A')}\n")
                    days = val.get('days_remaining', 'N/A')
                    days_tag = "ok" if isinstance(days, int) and days > 30 else "warn"
                    self._append_result(box, f"    Days Left:    {days}\n", days_tag)

                tls = results.get("tls", {})
                if tls:
                    self._append_result(box, "\n  ── TLS ──\n", "head")
                    self._append_result(box, f"    Protocol:     {tls.get('protocol', 'N/A')}\n")
                    self._append_result(box, f"    Cipher:       {tls.get('cipher_suite', 'N/A')}\n")
                    self._append_result(box, f"    Bits:         {tls.get('cipher_bits', 'N/A')}\n")

                flags = results.get("security_flags", [])
                if flags:
                    self._append_result(box, "\n  ── Security Flags ──\n", "head")
                    for f in flags:
                        self._append_result(box, f"    ⚠ {f}\n", "warn")

                if results.get("errors"):
                    for err in results["errors"]:
                        self._append_result(box, f"\n  [ERROR] {err}\n", "err")

                self.log(f"SSL inspect done: {status}", tag)
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"SSL error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Inspect SSL", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    # ── TOOL 11: PASSWORD STRENGTH ────────────────────────────
    def _panel_password(self):
        self._panel_header(self.content, "🔑", "Password Strength Analyzer")
        pw_e = self._labeled_entry(self.content, "Password", show="●")

        # Toggle show/hide
        show_var = tk.BooleanVar(value=False)
        toggle_row = tk.Frame(self.content, bg=C["bg"])
        toggle_row.pack(fill=tk.X, padx=24, pady=(0, 4))
        tk.Checkbutton(
            toggle_row, text="Show password", variable=show_var,
            bg=C["bg"], fg=C["muted"], selectcolor=C["bg3"],
            activebackground=C["bg"], font=("Segoe UI", 9),
            command=lambda: pw_e.config(show="" if show_var.get() else "●")
        ).pack(anchor=tk.W)

        box = self._results_box(self.content)

        def run():
            pw = pw_e.get()
            if not pw:
                messagebox.showerror("Error", "Enter a password.")
                return
            try:
                results = adizenpassword.analyze_password(pw)
                score   = results.get("score", 0)
                grade   = results.get("grade", "?")
                label   = results.get("strength", "?")
                tag     = "ok" if grade in ("A", "B") else "warn" if grade == "C" else "err"

                self._write_result(box, f"── PASSWORD ANALYSIS ─────────────────────\n\n", "head")
                self._append_result(box, f"  Grade:          {grade} — {label}\n", tag)
                self._append_result(box, f"  Score:          {score}/100\n", tag)
                self._append_result(box, f"  Length:         {results.get('password_length', 0)} characters\n")
                self._append_result(box, f"  Entropy:        {results.get('entropy_bits', 0)} bits\n")
                self._append_result(box, f"  Crack Time:     {results.get('crack_estimate', 'N/A')}\n")

                cc = results.get("character_classes", {})
                if cc:
                    self._append_result(box, "\n  ── Character Classes ──\n", "head")
                    for name in ("lowercase", "uppercase", "digits", "special"):
                        yn = "✓" if cc.get(name) else "✗"
                        ct = "ok" if cc.get(name) else "err"
                        self._append_result(box, f"    {yn}  {name.capitalize()}\n", ct)
                    self._append_result(box, f"    Pool size: {cc.get('pool_size', 0)} chars\n")

                issues = results.get("issues", [])
                if issues:
                    self._append_result(box, "\n  ── Issues ──\n", "head")
                    for i in issues:
                        self._append_result(box, f"    ✗ {i}\n", "err")

                recs = results.get("recommendations", [])
                if recs:
                    self._append_result(box, "\n  ── Recommendations ──\n", "head")
                    for r in recs:
                        self._append_result(box, f"    → {r}\n", "warn")

                self.log(f"Password analysis: {grade} — {label}", tag)
            except Exception as e:
                self._write_result(box, f"[ERROR] {e}", "err")
                self.log(f"Password error: {e}", "err")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Analyze Password", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    # ── TOOL 12: SUBDOMAIN ENUMERATOR ────────────────────────
    def _panel_subdomain(self):
        self._panel_header(self.content, "🔎", "Subdomain Enumerator")
        domain_e  = self._labeled_entry(self.content, "Base Domain", "example.com")
        custom_e  = self._labeled_entry(self.content, "Custom Wordlist (comma-separated, leave blank for built-in)", "")
        workers_e = self._labeled_entry(self.content, "Threads", "30")
        box = self._results_box(self.content)

        def run():
            domain  = domain_e.get().strip()
            custom  = custom_e.get().strip()
            workers = int(workers_e.get().strip() or "30")
            if not domain:
                messagebox.showerror("Error", "Enter a domain.")
                return
            wordlist = [w.strip() for w in custom.split(",") if w.strip()] if custom else None
            self._write_result(box, f"[+] Enumerating subdomains of {domain}...\n"
                               f"[+] Threads: {workers} | Wordlist: {len(wordlist) if wordlist else 'built-in (80)'}\n\n")
            self.log(f"Subdomain enum: {domain}", "info")
            self.set_status("● ENUMERATING", C["warn"])
            try:
                results = adizensubdomain.enumerate_subdomains(domain, wordlist, workers)
                found   = results.get("found", [])
                tested  = results.get("tested", 0)

                if found:
                    self._append_result(box, f"── FOUND {len(found)} SUBDOMAINS ──────────────────\n", "head")
                    for entry in found:
                        self._append_result(box, f"  {entry['subdomain']:<45}  {entry['ip']}\n", "ok")
                else:
                    self._append_result(box, "  No subdomains found\n", "warn")

                self._append_result(box, f"\n  Tested: {tested} | Found: {len(found)} | Not Found: {results.get('not_found', 0)}\n", "info")
                self.log(f"Subdomain enum done: {len(found)} found / {tested} tested", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"Subdomain error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Enumerate", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    # ── TOOL 13: CVE SEARCH ───────────────────────────────────
    def _panel_cve(self):
        self._panel_header(self.content, "📋", "CVE Search")
        query_e  = self._labeled_entry(self.content, "CVE ID or Keyword", "log4j")
        limit_e  = self._labeled_entry(self.content, "Max Results", "10")
        box = self._results_box(self.content)

        def run():
            query = query_e.get().strip()
            limit = int(limit_e.get().strip() or "10")
            if not query:
                messagebox.showerror("Error", "Enter a CVE ID or keyword.")
                return
            self._write_result(box, f"[+] Searching CVE database: {query}...\n")
            self.log(f"CVE search: {query}", "info")
            self.set_status("● SEARCHING", C["warn"])
            try:
                results = adizencve.search_cve(query, limit)
                cves    = results.get("cves", [])

                if cves:
                    self._append_result(box, f"\n── {len(cves)} CVEs FOUND (source: {results.get('source')}) ──\n", "head")
                    for cve in cves:
                        sev   = cve.get("severity", "N/A")
                        color = "err" if sev == "CRITICAL" else "warn" if sev == "HIGH" else "info"
                        self._append_result(box, f"\n  {cve['id']}  [{sev}]  CVSS: {cve.get('cvss_score', 'N/A')}\n", color)
                        self._append_result(box, f"  {cve.get('summary', '')[:200]}\n")
                        self._append_result(box, f"  Published: {cve.get('published', 'N/A')}\n")
                        if cve.get("references"):
                            self._append_result(box, f"  Ref: {cve['references'][0]}\n", "info")
                        self._append_result(box, "  " + "─" * 70 + "\n")
                else:
                    self._append_result(box, "\n  No CVEs found for this query.\n", "warn")

                if results.get("errors"):
                    for err in results["errors"]:
                        self._append_result(box, f"\n  [!] {err}\n", "err")

                self.log(f"CVE search done: {len(cves)} found", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"CVE error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Search CVEs", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    # ── TOOL 14: REVERSE SHELL DETECTOR ─────────────────────
    def _panel_revshell(self):
        self._panel_header(self.content, "💻", "Reverse Shell Detector")
        tk.Label(
            self.content,
            text="Paste code, script content, or any text to scan for reverse shell signatures (54 patterns).",
            bg=C["bg"], fg=C["muted"], font=("Segoe UI", 9)
        ).pack(anchor=tk.W, padx=24, pady=(0, 8))

        input_frame = tk.Frame(self.content, bg=C["bg"])
        input_frame.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(input_frame, text="CODE / TEXT TO SCAN", bg=C["bg"], fg=C["muted"],
                 font=("Consolas", 7)).pack(anchor=tk.W)
        input_box = tk.Text(
            input_frame, bg=C["bg3"], fg=C["pearl"],
            insertbackground=C["pearl"],
            font=("Consolas", 9), relief=tk.FLAT, height=6, wrap=tk.WORD,
            highlightthickness=1, highlightbackground=C["border2"],
            highlightcolor=C["crimson"]
        )
        input_box.pack(fill=tk.X, pady=2)
        input_box.insert(tk.END, "# Paste code here to scan for reverse shells, webshells, or malicious payloads")

        box = self._results_box(self.content)

        def run():
            text = input_box.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Error", "Enter code or text to scan.")
                return
            self._write_result(box, f"[+] Scanning {len(text)} chars / {text.count(chr(10))+1} lines...\n")
            self.log("Reverse shell scan started", "info")
            self.set_status("● SCANNING", C["warn"])
            try:
                results = adizenrevshell.detect_reverse_shells(text)
                matches = results.get("matches", [])
                risk    = results.get("risk_label", "CLEAN")
                score   = results.get("risk_score", 0)
                risk_tag = "err" if score >= 50 else "warn" if score > 0 else "ok"

                self._append_result(box, "\n")
                self._append_result(box, f"  Risk Level:  {risk}\n", risk_tag)
                self._append_result(box, f"  Risk Score:  {score}/100\n", risk_tag)
                self._append_result(box, f"  Matches:     {len(matches)}\n\n")

                sevs = results.get("severities", {})
                self._append_result(box, "  ── Severity Breakdown ──\n", "head")
                self._append_result(box, f"    CRITICAL: {sevs.get('CRITICAL',0)}  HIGH: {sevs.get('HIGH',0)}  "
                                    f"MEDIUM: {sevs.get('MEDIUM',0)}  LOW: {sevs.get('LOW',0)}\n")

                if matches:
                    self._append_result(box, "\n  ── Matched Signatures ──────────────────────\n", "head")
                    for m in matches:
                        sev_tag = "err" if m["severity"] == "CRITICAL" else "warn"
                        self._append_result(box, f"\n  [{m['signature_id']}] {m['name']}\n", sev_tag)
                        self._append_result(box, f"  Severity: {m['severity']}  |  Line: {m['line']}\n", sev_tag)
                        self._append_result(box, f"  Match:    {m['match']}\n")
                        if m.get("context"):
                            self._append_result(box, f"  Context:  {m['context']}\n")
                        self._append_result(box, "  " + "─" * 70 + "\n")
                else:
                    self._append_result(box, "\n  ✓ No reverse shell signatures detected\n", "ok")

                self.log(f"Shell scan done: {len(matches)} matches | {risk}", risk_tag)
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"Shell detector error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Scan for Shells", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear Input", lambda: input_box.delete(1.0, tk.END))
        self._secondary_btn(row, "Clear Output", lambda: box.delete(1.0, tk.END))

    # ── TOOL 15: SECURITY AUDIT ───────────────────────────────
    def _panel_security(self):
        self._panel_header(self.content, "🛡️", "Security Audit")
        tk.Label(
            self.content,
            text="Run a comprehensive security audit on a target URL — checks headers, SSL, cookies, and more.",
            bg=C["bg"], fg=C["muted"], font=("Segoe UI", 9)
        ).pack(anchor=tk.W, padx=24, pady=(0, 8))

        url_e = self._input_field(self.content, "Target URL", "https://example.com")
        box = self._results_box(self.content)

        def run():
            url = url_e.get().strip()
            if not url:
                messagebox.showerror("Error", "Enter a URL to audit.")
                return
            self._write_result(box, f"[+] Running security audit on {url}...\n\n")
            self.log(f"Security audit: {url}", "info")
            self.set_status("● AUDITING", C["warn"])
            try:
                results = adizensecurity.audit_security(url)
                if isinstance(results, dict):
                    for section, data in results.items():
                        self._append_result(box, f"\n── {section.upper()} ──\n", "head")
                        if isinstance(data, dict):
                            for k, v in data.items():
                                tag = "ok" if str(v).lower() in ("pass", "true", "yes", "secure") else ""
                                tag = "err" if str(v).lower() in ("fail", "false", "missing", "insecure") else tag
                                self._append_result(box, f"  {k:<30} {v}\n", tag)
                        elif isinstance(data, list):
                            for item in data:
                                self._append_result(box, f"  • {item}\n")
                        else:
                            self._append_result(box, f"  {data}\n")
                else:
                    self._append_result(box, str(results))
                self._append_result(box, "\n[✓] Security audit complete\n", "ok")
                self.log(f"Security audit done: {url}", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"Security audit error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Run Audit", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_ai(self):
        self._panel_header(self.content, "🤖", "AI Security Analyst")

        cfg = load_config().get("ai", {})

        tk.Label(
            self.content,
            text="Uses your saved AI provider config. Configure in ⚙ AI / BYOK Config.",
            bg=C["bg"], fg=C["muted"],
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, padx=24, pady=(0, 8))

        prompt_frame = tk.Frame(self.content, bg=C["bg"])
        prompt_frame.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(prompt_frame, text="PROMPT", bg=C["bg"], fg=C["muted"], font=("Consolas", 7)).pack(anchor=tk.W)
        prompt_box = tk.Text(
            prompt_frame, bg=C["bg3"], fg=C["pearl"],
            insertbackground=C["pearl"],
            font=("Segoe UI", 10), relief=tk.FLAT,
            height=4, wrap=tk.WORD,
            highlightthickness=1,
            highlightbackground=C["border2"],
            highlightcolor=C["crimson"],
        )
        prompt_box.pack(fill=tk.X, pady=2)
        prompt_box.insert(tk.END, "Analyze these results and identify the top security risks:")

        context_frame = tk.Frame(self.content, bg=C["bg"])
        context_frame.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(context_frame, text="CONTEXT (paste scan output)", bg=C["bg"], fg=C["muted"], font=("Consolas", 7)).pack(anchor=tk.W)
        context_box = tk.Text(
            context_frame, bg=C["bg3"], fg=C["pearl"],
            insertbackground=C["pearl"],
            font=("Consolas", 9), relief=tk.FLAT,
            height=4, wrap=tk.WORD,
            highlightthickness=1,
            highlightbackground=C["border2"],
            highlightcolor=C["crimson"],
        )
        context_box.pack(fill=tk.X, pady=2)

        box = self._results_box(self.content)

        def run():
            prompt  = prompt_box.get("1.0", tk.END).strip()
            context = context_box.get("1.0", tk.END).strip()
            cfg2 = load_config().get("ai", {})
            if not cfg2.get("api_key") and cfg2.get("provider", "google") != "ollama":
                messagebox.showerror("No API Key", "Configure your AI provider and API key in ⚙ AI / BYOK Config first.")
                return
            self._write_result(box, "[+] Sending to AI...\n")
            self.log("AI analysis requested", "info")
            self.set_status("● THINKING", C["warn"])
            try:
                full_prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}" if context else prompt
                ai_inst = adizenai.AdiZenAI()
                response = ai_inst.analyze(full_prompt)
                self._append_result(box, "\n" + (response or "No response"), "ok")
                self.log("AI analysis complete", "ok")
            except Exception as e:
                self._append_result(box, f"\n[ERROR] {e}", "err")
                self.log(f"AI error: {e}", "err")
            self.set_status("● READY")

        row = self._btn_row(self.content)
        self._primary_btn(row, "⚡  Analyze", lambda: self._run_threaded(run))
        self._secondary_btn(row, "Clear", lambda: box.delete(1.0, tk.END))

    def _panel_config(self):
        self._panel_header(self.content, "⚙", "AI Provider — Bring Your Own Key")

        tk.Label(
            self.content,
            text="Configure your AI provider. The API key is stored locally in adizen_config.json and never transmitted externally.",
            bg=C["bg"], fg=C["muted"],
            font=("Segoe UI", 9),
            wraplength=700, justify=tk.LEFT
        ).pack(anchor=tk.W, padx=24, pady=(0, 12))

        cfg = load_config().get("ai", {})

        # Provider
        prov_frame = tk.Frame(self.content, bg=C["bg"])
        prov_frame.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(prov_frame, text="PROVIDER", bg=C["bg"], fg=C["muted"], font=("Consolas", 7)).pack(anchor=tk.W)
        providers = ["google", "openai", "anthropic", "mistral", "groq", "ollama", "custom"]
        prov_var = tk.StringVar(value=cfg.get("provider", "google"))
        prov_combo = ttk.Combobox(prov_frame, textvariable=prov_var, values=providers, state="readonly")
        prov_combo.pack(fill=tk.X, pady=2)

        # Model
        model_frame = tk.Frame(self.content, bg=C["bg"])
        model_frame.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(model_frame, text="MODEL", bg=C["bg"], fg=C["muted"], font=("Consolas", 7)).pack(anchor=tk.W)
        model_e = tk.Entry(model_frame, bg=C["bg3"], fg=C["pearl"], insertbackground=C["pearl"],
            relief=tk.FLAT, font=("Segoe UI", 10),
            highlightthickness=1, highlightbackground=C["border2"], highlightcolor=C["crimson"])
        model_e.pack(fill=tk.X, ipady=7, pady=2)
        model_e.insert(0, cfg.get("model", "gemini-1.5-pro"))

        # Base URL
        url_frame = tk.Frame(self.content, bg=C["bg"])
        url_frame.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(url_frame, text="BASE URL (optional — for custom/self-hosted)", bg=C["bg"], fg=C["muted"], font=("Consolas", 7)).pack(anchor=tk.W)
        url_e = tk.Entry(url_frame, bg=C["bg3"], fg=C["pearl"], insertbackground=C["pearl"],
            relief=tk.FLAT, font=("Segoe UI", 10),
            highlightthickness=1, highlightbackground=C["border2"], highlightcolor=C["crimson"])
        url_e.pack(fill=tk.X, ipady=7, pady=2)
        url_e.insert(0, cfg.get("base_url", ""))

        # API Key
        key_frame = tk.Frame(self.content, bg=C["bg"])
        key_frame.pack(fill=tk.X, padx=24, pady=4)
        tk.Label(key_frame, text="API KEY", bg=C["bg"], fg=C["muted"], font=("Consolas", 7)).pack(anchor=tk.W)
        key_row = tk.Frame(key_frame, bg=C["bg"])
        key_row.pack(fill=tk.X, pady=2)
        key_e = tk.Entry(key_row, bg=C["bg3"], fg=C["pearl"], insertbackground=C["pearl"],
            relief=tk.FLAT, font=("Consolas", 10), show="●",
            highlightthickness=1, highlightbackground=C["border2"], highlightcolor=C["crimson"])
        key_e.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7)
        key_e.insert(0, cfg.get("api_key", ""))

        def toggle_key_vis():
            key_e.config(show="" if key_e.cget("show") == "●" else "●")

        tk.Button(key_row, text="👁", bg=C["bg3"], fg=C["muted"], relief=tk.FLAT,
            padx=10, command=toggle_key_vis).pack(side=tk.LEFT, padx=(4, 0))

        # Status label
        status_lbl = tk.Label(
            self.content, text="",
            bg=C["bg"], fg=C["muted"],
            font=("Consolas", 9)
        )
        status_lbl.pack(anchor=tk.W, padx=24, pady=4)

        # Provider defaults
        DEFAULTS = {
            "google":    ("gemini-1.5-pro", ""),
            "openai":    ("gpt-4o", "https://api.openai.com/v1"),
            "anthropic": ("claude-3-5-sonnet-20241022", ""),
            "mistral":   ("mistral-large-latest", "https://api.mistral.ai/v1"),
            "groq":      ("llama-3.3-70b-versatile", "https://api.groq.com/openai/v1"),
            "ollama":    ("llama3", "http://localhost:11434"),
            "custom":    ("", ""),
        }

        def on_provider_change(e=None):
            p = prov_var.get()
            defaults = DEFAULTS.get(p, ("", ""))
            model_e.delete(0, tk.END); model_e.insert(0, defaults[0])
            url_e.delete(0, tk.END);   url_e.insert(0, defaults[1])

        prov_combo.bind("<<ComboboxSelected>>", on_provider_change)

        def save():
            data = {
                "ai": {
                    "provider": prov_var.get(),
                    "model":    model_e.get().strip(),
                    "base_url": url_e.get().strip(),
                    "api_key":  key_e.get().strip(),
                }
            }
            save_config(data)
            if data["ai"]["api_key"]:
                status_lbl.config(text="✓ Configuration saved — AI assistant ready", fg=C["success"])
                self.log("AI config saved successfully", "ok")
            else:
                status_lbl.config(text="⚠ Saved without API key — AI features disabled", fg=C["warn"])
                self.log("AI config saved (no key)", "warn")

        def clear_key():
            key_e.delete(0, tk.END)
            status_lbl.config(text="API key cleared", fg=C["muted"])

        row = self._btn_row(self.content)
        self._primary_btn(row, "💾  Save Configuration", save)
        self._secondary_btn(row, "Clear Key", clear_key)
        self._secondary_btn(row, "Apply Provider Defaults", on_provider_change)


def main():
    root = tk.Tk()
    app = AdiZenDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
