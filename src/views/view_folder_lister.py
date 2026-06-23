"""
VIEW - Folder Lister CCTV
Módulo de vista MVC para la aplicación de gestión de cámaras CCTV.
Diseñado con PySide6, fiel al diseño de la imagen de referencia.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QSlider, QSizePolicy, QScrollArea,
    QGridLayout, QStackedWidget, QComboBox, QSpacerItem,
    QAbstractItemView, QMenuBar, QMenu, QApplication,
    QToolButton, QButtonGroup
)
from PySide6.QtCore import (
    Qt, Signal, QSize, QTimer, QTime
)
from PySide6.QtGui import (
    QColor, QPalette, QFont, QIcon, QPixmap, QPainter,
    QAction, QFontDatabase
)


# ─────────────────────────── PALETA DE COLORES ───────────────────────────
class Theme:
    BG_DARK      = "#0d0d0d"
    BG_PANEL     = "#111111"
    BG_TABLE     = "#131313"
    BG_ROW_ALT   = "#161616"
    BG_ROW_SEL   = "#1a3a6e"
    BG_HEADER    = "#0d0d0d"
    BG_TOOLBAR   = "#0d0d0d"
    BG_CARD      = "#1a1a1a"

    ACCENT_BLUE  = "#2563eb"
    ACCENT_HOVER = "#1d4ed8"
    BORDER_BLUE  = "#2563eb"
    BORDER_DIM   = "#2a2a2a"

    TEXT_PRIMARY = "#e5e5e5"
    TEXT_SECOND  = "#9ca3af"
    TEXT_ACCENT  = "#3b82f6"
    TEXT_HEADER  = "#6b7280"

    BTN_OUTLINE  = "#1e293b"
    BTN_OUTLINE_BORDER = "#2563eb"

    SLIDER_TRACK = "#2563eb"
    SLIDER_BG    = "#374151"

    STATUS_DOT   = "#3b82f6"

    MONO_FONT    = "Consolas, 'Courier New', monospace"


# ─────────────────────────── ESTILOS GLOBALES ────────────────────────────
GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {Theme.BG_DARK};
    color: {Theme.TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
}}

QMenuBar {{
    background-color: {Theme.BG_DARK};
    color: {Theme.TEXT_PRIMARY};
    border-bottom: 1px solid {Theme.BORDER_DIM};
    padding: 2px 6px;
}}
QMenuBar::item:selected {{
    background-color: {Theme.BG_CARD};
    border-radius: 4px;
}}
QMenu {{
    background-color: {Theme.BG_CARD};
    color: {Theme.TEXT_PRIMARY};
    border: 1px solid {Theme.BORDER_DIM};
}}
QMenu::item:selected {{
    background-color: {Theme.ACCENT_BLUE};
}}

QTableWidget {{
    background-color: {Theme.BG_TABLE};
    gridline-color: {Theme.BORDER_DIM};
    border: none;
    outline: none;
    selection-background-color: {Theme.BG_ROW_SEL};
    selection-color: {Theme.TEXT_PRIMARY};
}}
QTableWidget::item {{
    padding: 6px 10px;
    border-bottom: 1px solid {Theme.BORDER_DIM};
}}
QTableWidget::item:selected {{
    background-color: {Theme.BG_ROW_SEL};
    color: {Theme.TEXT_PRIMARY};
}}
QHeaderView::section {{
    background-color: {Theme.BG_HEADER};
    color: {Theme.TEXT_HEADER};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 8px 10px;
    border: none;
    border-bottom: 1px solid {Theme.BORDER_DIM};
    text-transform: uppercase;
}}

QScrollBar:vertical {{
    background: {Theme.BG_DARK};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: #374151;
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background: {Theme.BG_DARK};
    height: 6px;
}}
QScrollBar::handle:horizontal {{
    background: #374151;
    border-radius: 3px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QSlider::groove:horizontal {{
    height: 4px;
    background: {Theme.SLIDER_BG};
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {Theme.SLIDER_TRACK};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: white;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}

QLabel {{
    background: transparent;
}}
"""


# ─────────────────────────── WIDGETS AUXILIARES ──────────────────────────

