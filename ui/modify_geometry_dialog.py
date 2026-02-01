from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton, 
                             QMessageBox, QVBoxLayout, QLabel)
from utils.geometry_calculator import calculate_girders, calculate_spacing

class ModifyGeometryDialog(QDialog):
    def __init__(self, carriageway_width, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modify Additional Geometry")
        self.resize(350, 250)
        self.cw = carriageway_width
        self.overall_width = self.cw + 5.0  # Rule: Width = CW + 5m
        
        self.layout = QVBoxLayout(self)
        
        # Info
        info_label = QLabel(f"Overall Width: {self.overall_width:.2f} m\n(Carriageway + 5m)")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(info_label)
        
        form_layout = QFormLayout()
        
        self.inp_spacing = QLineEdit()
        self.inp_girders = QLineEdit()
        self.inp_overhang = QLineEdit()
        
        form_layout.addRow("Girder Spacing (m):", self.inp_spacing)
        form_layout.addRow("No. of Girders:", self.inp_girders)
        form_layout.addRow("Deck Overhang Width (m):", self.inp_overhang)
        
        self.layout.addLayout(form_layout)
        
        # Initial Values
        self.inp_girders.setText("4")
        self.inp_overhang.setText("1.0")
        # Calc initial spacing
        s = calculate_spacing(self.overall_width, 4, 1.0)
        self.inp_spacing.setText(f"{s:.2f}")
        
        # Signals
        self.inp_spacing.editingFinished.connect(self.on_spacing_changed)
        self.inp_girders.editingFinished.connect(self.on_girders_changed)
        self.inp_overhang.editingFinished.connect(self.on_overhang_changed)
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        self.layout.addWidget(btn_close)

    def on_spacing_changed(self):
        # If spacing changes -> update girders
        try:
            S = float(self.inp_spacing.text())
            O = float(self.inp_overhang.text())
            if S <= 0: return
            
            # Recalc Girders
            N = calculate_girders(self.overall_width, S, O)
            self.inp_girders.setText(str(N))
            
        except ValueError:
            pass

    def on_girders_changed(self):
        # If girders changes -> update spacing
        try:
            N = int(self.inp_girders.text())
            O = float(self.inp_overhang.text())
            if N <= 0: return
            
            S = calculate_spacing(self.overall_width, N, O)
            self.inp_spacing.setText(f"{S:.2f}")
            
        except ValueError:
            pass

    def on_overhang_changed(self):
        # If overhang changes -> update both
        # Logic: 1. Calc closest Girders (N), 2. Calc exact Spacing (S) for that N
        try:
            O = float(self.inp_overhang.text())
            try:
                S_old = float(self.inp_spacing.text())
            except ValueError:
                S_old = 1.0 # default
                
            # 1. Update Girders based on old spacing and new overhang
            N = calculate_girders(self.overall_width, S_old, O)
            if N <= 0: N = 1 # Avoid div by zero
            self.inp_girders.setText(str(N))
            
            # 2. Update Spacing to fit exactly
            S_new = calculate_spacing(self.overall_width, N, O)
            self.inp_spacing.setText(f"{S_new:.2f}")
            
        except ValueError:
            pass
