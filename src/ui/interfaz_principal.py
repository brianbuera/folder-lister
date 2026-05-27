import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from tkinter import filedialog
from .reproductor import Reproductor
from .widgets.flat_button import _FlatButton
from ..styles.colors import *
from ..styles.apply_style import _apply_styles
from ..tools.crop_tool import realizar_recortes
from ..utils import seleccionarDirectorio, seleccionarDirectorioVideos
from ..config.config_manager import config
from .mostrar_infovideo import mostrar_info_video

#Ventana principal
class InterfazPrincipal(tk.Tk):
    def __init__(self, video_service, caso_service):
        super().__init__()
        self.title("FOLDER LISTER")
        self.geometry("900x700")
        self.configure(bg=BG_DARK)
        self.video_service = video_service
        self.caso_service = caso_service
        self.carpeta_cctv = None
        # Variable que guarda el estado
        self.al_frente_var = tk.BooleanVar(value=False)
        self._drag_data = {"item": None, "index": None}
 
        self.config_manager = config
        self.ruta_destino = tk.StringVar(value=self.config_manager.ruta_destino)

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
        menu_archivo.add_command(label="Abrir",command=self.seleccionarCarpeta)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Agregar capturas a caso actual",command=self.crear_caso)
        menu_archivo.add_separator()
        menu_archivo.add_checkbutton(label="Al frente siempre",variable=self.al_frente_var,command=self.al_frente)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir",command=self.quit)
        barra_menus.add_cascade(label="Archivo",menu=menu_archivo)
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
            bd=3,
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
        self.tree.bind("<Button-3>", self.recortar_capturas)
        self.tree.bind("<w>", self.mostrar_infovideo)

        # ── Barra de botones ──────────────────────────────────────────────────
        btn_bar = tk.Frame(self, bg=BG_DARK)
        btn_bar.pack(fill="x", padx=16, pady=(10, 14))

        btn_defs = [
            ("Confirmar", self.enumerar_camaras,        ACCENT,      ACCENT_HOVER,  "btn_confirmar"),
            ("Copiar",    self.copiar_listbox,   BG_SURFACE,  BORDER,        "btn_copiar"),
            ("Limpiar",   self.vaciar_lista_videos, BG_SURFACE,  BORDER,        "btn_vaciar"),
            ("Eliminar",  self.eliminar_videos,  "#3A1A1A",   "#5A2A2A",     "btn_delete"),
            ("restaurar",  self.restaurar,  BG_SURFACE,   BORDER,     "btn_update"),

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

    def cambiar_ruta_destino(self):
        directorio = seleccionarDirectorio()
        if directorio:
            self.ruta_destino.set(directorio)
            self.config_manager.ruta_destino = directorio

    # ── Helpers UI ────────────────────────────────────────────────────────────

    def _set_controls(self, state):
        for attr in ("btn_confirmar", "btn_copiar", "btn_vaciar", "btn_delete","btn_update"):
            getattr(self, attr).set_state(state)
        # Habilitar/deshabilitar headings ordenables
        if state == "normal":
            self.tree.heading("Camara", command=lambda: self.ordenarPor("nombre"))
            self.tree.heading("Hora",   command=lambda: self.ordenarPor("horario"))
        else:
            self.tree.heading("Camara", command=lambda: None)
            self.tree.heading("Hora",   command=lambda: None)

    def vaciar_lista_videos(self):
        self.limpiarTreeView()
        self.video_service.limpiarRepo()
        self.carpeta_cctv = None
        self._set_controls("disabled")


    def limpiarTreeView(self):
        for item in self.tree.get_children():
            self.tree.delete(item)


    def seleccionarCarpeta(self):
        self.carpeta_cctv = seleccionarDirectorioVideos()
        if not self.carpeta_cctv:
            return
        self.video_service.cargarVideos(self.carpeta_cctv)
        self.cargar_camaras()

    def cargar_camaras(self):
        self.limpiarTreeView()
        videos = self.video_service.obtenerVideos()
        for idx, cam in enumerate(videos, 1):
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert(
                "", tk.END,
                values=(
                    str(idx).zfill(2),
                    cam.nombre,
                    cam.hora_fecha.strftime("%H:%M:%S"),
                    cam.hora_fecha.strftime("%d-%m-%Y"),
                ),
                tags=(tag,),
            )
        self._set_controls("normal" if videos else "disabled")

    def ordenarPor(self, estrategia):
        self.video_service.ordenar(estrategia)
        self.cargar_camaras()

    # ── Drag & Drop ─────────────────────────────────────────────

    def on_start_drag(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self._drag_data["item"]  = item
            self._drag_data["index"] = self.tree.index(item)
            self.tree.selection_set(item)
            indice = self.tree.index(item)


    def mostrar_infovideo(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        self.tree.selection_set(item_id)
        indice = self.tree.index(item_id)
        video = self.video_service.obtener_video(indice)
        print (video)
        mostrar_info_video(video, self)


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
        videos = self.video_service.obtenerVideos()
        target_item = self.tree.identify_row(event.y)
        source_item = self._drag_data["item"]
        if source_item and target_item and source_item != target_item:
            target_index = self.tree.index(target_item)
            source_index = self._drag_data["index"]
            obj_movido   = videos.pop(source_index)
            videos.insert(target_index, obj_movido)
            self.video_service.actualizarLista(videos)
            self.cargar_camaras()
            new_id = self.tree.get_children()[target_index]
            self.tree.selection_set(new_id)
        self._drag_data = {"item": None, "index": None}
        for item in self.tree.get_children():
            idx = self.tree.index(item)
            self.tree.item(item, tags=("even" if (idx + 1) % 2 == 0 else "odd",))

    # ── Acciones ────────────────────────────────────────────────

    def enumerar_camaras(self):
        ruta_destino = self.config_manager.ruta_destino
        if not ruta_destino:
            messagebox.showerror("No hay ruta destino", "Por favor seleccione una ruta destino")
            return
        cctv =  Path(ruta_destino) / "CCTV" 
        destino = self.video_service.enumerar_videos(cctv)
        self.btn_confirmar.set_state("disabled")
        self.btn_delete.set_state("disabled")
        messagebox.showinfo("Videos ordenados con exito", f"Los videos se encuentran en la carpeta {destino.name}")



    def copiar_listbox(self):
        filas = []
        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            filas.append("\t".join(map(str, valores[1:3])))
        texto = "\n".join(filas)
        self.clipboard_clear()
        self.clipboard_append(texto)
        messagebox.showinfo("Copiado", f"Lista de videos copiada en portapapeles")



    def eliminar_videos(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        indices = sorted([self.tree.index(i) for i in seleccion], reverse=True)
        self.video_service.eliminar_videos(indices)
        self.cargar_camaras()


    def abrir_video(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        self.tree.selection_set(item_id)
        indice = self.tree.index(item_id)
        Reproductor(self, self.video_service.obtener_video(indice), self.config_manager)
        print(self.video_service.obtener_video(indice))
        self.withdraw()


    def recortar_capturas(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        self.tree.selection_set(item_id)
        indice = self.tree.index(item_id)
        realizar_recortes(self,self.video_service.obtener_video(indice))


    def crear_caso(self):
        template = self.config_manager.ruta_template
        videos = self.video_service.obtenerVideos()
        resultado = self.caso_service.crear_nuevo_caso(videos, template)

        if resultado:
            messagebox.showinfo("Proceso completado","Todas las diapositivas se agregaron exitosamente")
        else:
            messagebox.showerror(
                "Error",
                "Ocurrió un problema al agregar diapositivas.\n\n"
                "Verifique lo siguiente:\n\n"
                "1. Tener un caso PowerPoint abierto en alguna de las pantallas.\n"
                "2. Que el archivo .pptx tenga exactamente el siguiente nombre:\n"
                "   'Presentación Análisis de Imagen'\n\n"
                "Recuerde haber realizado las capturas y recortes si eran necesarios."
            )
    def restaurar(self):
        self.video_service.cargarVideos(self.carpeta_cctv)
        self.cargar_camaras()
        

    def al_frente(self):
        estado = self.al_frente_var.get()
        self.attributes('-topmost', estado)