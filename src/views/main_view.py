from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame,
    QTreeWidget, QTreeWidgetItem,
    QMenu, QAbstractItemView, QHeaderView,QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCursor
from .styles.styles import  *

class MainView(QMainWindow):

    def __init__(self, video_service, controller = None):
        super().__init__()

        self.video_service = video_service
        self.controller = controller

        self.setWindowTitle("FOLDER LISTER")
        self.resize(900, 700)
        with open("src/views/styles/main.qss", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        self.layout = QVBoxLayout(central)
        self.layout.setContentsMargins(16, 14, 16, 14)
        self.layout.setSpacing(0)

        self._build_menu()
        self._build_header()
        self._build_tree()
        self._build_button_bar()

    # ------------------------------------------------------------------

    def _build_menu(self):
        menu = self.menuBar().addMenu("Archivo")

        importar = QAction("Importar videos", self)
        importar.triggered.connect(self.seleccionar_carpeta)
        menu.addAction(importar)

        menu.addSeparator()

        salir = QAction("Salir", self)
        salir.triggered.connect(self.close)
        menu.addAction(salir)

    # ------------------------------------------------------------------

    def _build_header(self):

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 8)

        punto = QLabel("●")
        punto.setStyleSheet(
            f"color:{ACCENT};font-family:Courier;font-size:10px;"
        )

        titulo = QLabel("  FOLDER LISTER")
        titulo.setStyleSheet(
            f"""
            color:{TEXT_PRIMARY};
            font-family:Courier;
            font-size:12px;
            font-weight:bold;
            """
        )

        layout.addWidget(punto)
        layout.addWidget(titulo)
        layout.addStretch()

        self.layout.addWidget(widget)

        linea = QFrame()
        linea.setObjectName("separator")
        linea.setFrameShape(QFrame.HLine)
        linea.setFixedHeight(1)

        self.layout.addWidget(linea)



       

    # ------------------------------------------------------------------

    def _build_tree(self):

        borde = QFrame()
        borde.setStyleSheet(
            f"background:{BORDER};border-radius:6px;"
        )

        layout = QVBoxLayout(borde)
        layout.setContentsMargins(1, 1, 1, 1)

        self.tree = QTreeWidget()

        self.tree.setColumnCount(4)
        self.tree.setHeaderLabels([
            "N°",
            "CÁMARA",
            "HORA",
            "FECHA"
        ])

        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree.setRootIsDecorated(False)

        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

        self.tree.setColumnWidth(0, 50)
        self.tree.setColumnWidth(2, 110)
        self.tree.setColumnWidth(3, 120)

        layout.addWidget(self.tree)

        self.layout.addSpacing(12)
        self.layout.addWidget(borde)

    # ------------------------------------------------------------------

    def _build_button_bar(self):

        widget = QWidget()

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)

        self.btn_guardar = QPushButton("Guardar carpeta CCTV")
        self.btn_guardar.setObjectName("btn_confirmar")
        self.btn_guardar.setEnabled(False)

        layout.addWidget(self.btn_guardar)
        layout.addStretch()

        self.layout.addWidget(widget)

    # ------------------------------------------------------------------

    def set_ruta_destino(self, ruta: str):
        self.entry_ruta.setText(ruta)

    # ------------------------------------------------------------------

    def cargar_camaras(self, videos):

        self.tree.clear()

        for i, video in enumerate(videos, start=1):

            item = QTreeWidgetItem([
                str(i),
                video.nombre,
                video.hora,
                video.fecha,
            ])

            item.setTextAlignment(0, Qt.AlignCenter)
            item.setTextAlignment(2, Qt.AlignCenter)
            item.setTextAlignment(3, Qt.AlignCenter)

            self.tree.addTopLevelItem(item)

    def seleccionar_carpeta(self):
        directorio = QFileDialog.getExistingDirectory(
                    self,
                    "Seleccionar carpeta de videos",
                    "C:/"
                )
        
        videos = self.controller.seleccionar_directorio(directorio)
        self.cargar_camaras(videos)