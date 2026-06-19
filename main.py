import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QSizePolicy,
)
from data_handling import GameDb
from parser import OutcomeParser
from models import Paragraph
import game_state

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.gamedb = GameDb()
        self.outcomeParser = OutcomeParser()
        current_paragraph_id = 1 #game_state.getValue("CURRENT_PARAGRAPH_ID")
        self.current_paragraph = self.setParagraph(current_paragraph_id)
        
        self.setWindowTitle("Simple Text Adventure Game Engine (STAGE) - Proof of Concept")
        self.resize(1200, 800)

        # Central image area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.setCentralWidget(self.image_label)

        # Bottom dock widget
        dock = QDockWidget("Controls", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setTitleBarWidget(QWidget())

        dock_content = QWidget()
        layout = QVBoxLayout(dock_content)

        # Text field (~5 visible lines)
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setEnabled(False)

        font_metrics = self.text_display.fontMetrics()
        self.text_display.setFixedHeight(
            font_metrics.lineSpacing() * 5 + 20
        )

        layout.addWidget(self.text_display)

        #max five vertical buttons
        self.buttons = []
        for i in range(5):
            button = QPushButton()
            button.hide()

            button.clicked.connect(self.answer_clicked)

            layout.addWidget(button)
            self.buttons.append(button)

        layout.addStretch()

        dock.setWidget(dock_content)

        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            dock
        )

        #dock approx. 1/3 of window height
        self.resizeDocks(
            [dock],
            [260],  # ~1/3 of 800px window
            Qt.Orientation.Vertical
        )
        
        self.display()

    def answer_clicked(self):
        button = self.sender()

        outcome_str = button.property("outcome_str")
        next_paragraph_id = button.property("next_paragraph_id")
        self.outcomeParser.parseOutcomeText(outcome_str)
        current_paragraph_id = next_paragraph_id
        
        self.current_paragraph = self.setParagraph(current_paragraph_id)

        self.display()
        
    def setParagraph(self, id):
        return Paragraph(
                id,
                self.gamedb.getParagraphData(id),
                self.gamedb.getParagraphAdditionalTexts(id),
                self.gamedb.getParagraphChoices(id)
            )

    def display(self):
        self.text_display.setPlainText(str(self.current_paragraph))

        # Hide all buttons first
        for button in self.buttons:
            button.hide()

        # Populate buttons with answers
        for button, choice in zip(self.buttons, self.current_paragraph.visible_choices):
            button.setText(choice.base_text)

            button.setProperty("outcome_str", choice.outcome)
            button.setProperty("next_paragraph_id", choice.paragraph_id_next)

            button.show()
        
        self.setImage()
            
    def setImage(self):
        # Replace with image
        img = self.current_paragraph.img
        pixmap = QPixmap(f"img\\{img}.png")

        if not pixmap.isNull():
            self.image_label.setPixmap(
                pixmap.scaled(
                    540,
                    1200,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            self.image_label.setText("Image placeholder")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())