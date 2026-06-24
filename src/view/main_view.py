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
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QFrame, QSlider, QSizePolicy, QScrollArea,
    QGridLayout, QComboBox, QAbstractItemView, QButtonGroup,
    QFileDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPalette, QFont, QAction

from ..styles import Theme, load_qss
from .widgets import (
    NavButton, ActionButton,
    PaginationButton, ArrowButton,
    PlayerControlBtn, SectionLabel, ThumbnailWidget,
)


class FolderListerView(QMainWindow):
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
    sig_eliminar_video      = Signal(int)
    sig_ver_video        = Signal(int)
    sig_guardar          = Signal()
    sig_pagina           = Signal(int)
    sig_nav_videos       = Signal()
    sig_nav_diapositivas = Signal()
    sig_play             = Signal()
    sig_pause            = Signal()
    sig_stop             = Signal()
    sig_captura          = Signal()
    sig_grabar           = Signal()
    sig_fullscreen       = Signal()
    sig_speed_change     = Signal(str)
    sig_seek             = Signal(int)
    sig_volume           = Signal(int)

    def __init__(self, controller = None):
        super().__init__()
        self.setWindowTitle("FOLDER LISTER")
        self.setMinimumSize(1200, 820)
        self.resize(1340, 860)
        self.setStyleSheet(load_qss("global"))
        self._build_ui()
        self.controller = controller

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

        content = QWidget()
        h = QHBoxLayout(content)
        h.setContentsMargins(16, 16, 16, 16)
        h.setSpacing(16)
        h.addWidget(self._build_left_column(),  stretch=5)
        h.addWidget(self._build_right_column(), stretch=4)

        root.addWidget(content, stretch=1)

    # ── Menú ────────────────────────────────────────────────────────────
    def _build_menubar(self):
        bar = self.menuBar()
        bar.setNativeMenuBar(False)
        archivo = bar.addMenu("Archivo  ▾")

        self.act_abrir_proyecto = QAction("Abrir", self)
        self.act_importar_videos = QAction("Importar videos", self)
        self.act_guardar = QAction("Guardar", self)
        self.act_guardar_como = QAction("Guardar como", self)
        self.act_salir = QAction("Salir", self)

        archivo.addAction(self.act_abrir_proyecto)
        archivo.addAction(self.act_importar_videos)
        archivo.addSeparator()
        archivo.addAction(self.act_guardar)
        archivo.addAction(self.act_guardar_como)
        archivo.addSeparator()
        archivo.addAction(self.act_salir)

        
        self.act_importar_videos.triggered.connect(self._on_importar_videos)
        self.act_salir.triggered.connect(self.close)

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

    # ════════════════ COLUMNA IZQUIERDA ═════════════════════════════════

    def _build_left_column(self) -> QWidget:
        col = QWidget()
        col.setProperty("panel", "true")
        col.setStyleSheet(load_qss("panels"))

        layout = QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_table_header())
        self.table = self._build_table()
        layout.addWidget(self.table, stretch=1)
        layout.addWidget(self._build_bottom_bar())

        return col

    def _build_table_header(self) -> QWidget:
        header = QWidget()
        header.setFixedHeight(44)
        header.setProperty("panel_header", "true")
        header.setStyleSheet(load_qss("panels"))

        h = QHBoxLayout(header)
        h.setContentsMargins(16, 0, 16, 0)

        dot = QLabel("●")
        dot.setObjectName("status_dot")
        dot.setStyleSheet(load_qss("panels"))

        title = QLabel("FOLDER LISTER")
        title.setObjectName("lbl_title")
        title.setStyleSheet(load_qss("panels"))

        h.addWidget(dot)
        h.addSpacing(6)
        h.addWidget(title)
        h.addStretch()
        return header

    def _build_table(self) -> QTableWidget:
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["N°", "CÁMARA", "HORA", "FECHA", "ACCIÓN"])

        hh = table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(0, 48)
        table.setColumnWidth(2, 90)
        table.setColumnWidth(3, 110)
        table.setColumnWidth(4, 110)

        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        table.setRowCount(0)

        return table
    
    def _create_actions_buttons_cell(self, row: int, active: bool = False) -> QWidget:
        cell = QWidget()
        cell.setStyleSheet("background: transparent;")

        cell_layout = QHBoxLayout(cell)
        cell_layout.setContentsMargins(4, 4, 4, 4)
        cell_layout.setSpacing(4)

        btn_ver = ActionButton("▶")
        btn_eliminar = ActionButton("🗑")


        btn_ver.clicked.connect(lambda _, r=row: self._on_ver_video(r))
        btn_eliminar.clicked.connect(lambda _, r=row: self._on_delete_video(r))

        cell_layout.addWidget(btn_ver)
        cell_layout.addWidget(btn_eliminar)

        return cell
        
    def _build_bottom_bar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(60)
        bar.setProperty("bottom_bar", "true")
        bar.setStyleSheet(load_qss("panels"))

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(6)

        self.btn_prev = ArrowButton("‹")
        layout.addWidget(self.btn_prev)

        self.page_buttons: list[PaginationButton] = []
        self._page_group = QButtonGroup(self)
        self._page_group.setExclusive(True)

        for p in range(1, 6):
            pb = PaginationButton(str(p), active=(p == 1))
            self._page_group.addButton(pb)
            self.page_buttons.append(pb)
            pb.clicked.connect(lambda _, pg=p: self.sig_pagina.emit(pg))
            layout.addWidget(pb)

        self.btn_next = ArrowButton("›")
        layout.addWidget(self.btn_next)
        layout.addStretch()

        self.btn_guardar = QPushButton("  Guardar carpeta CCTV")
        self.btn_guardar.setObjectName("btn_guardar")
        self.btn_guardar.setFixedHeight(38)
        self.btn_guardar.setStyleSheet(load_qss("player"))
        self.btn_guardar.clicked.connect(self.sig_guardar.emit)
        layout.addWidget(self.btn_guardar)

        return bar

    # ════════════════ COLUMNA DERECHA ═══════════════════════════════════

    def _build_right_column(self) -> QWidget:
        col = QWidget()
        col.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(self._build_player_panel(),   stretch=3)
        layout.addWidget(self._build_captures_panel(), stretch=2)
        return col

    # ── Reproductor ─────────────────────────────────────────────────────
    def _build_player_panel(self) -> QWidget:
        panel = QWidget()
        panel.setProperty("panel", "true")
        panel.setStyleSheet(load_qss("panels"))

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        # Encabezado
        hdr = QHBoxLayout()
        hdr.addWidget(SectionLabel("▶", "REPRODUCTOR"))
        hdr.addStretch()
        self.lbl_cam_active = QLabel("CAM 01 - Acceso Principal")
        self.lbl_cam_active.setProperty("cam_active_label", "true")
        self.lbl_cam_active.setStyleSheet(load_qss("panels"))
        hdr.addWidget(self.lbl_cam_active)
        layout.addLayout(hdr)

        # Área de video
        self.video_area = QLabel()
        self.video_area.setObjectName("video_area")
        self.video_area.setMinimumHeight(230)
        self.video_area.setStyleSheet(load_qss("panels"))
        self.video_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Overlays
        self._overlay_ts = QLabel("24/05/2025  08:15:32", self.video_area)
        self._overlay_ts.setProperty("video_overlay", "true")
        self._overlay_ts.setStyleSheet(load_qss("panels"))
        self._overlay_ts.move(8, 8)
        self._overlay_ts.adjustSize()

        self._overlay_cam = QLabel("CAM 01", self.video_area)
        self._overlay_cam.setProperty("video_overlay", "true")
        self._overlay_cam.setStyleSheet(load_qss("panels"))
        self._overlay_cam.adjustSize()

        layout.addWidget(self.video_area)

        # Barra de progreso
        self.slider_progress = QSlider(Qt.Orientation.Horizontal)
        self.slider_progress.setRange(0, 100)
        self.slider_progress.setValue(10)
        self.slider_progress.valueChanged.connect(self.sig_seek.emit)
        layout.addWidget(self.slider_progress)

        # Tiempos
        times = QHBoxLayout()
        self.lbl_current = QLabel("00:00:15")
        self.lbl_current.setProperty("time_label", "true")
        self.lbl_current.setStyleSheet(load_qss("panels"))
        self.lbl_duration = QLabel("00:02:37")
        self.lbl_duration.setProperty("time_label", "true")
        self.lbl_duration.setStyleSheet(load_qss("panels"))
        times.addWidget(self.lbl_current)
        times.addStretch()
        times.addWidget(self.lbl_duration)
        layout.addLayout(times)

        layout.addWidget(self._build_player_controls())
        return panel

    def _build_player_controls(self) -> QWidget:
        bar = QWidget()
        bar.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.btn_play  = PlayerControlBtn("▶")
        self.btn_pause = PlayerControlBtn("⏸")
        self.btn_stop  = PlayerControlBtn("⏹")
        self.btn_play.clicked.connect(self.sig_play.emit)
        self.btn_pause.clicked.connect(self.sig_pause.emit)
        self.btn_stop.clicked.connect(self.sig_stop.emit)

        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_stop)

        self.cmb_speed = QComboBox()
        self.cmb_speed.setObjectName("cmb_speed")
        self.cmb_speed.addItems(["0.5x", "1.00x", "1.5x", "2.0x"])
        self.cmb_speed.setCurrentIndex(1)
        self.cmb_speed.setFixedWidth(72)
        self.cmb_speed.setStyleSheet(load_qss("player"))
        self.cmb_speed.currentTextChanged.connect(self.sig_speed_change.emit)
        layout.addWidget(self.cmb_speed)

        layout.addStretch()

        self.btn_screenshot = PlayerControlBtn("📷")
        self.btn_record     = PlayerControlBtn("⏺")
        self.btn_fullscreen = PlayerControlBtn("⤢")
        self.btn_screenshot.clicked.connect(self.sig_captura.emit)
        self.btn_record.clicked.connect(self.sig_grabar.emit)
        self.btn_fullscreen.clicked.connect(self.sig_fullscreen.emit)
        layout.addWidget(self.btn_screenshot)
        layout.addWidget(self.btn_record)
        layout.addWidget(self.btn_fullscreen)

        # Volumen
        lbl_vol = QLabel("🔊")
        lbl_vol.setStyleSheet(f"color: {Theme.TEXT_SECOND}; font-size: 14px;")
        self.slider_vol = QSlider(Qt.Orientation.Horizontal)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(70)
        self.slider_vol.setFixedWidth(70)
        self.slider_vol.valueChanged.connect(self.sig_volume.emit)
        layout.addWidget(lbl_vol)
        layout.addWidget(self.slider_vol)

        return bar

    # ── Capturas ────────────────────────────────────────────────────────
    def _build_captures_panel(self) -> QWidget:
        panel = QWidget()
        panel.setProperty("panel", "true")
        panel.setStyleSheet(load_qss("panels"))

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        hdr = QHBoxLayout()
        hdr.addWidget(SectionLabel("📷", "CAPTURAS DEL VIDEO"))
        hdr.addStretch()
        layout.addLayout(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        grid = QGridLayout(container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(8)

        timestamps = [
            "08:15:32", "08:15:40", "08:15:48", "08:16:02", "08:16:15",
            "08:16:28", "08:16:40", "08:16:55", "08:17:05", "08:17:20",
        ]
        self.thumbnails: list[ThumbnailWidget] = []
        for idx, ts in enumerate(timestamps):
            thumb = ThumbnailWidget(ts, active=(idx == 0))
            self.thumbnails.append(thumb)
            grid.addWidget(thumb, idx // 5, idx % 5)

        scroll.setWidget(container)
        layout.addWidget(scroll)
        return panel

    # ════════════════════════════════════════════════════════════════════
    #  SLOTS INTERNOS
    # ════════════════════════════════════════════════════════════════════

    def _on_ver_video(self, row: int):
        self.table.selectRow(row)
        self.sig_ver_video.emit(row)

    def _on_delete_video(self, row: int):
        self.table.selectRow(row)
        self.sig_eliminar_video.emit(row)

    # ════════════════════════════════════════════════════════════════════
    #  API PÚBLICA — métodos llamados por el Controlador
    # ════════════════════════════════════════════════════════════════════

    def set_camera_label(self, text: str):
        """Actualiza el label de la cámara activa en el reproductor."""
        self.lbl_cam_active.setText(text)
        self._overlay_cam.setText(text.split(" - ")[0] if " - " in text else text)
        self._overlay_cam.adjustSize()

    def set_timestamp(self, ts: str):
        """Actualiza el overlay de timestamp del área de video."""
        self._overlay_ts.setText(ts)
        self._overlay_ts.adjustSize()

    def set_progress(self, value: int):
        """Mueve la barra de progreso sin emitir sig_seek (0–100)."""
        self.slider_progress.blockSignals(True)
        self.slider_progress.setValue(value)
        self.slider_progress.blockSignals(False)

    def set_current_time(self, time_str: str):
        self.lbl_current.setText(time_str)

    def set_duration(self, time_str: str):
        self.lbl_duration.setText(time_str)

    def update_table_data(self, cameras: list[dict]):
        if self.table.rowCount():
            self.table.setRowCount(0)
        """
        Recarga la tabla con datos del Modelo.

        Args:
            cameras: lista de dicts con claves:
                    num (int), nombre (str), hora (str), fecha (str)
        """
        self.table.setRowCount(len(cameras))

        for i, cam in enumerate(cameras):
            self.table.setRowHeight(i, 40)

            n = QTableWidgetItem(str(i + 1))
            n.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            n.setForeground(QColor(Theme.TEXT_SECOND))
            self.table.setItem(i, 0, n)

            nombre = QTableWidgetItem(cam.get("nombre", ""))
            self.table.setItem(i, 1, nombre)

            h = QTableWidgetItem(cam.get("hora", ""))
            h.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            h.setFont(QFont("Consolas", 11))
            self.table.setItem(i, 2, h)

            f = QTableWidgetItem(cam.get("fecha", ""))
            f.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, f)

            self.table.setCellWidget(
                i,
                4,
                self._create_actions_buttons_cell(i, active=(i == 0))
            )

        if cameras:
            self.table.selectRow(0)

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



