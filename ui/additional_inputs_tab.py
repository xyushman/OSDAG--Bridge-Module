from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AdditionalInputsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Additional Inputs (Not fully implemented but present)"))
        layout.addStretch()
