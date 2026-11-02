"""Graphical user interface for the Password Strength Checker.

All analysis is performed locally. Password text is not logged, saved, or sent.
"""

import tkinter as tk
from tkinter import ttk

from .analyzer import analyze_password


class PasswordCheckerApp:
    BG = "#101827"
    PANEL = "#182338"
    PANEL_ALT = "#202e45"
    TEXT = "#edf2f7"
    MUTED = "#a8b4c7"
    ACCENT = "#63d6b0"
    BLUE = "#78a9ff"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("760x680")
        self.root.minsize(620, 600)
        self.root.configure(bg=self.BG)

        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar(value=False)
        self.password_var.trace_add("write", self._on_password_change)

        self._configure_styles()
        self._build_interface()
        self.root.bind("<Escape>", lambda _event: self._clear())

    def _configure_styles(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Strength.Horizontal.TProgressbar",
            troughcolor=self.PANEL_ALT,
            background=self.ACCENT,
            bordercolor=self.PANEL_ALT,
            lightcolor=self.ACCENT,
            darkcolor=self.ACCENT,
            thickness=10,
        )
        style.configure(
            "TCheckbutton",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("Segoe UI", 10),
        )
        style.map(
            "TCheckbutton",
            background=[("active", self.PANEL)],
            foreground=[("active", self.TEXT)],
        )

    def _label(self, parent, text, *, size=10, color=None, weight="normal"):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color or self.TEXT,
            font=("Segoe UI", size, weight),
            anchor="w",
        )

    def _build_interface(self) -> None:
        outer = tk.Frame(self.root, bg=self.BG, padx=30, pady=24)
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg=self.BG)
        header.pack(fill="x")
        self._label(header, "SECURITY TOOLKIT  /  PASSWORD AUDIT", size=9,
                    color=self.ACCENT, weight="bold").pack(anchor="w")
        self._label(header, "Password Strength Checker", size=24,
                    weight="bold").pack(anchor="w", pady=(7, 3))
        self._label(
            header,
            "Evaluate password quality and get practical improvement guidance.",
            size=10, color=self.MUTED
        ).pack(anchor="w")

        input_card = self._card(outer)
        input_card.pack(fill="x", pady=(22, 14))
        self._label(input_card, "ENTER A TEST PASSWORD", size=9,
                    color=self.MUTED, weight="bold").pack(anchor="w")

        input_row = tk.Frame(input_card, bg=self.PANEL)
        input_row.pack(fill="x", pady=(10, 8))
        self.entry = tk.Entry(
            input_row,
            textvariable=self.password_var,
            show="•",
            font=("Consolas", 14),
            bg=self.PANEL_ALT,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            bd=0,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 10))
        self.show_button = tk.Button(
            input_row,
            text="Show",
            command=self._toggle_visibility,
            bg=self.PANEL_ALT,
            fg=self.TEXT,
            activebackground="#31425e",
            activeforeground=self.TEXT,
            relief="flat",
            padx=15,
            pady=9,
            cursor="hand2",
        )
        self.show_button.pack(side="right")

        controls = tk.Frame(input_card, bg=self.PANEL)
        controls.pack(fill="x", pady=(3, 0))
        ttk.Checkbutton(
            controls,
            text="Show password",
            variable=self.show_password_var,
            command=self._toggle_visibility,
        ).pack(side="left")
        tk.Button(
            controls, text="Clear",
            command=self._clear,
            bg=self.PANEL, fg=self.BLUE,
            activebackground=self.PANEL, activeforeground=self.ACCENT,
            relief="flat", cursor="hand2"
        ).pack(side="right")

        result_card = self._card(outer)
        result_card.pack(fill="x", pady=(0, 14))
        result_header = tk.Frame(result_card, bg=self.PANEL)
        result_header.pack(fill="x")
        self._label(result_header, "SECURITY ASSESSMENT", size=9,
                    color=self.MUTED, weight="bold").pack(side="left")
        self.rating_label = self._label(
            result_header, "WAITING FOR INPUT", size=10,
            color=self.MUTED, weight="bold"
        )
        self.rating_label.pack(side="right")

        score_row = tk.Frame(result_card, bg=self.PANEL)
        score_row.pack(fill="x", pady=(13, 5))
        self.score_label = self._label(score_row, "0 / 7", size=21, weight="bold")
        self.score_label.pack(side="left")
        self._label(score_row, "Strength score", size=9,
                    color=self.MUTED).pack(side="left", padx=(10, 0), pady=(7, 0))

        self.progress = ttk.Progressbar(
            result_card, style="Strength.Horizontal.TProgressbar",
            maximum=7, value=0
        )
        self.progress.pack(fill="x", pady=(5, 13))

        self._label(result_card, "SECURITY CHECKLIST", size=9,
                    color=self.MUTED, weight="bold").pack(anchor="w")
        self.checks_frame = tk.Frame(result_card, bg=self.PANEL)
        self.checks_frame.pack(fill="x", pady=(9, 0))
        self.check_labels = []
        for _ in range(6):
            line = self._label(self.checks_frame, "○  Waiting for input",
                               size=10, color=self.MUTED)
            line.pack(anchor="w", pady=3)
            self.check_labels.append(line)

        advice_card = self._card(outer)
        advice_card.pack(fill="both", expand=True)
        self._label(advice_card, "RECOMMENDATIONS", size=9,
                    color=self.MUTED, weight="bold").pack(anchor="w")
        self.feedback_text = tk.Label(
            advice_card,
            text="Enter a fictional test password to see tailored guidance.",
            bg=self.PANEL, fg=self.MUTED,
            font=("Segoe UI", 10), justify="left",
            anchor="nw", wraplength=660,
        )
        self.feedback_text.pack(fill="both", expand=True, pady=(10, 4))

        footer = tk.Frame(outer, bg=self.BG)
        footer.pack(fill="x", pady=(13, 0))
        self._label(
            footer,
            "LOCAL ANALYSIS ONLY  •  No network requests  •  No password storage",
            size=8, color=self.ACCENT
        ).pack(anchor="center")
        self._label(
            footer,
            "Educational heuristic; not a guarantee of password security.",
            size=8, color=self.MUTED
        ).pack(anchor="center", pady=(4, 0))

    def _card(self, parent):
        return tk.Frame(parent, bg=self.PANEL, padx=18, pady=16,
                        highlightthickness=1, highlightbackground="#2b3b55")

    def _toggle_visibility(self) -> None:
        visible = self.show_password_var.get()
        self.entry.configure(show="" if visible else "•")
        self.show_button.configure(text="Hide" if visible else "Show")

    def _clear(self) -> None:
        self.password_var.set("")
        self.entry.focus_set()

    def _on_password_change(self, *_args) -> None:
        password = self.password_var.get()
        if not password:
            self.rating_label.configure(text="WAITING FOR INPUT", fg=self.MUTED)
            self.score_label.configure(text="0 / 7")
            self.progress.configure(value=0)
            self.feedback_text.configure(
                text="Enter a fictional test password to see tailored guidance.",
                fg=self.MUTED,
            )
            for label in self.check_labels:
                label.configure(text="○  Waiting for input", fg=self.MUTED)
            return

        report = analyze_password(password)
        colors = {
            "WEAK": "#ff7777",
            "MODERATE": "#f3c969",
            "STRONG": "#78a9ff",
            "VERY STRONG": self.ACCENT,
        }
        color = colors[report.rating]
        self.rating_label.configure(text=report.rating, fg=color)
        self.score_label.configure(text=f"{report.score} / 7")
        self.progress.configure(value=report.score)
        self.progress.configure(style="Strength.Horizontal.TProgressbar")
        for label, (description, passed) in zip(self.check_labels, report.checks):
            symbol = "✓" if passed else "○"
            label.configure(
                text=f"{symbol}  {description}",
                fg=self.ACCENT if passed else self.MUTED,
            )
        self.feedback_text.configure(
            text="\n".join(f"•  {item}" for item in report.feedback),
            fg=self.TEXT,
        )


def main() -> None:
    root = tk.Tk()
    PasswordCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
