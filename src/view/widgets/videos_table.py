from PySide6.QtWidgets import (
 QTableWidget,
    QHeaderView, QAbstractItemView, QTableWidgetItem, QWidget,QHBoxLayout

)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from . import ActionButton
from ...styles import Theme




class VideosTable(QTableWidget):
        
        sig_ordenar_por_hora = Signal()
        sig_ver_video = Signal(int)
        sig_eliminar_video = Signal(int)

        def __init__(self):
            super().__init__()
            self._build()


        def _build(self):
            self.setColumnCount(5)
            self.setHorizontalHeaderLabels(["N°", "CÁMARA", "HORA", "FECHA", "ACCIÓN"])

            hh = self.horizontalHeader()
            hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            hh.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            hh.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)

            hh.sectionClicked.connect(self._on_header_clicked)

            self.setColumnWidth(0, 48)
            self.setColumnWidth(2, 90)
            self.setColumnWidth(3, 110)
            self.setColumnWidth(4, 110)

            self.verticalHeader().setVisible(False)
            self.setShowGrid(False)
            self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            self.setRowCount(0)

        # ── Actualizar tabla ────────────────────────────────────────────────────────
        def update_table_data(self, cameras: list[dict]):
            if self.rowCount():
                self.setRowCount(0)
            """
            Recarga la tabla con datos del Modelo.

            Args:
                cameras: lista de dicts con claves:
                        num (int), nombre (str), hora (str), fecha (str)
            """
            self.setRowCount(len(cameras))

            for i, cam in enumerate(cameras):
                self.setRowHeight(i, 40)

                n = QTableWidgetItem(str(i + 1))
                n.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                n.setForeground(QColor(Theme.TEXT_SECOND))
                self.setItem(i, 0, n)

                nombre = QTableWidgetItem(cam.get("nombre", ""))
                self.setItem(i, 1, nombre)

                h = QTableWidgetItem(cam.get("hora", ""))
                h.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                h.setFont(QFont("Consolas", 11))
                self.setItem(i, 2, h)

                f = QTableWidgetItem(cam.get("fecha", ""))
                f.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(i, 3, f)

                self.setCellWidget(
                    i,
                    4,
                    self._create_actions_buttons_cell(i)
                )

        #   crear botones play y eliminar en tabla
        def _create_actions_buttons_cell(self, row: int) -> QWidget:
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
        
        # ════════════════════════════════════════════════════════════════════
        #  Funciones tabla
        # ════════════════════════════════════════════════════════════════════

        # ── Reproducir fila ────────────────────────────────────────────────────────
        def _on_ver_video(self, row: int):
            self.selectRow(row)
            self.sig_ver_video.emit(row)

        # ── Eliminar fila ────────────────────────────────────────────────────────
        def _on_delete_video(self, row: int):
            self.selectRow(row)
            self.sig_eliminar_video.emit(row)

        # ── Ordenar tabla por hora y fecha ────────────────────────────────────────────────────────
        def _on_header_clicked(self, column: int):
            if column == 2:  # Columna HORA
                self.sig_ordenar_por_hora.emit()