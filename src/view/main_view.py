"""
view/main_view.py
─────────────────
Vista principal del sistema Folder Lister CCTV (capa V del patrón MVC).

Responsabilidades:
    • Construir y organizar la jerarquía de widgets.
    • Exponer señales Qt para que el Controlador las conecte.
    • Exponer métodos públicos para que el Controlador actualice el estado.

No contiene lógica de negocio ni strings de estilo inline.
Todo el QSS se carga desde el paquete `styles/`.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel,QPushButton,
    QFrame, QButtonGroup,
    QFileDialog, QMessageBox, QStackedWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from ..styles.loader import load_qss
from ..styles.theme import Theme
from .widgets import (
    NavButton
)
from .pages.videos_page import VideosPage


class MainView(QMainWindow):
    """
    Ventana principal de la aplicación CCTV Folder Lister.

    Señales (para conectar desde el Controlador):
        sig_ver_video(int)      — usuario hizo clic en "Ver video" de la fila N
        sig_guardar()           — botón "Guardar carpeta CCTV"
        sig_pagina(int)         — cambio de página
        sig_nav_videos()        — pestaña VIDEOS seleccionada
        sig_nav_diapositivas()  — pestaña DIAPOSITIVAS seleccionada
        sig_play / pause / stop — controles del reproductor
        sig_captura()           — captura de pantalla
        sig_grabar()            — iniciar/detener grabación
        sig_fullscreen()        — pantalla completa
        sig_speed_change(str)   — cambio de velocidad de reproducción
        sig_seek(int)           — arrastre de la barra de progreso (0-100)
        sig_volume(int)         — cambio de volumen (0-100)
    """

    # ── Señales ─────────────────────────────────────────────────────────
    sig_importar_videos      = Signal(str)
    sig_pagina           = Signal(int)
    sig_nav_videos       = Signal()
    sig_nav_diapositivas = Signal()




    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOLDER LISTER")
        self.setMinimumSize(1200, 820)
        self.resize(1340, 860)
        self.setStyleSheet(load_qss("global"))
        self.page_videos = VideosPage()
        self._build_ui()


    # ════════════════════════════════════════════════════════════════════
    #  CONSTRUCCIÓN DE LA UI
    # ════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        self._build_menubar()

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_toolbar())
        root.addWidget(self._make_hsep())
        self.stack = QStackedWidget()

        
        self.page_diapositivas = self._build_diapositivas_page()

        self.stack.addWidget(self.page_videos)
        self.stack.addWidget(self.page_diapositivas)

        root.addWidget(self.stack, stretch=1)

    # ── Menú ────────────────────────────────────────────────────────────
    def _build_menubar(self):
        bar = self.menuBar()
        bar.setNativeMenuBar(False)
        archivo = bar.addMenu("Archivo  ▾")

        self.act_abrir_proyecto = QAction("Abrir", self)
        
        self.act_guardar = QAction("Guardar", self)
        self.act_guardar_como = QAction("Guardar como", self)
        self.act_salir = QAction("Salir", self)

        archivo.addAction(self.act_abrir_proyecto)
        
        archivo.addSeparator()
        archivo.addAction(self.act_guardar)
        archivo.addAction(self.act_guardar_como)
        archivo.addSeparator()
        archivo.addAction(self.act_salir) 
        
        self.act_salir.triggered.connect(self.close)

        insertar = bar.addMenu("Insertar  ▾")
        self.act_importar_videos = QAction("Exportaciones Milestone XProtect", self)
        self.act_insertar_video_particular = QAction("Camara Particular", self)
        insertar.addAction(self.act_importar_videos)
        insertar.addAction(self.act_insertar_video_particular)
        self.act_importar_videos.triggered.connect(self._on_importar_videos)


    # ── Toolbar ─────────────────────────────────────────────────────────
    def _build_toolbar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(56)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 8, 16, 8)

        # Logo
        lbl_dot = QLabel("●")
        lbl_dot.setObjectName("status_dot")
        lbl_dot.setStyleSheet(load_qss("panels"))

        lbl_title = QLabel("FOLDER LISTER")
        lbl_title.setObjectName("lbl_title")
        lbl_title.setStyleSheet(load_qss("panels"))

        layout.addWidget(lbl_dot)
        layout.addSpacing(6)
        layout.addWidget(lbl_title)
        layout.addStretch()

        # Navegación central
        self.btn_videos = NavButton("VIDEOS", "⬜", active=True)
        self.btn_diapositivas = NavButton("DIAPOSITIVAS", "🖥")

        nav_group = QButtonGroup(self)
        nav_group.setExclusive(True)
        nav_group.addButton(self.btn_videos)
        nav_group.addButton(self.btn_diapositivas)

        self.btn_videos.toggled.connect(
            lambda checked: self.sig_nav_videos.emit() if checked else None
        )
        self.btn_diapositivas.toggled.connect(
            lambda checked: self.sig_nav_diapositivas.emit() if checked else None
        )

        center = QHBoxLayout()
        center.setSpacing(8)
        center.addWidget(self.btn_videos)
        center.addWidget(self.btn_diapositivas)
        layout.addLayout(center)
        layout.addStretch()

        # Botón configuración
        btn_settings = QPushButton("⚙")
        btn_settings.setObjectName("btn_settings")
        btn_settings.setFixedSize(36, 36)
        btn_settings.setStyleSheet(load_qss("player"))
        layout.addWidget(btn_settings)

        return bar



    # ════════════════ PAGINA DIAPOSITIVAS (En desarrollo) ═════════════════════════════════
    def _build_diapositivas_page(self) -> QWidget:
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)

        label = QLabel("Página DIAPOSITIVAS")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)

        return page

 
    
    # ════════════════════════════════════════════════════════════════════
    #  Cambiar de pagina
    # ════════════════════════════════════════════════════════════════════

    def show_videos_page(self):
        self.stack.setCurrentWidget(self.page_videos)


    def show_diapositivas_page(self):
        self.stack.setCurrentWidget(self.page_diapositivas)




    def set_active_page(self, page: int):
        """Marca el botón de página correspondiente como activo."""
        for btn in self.page_buttons:
            btn.setChecked(btn.text() == str(page))


    # ── Importar videos ─────────────────────────────────────────────────────────
    def _on_importar_videos(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta de videos",
            "",
            QFileDialog.Option.ShowDirsOnly
        )

        if folder_path:
            self.sig_importar_videos.emit(folder_path)

    # ── Helpers ─────────────────────────────────────────────────────────
    @staticmethod
    def _make_hsep() -> QFrame:
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {Theme.BORDER_DIM};")
        return sep

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "_overlay_cam") and hasattr(self, "video_area"):
            h = self.video_area.height()
            self._overlay_cam.move(8, h - self._overlay_cam.height() - 8)


    # ── Message Box ─────────────────────────────────────────────────────────
    def show_info_message(self, title: str, message: str):
        QMessageBox.information(
            self,
            title,
            message
        )

    def show_warning_message(self, title: str, message: str):
        QMessageBox.warning(
            self,
            title,
            message
        )