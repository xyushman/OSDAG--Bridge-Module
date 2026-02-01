from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QGroupBox, QFormLayout, QRadioButton, QButtonGroup, 
                             QCheckBox, QPushButton, QLineEdit, QHBoxLayout, QMessageBox, QDialog)
from PyQt6.QtCore import Qt
import json
import os
from .modify_geometry_dialog import ModifyGeometryDialog
from utils.validators import validate_span, validate_carriageway, validate_skew

class BasicInputsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Load Data
        self.state_data = self.load_state_data()
        
        # 1. Structure Type
        self.create_structure_section()
        
        # 2. Project Location
        self.create_location_section()
        
        # 3. Geometric Inputs
        self.create_geometry_section()
        
        # 4. Material Inputs
        self.create_material_section()
        
        self.layout.addStretch()

    def load_state_data(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "india_data.json")
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def create_structure_section(self):
        group = QGroupBox("1. Type of Structure")
        layout = QFormLayout()
        
        self.structure_combo = QComboBox()
        self.structure_combo.addItems(["Highway", "Other"])
        self.structure_combo.currentTextChanged.connect(self.on_structure_changed)
        
        self.other_label = QLabel("Other structures not included.")
        self.other_label.setStyleSheet("color: red; font-weight: bold;")
        self.other_label.setVisible(False)
        
        layout.addRow("Select Type:", self.structure_combo)
        layout.addRow(self.other_label)
        group.setLayout(layout)
        self.layout.addWidget(group)

    def create_location_section(self):
        group = QGroupBox("2. Project Location")
        layout = QVBoxLayout()
        
        # Mode Selection
        mode_layout = QHBoxLayout()
        self.mode_group = QButtonGroup(self)
        self.radio_city = QRadioButton("Select Location")
        self.radio_custom = QRadioButton("Custom Parameters")
        self.mode_group.addButton(self.radio_city)
        self.mode_group.addButton(self.radio_custom)
        self.radio_city.setChecked(True)
        self.radio_city.toggled.connect(self.toggle_location_mode)
        
        mode_layout.addWidget(self.radio_city)
        mode_layout.addWidget(self.radio_custom)
        layout.addLayout(mode_layout)
        
        # Mode 1: State & District Selection
        self.loc_widget = QWidget()
        loc_layout = QFormLayout(self.loc_widget)
        
        self.combo_state = QComboBox()
        self.combo_district = QComboBox()
        
        # Populate States
        states = sorted(list(self.state_data.keys()))
        self.combo_state.addItems(["Select State..."] + states)
        
        self.combo_state.currentTextChanged.connect(self.on_state_changed)
        self.combo_district.currentTextChanged.connect(self.on_district_changed)
        
        loc_layout.addRow("State:", self.combo_state)
        loc_layout.addRow("District:", self.combo_district)
        layout.addWidget(self.loc_widget)
        
        # Mode 2: Custom
        self.custom_widget = QWidget()
        custom_layout = QHBoxLayout(self.custom_widget)
        self.btn_custom_table = QPushButton("Tabulate Custom Loading Parameters")
        self.btn_custom_table.clicked.connect(self.open_custom_table)
        custom_layout.addWidget(self.btn_custom_table)
        layout.addWidget(self.custom_widget)
        self.custom_widget.setVisible(False)
        
        # Display Area (Detailed Info)
        # Requirement: "values should be displayed in green"
        self.info_label = QLabel("Select State and District.")
        self.info_label.setStyleSheet("color: #2E7D32; font-weight: bold; border: 1px solid #C8E6C9; padding: 10px; background: #E8F5E9;")
        layout.addWidget(self.info_label)
        
        group.setLayout(layout)
        self.layout.addWidget(group)

    def create_geometry_section(self):
        group = QGroupBox("3. Geometric Inputs")
        layout = QFormLayout()
        
        self.input_span = QLineEdit()
        self.input_carriageway = QLineEdit()
        self.combo_footpath = QComboBox()
        self.combo_footpath.addItems(["None", "Single-sided", "Both"])
        self.input_skew = QLineEdit()
        
        self.input_span.editingFinished.connect(self.check_span)
        self.input_carriageway.editingFinished.connect(self.check_carriageway)
        self.input_skew.editingFinished.connect(self.check_skew)

        layout.addRow("Span (m):", self.input_span)
        layout.addRow("Carriageway Width (m):", self.input_carriageway)
        layout.addRow("Footpath:", self.combo_footpath)
        layout.addRow("Skew Angle (°):", self.input_skew)
        
        self.btn_modify_geometry = QPushButton("Modify Additional Geometry")
        self.btn_modify_geometry.clicked.connect(self.open_geometry_dialog)
        layout.addRow(self.btn_modify_geometry)
        
        group.setLayout(layout)
        self.layout.addWidget(group)

    def create_material_section(self):
        group = QGroupBox("4. Material Inputs")
        layout = QFormLayout()
        
        items_steel = ["E250", "E350", "E450"]
        items_concrete = [f"M{i}" for i in range(25, 65, 5)]
        
        self.combo_girder = QComboBox()
        self.combo_girder.addItems(items_steel)
        self.combo_bracing = QComboBox()
        self.combo_bracing.addItems(items_steel)
        self.combo_deck = QComboBox()
        self.combo_deck.addItems(items_concrete)
        
        layout.addRow("Girder Steel:", self.combo_girder)
        layout.addRow("Cross Bracing Steel:", self.combo_bracing)
        layout.addRow("Deck Concrete:", self.combo_deck)
        
        group.setLayout(layout)
        self.layout.addWidget(group)

    # Logic
    def on_structure_changed(self, text):
        if text == "Other":
            self.other_label.setVisible(True)
        else:
            self.other_label.setVisible(False)

    def toggle_location_mode(self):
        is_city = self.radio_city.isChecked()
        self.loc_widget.setVisible(is_city)
        self.custom_widget.setVisible(not is_city)
        if not is_city:
            self.info_label.setText("Enter parameters manually via popup...")
        else:
             self.on_district_changed(self.combo_district.currentText())

    def on_state_changed(self, state):
        self.combo_district.blockSignals(True)
        self.combo_district.clear()
        
        if state in self.state_data:
            districts = sorted(list(self.state_data[state].keys()))
            self.combo_district.addItems(["Select District..."] + districts)
            self.info_label.setText("Select District.")
        else:
            self.info_label.setText("Select State.")
            
        self.combo_district.blockSignals(False)

    def on_district_changed(self, district):
        state = self.combo_state.currentText()
        if state not in self.state_data or district not in self.state_data[state]:
            return
            
        info = self.state_data[state][district]
        
        wind = info.get('wind', 'N/A')
        zone = info.get('zone', 'N/A')
        # Factor map for extra credit correctness (IS 1893)
        factors = {"II": 0.10, "III": 0.16, "IV": 0.24, "V": 0.36}
        zone_factor = factors.get(zone, "N/A")
        
        max_t = info.get('max', 'N/A')
        min_t = info.get('min', 'N/A')
        
        # Requirement: "values automatically appear... displayed in green"
        text = (f"Basic Wind Speed: {wind} m/s\n"
                f"Seismic Zone: {zone} (Z = {zone_factor})\n"
                f"Max Shade Temp: {max_t} °C\n"
                f"Min Shade Temp: {min_t} °C")
        self.info_label.setText(text)

    def open_custom_table(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Custom Loading")
        layout = QFormLayout(dialog)
        
        i_wind = QLineEdit()
        i_zone = QComboBox()
        i_zone.addItems(["II", "III", "IV", "V"])
        i_max = QLineEdit()
        i_min = QLineEdit()
        
        layout.addRow("Wind Speed", i_wind)
        layout.addRow("Seismic Zone", i_zone)
        layout.addRow("Max Temp", i_max)
        layout.addRow("Min Temp", i_min)
        
        btn = QPushButton("OK")
        btn.clicked.connect(lambda: self.apply_custom(dialog, i_wind.text(), i_zone.currentText(), i_max.text(), i_min.text()))
        layout.addRow(btn)
        dialog.exec()
        
    def apply_custom(self, dialog, w, z, max_t, min_t):
        self.info_label.setText(f"Wind: {w} m/s\nZone: {z}\nMax T: {max_t} °C\nMin T: {min_t} °C")
        dialog.accept()

    def check_span(self):
        valid, msg = validate_span(self.input_span.text())
        if not valid:
             QMessageBox.warning(self, "Error", msg)

    def check_carriageway(self):
        valid, msg = validate_carriageway(self.input_carriageway.text())
        if not valid:
             QMessageBox.warning(self, "Error", msg)
             
    def check_skew(self):
        valid, msg = validate_skew(self.input_skew.text())
        if msg: # Warning
             QMessageBox.warning(self, "Warning", msg)

    def open_geometry_dialog(self):
        try:
             # Clean input to ensure valid float
            text = self.input_carriageway.text()
            if not text:
                 raise ValueError
            cw = float(text)
            dialog = ModifyGeometryDialog(cw, self)
            dialog.exec()
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter Carriageway Width first.")
