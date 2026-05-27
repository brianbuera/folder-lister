import tkinter as tk

from .styles import (
    BG_CARD,
    BG_SURFACE,
    BORDER,
    ACCENT,
    TEXT_MUTED,
    TEXT_PRIMARY,
    T_PRI,
)


class ObservationSidebar(tk.Frame):

    LIMITE = 219

    def __init__(self, master, on_close=None, **kw):

        super().__init__(
            master,
            bg=BG_CARD,
            width=600,
            highlightthickness=1,
            highlightbackground=BORDER,
            **kw
        )

        self.pack_propagate(True)
        self._on_close = on_close

        self._build()

    # ─────────────────────────────────────────────

    def _build(self):

        # Header
        header = tk.Frame(self, bg=BG_CARD, height=44)
        header.pack(fill="x")

        header.pack_propagate(False)

        tk.Label(
            header,
            text="Observación",
            bg=BG_CARD,
            fg=T_PRI,
            font=("Helvetica", 11, "bold"),
        ).pack(side="left", padx=12)

        tk.Button(
            header,
            text="✕",
            command=self._close,
            bg=BG_CARD,
            fg=TEXT_MUTED,
            activebackground=BG_CARD,
            activeforeground=T_PRI,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Helvetica", 10),
        ).pack(side="right", padx=8)

        # Divider
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # Body
        body = tk.Frame(self, bg=BG_CARD, padx=12, pady=12)
        body.pack(fill="x")
        # Counter
        top_row = tk.Frame(body, bg=BG_CARD)
        top_row.pack(fill="x", pady=(0, 8))

        tk.Label(
            top_row,
            text="OBSERVACIÓN",
            font=("Courier", 9, "bold"),
            fg=TEXT_MUTED,
            bg=BG_CARD,
        ).pack(side="left")

        self.counter = tk.Label(
            top_row,
            text=f"0 / {self.LIMITE}",
            font=("Courier", 9),
            fg=TEXT_MUTED,
            bg=BG_CARD,
        )
        self.counter.pack(side="right")

        # Text container
        text_frame = tk.Frame(body, bg=BORDER, padx=1, pady=1, height=5)
        text_frame.pack(side="left",fill="x")

        self.text = tk.Text(
            text_frame,
            font=("Courier", 11),
            bg=BG_SURFACE,
            fg=TEXT_PRIMARY,
            insertbackground=ACCENT,
            relief="flat",
            wrap="word",
            padx=10,
            pady=8,
            undo=True,
            selectbackground=ACCENT,
            selectforeground=TEXT_PRIMARY,
            height=5
        )

        self.text.pack(side="left",fill="x")

        scrollbar = tk.Scrollbar(
            text_frame,
            command=self.text.yview,
            width=6,
            relief="flat",
        )

        self.text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")

        self.text.bind("<KeyPress>", self._on_keypress)

    # ─────────────────────────────────────────────

    def _close(self):

        if self._on_close:
            self._on_close()

    # ─────────────────────────────────────────────

    def _on_keypress(self, event):

        n = len(self.text.get("1.0", "end-1c"))

        if n >= self.LIMITE:
            color = "#FF5A5A"
        elif n >= 180:
            color = "#FFB347"
        else:
            color = TEXT_MUTED

        self.counter.config(
            text=f"{n} / {self.LIMITE}",
            fg=color,
        )

        if n >= self.LIMITE and event.keysym not in (
            "BackSpace",
            "Delete",
            "Left",
            "Right",
            "Up",
            "Down",
        ):
            return "break"

    # ─────────────────────────────────────────────

    def get_text(self) -> str:
        return self.text.get("1.0", "end-1c")

    def clear(self):
        self.text.delete("1.0", "end")

    def set_text(self, value: str):

        self.clear()

        self.text.insert("1.0", value)

        self.counter.config(
            text=f"{len(value)} / {self.LIMITE}"
        )