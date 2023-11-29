import os
import tempfile
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QInputDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from .preview_widget import PreviewWidget
from data_processing.excel_reader import read_excel
from data_processing.time_calculator import calculate_hours

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Work Management Application")
        self.setGeometry(100, 100, 800, 600)  # Adjust size as needed

        # Set the window icon
        self.setWindowIcon(QIcon('../ziegler_aerospace_logo.png'))  # Update with your image path
        self.initUI()
        self.calculate_button = None

    def initUI(self):
        # Main layout
        self.layout = QVBoxLayout()

        # Load and display image
        self.image_label = QLabel(self)
        pixmap = QPixmap('../ziegler_aerospace_logo.png')  # Update with your image path
        self.image_label.setPixmap(pixmap)
        self.layout.addWidget(self.image_label)

        # Button to load Excel/CSV file
        self.load_button = QPushButton('Load Excel/CSV File', self)
        self.load_button.clicked.connect(self.loadFile)
        self.layout.addWidget(self.load_button)

        # Placeholder for the PreviewWidget
        self.preview_widget = PreviewWidget(self)
        self.layout.addWidget(self.preview_widget)

        # Set the layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def loadFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Excel Files (*.xlsx);;CSV Files (*.csv);;old Excel file types (*.xls)", options=options)
        if file_name:
            self.preview_widget.load_data(file_name)
            self.show_calculate_button()

    def show_calculate_button(self):
        if not self.calculate_button:
            self.calculate_button = QPushButton('Calculate Hours Worked', self)
            self.calculate_button.clicked.connect(self.calculate_hours)
            self.layout.insertWidget(1, self.calculate_button)
            self.load_button.setFixedWidth(self.load_button.sizeHint().width() / 2)

    def calculate_hours(self):
    # Step 1: Collect the data from the TableModel
        current_data = self.preview_widget.model._data

        # Step 2: Save the data to a temporary Excel file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            current_data.to_excel(tmp.name, index=False)
            tmp_path = tmp.name  # Keep the temp file path

        # Step 3: Call read_excel from data_processing.excel_reader
        processed_data = read_excel(tmp_path)

        # Prompt user to enter the number of Public Holidays
        num_ph, okPressed = QInputDialog.getInt(self, "Enter Public Holidays","Number of Public Holidays:", 0, 0, 100, 1)
        if okPressed:
            # Step 4: Call calculate_hours from data_processing.time_calculator
            calculated_df = calculate_hours(processed_data, num_ph)

            # Step 5: Prompt the user for a location to save the final Excel file
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"Save Calculated Hours","","Excel Files (*.xlsx);;All Files (*)", options=options)
            if fileName:
                # Step 6: Save the final DataFrame to the chosen location
                calculated_df.to_excel(fileName, index=False)
                QMessageBox.information(self, 'Saved', f'The calculated data has been saved to {fileName}', QMessageBox.Ok)

        # Cleanup: Delete the temporary file
        os.unlink(tmp_path)