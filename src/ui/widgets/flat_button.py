import tkinter as tk
from ...styles.colors import *
# ── Widget auxiliar: botón flat con hover ────────────────────────────────────

class _FlatButton(tk.Canvas):
    """Botón rectangular sin relieve, con transición de color al hover."""

    def __init__(self, parent, text, command, bg, fg, hover_bg,
                 font, padx=12, pady=8, width=200, **kwargs):
        h = pady * 2 + 22
        super().__init__(parent, bg=parent["bg"], bd=0, highlightthickness=0,
                         height=h, width=width)
        self._bg       = bg
        self._hover_bg = hover_bg
        self._fg       = fg
        self._font     = font
        self._text     = text
        self._cmd      = command
        self._width    = width
        self._height   = h
        self._padx     = padx
        self._pady     = pady

        self._rect = self.create_rectangle(0, 0, width, h, fill=bg, outline="", tags="btn")
        self._lbl  = self.create_text(
            width // 2, h // 2,
            text=text, fill=fg,
            font=font, tags="btn"
        )

        self.tag_bind("btn", "<Enter>",   self._on_enter)
        self.tag_bind("btn", "<Leave>",   self._on_leave)
        self.tag_bind("btn", "<Button-1>", self._on_click)

    def _on_enter(self, _):
        if not getattr(self, '_disabled', False):
            self.itemconfig(self._rect, fill=self._hover_bg)

    def _on_leave(self, _):
        if not getattr(self, '_disabled', False):
            self.itemconfig(self._rect, fill=self._bg)
        else:
            self.itemconfig(self._rect, fill=BORDER)

    def _on_click(self, _):
        if not getattr(self, '_disabled', False):
            self._cmd()

    def set_state(self, state):
        """'normal' o 'disabled'. Cambia apariencia y bloquea clicks."""
        self._disabled = (state == "disabled")
        alpha = TEXT_MUTED if self._disabled else self._fg
        fill  = BORDER     if self._disabled else self._bg
        self.itemconfig(self._rect, fill=fill)
        self.itemconfig(self._lbl,  fill=alpha)