class NavButton(QPushButton):
    """Botón de navegación superior (VIDEOS / DIAPOSITIVAS)."""
    def __init__(self, text: str, icon_char: str = "", active: bool = False, parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_char}  {text}" if icon_char else text)
        self.setCheckable(True)
        self.setChecked(active)
        self.setFixedHeight(36)
        self.setMinimumWidth(150)
        self._apply_style()
        self.toggled.connect(self._apply_style)

    def _apply_style(self):
        if self.isChecked():
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Theme.TEXT_PRIMARY};
                    border: 1px solid {Theme.BORDER_BLUE};
                    border-radius: 6px;
                    padding: 0 20px;
                    font-size: 13px;
                    font-weight: 500;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Theme.TEXT_SECOND};
                    border: 1px solid transparent;
                    border-radius: 6px;
                    padding: 0 20px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    color: {Theme.TEXT_PRIMARY};
                    border: 1px solid {Theme.BORDER_DIM};
                }}
            """)


class VideoButton(QPushButton):
    """Botón 'Ver video' de la tabla."""
    def __init__(self, active: bool = False, parent=None):
        super().__init__("Ver video", parent)
        self.setFixedSize(90, 28)
        if active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Theme.ACCENT_BLUE};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 500;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Theme.TEXT_PRIMARY};
                    border: 1px solid {Theme.BORDER_BLUE};
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {Theme.ACCENT_BLUE};
                    color: white;
                }}
            """)


class PaginationButton(QPushButton):
    def __init__(self, text: str, active: bool = False, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(32, 32)
        self.setCheckable(True)
        self.setChecked(active)
        self._apply_style()
        self.toggled.connect(self._apply_style)

    def _apply_style(self):
        if self.isChecked():
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Theme.ACCENT_BLUE};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Theme.TEXT_SECOND};
                    border: 1px solid {Theme.BORDER_DIM};
                    border-radius: 6px;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    color: {Theme.TEXT_PRIMARY};
                    border-color: {Theme.ACCENT_BLUE};
                }}
            """)


class ArrowButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(32, 32)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.TEXT_SECOND};
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 6px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {Theme.TEXT_PRIMARY};
                border-color: {Theme.ACCENT_BLUE};
            }}
        """)


class PlayerControlBtn(QPushButton):
    """Botón de control del reproductor."""
    def __init__(self, symbol: str, size: int = 36, parent=None):
        super().__init__(symbol, parent)
        self.setFixedSize(size, size)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 6px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {Theme.ACCENT_BLUE};
                border-color: {Theme.ACCENT_BLUE};
            }}
        """)


class SectionLabel(QLabel):
    """Etiqueta de sección con ícono."""
    def __init__(self, icon: str, text: str, parent=None):
        super().__init__(parent)
        self.setText(f"  {icon}  {text}")
        self.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.08em;
            }}
        """)


class ThumbnailWidget(QFrame):
    """Miniatura de captura con timestamp."""
    def __init__(self, timestamp: str, active: bool = False, parent=None):
        super().__init__(parent)
        self.setFixedSize(116, 90)
        border_color = Theme.ACCENT_BLUE if active else Theme.BORDER_DIM
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1c2231;
                border: 2px solid {border_color};
                border-radius: 4px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Área de imagen simulada
        img_area = QLabel()
        img_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_area.setStyleSheet("border: none; background-color: #1c2a3a;")
        img_area.setText("▪")
        img_area.setStyleSheet(f"color: {Theme.TEXT_SECOND}; font-size: 20px; border: none; background: #1c2a3a;")
        img_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        ts_label = QLabel(timestamp)
        ts_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ts_label.setFixedHeight(20)
        ts_label.setStyleSheet(f"""
            QLabel {{
                background-color: #0d1117;
                color: {Theme.TEXT_PRIMARY};
                font-size: 10px;
                font-family: 'Consolas', monospace;
                border: none;
                border-top: 1px solid {Theme.BORDER_DIM};
            }}
        """)

        layout.addWidget(img_area)
        layout.addWidget(ts_label)


# ─────────────────────────── VISTA PRINCIPAL ─────────────────────────────

