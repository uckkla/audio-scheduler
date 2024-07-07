from PyQt6.QtCore import QSize, Qt, QTime
from PyQt6.QtGui import QPixmap, QPalette, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QMenu, QHBoxLayout, \
    QGridLayout, QStackedLayout, QPushButton, QTimeEdit, QListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Scheduler")
        self.setFixedSize(500, 400)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout(centralWidget)

        # Time design
        timeLayout = QHBoxLayout()
        self.startTimeEdit = QTimeEdit()
        self.endTimeEdit = QTimeEdit()

        timeLayout.addWidget(self.startTimeEdit)
        timeLayout.addWidget(self.endTimeEdit)
        mainLayout.addLayout(timeLayout)

        # Link design
        self.linkEntry = QLineEdit()
        self.linkEntry.setPlaceholderText("Enter Youtube Link")
        mainLayout.addWidget(self.linkEntry)

        # Schedule/Remove button
        buttonLayout = QHBoxLayout()

        scheduleButton = QPushButton("Schedule")
        removeButton = QPushButton("Remove")

        scheduleButton.clicked.connect(self.ScheduleVideo)
        removeButton.clicked.connect(self.RemoveVideo)

        buttonLayout.addWidget(scheduleButton)
        buttonLayout.addWidget(removeButton)
        mainLayout.addLayout(buttonLayout)

        # Scheduled list
        self.scheduleList = QListWidget()
        mainLayout.addWidget(self.scheduleList)

    def ScheduleVideo(self):
        startTime = self.startTimeEdit.time().toString("HH:mm")
        endTime = self.endTimeEdit.time().toString("HH:mm")
        link = self.linkEntry.text()

        # Check if user inputted link and correct times
        if link and endTime > startTime:
            self.scheduleList.addItem(f"{link} from {startTime} to {endTime}")
            self.linkEntry.clear()

    def RemoveVideo(self):
        self.scheduleList.takeItem(self.scheduleList.currentRow())


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
