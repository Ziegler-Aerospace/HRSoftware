from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence

class CustomTableView(QTableView):
    calculateHours = pyqtSignal()

    def __init__(self, parent=None):
        super(CustomTableView, self).__init__(parent)
        self.setEditTriggers(QTableView.NoEditTriggers)  # Disable default edit triggers

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and (event.modifiers() & Qt.ControlModifier):
            index = self.currentIndex()
            current_text = self.model().data(index, Qt.EditRole)
            self.model().setData(index, current_text + '\n', Qt.EditRole)
        elif event.key() == Qt.Key_Return and not event.modifiers():
            self.calculateHours.emit()  # Emit signal when Enter is pressed without modifiers
        else:
            super(CustomTableView, self).keyPressEvent(event)
