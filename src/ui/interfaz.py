import tkinter as tk
from tkinter import ttk
from ..utils.seleccionar_directorio import seleccionarDirectorio
from pathlib import Path
from tkinter import filedialog, messagebox
import json
from .reproductor import Reproductor, _FlatButton, BG_DARK, BG_CARD, BG_SURFACE, ACCENT, ACCENT_HOVER, TEXT_PRIMARY, TEXT_MUTED, BORDER, SUCCESS
import shutil


CONFIG_FILE = "config.json"


def _apply_styles(root):
    """Configura los estilos ttk globales para toda la app."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Treeview ──────────────────────────────────────────────────────────────
    style.configure(
        "FP.Treeview",
        background=BG_CARD,
        foreground=TEXT_PRIMARY,
        fieldbackground=BG_CARD,
        rowheight=28,
        font=("Courier", 10),
        borderwidth=0,
        relief="flat",
    )
    style.configure(
        "FP.Treeview.Heading",
        background=BG_SURFACE,
        foreground=TEXT_MUTED,
        font=("Courier", 9, "bold"),
        relief="flat",
        borderwidth=0,
        padding=(8, 6),
    )
    style.map(
        "FP.Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "#FFFFFF")],
    )
    style.map(
        "FP.Treeview.Heading",
        background=[("active", BORDER)],
        foreground=[("active", TEXT_PRIMARY)],
    )

    # ── Scrollbar ─────────────────────────────────────────────────────────────
    style.configure(
        "FP.Vertical.TScrollbar",
        background=BG_SURFACE,
        troughcolor=BG_CARD,
        bordercolor=BG_CARD,
        arrowcolor=TEXT_MUTED,
        relief="flat",
        width=8,
    )
    style.map("FP.Vertical.TScrollbar", background=[("active", BORDER)])

    # ── Entry (ruta destino) ──────────────────────────────────────────────────
    style.configure(
        "FP.TEntry",
        fieldbackground=BG_SURFACE,
        foreground=TEXT_MUTED,
        insertcolor=ACCENT,
        bordercolor=BORDER,
        relief="flat",
        font=("Courier", 10),
        padding=(8, 5),
    )


class ListaDeCamaras(tk.Tk):
    def __init__(self, service, caso_service):
        super().__init__()
        self.title("Treeview Reordenable (Drag & Drop)")
        self.geometry("720x520")
        self.configure(bg=BG_DARK)
        self.service = service
        self.caso_service = caso_service
        self.camaras = None

        self._drag_data = {"item": None, "index": None}
        self.drag_item  = None
        self.drag_index = None
        self.target_row = None

        self.ruta_destino = tk.StringVar()
        self.cargar_configuracion()

        _apply_styles(self)
        self._build_ui()

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _build_ui(self):

        # ── Menú ──────────────────────────────────────────────────────────────
        barra_menus = tk.Menu(
            self,
            bg=BG_CARD, fg=TEXT_PRIMARY,
            activebackground=ACCENT, activeforeground=BORDER,
            relief="flat", bd=0,
        )
        menu_archivo = tk.Menu(
            barra_menus, tearoff=0,
            bg=BG_CARD, fg=TEXT_PRIMARY,
            activebackground=ACCENT, activeforeground=BORDER,
            relief="flat",
        )
        menu_archivo.add_command(label="Abrir",            command=self.seleccionarCarpeta)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Crear caso base",  command=self.crear_caso)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir",            command=self.quit)
        barra_menus.add_cascade(label="Archivo", menu=menu_archivo)
        self.config(menu=barra_menus)

        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(
            header, text="●", font=("Courier", 10),
            fg=ACCENT, bg=BG_DARK,
        ).pack(side="left")
        tk.Label(
            header, text="  FOLDER LISTER",
            font=("Courier", 12, "bold"),
            fg=TEXT_PRIMARY, bg=BG_DARK,
        ).pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=16)

        # ── Config: ruta destino ──────────────────────────────────────────────
        config_card = tk.Frame(self, bg=BG_CARD, padx=14, pady=10)
        config_card.pack(fill="x", padx=16, pady=(12, 0))

        tk.Label(
            config_card, text="RUTA DESTINO",
            font=("Courier", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD,
        ).pack(anchor="w", pady=(0, 4))

        ruta_row = tk.Frame(config_card, bg=BG_CARD)
        ruta_row.pack(fill="x")

        # borde del entry
        entry_border = tk.Frame(ruta_row, bg=BORDER, padx=1, pady=1)
        entry_border.pack(side="left", fill="x", expand=True, padx=(0, 8))

        entry_ruta = tk.Entry(
            entry_border,
            textvariable=self.ruta_destino,
            state="readonly",
            font=("Courier", 10),
            bg=BG_SURFACE, fg=TEXT_MUTED,
            readonlybackground=BG_SURFACE,
            disabledforeground=TEXT_MUTED,
            relief="flat",
            bd=4,
            insertbackground=ACCENT,
        )
        entry_ruta.pack(fill="x")

        btn_cambiar = _FlatButton(
            ruta_row,
            text="Cambiar...",
            command=self.cambiar_ruta_destino,
            bg=BG_SURFACE, fg=TEXT_PRIMARY,
            hover_bg=BORDER,
            font=("Courier", 9),
            padx=12, pady=6,
            width=100,
        )
        btn_cambiar.pack(side="left")

        # ── Treeview ──────────────────────────────────────────────────────────
        tree_wrapper = tk.Frame(self, bg=BG_DARK)
        tree_wrapper.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        # borde decorativo alrededor del tree
        tree_border = tk.Frame(tree_wrapper, bg=BORDER, padx=1, pady=1)
        tree_border.pack(fill="both", expand=True)

        tree_inner = tk.Frame(tree_border, bg=BG_CARD)
        tree_inner.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tree_inner,
            columns=("N", "Camara", "Hora", "Fecha"),
            show="headings",
            selectmode="extended",
            style="FP.Treeview",
        )
        self.tree.tag_configure("drag_hover", background=BORDER)
        self.tree.tag_configure("odd",  background=BG_CARD)
        self.tree.tag_configure("even", background=BG_SURFACE)

        self.tree.heading("N",      text="N°",     anchor=tk.W)
        self.tree.heading("Camara", text="CÁMARA", anchor=tk.W,
                          command=lambda: self.ordenarPor("nombre"))
        self.tree.heading("Hora",   text="HORA",   anchor=tk.W,
                          command=lambda: self.ordenarPor("horario"))
        self.tree.heading("Fecha",  text="FECHA",  anchor=tk.W)

        self.tree.column("N",      width=48,  anchor=tk.CENTER, stretch=False)
        self.tree.column("Camara", width=300, anchor=tk.W)
        self.tree.column("Hora",   width=110, anchor=tk.CENTER)
        self.tree.column("Fecha",  width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(
            tree_inner,
            orient="vertical",
            command=self.tree.yview,
            style="FP.Vertical.TScrollbar",
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Eventos drag & drop y doble click (sin cambios)
        self.tree.bind("<ButtonPress-1>",   self.on_start_drag, add="+")
        self.tree.bind("<B1-Motion>",       self.on_drag_motion, add="+")
        self.tree.bind("<ButtonRelease-1>", self.on_drop,       add="+")
        self.tree.bind("<Double-Button-1>", self.abrir_video,   add="+")

        # ── Barra de botones ──────────────────────────────────────────────────
        btn_bar = tk.Frame(self, bg=BG_DARK)
        btn_bar.pack(fill="x", padx=16, pady=(10, 14))

        btn_defs = [
            ("Confirmar", self.enumerar,        ACCENT,      ACCENT_HOVER,  "btn_confirmar"),
            ("Copiar",    self.copiar_listbox,   BG_SURFACE,  BORDER,        "btn_copiar"),
            ("Limpiar",   self.limpiarListBox,   BG_SURFACE,  BORDER,        "btn_limpiar"),
            ("Eliminar",  self.eliminar_camara,  "#3A1A1A",   "#5A2A2A",     "btn_delete"),
        ]

        for label, cmd, bg, hbg, attr in btn_defs:
            btn = _FlatButton(
                btn_bar,
                text=label,
                command=cmd,
                bg=bg, fg=TEXT_PRIMARY,
                hover_bg=hbg,
                font=("Courier", 10, "bold"),
                padx=14, pady=9,
                width=110,
            )
            btn.pack(side="left", padx=(0, 6))
            # guardamos referencia para enable/disable
            setattr(self, attr, btn)
            btn.set_state("disabled")

    # ── Métodos de configuración (sin cambios) ────────────────────────────────

    def cargar_configuracion(self):
        try:
            if Path(CONFIG_FILE).exists():
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    ruta = data.get("ruta_destino", "")
                    if Path(ruta).exists():
                        self.ruta_destino.set(ruta)
                    else:
                        self.ruta_destino.set(str(Path.cwd()))
            else:
                self.ruta_destino.set(str(Path.cwd()))
        except Exception as e:
            print(f"Error cargando config: {e}")
            self.ruta_destino.set(str(Path.cwd()))

    def guardar_configuracion(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
            data ["ruta_destino"] = self.ruta_destino.get()
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {e}")

    def cambiar_ruta_destino(self):
        directorio = filedialog.askdirectory(
            initialdir=self.ruta_destino.get(),
            title="Seleccionar carpeta de destino",
        )
        if directorio:
            self.ruta_destino.set(directorio)
            self.guardar_configuracion()

    # ── Helpers UI ────────────────────────────────────────────────────────────

    def _set_controls(self, state):
        for attr in ("btn_confirmar", "btn_copiar", "btn_limpiar", "btn_delete"):
            getattr(self, attr).set_state(state)
        # Habilitar/deshabilitar headings ordenables
        if state == "normal":
            self.tree.heading("Camara", command=lambda: self.ordenarPor("nombre"))
            self.tree.heading("Hora",   command=lambda: self.ordenarPor("horario"))
        else:
            self.tree.heading("Camara", command=lambda: None)
            self.tree.heading("Hora",   command=lambda: None)

    def limpiarListBox(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.camaras.clear()
        self.service.limpiarRepo()
        self._set_controls("disabled")

    def seleccionarCarpeta(self):
        carpetaCCTV = seleccionarDirectorio()
        if not carpetaCCTV:
            return
        self.service.cargarVideos(carpetaCCTV)
        self.camaras = self.service.obtenerVideos()
        self.cargar_camaras()

    def cargar_camaras(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, dir in enumerate(self.camaras, 1):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "", tk.END,
                values=(
                    str(idx).zfill(2),
                    dir.nombre,
                    dir.hora_fecha.strftime("%H:%M:%S"),
                    dir.hora_fecha.strftime("%Y-%m-%d"),
                ),
                tags=(tag,),
            )
        self._set_controls("normal" if self.camaras else "disabled")

    def ordenarPor(self, estrategia):
        self.camaras = self.service.ordenar(estrategia)
        self.service.actualizarLista(self.camaras)
        self.cargar_camaras()
        self.service.actualizarLista(self.camaras)

    # ── Drag & Drop (sin cambios) ─────────────────────────────────────────────

    def on_start_drag(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self._drag_data["item"]  = item
            self._drag_data["index"] = self.tree.index(item)

    def on_drag_motion(self, event):
        if not self._drag_data["item"]:
            return
        target_item = self.tree.identify_row(event.y)
        for item in self.tree.get_children():
            idx = self.tree.index(item)
            self.tree.item(item, tags=("even" if (idx + 1) % 2 == 0 else "odd",))
        if target_item and target_item != self._drag_data["item"]:
            self.tree.item(target_item, tags=("drag_hover",))

    def on_drop(self, event):
        target_item = self.tree.identify_row(event.y)
        source_item = self._drag_data["item"]
        if source_item and target_item and source_item != target_item:
            target_index = self.tree.index(target_item)
            source_index = self._drag_data["index"]
            obj_movido   = self.camaras.pop(source_index)
            self.camaras.insert(target_index, obj_movido)
            self.service.actualizarLista(self.camaras)
            self.cargar_camaras()
            new_id = self.tree.get_children()[target_index]
            self.tree.selection_set(new_id)
        self._drag_data = {"item": None, "index": None}
        for item in self.tree.get_children():
            idx = self.tree.index(item)
            self.tree.item(item, tags=("even" if (idx + 1) % 2 == 0 else "odd",))

    # ── Acciones (sin cambios) ────────────────────────────────────────────────

    def enumerar(self):
        for idx, video in enumerate(self.camaras, 1):
            base       = Path(self.ruta_destino.get())
            nueva_ruta = base / f"{str(idx).zfill(2)} - {video.nombre}"
            nueva_ruta.mkdir()
            shutil.copy(video.ruta_inicial, nueva_ruta)
        self.btn_confirmar.set_state("disabled")
        self.btn_delete.set_state("disabled")

    def copiar_listbox(self):
        filas = []
        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            filas.append("\t".join(map(str, valores[1:3])))
        texto = "\n".join(filas)
        self.clipboard_clear()
        self.clipboard_append(texto)

    def eliminar_camara(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        indices = sorted([self.tree.index(i) for i in seleccion], reverse=True)
        for i in indices:
            del self.camaras[i]
        self.service.actualizarLista(self.camaras)
        self.cargar_camaras()

    def abrir_video(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        self.tree.selection_set(item_id)
        indice = self.tree.index(item_id)
        Reproductor(self, self.camaras[indice], Path(self.ruta_destino.get()), self.service)
        self.camaras = self.service.obtenerVideos()
        self.cargar_camaras()

    def crear_caso(self):
        self.caso_service.agregar_videos(self.camaras)
        self.caso_service.crear_nuevo_caso()