class FolderListerView(QMainWindow):
    """
    Vista principal del sistema Folder Lister CCTV (MVC).
    Emite señales para que el Controlador las conecte.
    """

    # Señales para el controlador
    sig_ver_video    = Signal(int)          # fila seleccionada
    sig_guardar      = Signal()
    sig_pagina       = Signal(int)
    sig_nav_videos   = Signal()
    sig_nav_diapositivas = Signal()
    sig_play         = Signal()
    sig_pause        = Signal()
    sig_stop         = Signal()
    sig_captura      = Signal()
    sig_grabar       = Signal()
    sig_fullscreen   = Signal()
    sig_speed_change = Signal(str)
    sig_seek         = Signal(int)          # posición slider (0-100)
    sig_volume       = Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOLDER LISTER")
        self.setMinimumSize(1200, 820)
        self.resize(1340, 860)
        self.setStyleSheet(GLOBAL_STYLE)
        self._build_ui()

    # ──────────────────────── CONSTRUCCIÓN UI ────────────────────────────

    def _build_ui(self):
        # Barra de menú
        self._build_menubar()

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Toolbar superior
        root.addWidget(self._build_toolbar())

        # Separador
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {Theme.BORDER_DIM};")
        root.addWidget(sep)

        # Contenido principal (dos columnas)
        content = QWidget()
        content.setStyleSheet(f"background-color: {Theme.BG_DARK};")
        h_layout = QHBoxLayout(content)
        h_layout.setContentsMargins(16, 16, 16, 16)
        h_layout.setSpacing(16)

        # Columna izquierda
        left_col = self._build_left_column()
        h_layout.addWidget(left_col, stretch=5)

        # Columna derecha
        right_col = self._build_right_column()
        h_layout.addWidget(right_col, stretch=4)

        root.addWidget(content, stretch=1)

    def _build_menubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        archivo_menu = menubar.addMenu("Archivo  ▾")
        archivo_menu.addAction(QAction("Abrir carpeta", self))
        archivo_menu.addAction(QAction("Guardar carpeta CCTV", self))
        archivo_menu.addSeparator()
        archivo_menu.addAction(QAction("Salir", self))

    def _build_toolbar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(56)
        bar.setStyleSheet(f"background-color: {Theme.BG_TOOLBAR};")

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 8, 16, 8)

        # Logo / título
        title_lbl = QLabel("● FOLDER LISTER")
        title_lbl.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_PRIMARY};
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.12em;
                font-family: 'Consolas', monospace;
            }}
        """)
        layout.addWidget(title_lbl)
        layout.addStretch()

        # Botones de navegación central
        btn_group = QButtonGroup(self)
        btn_group.setExclusive(True)

        self.btn_videos = NavButton("VIDEOS", "⬜", active=True)
        self.btn_diapositivas = NavButton("DIAPOSITIVAS", "🖥")
        btn_group.addButton(self.btn_videos)
        btn_group.addButton(self.btn_diapositivas)

        self.btn_videos.toggled.connect(lambda c: self.sig_nav_videos.emit() if c else None)
        self.btn_diapositivas.toggled.connect(lambda c: self.sig_nav_diapositivas.emit() if c else None)

        center = QHBoxLayout()
        center.setSpacing(8)
        center.addWidget(self.btn_videos)
        center.addWidget(self.btn_diapositivas)
        layout.addLayout(center)

        layout.addStretch()

        # Botón configuración
        btn_settings = QPushButton("⚙")
        btn_settings.setFixedSize(36, 36)
        btn_settings.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {Theme.TEXT_SECOND};
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 6px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                color: {Theme.TEXT_PRIMARY};
                border-color: {Theme.ACCENT_BLUE};
            }}
        """)
        layout.addWidget(btn_settings)

        return bar

    # ──────────── COLUMNA IZQUIERDA ─────────────

    def _build_left_column(self) -> QWidget:
        col = QWidget()
        col.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_PANEL};
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header de sección
        header = QWidget()
        header.setFixedHeight(44)
        header.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_HEADER};
                border-bottom: 1px solid {Theme.BORDER_DIM};
                border-radius: 8px 8px 0 0;
                border: none;
            }}
        """)
        h_lyt = QHBoxLayout(header)
        h_lyt.setContentsMargins(16, 0, 16, 0)

        dot = QLabel("●")
        dot.setStyleSheet(f"color: {Theme.STATUS_DOT}; font-size: 10px;")
        title = QLabel("FOLDER LISTER")
        title.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.1em;
            font-family: 'Consolas', monospace;
        """)
        h_lyt.addWidget(dot)
        h_lyt.addSpacing(6)
        h_lyt.addWidget(title)
        h_lyt.addStretch()

        layout.addWidget(header)

        # Tabla de cámaras
        self.table = self._build_table()
        layout.addWidget(self.table, stretch=1)

        # Paginación + botón guardar
        layout.addWidget(self._build_bottom_bar())

        return col

    def _build_table(self) -> QTableWidget:
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["N°", "CÁMARA", "HORA", "FECHA", "ACCIÓN"])
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(0, 48)
        table.setColumnWidth(2, 90)
        table.setColumnWidth(3, 110)
        table.setColumnWidth(4, 110)

        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setAlternatingRowColors(False)
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Theme.BG_TABLE};
                border: none;
                outline: none;
                selection-background-color: transparent;
            }}
            QTableWidget::item {{
                border-bottom: 1px solid {Theme.BORDER_DIM};
                padding: 4px 10px;
            }}
            QTableWidget::item:selected {{
                background-color: {Theme.BG_ROW_SEL};
                color: {Theme.TEXT_PRIMARY};
            }}
        """)

        # Datos de ejemplo
        cameras = [
            (1, "CAM 01 - Acceso Principal",   "08:15:32", "24/05/2025"),
            (2, "CAM 02 - Estacionamiento",     "08:16:10", "24/05/2025"),
            (3, "CAM 03 - Pasillo Norte",       "08:17:05", "24/05/2025"),
            (4, "CAM 04 - Recepción",           "08:18:22", "24/05/2025"),
            (5, "CAM 05 - Almacén",             "08:19:47", "24/05/2025"),
            (6, "CAM 06 - Pasillo Sur",         "08:20:13", "24/05/2025"),
            (7, "CAM 07 - Salida Emergencia",   "08:21:35", "24/05/2025"),
            (8, "CAM 08 - Patio Trasero",       "08:22:11", "24/05/2025"),
            (9, "CAM 09 - Ascensor",            "08:23:50", "24/05/2025"),
            (10,"CAM 10 - Laboratorio",         "08:24:33", "24/05/2025"),
            (11,"CAM 11 - Oficina 1",           "08:25:45", "24/05/2025"),
            (12,"CAM 12 - Oficina 2",           "08:26:30", "24/05/2025"),
        ]

        table.setRowCount(len(cameras))
        table.setRowHeight

        for i, (num, cam, hora, fecha) in enumerate(cameras):
            row_height = 40
            table.setRowHeight(i, row_height)
            is_active = (i == 0)

            # N°
            n_item = QTableWidgetItem(str(num))
            n_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            n_item.setForeground(QColor(Theme.TEXT_SECOND))
            table.setItem(i, 0, n_item)

            # Cámara
            cam_item = QTableWidgetItem(cam)
            cam_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            table.setItem(i, 1, cam_item)

            # Hora
            hora_item = QTableWidgetItem(hora)
            hora_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            hora_item.setFont(QFont("Consolas", 11))
            table.setItem(i, 2, hora_item)

            # Fecha
            fecha_item = QTableWidgetItem(fecha)
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 3, fecha_item)

            # Acción (botón)
            btn_widget = QWidget()
            btn_widget.setStyleSheet("background: transparent;")
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(8, 4, 8, 4)
            btn = VideoButton(active=is_active)
            row_index = i
            btn.clicked.connect(lambda _, r=row_index: self._on_ver_video(r))
            btn_layout.addWidget(btn)
            table.setCellWidget(i, 4, btn_widget)

            # Highlight primera fila
            if is_active:
                for col in range(4):
                    item = table.item(i, col)
                    if item:
                        item.setBackground(QColor(Theme.BG_ROW_SEL))

        table.selectRow(0)
        return table

    def _build_bottom_bar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(60)
        bar.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_PANEL};
                border-top: 1px solid {Theme.BORDER_DIM};
                border-radius: 0 0 8px 8px;
            }}
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(6)

        # Flechas paginación
        self.btn_prev = ArrowButton("‹")
        layout.addWidget(self.btn_prev)

        # Botones de página
        self.page_buttons = []
        self.page_btn_group = QButtonGroup(self)
        self.page_btn_group.setExclusive(True)

        for p in range(1, 6):
            pb = PaginationButton(str(p), active=(p == 1))
            self.page_btn_group.addButton(pb)
            self.page_buttons.append(pb)
            pb.clicked.connect(lambda _, pg=p: self.sig_pagina.emit(pg))
            layout.addWidget(pb)

        self.btn_next = ArrowButton("›")
        layout.addWidget(self.btn_next)

        layout.addStretch()

        # Botón guardar
        self.btn_guardar = QPushButton("  Guardar carpeta CCTV")
        self.btn_guardar.setFixedHeight(38)
        self.btn_guardar.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.ACCENT_BLUE};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: {Theme.ACCENT_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #1e40af;
            }}
        """)
        self.btn_guardar.clicked.connect(self.sig_guardar.emit)
        layout.addWidget(self.btn_guardar)

        return bar

    # ──────────── COLUMNA DERECHA ─────────────

    def _build_right_column(self) -> QWidget:
        col = QWidget()
        col.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(col)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Panel reproductor
        layout.addWidget(self._build_player_panel(), stretch=3)

        # Panel capturas
        layout.addWidget(self._build_captures_panel(), stretch=2)

        return col

    def _build_player_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_PANEL};
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        # Header del reproductor
        hdr = QHBoxLayout()
        sec_lbl = SectionLabel("▶", "REPRODUCTOR")
        cam_lbl = QLabel("CAM 01 - Acceso Principal")
        cam_lbl.setStyleSheet(f"color: {Theme.TEXT_ACCENT}; font-size: 12px; font-weight: 500;")
        hdr.addWidget(sec_lbl)
        hdr.addStretch()
        hdr.addWidget(cam_lbl)
        layout.addLayout(hdr)

        # Área de video
        self.video_area = QLabel()
        self.video_area.setMinimumHeight(230)
        self.video_area.setStyleSheet(f"""
            QLabel {{
                background-color: #0a0f1a;
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 4px;
                color: {Theme.TEXT_SECOND};
            }}
        """)
        self.video_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Timestamp overlay
        self._timestamp_overlay = QLabel("24/05/2025  08:15:32", self.video_area)
        self._timestamp_overlay.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(0,0,0,0.65);
                color: white;
                font-size: 11px;
                font-family: 'Consolas', monospace;
                padding: 2px 8px;
                border-radius: 3px;
                border: none;
            }}
        """)
        self._timestamp_overlay.move(8, 8)
        self._timestamp_overlay.adjustSize()

        # Etiqueta CAM
        self._cam_overlay = QLabel("CAM 01", self.video_area)
        self._cam_overlay.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(0,0,0,0.65);
                color: white;
                font-size: 11px;
                font-family: 'Consolas', monospace;
                padding: 2px 8px;
                border-radius: 3px;
                border: none;
            }}
        """)
        self._cam_overlay.adjustSize()

        layout.addWidget(self.video_area)

        # Slider de progreso
        progress_row = QHBoxLayout()
        self.slider_progress = QSlider(Qt.Orientation.Horizontal)
        self.slider_progress.setRange(0, 100)
        self.slider_progress.setValue(10)
        self.slider_progress.valueChanged.connect(self.sig_seek.emit)
        progress_row.addWidget(self.slider_progress)
        layout.addLayout(progress_row)

        # Tiempos
        times_row = QHBoxLayout()
        self.lbl_current = QLabel("00:00:15")
        self.lbl_current.setStyleSheet(f"color: {Theme.TEXT_SECOND}; font-size: 11px; font-family: Consolas;")
        self.lbl_duration = QLabel("00:02:37")
        self.lbl_duration.setStyleSheet(f"color: {Theme.TEXT_SECOND}; font-size: 11px; font-family: Consolas;")
        times_row.addWidget(self.lbl_current)
        times_row.addStretch()
        times_row.addWidget(self.lbl_duration)
        layout.addLayout(times_row)

        # Controles del reproductor
        layout.addWidget(self._build_player_controls())

        return panel

    def _build_player_controls(self) -> QWidget:
        bar = QWidget()
        bar.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.btn_play     = PlayerControlBtn("▶")
        self.btn_pause    = PlayerControlBtn("⏸")
        self.btn_stop     = PlayerControlBtn("⏹")

        self.btn_play.clicked.connect(self.sig_play.emit)
        self.btn_pause.clicked.connect(self.sig_pause.emit)
        self.btn_stop.clicked.connect(self.sig_stop.emit)

        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_stop)

        # Speed selector
        self.cmb_speed = QComboBox()
        self.cmb_speed.addItems(["0.5x", "1.00x", "1.5x", "2.0x"])
        self.cmb_speed.setCurrentIndex(1)
        self.cmb_speed.setFixedWidth(72)
        self.cmb_speed.setStyleSheet(f"""
            QComboBox {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 12px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 18px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Theme.BG_CARD};
                color: {Theme.TEXT_PRIMARY};
                selection-background-color: {Theme.ACCENT_BLUE};
                border: 1px solid {Theme.BORDER_DIM};
            }}
        """)
        self.cmb_speed.currentTextChanged.connect(self.sig_speed_change.emit)
        layout.addWidget(self.cmb_speed)

        layout.addStretch()

        # Botones adicionales
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
        vol_icon = QLabel("🔊")
        vol_icon.setStyleSheet(f"color: {Theme.TEXT_SECOND}; font-size: 14px;")
        self.slider_vol = QSlider(Qt.Orientation.Horizontal)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(70)
        self.slider_vol.setFixedWidth(70)
        self.slider_vol.valueChanged.connect(self.sig_volume.emit)

        layout.addWidget(vol_icon)
        layout.addWidget(self.slider_vol)

        return bar

    def _build_captures_panel(self) -> QWidget:
        panel = QWidget()
        panel.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_PANEL};
                border: 1px solid {Theme.BORDER_DIM};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        # Header
        hdr = QHBoxLayout()
        sec_lbl = SectionLabel("📷", "CAPTURAS DEL VIDEO")
        hdr.addWidget(sec_lbl)
        hdr.addStretch()
        layout.addLayout(hdr)

        # Grid de miniaturas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")

        thumb_container = QWidget()
        thumb_container.setStyleSheet("background: transparent;")
        grid = QGridLayout(thumb_container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(8)

        # Timestamps de ejemplo
        timestamps = [
            "08:15:32", "08:15:40", "08:15:48", "08:16:02", "08:16:15",
            "08:16:28", "08:16:40", "08:16:55", "08:17:05", "08:17:20",
        ]
        self.thumbnails = []
        for idx, ts in enumerate(timestamps):
            thumb = ThumbnailWidget(ts, active=(idx == 0))
            self.thumbnails.append(thumb)
            row = idx // 5
            col = idx % 5
            grid.addWidget(thumb, row, col)

        scroll.setWidget(thumb_container)
        layout.addWidget(scroll)

        return panel

    # ──────────────────────── SLOTS INTERNOS ─────────────────────────────

    def _on_ver_video(self, row: int):
        self.table.selectRow(row)
        self.sig_ver_video.emit(row)

    # ──────────────────────── API PÚBLICA (para el Controlador) ──────────

    def set_camera_label(self, text: str):
        """Actualiza la etiqueta de cámara en el reproductor."""
        pass  # Implementar con referencia al label

    def set_timestamp(self, ts: str):
        """Actualiza el timestamp del overlay del video."""
        self._timestamp_overlay.setText(ts)
        self._timestamp_overlay.adjustSize()

    def set_progress(self, value: int):
        """Actualiza el slider de progreso (0-100)."""
        self.slider_progress.blockSignals(True)
        self.slider_progress.setValue(value)
        self.slider_progress.blockSignals(False)

    def set_current_time(self, time_str: str):
        self.lbl_current.setText(time_str)

    def set_duration(self, time_str: str):
        self.lbl_duration.setText(time_str)

    def update_table_data(self, cameras: list[dict]):
        """
        Actualiza la tabla con datos del modelo.
        cameras: lista de dicts con keys: num, nombre, hora, fecha
        """
        self.table.setRowCount(len(cameras))
        for i, cam in enumerate(cameras):
            self.table.setRowHeight(i, 40)
            n_item = QTableWidgetItem(str(cam.get("num", i+1)))
            n_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, n_item)
            self.table.setItem(i, 1, QTableWidgetItem(cam.get("nombre", "")))
            hora_item = QTableWidgetItem(cam.get("hora", ""))
            hora_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 2, hora_item)
            fecha_item = QTableWidgetItem(cam.get("fecha", ""))
            fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 3, fecha_item)

    def set_active_page(self, page: int):
        for btn in self.page_buttons:
            btn.setChecked(btn.text() == str(page))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reposicionar overlay CAM en la esquina inferior izquierda del video
        if hasattr(self, '_cam_overlay') and hasattr(self, 'video_area'):
            va = self.video_area
            h = va.height()
            self._cam_overlay.move(8, h - self._cam_overlay.height() - 8)


# ─────────────────────────── PUNTO DE ENTRADA ────────────────────────────

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Paleta oscura base
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(Theme.BG_DARK))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base, QColor(Theme.BG_TABLE))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Theme.BG_ROW_ALT))
    palette.setColor(QPalette.ColorRole.Text, QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button, QColor(Theme.BG_CARD))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Theme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Theme.ACCENT_BLUE))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = FolderListerView()
    window.show()
    sys.exit(app.exec())