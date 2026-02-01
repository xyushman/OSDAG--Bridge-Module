
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QTabWidget, QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QColor
from .basic_inputs_tab import BasicInputsTab
from .additional_inputs_tab import AdditionalInputsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Group Design")
        self.resize(1200, 800)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Layout (Split Left/Right)
        main_layout = QHBoxLayout(central_widget)
        
        # --- Left Panel (Tabs) ---
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CFD8DC;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #F8F9FA;
                color: #546E7A;
                padding: 10px 20px;
                border: 1px solid transparent;
                border-bottom: none;
                margin-right: 4px;
                font-family: "Segoe UI";
                font-weight: 500;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #1976D2;
                border-bottom: 3px solid #1976D2;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #ECEFF1;
            }
        """)

        # Tab Shadow
        tab_shadow = QGraphicsDropShadowEffect()
        tab_shadow.setBlurRadius(15)
        tab_shadow.setColor(QColor(0, 0, 0, 20))
        tab_shadow.setOffset(0, 4)
        self.tabs.setGraphicsEffect(tab_shadow)
        self.basic_inputs = BasicInputsTab()
        self.additional_inputs = AdditionalInputsTab()
        
        self.tabs.addTab(self.basic_inputs, "Basic Inputs")
        self.tabs.addTab(self.additional_inputs, "Additional Inputs")
        
        main_layout.addWidget(self.tabs, stretch=1)
        
        # --- Right Panel (Reference Image) ---
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        self.image_label = QLabel("Reference Image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: white; border: 1px solid #ddd;")
        
        # Load Image
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "bridge_section.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.image_label.setText("Image not found")
            
        right_layout.addWidget(self.image_label)
        main_layout.addWidget(right_panel, stretch=1)
