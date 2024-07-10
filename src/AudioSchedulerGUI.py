from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QMenu, QHBoxLayout, \
    QPushButton, QTimeEdit, QListWidget, QMessageBox, QFileDialog

from src.AudioPlayer import playAudio, stopAudio
from src.Scheduler import Scheduler


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

        # Link/MP3 option
        selectionLayout = QHBoxLayout()
        self.linkEntry = QLineEdit()
        self.linkEntry.setPlaceholderText("Enter YouTube link or MP3")
        self.mp3Button = QPushButton("Select MP3")

        self.mp3Button.clicked.connect(self.selectMP3)

        selectionLayout.addWidget(self.linkEntry)
        selectionLayout.addWidget(self.mp3Button)
        mainLayout.addLayout(selectionLayout)

        # Schedule/Stop/Remove button
        buttonLayout = QHBoxLayout()
        scheduleButton = QPushButton("Schedule")
        stopButton = QPushButton("Stop")
        removeButton = QPushButton("Remove")

        scheduleButton.clicked.connect(self.scheduleVideo)
        stopButton.clicked.connect(stopAudio)
        removeButton.clicked.connect(self.removeVideo)

        buttonLayout.addWidget(scheduleButton)
        buttonLayout.addWidget(stopButton)
        buttonLayout.addWidget(removeButton)
        mainLayout.addLayout(buttonLayout)

        # Scheduled list
        self.scheduleList = QListWidget()
        mainLayout.addWidget(self.scheduleList)

        # Save/Load button
        dataLayout = QHBoxLayout()
        saveButton = QPushButton("Save")
        loadButton = QPushButton("Load")

        saveButton.clicked.connect(self.saveSchedule)
        loadButton.clicked.connect(self.loadSchedule)

        dataLayout.addWidget(saveButton)
        dataLayout.addWidget(loadButton)
        mainLayout.addLayout(dataLayout)


        # Starts the scheduler
        self.scheduler = Scheduler()
        self.scheduler.startBackgroundTask()

    def scheduleVideo(self):
        startTime = self.startTimeEdit.time().toString("HH:mm")
        endTime = self.endTimeEdit.time().toString("HH:mm")
        audioPath = self.linkEntry.text()

        # Check if user inputted link and correct times
        if audioPath and endTime > startTime:
            self.scheduleList.addItem(f"{audioPath} from {startTime} to {endTime}")
            self.scheduler.addAudio(audioPath, startTime, endTime)
            self.linkEntry.clear()
        else:
            QMessageBox.critical(self, "Invalid Input", "Please enter a valid youtube link and time.")

    def removeVideo(self):
        item = self.scheduleList.takeItem(self.scheduleList.currentRow())

        # Separate info from schedule list so it can be passed
        splitStr = item.text().split(" from ")
        audioPath = splitStr[0]
        timeRange = splitStr[1]
        startTime, endTime = timeRange.split(" to ")

        self.scheduler.removeAudio(audioPath, startTime, endTime)

        print(item.text())

    def saveSchedule(self):
        print("test1")
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Schedule", "", "JSON Files (*.json)")
        print("test2")
        if fileName:
            self.scheduler.saveSchedule(fileName)
            print("test3")

    def loadSchedule(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Schedule", "", "JSON Files (*.json)")
        if fileName:
            self.scheduler.loadSchedule(fileName)
            self.refreshScheduleList()

    def refreshScheduleList(self):
        self.scheduleList.clear()
        for (startTime, endTime), audios in self.scheduler.getScheduledAudios().items():
            for audioPath in audios:
                self.scheduleList.addItem(f"{audioPath} from {startTime} to {endTime}")

    def selectMP3(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select MP3 File", "", "MP3 Files (*.mp3)")
        if fileName:
            self.linkEntry.setText(fileName)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
