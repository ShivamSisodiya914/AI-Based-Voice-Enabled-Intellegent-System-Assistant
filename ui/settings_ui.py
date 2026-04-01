from ui.tray_icon import setup_tray
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import qdarktheme

class AssistantThread(QThread):
    output_signal = pyqtSignal(str) 

    def set_logic(self, logic_function):
        self.logic = logic_function

    def run(self):
        self.logic(self.output_signal)

class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS AI SYSTEM")
        self.setMinimumSize(400, 550)

        # Layout
        layout = QVBoxLayout()
        
        # High-tech Status Label
        self.status_label = QLabel("STATUS: SYSTEM OFFLINE")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #ff4c4c; padding: 10px;")
        layout.addWidget(self.status_label)

        # Console for logs
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("font-family: 'Consolas'; font-size: 11px; background-color: #1e1e1e;")
        layout.addWidget(self.console)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize Tray
        self.tray = setup_tray(self)

    def update_console(self, text):
        # --- THE "CLOSE SYSTEM" TRIGGER ---
        if text == "CLOSE_WINDOW":
            print(">>> Shutting down UI...")
            self.close() # Closes the popup window
            sys.exit()   # Stops the program
            return

        # Regular logging
        self.console.append(text)
        
        # Dynamic Status Colors
        if "Listening" in text:
            self.status_label.setText("STATUS: LISTENING...")
            self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #00ff00;") # Green
        elif "Sleeping" in text or "standby" in text.lower():
            self.status_label.setText("STATUS: STANDBY")
            self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #ff4c4c;") # Red
        elif "Thinking" in text or "Processing" in text:
            self.status_label.setText("STATUS: PROCESSING...")
            self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffa500;") # Orange
        else:
            # Only reset if it's a general message
            if not self.status_label.text().startswith("STATUS: LISTENING"):
                self.status_label.setText("STATUS: READY")
                self.status_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #00acee;") # Blue

def run_gui(logic_func):
    app = QApplication(sys.argv)
    
    try:
        app.setStyleSheet(qdarktheme.load_stylesheet())
    except:
        pass

    window = AssistantWindow()
    window.show()
    app.processEvents()

    # Create and start the background thread
    thread = AssistantThread()
    thread.set_logic(logic_func)
    
    # Connect the thread signal to our update function
    thread.output_signal.connect(window.update_console)
    
    thread.start()

    sys.exit(app.exec())