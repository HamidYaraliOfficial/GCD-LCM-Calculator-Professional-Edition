import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QGroupBox,
    QRadioButton, QButtonGroup, QFrame, QSpacerItem, QSizePolicy,
    QGridLayout, QStackedWidget, QListWidget, QFormLayout
)
from PyQt6.QtCore import Qt, QTranslator, pyqtSignal, QPropertyAnimation, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush, QPainter, QIntValidator

class LanguageManager:
    def __init__(self):
        self.translators = {}
        self.load_translators()

    def load_translators(self):
        self.translators['fa'] = QTranslator()
        self.translators['fa'].load(":/translations/fa.qm")
        self.translators['zh'] = QTranslator()
        self.translators['zh'].load(":/translations/zh.qm")
        self.translators['ru'] = QTranslator()
        self.translators['ru'].load(":/translations/ru.qm")

    def install(self, app, lang):
        if lang in self.translators:
            app.installTranslator(self.translators[lang])

class ThemeManager:
    def __init__(self):
        self.themes = {
            'light': self.light_theme,
            'dark': self.dark_theme,
            'windows': self.windows_theme,
            'red': self.red_theme,
            'blue': self.blue_theme
        }

    def light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 247))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(230, 230, 230))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 122, 255))
        return palette

    def dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 100, 100))
        palette.setColor(QPalette.ColorRole.Link, QColor(100, 180, 255))
        return palette

    def windows_theme(self):
        return QApplication.palette()

    def red_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(120, 15, 15))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(150, 25, 25))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(180, 40, 40))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 80, 80))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 200, 200))
        return palette

    def blue_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(10, 25, 80))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 230, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(15, 40, 120))
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 230, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(30, 70, 150))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 240, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(70, 130, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 150))
        return palette

    def apply(self, app, theme_name):
        if theme_name in self.themes:
            app.setPalette(self.themes[theme_name]())

class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        palette = self.palette()
        color1 = palette.color(QPalette.ColorRole.Window).lighter(105)
        color2 = palette.color(QPalette.ColorRole.Window).darker(108)
        gradient.setColorAt(0, color1)
        gradient.setColorAt(1, color2)
        painter.fillRect(self.rect(), QBrush(gradient))

class CalculatorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title = QLabel()
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: palette(text);")
        main_layout.addWidget(title)

        input_group = QGroupBox()
        input_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid palette(mid);
                border-radius: 14px;
                margin-top: 12px;
                padding-top: 12px;
                color: palette(text);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: palette(text);
            }
        """)
        form_layout = QFormLayout(input_group)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(18)

        validator = QIntValidator()
        validator.setBottom(0)

        self.num1_input = QLineEdit()
        self.num1_input.setFixedHeight(50)
        self.num1_input.setFont(QFont("Segoe UI", 15))
        self.num1_input.setValidator(validator)
        self.num1_input.setPlaceholderText("0")
        self.num1_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #cccccc;
                border-radius: 14px;
                padding: 0 18px;
                background-color: palette(base);
                color: palette(text);
                font-weight: 500;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                background-color: palette(base);
            }
        """)

        self.num2_input = QLineEdit()
        self.num2_input.setFixedHeight(50)
        self.num2_input.setFont(QFont("Segoe UI", 15))
        self.num2_input.setValidator(validator)
        self.num2_input.setPlaceholderText("0")
        self.num2_input.setStyleSheet(self.num1_input.styleSheet())

        label1 = QLabel()
        label1.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        label1.setStyleSheet("color: palette(text);")
        label2 = QLabel()
        label2.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        label2.setStyleSheet("color: palette(text);")

        form_layout.addRow(label1, self.num1_input)
        form_layout.addRow(label2, self.num2_input)
        main_layout.addWidget(input_group)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(25)

        self.gcd_button = QPushButton()
        self.gcd_button.setFixedHeight(60)
        self.gcd_button.setFont(QFont("Segoe UI", 15, 600))  # 600 = SemiBold
        self.gcd_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.gcd_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 16px;
                padding: 0 35px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #a0a0a0;
                color: #e0e0e0;
            }
        """)

        self.lcm_button = QPushButton()
        self.lcm_button.setFixedHeight(60)
        self.lcm_button.setFont(QFont("Segoe UI", 15, 600))  # 600 = SemiBold
        self.lcm_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lcm_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border-radius: 16px;
                padding: 0 35px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0e6b0e;
            }
            QPushButton:pressed {
                background-color: #0a5a0a;
            }
            QPushButton:disabled {
                background-color: #a0a0a0;
                color: #e0e0e0;
            }
        """)

        button_layout.addWidget(self.gcd_button)
        button_layout.addWidget(self.lcm_button)
        main_layout.addLayout(button_layout)

        result_group = QGroupBox()
        result_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        result_group.setStyleSheet(input_group.styleSheet().replace("margin-top: 12px;", "margin-top: 10px;"))
        result_layout = QGridLayout(result_group)
        result_layout.setVerticalSpacing(18)
        result_layout.setHorizontalSpacing(25)

        gcd_title = QLabel()
        gcd_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        gcd_title.setStyleSheet("color: palette(text);")
        self.gcd_label = QLabel("—")
        self.gcd_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.gcd_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gcd_label.setStyleSheet("""
            background-color: palette(alternateBase);
            color: palette(text);
            border-radius: 16px;
            padding: 25px;
            font-weight: bold;
            border: 1px solid palette(mid);
        """)

        lcm_title = QLabel()
        lcm_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        lcm_title.setStyleSheet("color: palette(text);")
        self.lcm_label = QLabel("—")
        self.lcm_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.lcm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lcm_label.setStyleSheet(self.gcd_label.styleSheet())

        result_layout.addWidget(gcd_title, 0, 0)
        result_layout.addWidget(self.gcd_label, 0, 1)
        result_layout.addWidget(lcm_title, 1, 0)
        result_layout.addWidget(self.lcm_label, 1, 1)
        main_layout.addWidget(result_group)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.gcd_button.clicked.connect(self.calculate_gcd)
        self.lcm_button.clicked.connect(self.calculate_lcm)

    def calculate_gcd(self):
        try:
            a = int(self.num1_input.text() or "0")
            b = int(self.num2_input.text() or "0")
            result = math.gcd(a, b)
            self.gcd_label.setText(f"{result}")
            self.gcd_label.setStyleSheet(self.gcd_label.styleSheet().split("; border:")[0] + "; color: palette(text);")
        except Exception:
            self.gcd_label.setText("Invalid")
            self.gcd_label.setStyleSheet(self.gcd_label.styleSheet().replace("palette(text)", "#d32f2f"))

    def calculate_lcm(self):
        try:
            a = int(self.num1_input.text() or "0")
            b = int(self.num2_input.text() or "0")
            if a == 0 or b == 0:
                self.lcm_label.setText("Positive numbers only")
                self.lcm_label.setStyleSheet(self.lcm_label.styleSheet().replace("palette(text)", "#d32f2f"))
                return
            result = abs(a * b) // math.gcd(a, b)
            self.lcm_label.setText(f"{result}")
            self.lcm_label.setStyleSheet(self.lcm_label.styleSheet().split("; border:")[0] + "; color: palette(text);")
        except Exception:
            self.lcm_label.setText("Invalid")
            self.lcm_label.setStyleSheet(self.lcm_label.styleSheet().replace("palette(text)", "#d32f2f"))

    def retranslate(self):
        self.findChild(QLabel, "mainTitle").setText(self.tr("GCD & LCM Calculator"))
        group = self.findChild(QGroupBox)
        if group:
            group.setTitle(self.tr("Enter two numbers:"))
        form = group.layout()
        form.labelForField(self.num1_input).setText(self.tr("First number:"))
        form.labelForField(self.num2_input).setText(self.tr("Second number:"))
        self.gcd_button.setText(self.tr("Calculate GCD"))
        self.lcm_button.setText(self.tr("Calculate LCM"))
        result_group = self.findChildren(QGroupBox)[1]
        result_group.setTitle(self.tr("Results:"))
        grid = result_group.layout()
        grid.itemAtPosition(0, 0).widget().setText(self.tr("GCD:"))
        grid.itemAtPosition(1, 0).widget().setText(self.tr("LCM:"))

