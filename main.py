import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.welcome_window import WelcomeWindow

from PyQt6.QtGui import QIcon
import os

def main():
    app = QApplication(sys.argv)

    # Set App Icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Global Stylesheet (Custom Color Code)
    app.setStyleSheet("""
        QMainWindow {
            background-color: white;
        }
        
        /* 1. Informational Points (General styling for labels that might be info) */
        /* Note: Specific info label is styled in basic_inputs_tab.py */
        
        /* 2. Dropdowns are Blue */
        QComboBox {
            border: 2px solid #1976D2; /* Blue Border */
            border-radius: 4px;
            padding: 5px;
            background: white;
            color: black;
        }
        /* Labels */
        QLabel {
            color: black;
        }
        QWidget {
            color: black;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left-width: 1px;
            border-left-color: #1976D2;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            background: white; /* White BG for arrow area */
        }
        QComboBox QAbstractItemView {
            background: white;
            selection-background-color: #E3F2FD;
            selection-color: black;
        }
        QComboBox:on { /* shift the text when the popup opens */
            padding-top: 3px;
            padding-left: 4px;
        }
        
        /* 3. Checkboxes are Orange */
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #F57C00; /* Orange Border */
            border-radius: 3px;
            background: white;
        }
        QCheckBox::indicator:checked {
            background-color: #F57C00; /* Orange Fill */
            image: url(none); /* In real app custom checkmark, standard is fine */
            border: 2px solid #E65100;
        }
        QRadioButton::indicator { /* Applying to Radio too as layout often groups them */
            width: 18px;
            height: 18px;
            border: 2px solid #F57C00;
            border-radius: 10px;
            background: white;
        }
        QRadioButton::indicator:checked {
            background-color: #F57C00;
        }
        
        /* 4. Pop-up dialog boxes are Yellow */
        QDialog {
            background-color: #FFFDE7; /* Light Yellow Background */
        }
        /* Buttons */
        QPushButton {
            background-color: #FFFFFF;
            border: 1px solid #B0BEC5;
            border-bottom: 3px solid #B0BEC5; /* Pseudo-3D effect */
            border-radius: 6px;
            padding: 6px 16px;
            color: #455A64;
            font-weight: bold;
            font-family: "Segoe UI";
        }
        QPushButton:hover {
            background-color: #F1F8E9; /* Slight Green tint for action */
            border-color: #81C784;
            border-bottom-color: #66BB6A;
            color: #2E7D32;
            margin-top: 1px; /* Press effect simulation */
            border-bottom-width: 2px;
        }
        QPushButton:pressed {
            background-color: #DCEDC8;
            margin-top: 3px;
            border-bottom-width: 0px;
        }
        
        /* Text Inputs */
        QLineEdit {
            border: 1px solid #999;
            border-radius: 4px;
            padding: 5px;
            background: white;
        }
        QLineEdit:focus {
            border: 2px solid #1976D2;
        }
        
        /* Tabs (Keeping clean) */
        QTabWidget::pane {
            border: 1px solid #CCC;
            background: white;
        }
        QTabBar::tab {
            background: #EEE;
            padding: 8px 20px;
            border: 1px solid #CCC;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: white;
            border-bottom: 2px solid #1976D2; /* Blue accent */
        }
    """)
    
    # Window Management
    windows = {}
    
    def show_main():
        windows['main'] = MainWindow()
        windows['main'].show()
        windows['welcome'].close()
        
    windows['welcome'] = WelcomeWindow()
    windows['welcome'].start_btn.clicked.connect(show_main)
    windows['welcome'].show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
