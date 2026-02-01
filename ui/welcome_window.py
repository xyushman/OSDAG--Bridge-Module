import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QFrame, QHBoxLayout, QGraphicsDropShadowEffect, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPixmap

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome - OSDAG Group Design")
        self.resize(1100, 750)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # --- Split Layout (Left: Content, Right: Hero) ---
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ==========================================================
        # LEFT PANEL: Clean, Typography-focused
        # ==========================================================
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #FFFFFF;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(60, 60, 60, 60)
        left_layout.setSpacing(10)
        
        # 1. Logo (Small, Top Left)
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "app_icon.png")
        if os.path.exists(icon_path):
            pix = QPixmap(icon_path)
            logo_label.setPixmap(pix.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        left_layout.addWidget(logo_label)
        
        left_layout.addSpacing(30)
        
        # 2. Main Title (Huge & Bold)
        title_top = QLabel("OSDAG")
        title_top.setFont(QFont("Segoe UI Black", 56, QFont.Weight.Bold))
        title_top.setStyleSheet("color: #1A237E; letter-spacing: -2px;")
        left_layout.addWidget(title_top)
        
        # 3. Subtitle (Light & Modern)
        title_sub = QLabel("Group Design")
        title_sub.setFont(QFont("Segoe UI Light", 48, QFont.Weight.Light))
        title_sub.setStyleSheet("color: #37474F;")
        left_layout.addWidget(title_sub)
        
        left_layout.addSpacing(20)
        
        # 4. Description
        desc_label = QLabel("Interactive Steel Structure Design Module for Civil Engineers.")
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setStyleSheet("color: #78909C; line-height: 150%;")
        left_layout.addWidget(desc_label)
        
        left_layout.addStretch()
        
        # 5. Call to Action Button (Floating Shadow)
        self.start_btn = QPushButton("Start Project  →")
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setFixedSize(280, 70)
        self.start_btn.setFont(QFont("Segoe UI Semibold", 13, QFont.Weight.DemiBold))
        
        # Gradient & Shadow for Button
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #2962FF, stop:1 #2979FF);
                color: white;
                border-radius: 8px;
                border: none;
                padding-left: 25px;
                text-align: left;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #448AFF, stop:1 #2962FF);
                padding-left: 30px; /* Slide effect */
            }
            QPushButton:pressed {
                background: #1565C0;
            }
        """)
        
        # Button Shadow
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(20)
        btn_shadow.setColor(QColor(41, 98, 255, 80)) # Blue glow
        btn_shadow.setOffset(0, 8)
        self.start_btn.setGraphicsEffect(btn_shadow)
        
        left_layout.addWidget(self.start_btn)
        
        left_layout.addSpacing(40)
        
        # 6. Footer
        footer = QLabel("v1.0.0  •  Department of Civil Engineering")
        footer.setFont(QFont("Segoe UI", 9))
        footer.setStyleSheet("color: #B0BEC5;")
        left_layout.addWidget(footer)
        
        # ==========================================================
        # RIGHT PANEL: Hero Image & Rich Background
        # ==========================================================
        right_panel = QFrame()
        # Deep Engineering Blue Gradient
        right_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #0D47A1, stop:1 #1565C0);
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        # Hero Image Container (Floating)
        img_container = QFrame()
        img_container.setFixedSize(600, 300)
        img_container.setStyleSheet("""
            background: rgba(255, 255, 255, 10); /* Glass effect */
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 20px;
        """)
        
        img_layout = QVBoxLayout(img_container)
        img_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Hero Image
        hero_img = QLabel()
        hero_img.setStyleSheet("background: transparent; border: none;")
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "bridge_section.png")
        if os.path.exists(image_path):
            pix = QPixmap(image_path)
            # Invert colors not easily possible without PIL/Opencv in raw qt efficiently here
            # We will display the diagram as is, assuming it contrasts okay or putting it in a white box
            # Actually, let's put it in a white box for clarity
            img_container.setStyleSheet("""
                background: white;
                border-radius: 20px;
            """)
            hero_img.setPixmap(pix.scaled(500, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        # Hero Shadow
        hero_shadow = QGraphicsDropShadowEffect()
        hero_shadow.setBlurRadius(50)
        hero_shadow.setColor(QColor(0, 0, 0, 100))
        hero_shadow.setOffset(0, 20)
        img_container.setGraphicsEffect(hero_shadow)
        
        img_layout.addWidget(hero_img)
        right_layout.addWidget(img_container)
        
        # Add Layouts to Main
        main_layout.addWidget(left_panel, stretch=40)
        main_layout.addWidget(right_panel, stretch=60)
