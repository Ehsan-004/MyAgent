from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit,
                             QPushButton, QLabel, QProgressBar, QSystemTrayIcon, QMenu, QDialog,
                             )
from PyQt6.QtCore import Qt, QPoint, QSettings
from PyQt6.QtGui import QAction

import subprocess

class SystemPromptDialog(QDialog):
    def __init__(self, parent=None, prompt_manager=None):
        super().__init__(parent)
        self.prompt_manager = prompt_manager
        self.setWindowTitle("Edit System Prompt")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Description
        desc_label = QLabel(
            "Edit the system prompt that defines the agent's behavior. Be careful with changes as they may affect functionality.")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666; margin: 10px 0;")
        layout.addWidget(desc_label)

        # Prompt editor
        self.prompt_editor = QTextEdit()
        self.prompt_editor.setPlainText(self.prompt_manager.get_current_prompt())
        self.prompt_editor.setStyleSheet("""
            QTextEdit {
                background-color: #262626;
                border: 1px solid #333333;
                border-radius: 8px;
                color: #ffffff;
                padding: 12px;
                font-family: Inter;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.prompt_editor)

        # Buttons
        button_layout = QHBoxLayout()

        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_prompt)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)

        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_changes)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def reset_prompt(self):
        if self.prompt_manager.reset_to_default():
            self.prompt_editor.setPlainText(self.prompt_manager.get_current_prompt())

    def save_changes(self):
        new_prompt = self.prompt_editor.toPlainText()
        if self.prompt_manager.save_prompt(new_prompt):
            self.accept()
        else:
            # Show error message
            pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize theme settings
        self.settings = QSettings('Grunty', 'Preferences')
        self.dark_mode = self.settings.value('dark_mode', True, type=bool)
        
        self.setWindowTitle("Grunty 👨💻")
        self.setGeometry(100, 100, 400, 600)
        self.setMinimumSize(400, 500)  # Increased minimum size for better usability

        # Set rounded corners and border
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setup_ui()

    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        central_widget.setLayout(main_layout)

        # Container widget for rounded corners
        self.container = QWidget()  # Make it an instance variable
        self.container.setObjectName("container")
        container_layout = QVBoxLayout()
        container_layout.setSpacing(0)  # Remove spacing between elements
        self.container.setLayout(container_layout)

        # Create title bar
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 5, 10, 5)

        # Add Grunty title with robot emoji
        title_label = QLabel("Grunty 🤖")
        title_label.setObjectName("titleLabel")
        title_bar_layout.addWidget(title_label)

        # Add File Menu
        file_menu = QMenu("File")
        new_task_action = QAction("New Task", self)
        new_task_action.setShortcut("Ctrl+N")
        edit_prompt_action = QAction("Edit System Prompt", self)
        edit_prompt_action.setShortcut("Ctrl+E")
        edit_prompt_action.triggered.connect(self.show_prompt_dialog)
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        # quit_action.triggered.connect(self.quit_application)
        file_menu.addAction(new_task_action)
        file_menu.addAction(edit_prompt_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        file_button = QPushButton("File")
        file_button.setObjectName("menuButton")
        file_button.clicked.connect(lambda: file_menu.exec(file_button.mapToGlobal(QPoint(0, file_button.height()))))
        title_bar_layout.addWidget(file_button)

        # Add spacer to push remaining items to the right
        title_bar_layout.addStretch()

        # Theme toggle button
        self.theme_button = QPushButton()
        self.theme_button.setObjectName("titleBarButton")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.update_theme_button()
        title_bar_layout.addWidget(self.theme_button)

        # Minimize and close buttons
        minimize_button = QPushButton("−")
        minimize_button.setObjectName("titleBarButton")
        minimize_button.clicked.connect(self.showMinimized)
        title_bar_layout.addWidget(minimize_button)

        close_button = QPushButton("×")
        close_button.setObjectName("titleBarButton")
        close_button.clicked.connect(self.close)
        title_bar_layout.addWidget(close_button)

        container_layout.addWidget(title_bar)

        # Action log with modern styling
        self.action_log = QTextEdit()
        self.action_log.setReadOnly(True)
        self.action_log.setStyleSheet("""
            QTextEdit {
                background-color: #262626;
                border: none;
                border-radius: 0;
                color: #ffffff;
                padding: 16px;
                font-family: Inter;
                font-size: 13px;
            }
        """)
        container_layout.addWidget(self.action_log, stretch=1)  # Give it flexible space

        # Progress bar - Now above input area
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #262626;
                height: 2px;
                margin: 0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        self.progress_bar.hide()
        container_layout.addWidget(self.progress_bar)

        # Input section container - Fixed height at bottom
        input_section = QWidget()
        input_section.setObjectName("input_section")
        input_section.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-top: 1px solid #333333;
            }
        """)
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(16, 16, 16, 16)
        input_layout.setSpacing(12)
        input_section.setLayout(input_layout)

        # Input area with modern styling
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("What can I do for you today?")
        self.input_area.setFixedHeight(100)  # Fixed height for input
        self.input_area.setStyleSheet("""
            QTextEdit {
                background-color: #262626;
                border: 1px solid #333333;
                border-radius: 8px;
                color: #ffffff;
                padding: 12px;
                font-family: Inter;
                font-size: 14px;
                selection-background-color: #4CAF50;
            }
            QTextEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        # Connect textChanged signal
        self.input_area.textChanged.connect(self.update_run_button)
        input_layout.addWidget(self.input_area)

        # Control buttons with modern styling
        control_layout = QHBoxLayout()

        self.run_button = QPushButton(text="Start")
        self.stop_button = QPushButton(text="Stop")

        # Connect button signals
        self.run_button.clicked.connect(self.run_agent)
        self.stop_button.clicked.connect(self.stop_agent)

        # Initialize button states
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        for button in (self.run_button, self.stop_button):
            button.setFixedHeight(40)
            if button == self.run_button:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 0 24px;
                        font-family: Inter;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QPushButton:disabled {
                        background-color: #333333;
                        color: #666666;
                    }
                """)
            else:  # Stop button
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #ff4444;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 0 24px;
                        font-family: Inter;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #ff3333;
                    }
                    QPushButton:disabled {
                        background-color: #333333;
                        color: #666666;
                    }
                """)
            control_layout.addWidget(button)

        input_layout.addLayout(control_layout)
        container_layout.addWidget(input_section)
        main_layout.addWidget(self.container)
        self.apply_theme()

    def update_theme_button(self):
        if self.dark_mode:
            
            self.theme_button.setToolTip("Switch to Light Mode")
        else:
            
            self.theme_button.setToolTip("Switch to Dark Mode")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.settings.setValue('dark_mode', self.dark_mode)
        self.update_theme_button()
        self.apply_theme()

    def apply_theme(self):
        # Apply styles based on theme
        colors = {
            'bg': '#1a1a1a' if self.dark_mode else '#ffffff',
            'text': '#ffffff' if self.dark_mode else '#000000',
            'button_bg': '#333333' if self.dark_mode else '#f0f0f0',
            'button_text': '#ffffff' if self.dark_mode else '#000000',
            'button_hover': '#4CAF50' if self.dark_mode else '#e0e0e0',
            'border': '#333333' if self.dark_mode else '#e0e0e0'
        }

        # Container style
        container_style = f"""
            QWidget#container {{
                background-color: {colors['bg']};
                border-radius: 12px;
                border: 1px solid {colors['border']};
            }}
        """
        self.container.setStyleSheet(container_style)  # Use instance variable

        # Update title label
        self.findChild(QLabel, "titleLabel").setStyleSheet(f"color: {colors['text']}; padding: 5px;")

        # Update action log
        self.action_log.setStyleSheet(f"""
            QTextEdit {{
                background-color: {colors['bg']};
                border: none;
                border-radius: 0;
                color: {colors['text']};
                padding: 16px;
                font-family: Inter;
                font-size: 13px;
            }}
        """)

        # Update input area
        self.input_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {colors['bg']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                color: {colors['text']};
                padding: 12px;
                font-family: Inter;
                font-size: 14px;
                selection-background-color: {colors['button_hover']};
            }}
            QTextEdit:focus {{
                border: 1px solid {colors['button_hover']};
            }}
        """)

        # Update progress bar
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {colors['bg']};
                height: 2px;
                margin: 0;
            }}
            QProgressBar::chunk {{
                background-color: {colors['button_hover']};
            }}
        """)

        # Update input section
        input_section_style = f"""
            QWidget {{
                background-color: {colors['button_bg']};
                border-top: 1px solid {colors['border']};
            }}
        """
        self.findChild(QWidget, "input_section").setStyleSheet(input_section_style)

        # Update window controls style
        window_control_style = f"""
            QPushButton {{
                color: {colors['button_text']};
                background-color: transparent;
                border-radius: 8px;
                padding: 4px 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['button_hover']};
            }}
        """

        # Apply to all window control buttons
        for button in [self.theme_button,
                       self.findChild(QPushButton, "menuButton"),
                       self.findChild(QPushButton, "titleBarButton")]:
            if button:
                button.setStyleSheet(window_control_style)


    def update_run_button(self):
        self.run_button.setEnabled(bool(self.input_area.toPlainText().strip()))

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.toggle_window()

    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()       
        
        
    def run_agent(self):
        instructions = self.input_area.toPlainText()
        if not instructions:
            self.update_log("لطفا یک دستور به من بده تا انجامش بدم.")
            return

        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.show()
        self.action_log.clear()
        self.input_area.clear()

        # 💬 CHAT RESPONSE - اتصال به مدل زبانی
        try:
            self.update_log(f"فعلا چیزی برای گفتن ندارم عزیزم")
        except Exception as e:
            self.update_log(f"Assistant: ⚠️ Failed to get response.\n{e}")
        finally:
            self.agent_finished()  # مخفی کردن progress bar و فعال کردن دکمه‌ها

    def stop_agent(self):
        self.stop_button.setEnabled(False)

    def agent_finished(self):
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.hide()

        # Yellow completion message with sparkle emoji
        completion_message = '''
            <div style="margin: 6px 0;">
                <span style="
                    display: inline-flex;
                    align-items: center;
                    background-color: rgba(45, 45, 45, 0.95);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 100px;
                    padding: 4px 12px;
                    color: #FFD700;
                    font-family: Inter, -apple-system, system-ui, sans-serif;
                    font-size: 13px;
                    line-height: 1.4;
                    white-space: nowrap;
                ">✨ اجرای دستور کامل شد!</span>
            </div>
        '''
        self.action_log.append(completion_message)

        # Notify voice controller that processing is complete
        if hasattr(self, 'voice_controller'):
            self.voice_controller.finish_processing()

    def update_log(self, message):
        if message.startswith("Performed action:"):
            action_text = message.replace("Performed action:", "").strip()

            # Pill-shaped button style with green text
            button_style = '''
                <div style="margin: 6px 0;">
                    <span style="
                        display: inline-flex;
                        align-items: center;
                        background-color: rgba(45, 45, 45, 0.95);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        border-radius: 100px;
                        padding: 4px 12px;
                        color: #4CAF50;
                        font-family: Inter, -apple-system, system-ui, sans-serif;
                        font-size: 13px;
                        line-height: 1.4;
                        white-space: nowrap;
                    ">{}</span>
                </div>
            '''

            try:
                import json
                action_data = json.loads(action_text)
                action_type = action_data.get('type', '').lower()

                if action_type == "type":
                    text = action_data.get('text', '')
                    msg = f'⌨️ <span style="margin: 0 4px; color: #4CAF50;">Typed</span> <span style="color: #4CAF50">"{text}"</span>'
                    self.action_log.append(button_style.format(msg))

                elif action_type == "key":
                    key = action_data.get('text', '')
                    msg = f'⌨️ <span style="margin: 0 4px; color: #4CAF50;">Pressed</span> <span style="color: #4CAF50">{key}</span>'
                    self.action_log.append(button_style.format(msg))

                elif action_type == "mouse_move":
                    x = action_data.get('x', 0)
                    y = action_data.get('y', 0)
                    msg = f'🖱️ <span style="margin: 0 4px; color: #4CAF50;">Moved to</span> <span style="color: #4CAF50">({x}, {y})</span>'
                    self.action_log.append(button_style.format(msg))

                elif action_type == "screenshot":
                    msg = '📸 <span style="margin: 0 4px; color: #4CAF50;">Captured Screenshot</span>'
                    self.action_log.append(button_style.format(msg))

                elif "click" in action_type:
                    x = action_data.get('x', 0)
                    y = action_data.get('y', 0)
                    click_map = {
                        "left_click": "Left Click",
                        "right_click": "Right Click",
                        "middle_click": "Middle Click",
                        "double_click": "Double Click"
                    }
                    click_type = click_map.get(action_type, "Click")
                    msg = f'👆 <span style="margin: 0 4px; color: #4CAF50;">{click_type}</span> <span style="color: #4CAF50">({x}, {y})</span>'
                    self.action_log.append(button_style.format(msg))

            except json.JSONDecodeError:
                self.action_log.append(button_style.format(action_text))

        # Clean assistant message style without green background
        elif message.startswith("Assistant:"):
            message_style = '''
                <div style="
                    border-left: 2px solid #666;
                    padding: 8px 16px;
                    margin: 8px 0;
                    font-family: Inter, -apple-system, system-ui, sans-serif;
                    font-size: 13px;
                    line-height: 1.5;
                    color: #e0e0e0;
                ">{}</div>
            '''
            clean_message = message.replace("Assistant:", "").strip()
            self.action_log.append(message_style.format(f'💬 {clean_message}'))

        # Subtle assistant action style
        elif message.startswith("Assistant action:"):
            action_style = '''
                <div style="
                    color: #666;
                    font-style: italic;
                    padding: 4px 0;
                    font-size: 12px;
                    font-family: Inter, -apple-system, system-ui, sans-serif;
                    line-height: 1.4;
                ">🤖 {}</div>
            '''
            clean_message = message.replace("Assistant action:", "").strip()
            self.action_log.append(action_style.format(clean_message))

        # Regular message style
        else:
            regular_style = '''
                <div style="
                    padding: 4px 0;
                    color: #e0e0e0;
                    font-family: Inter, -apple-system, system-ui, sans-serif;
                    font-size: 13px;
                    line-height: 1.4;
                ">{}</div>
            '''
            self.action_log.append(regular_style.format(message))

        # Scroll to bottom
        self.action_log.verticalScrollBar().setValue(
            self.action_log.verticalScrollBar().maximum()
        )


    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()


    def show_prompt_dialog(self):
        dialog = SystemPromptDialog(self, self.prompt_manager)
        dialog.exec()