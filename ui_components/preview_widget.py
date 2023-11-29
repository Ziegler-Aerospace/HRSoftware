from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd
from .custom_table_view import CustomTableView

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None
    
    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

class PreviewWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Changed from QTableView to CustomTableView
        self.tableView = CustomTableView(self)
        self.layout.addWidget(self.tableView)

    def load_data(self, file_path):
        data = pd.read_excel(file_path)  # Use pandas to load data
        self.model = TableModel(data)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()  # Adjust columns to fit content
        self.tableView.resizeRowsToContents()  # Adjust rows to fit content
