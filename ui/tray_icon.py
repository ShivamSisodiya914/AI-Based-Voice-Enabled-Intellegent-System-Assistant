from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
import sys
import os

def setup_tray(window):
    # Path to your JPEG image
    icon_path = os.path.join("ui", "icon.jpg")
    
    if not os.path.exists(icon_path):
        print(f"⚠️ Warning: Tray icon not found at {icon_path}. Using default.")
        tray_icon = QSystemTrayIcon(window)
    else:
        tray_icon = QSystemTrayIcon(QIcon(icon_path), window)
    
    # Create the right-click menu
    menu = QMenu()
    show_action = menu.addAction("Show Jarvis")
    hide_action = menu.addAction("Hide Jarvis")
    menu.addSeparator()
    quit_action = menu.addAction("Exit System")
    
    # Connect actions
    show_action.triggered.connect(window.showNormal)
    hide_action.triggered.connect(window.hide)
    quit_action.triggered.connect(sys.exit)
    
    tray_icon.setContextMenu(menu)
    tray_icon.setToolTip("Jarvis AI Assistant")
    tray_icon.show()
    
    return tray_icon