import tkinter as tk
from tkinter import ttk
from ..utils.seleccionar_directorio import seleccionarDirectorio
from pathlib import Path
from tkinter import filedialog, messagebox
import json
from .reproductor import Reproductor
# Nombre del archivo donde guardaremos la configuración
CONFIG_FILE = "config.json"
class ListaDeCamaras(tk.Tk):
    def __init__(self, service):
        super().__init__()
        self.title("Treeview Reordenable (Drag & Drop)")
        self.geometry("600x400")
        self.service = service
        self.camaras = None
        # Variables de estado para el arrastre
        self._drag_data = {"item": None, "index": None}
        # Estado de arrastre
        self.drag_item = None
        self.drag_index = None
        self.target_row = None

        # --- 1. Inicializar variable de ruta y Cargar Configuración ---
        self.ruta_destino = tk.StringVar()
        self.cargar_configuracion()
        
        main_frame = ttk.Frame(self, padding="10") 
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- 2. SECCIÓN DE CONFIGURACIÓN (NUEVA) ---
        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 10)) # pady bottom 10
        
        lbl_ruta = ttk.Label(config_frame, text="Ruta Destino:")
        lbl_ruta.pack(side=tk.LEFT)
        
        # Entry de solo lectura para mostrar la ruta actual
        entry_ruta = ttk.Entry(config_frame, textvariable=self.ruta_destino, state="readonly", width=50)
        entry_ruta.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_cambiar_ruta = ttk.Button(config_frame, text="Cambiar...", command=self.cambiar_ruta_destino)
        btn_cambiar_ruta.pack(side=tk.LEFT)
        
        # --- CONFIGURACIÓN DEL MENÚ ---
        # Usamos self para que pertenezca a esta instancia de Tk
        barra_menus = tk.Menu(self)


        menu_archivo = tk.Menu(barra_menus, tearoff=0)
        menu_archivo.add_command(label="Abrir", command=self.seleccionarCarpeta)
        menu_archivo.add_separator() 
        menu_archivo.add_command(label="Salir", command=self.quit)  
        
        # Agregamos el menú a la barra y la barra a la ventana
        barra_menus.add_cascade(label="Archivo", menu=menu_archivo)
        self.config(menu=barra_menus)

        # --- CONFIGURACIÓN DEL TREEVIEW ---
        # 'fill=both' y 'expand=True' hacen que ocupe el espacio disponible
        self.tree = ttk.Treeview(self, columns=('N', 'Camara', 'Hora', 'Fecha'), show='headings', selectmode="extended")
        self.tree.tag_configure("drag_hover", background="#cce5ff")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.tree.heading('N', text='N', anchor=tk.W)
        self.tree.heading('Camara', text='Camara', anchor=tk.W,command=lambda: self.ordenarPor("nombre"))
        self.tree.heading('Hora', text='Hora', anchor=tk.W, command=lambda: self.ordenarPor("horario"))
        self.tree.heading(column='Fecha', text='Fecha', anchor=tk.W)

        
        self.tree.column('N', width=50, anchor=tk.CENTER)
        self.tree.column('Camara', width=200, anchor=tk.W)
        self.tree.column('Hora', width=100, anchor=tk.CENTER)
        self.tree.column('Fecha', width=100, anchor=tk.CENTER)



        # --- EVENTOS DRAG & DROP ---
        # Usamos <ButtonPress-1> para capturar el ítem sin romper la selección
        self.tree.bind('<ButtonPress-1>', self.on_start_drag, add='+')
        self.tree.bind('<B1-Motion>', self.on_drag_motion, add='+')
        self.tree.bind('<ButtonRelease-1>', self.on_drop, add='+')
        self.tree.bind('<Double-Button-1>', self.abrir_video, add='+')



        # --- CONTENEDOR DE BOTONES ---
        frame_botones = tk.Frame(self)
        frame_botones.pack(side="bottom", fill="x", padx=10, pady=5)

        self.btn_confirmar = ttk.Button(frame_botones, text="Confirmar", command=self.enumerar)
        self.btn_confirmar.pack(side="left", padx=2)
        self.btn_confirmar.config(state="disabled")

        self.btn_copiar = ttk.Button(frame_botones, text="Copiar", command=self.copiar_listbox)
        self.btn_copiar.pack(side="left", padx=2)
        self.btn_copiar.config(state="disabled")

        self.btn_limpiar = ttk.Button(frame_botones, text="Limpiar", command=self.limpiarListBox)
        self.btn_limpiar.pack(side="left", padx=2)
        self.btn_limpiar.config(state="disabled")

        
        self.btn_delete = ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_camara)
        self.btn_delete.pack(side="left", padx=2)
        self.btn_delete.config(state="disabled")

    # --- MÉTODOS DE CONFIGURACIÓN ---
    def cargar_configuracion(self):
        """Carga la ruta desde el archivo JSON o usa una por defecto."""
        try:
            if Path(CONFIG_FILE).exists():
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    ruta = data.get("ruta_destino", "")
                    if Path(ruta).exists():
                        self.ruta_destino.set(ruta)
                    else:
                        # Si la ruta guardada ya no existe, usamos la carpeta actual
                        self.ruta_destino.set(str(Path.cwd()))
            else:
                # Si no existe archivo config, usamos carpeta actual por defecto
                self.ruta_destino.set(str(Path.cwd()))
        except Exception as e:
            print(f"Error cargando config: {e}")
            self.ruta_destino.set(str(Path.cwd()))

    def guardar_configuracion(self):
        """Guarda la ruta actual en un archivo JSON."""
        data = {"ruta_destino": self.ruta_destino.get()}
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {e}")

    def cambiar_ruta_destino(self):
        """Abre el diálogo para seleccionar carpeta."""
        directorio = filedialog.askdirectory(initialdir=self.ruta_destino.get(), 
                                             title="Seleccionar carpeta de destino")
        if directorio:
            self.ruta_destino.set(directorio)
            self.guardar_configuracion() # Guardamos inmediatamente al cambiar


    def limpiarListBox(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.camaras.clear() 
        self.service.limpiarRepo()
        self.btn_confirmar.config(state="disabled")
        self.btn_copiar.config(state="disabled")
        self.btn_limpiar.config(state="disabled")
        self.btn_delete.config(state="disabled")


    def seleccionarCarpeta(self):
        carpetaCCTV = seleccionarDirectorio()
        if not carpetaCCTV:
            return
        self.service.cargarVideos(carpetaCCTV)
        self.camaras = self.service.obtenerVideos()
        self.cargar_camaras()


    def cargar_camaras(self):
        """Limpia y vuelve a cargar el Treeview con nuevos datos."""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, dir in enumerate(self.camaras,1):
            self.tree.insert('', tk.END, values=(str(idx).zfill(2),dir.nombre, dir.hora_fecha.strftime("%H:%M:%S"), dir.hora_fecha.strftime("%Y-%m-%d")))

        self.btn_confirmar.config(state="normal")
        self.btn_copiar.config(state="normal")
        self.btn_limpiar.config(state="normal")
        self.btn_delete.config(state="normal")



    def ordenarPor(self, estrategia):
        self.camaras = self.service.ordenar(estrategia)
        self.service.actualizarLista(self.camaras)
        self.cargar_camaras()
        self.service.actualizarLista(self.camaras)


# --- LÓGICA DE DRAG & DROP ---

    def on_start_drag(self, event):
        """Identifica qué fila se está intentando arrastrar."""
        item = self.tree.identify_row(event.y)
        if item:
            self._drag_data["item"] = item
            self._drag_data["index"] = self.tree.index(item)

    def on_drag_motion(self, event):
        """Visualiza dónde caería el ítem mientras se arrastra."""
        if not self._drag_data["item"]:
            return

        target_item = self.tree.identify_row(event.y)
        
        # Limpiar estilos previos
        for item in self.tree.get_children():
            self.tree.item(item, tags=())

        # Resaltar la fila destino
        if target_item and target_item != self._drag_data["item"]:
            self.tree.item(target_item, tags=("drag_hover",))

    def on_drop(self, event):
        """Ejecuta el reordenamiento real en los datos y la UI."""
        target_item = self.tree.identify_row(event.y)
        source_item = self._drag_data["item"]

        if source_item and target_item and source_item != target_item:
            target_index = self.tree.index(target_item)
            source_index = self._drag_data["index"]

            # --- REORDENAR LISTA DE DATOS ---
            # Extraemos el objeto de la posición original e insertamos en la nueva
            obj_movido = self.camaras.pop(source_index)
            self.camaras.insert(target_index, obj_movido)

            # Sincronizar el Service (opcional, dependiendo de tu arquitectura)
            # self.service.actualizar_orden(self.camaras)
            self.service.actualizarLista(self.camaras)

            # Refrescar vista
            self.cargar_camaras()
            
            # Mantener la selección en el nuevo lugar
            new_id = self.tree.get_children()[target_index]
            self.tree.selection_set(new_id)

        # Limpiar estado
        self._drag_data = {"item": None, "index": None}
        for item in self.tree.get_children():
            self.tree.item(item, tags=())



    def enumerar(self):
        for idx, video in enumerate(self.camaras, 1):
            base = Path(self.ruta_destino.get())
            nueva_ruta = base / f"{str(idx).zfill(2)} - {video.nombre}"
            print(nueva_ruta)
        self.limpiarListBox()

   
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

        indices = [self.tree.index(item_id) for item_id in seleccion]
        indices.sort(reverse=True)

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
        Reproductor(self, self.camaras[indice].ruta_inicial, Path(self.ruta_destino.get()))