class SettingsTab(QWidget):
    language_changed = pyqtSignal(str)
    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(28)

        title = QLabel(self.tr("Settings"))
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: palette(text);")
        layout.addWidget(title)

        lang_group = QGroupBox(self.tr("Language"))
        lang_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        lang_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid palette(mid);
                border-radius: 14px;
                margin-top: 12px;
                padding-top: 12px;
                color: palette(text);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: palette(text);
            }
        """)
        lang_layout = QVBoxLayout(lang_group)

        self.lang_combo = QComboBox()
        self.lang_combo.setFixedHeight(52)
        self.lang_combo.setFont(QFont("Segoe UI", 14))
        self.lang_combo.addItems([
            "English", "فارسی", "中文", "Русский"
        ])
        self.lang_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #cccccc;
                border-radius: 14px;
                padding: 0 18px;
                background-color: palette(base);
                color: palette(text);
                font-weight: 500;
            }
            QComboBox::drop-down {
                border: none;
                width: 45px;
            }
            QComboBox:focus {
                border: 2px solid #0078d4;
            }
        """)
        lang_layout.addWidget(self.lang_combo)
        layout.addWidget(lang_group)

        theme_group = QGroupBox(self.tr("Theme"))
        theme_group.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        theme_group.setStyleSheet(lang_group.styleSheet())
        theme_layout = QGridLayout(theme_group)
        theme_layout.setSpacing(18)

        self.theme_buttons = QButtonGroup()
        self.theme_buttons.setExclusive(True)

        themes = [
            ("light", self.tr("Light"), "#f5f5f5"),
            ("dark", self.tr("Dark"), "#2d2d2d"),
            ("windows", self.tr("Windows Default"), "#0078d4"),
            ("red", self.tr("Red"), "#c41a1a"),
            ("blue", self.tr("Blue"), "#1a5fb4")
        ]

        for i, (name, text, color) in enumerate(themes):
            btn = QRadioButton(text)
            btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
            btn.setStyleSheet(f"""
                QRadioButton {{
                    color: palette(text);
                    spacing: 12px;
                }}
                QRadioButton::indicator {{
                    width: 24px;
                    height: 24px;
                    border-radius: 12px;
                    border: 3px solid #888888;
                    background-color: {color};
                }}
                QRadioButton::indicator:checked {{
                    border: 3px solid #000000;
                    background-color: {color};
                }}
            """)
            btn.setProperty("theme", name)
            self.theme_buttons.addButton(btn)
            theme_layout.addWidget(btn, i // 2, i % 2)

        layout.addWidget(theme_group)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        self.theme_buttons.buttonClicked.connect(self.on_theme_changed)

    def on_language_changed(self, index):
        languages = ['en', 'fa', 'zh', 'ru']
        lang = languages[index]
        self.language_changed.emit(lang)

    def on_theme_changed(self, button):
        theme = button.property("theme")
        self.theme_changed.emit(theme)

    def set_language(self, lang_code):
        mapping = {'en': 0, 'fa': 1, 'zh': 2, 'ru': 3}
        self.lang_combo.setCurrentIndex(mapping.get(lang_code, 0))

    def set_theme(self, theme_name):
        for btn in self.theme_buttons.buttons():
            if btn.property("theme") == theme_name:
                btn.setChecked(True)
                break

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language_manager = LanguageManager()
        self.theme_manager = ThemeManager()
        self.current_lang = 'en'
        self.current_theme = 'light'
        self.init_ui()
        self.apply_initial_settings()

    def init_ui(self):
        self.setWindowTitle("GCD & LCM Calculator")
        self.setMinimumSize(950, 720)

        central_widget = GradientWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: palette(window);
                border-right: 1px solid palette(mid);
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(22, 35, 22, 35)
        sidebar_layout.setSpacing(28)

        logo = QLabel("GCD/LCM")
        logo.setFixedHeight(85)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        logo.setStyleSheet("color: palette(text);")
        sidebar_layout.addWidget(logo)

        nav_buttons = [
            ("calculator", self.tr("Calculator")),
            ("settings", self.tr("Settings"))
        ]

        self.nav_group = QButtonGroup()
        self.nav_group.setExclusive(True)

        for name, text in nav_buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setFixedHeight(55)
            btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 0 22px;
                    border-radius: 14px;
                    background-color: transparent;
                    color: palette(text);
                    font-weight: 500;
                }
                QPushButton:checked {
                    background-color: #0078d4;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover:!checked {
                    background-color: palette(alternateBase);
                }
            """)
            btn.setProperty("page", name)
            self.nav_group.addButton(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: transparent;")

        self.calc_tab = CalculatorTab()
        self.settings_tab = SettingsTab()

        self.stacked_widget.addWidget(self.calc_tab)
        self.stacked_widget.addWidget(self.settings_tab)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget, 1)

        self.nav_group.buttonClicked.connect(self.switch_page)
        self.settings_tab.language_changed.connect(self.change_language)
        self.settings_tab.theme_changed.connect(self.change_theme)

        self.nav_group.buttons()[0].setChecked(True)
        self.stacked_widget.setCurrentIndex(0)

    def apply_initial_settings(self):
        self.theme_manager.apply(QApplication.instance(), self.current_theme)
        self.settings_tab.set_language(self.current_lang)
        self.settings_tab.set_theme(self.current_theme)
        self.update_direction()

    def switch_page(self, button):
        pages = {'calculator': 0, 'settings': 1}
        page = button.property("page")
        self.stacked_widget.setCurrentIndex(pages[page])

    def change_language(self, lang_code):
        app = QApplication.instance()
        if self.current_lang != 'en' and self.current_lang in self.language_manager.translators:
            app.removeTranslator(self.language_manager.translators[self.current_lang])
        
        self.current_lang = lang_code
        if lang_code != 'en' and lang_code in self.language_manager.translators:
            self.language_manager.install(app, lang_code)
        
        self.retranslate_ui()
        self.update_direction()

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.theme_manager.apply(QApplication.instance(), theme_name)

    def update_direction(self):
        direction = Qt.LayoutDirection.RightToLeft if self.current_lang == 'fa' else Qt.LayoutDirection.LeftToRight
        QApplication.instance().setLayoutDirection(direction)
        self.setLayoutDirection(direction)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("GCD & LCM Calculator"))
        self.calc_tab.retranslate()
        self.settings_tab.findChild(QLabel).setText(self.tr("Settings"))
        lang_group = self.settings_tab.findChild(QGroupBox)
        if lang_group:
            lang_group.setTitle(self.tr("Language"))
        theme_group = self.settings_tab.findChildren(QGroupBox)[1]
        if theme_group:
            theme_group.setTitle(self.tr("Theme"))

        nav_buttons = [b for b in self.findChildren(QPushButton) if b.property("page")]
        texts = [self.tr("Calculator"), self.tr("Settings")]
        for btn, text in zip(nav_buttons, texts):
            btn.setText(text)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    font = QFont("Segoe UI", 11)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# Advanced features
class HistoryWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(220)
        self.setStyleSheet("""
            background-color: palette(base);
            border: 2px solid palette(mid);
            border-radius: 16px;
            margin: 10px;
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)

        title = QLabel(self.tr("Calculation History"))
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: palette(text);")
        layout.addWidget(title)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
                color: palette(text);
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid palette(mid);
            }
            QListWidget::item:hover {
                background-color: palette(alternateBase);
            }
        """)
        layout.addWidget(self.history_list)

    def add_entry(self, operation, a, b, result):
        text = f"{operation}({a}, {b}) = {result}"
        self.history_list.addItem(text)
        self.history_list.scrollToBottom()

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

class ExtraThemes:
    @staticmethod
    def purple():
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor(60, 0, 100))
        p.setColor(QPalette.ColorRole.Base, QColor(80, 20, 120))
        p.setColor(QPalette.ColorRole.Text, QColor(220, 200, 255))
        p.setColor(QPalette.ColorRole.Button, QColor(100, 40, 140))
        p.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        return p

    @staticmethod
    def green():
        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor(10, 60, 10))
        p.setColor(QPalette.ColorRole.Base, QColor(20, 80, 20))
        p.setColor(QPalette.ColorRole.Text, QColor(180, 255, 180))
        return p

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def export_results(gcd, lcm, path="results.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"GCD: {gcd}\nLCM: {lcm}\n")

# Placeholder for translation files
"""
:/translations/fa.qm
:/translations/zh.qm
:/translations/ru.qm
"""

