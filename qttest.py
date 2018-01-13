import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QSettings
from PyQt5.QtGui import QIcon
from waveWidget import WaveWidget

class PicButton(QPushButton):
	def __init__(self, pic_name, parent=None):
		super(PicButton, self).__init__('', parent)
		self.setIcon(QIcon(pic_name))


class App(QMainWindow):
	def __init__(self):
		super(App, self).__init__()
		self.left = 100
		self.top = 100
		self.title = 'Wave Spliter'
		self.width = 840
		self.height = 400
		self.pause = True
		self.initUI()
		self.move_center()
		self.load_settings()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.inputBtn = PicButton('./icons/wave.png', self)
		self.inputBtn.clicked.connect(self.on_inputBtn_clicked)
		self.inputLine = QLineEdit()
		inputLayout = QHBoxLayout()
		inputLayout.addWidget(self.inputLine)
		inputLayout.addWidget(self.inputBtn)

		self.outputBtn = PicButton('./icons/label.png', self)
		self.outputBtn.clicked.connect(self.on_outputBtn_clicked)
		self.outputLine = QLineEdit()
		outputLayout = QHBoxLayout()
		outputLayout.addWidget(self.outputLine)
		outputLayout.addWidget(self.outputBtn)


		self.lableInput = QLineEdit(self)
		self.lableInput.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed))
		self.undoBtn = PicButton('./icons/undo.png', self)
		self.undoBtn.clicked.connect(self.on_undoBtn_clicked)
		self.playBtn = PicButton('./icons/play.png', self)
		self.playBtn.clicked.connect(self.on_playBtn_clicked)
		self.clearBtn = PicButton('./icons/clear.png', self)
		self.clearBtn.clicked.connect(self.on_clearBtn_clicked)
		playLayout = QVBoxLayout()
		playLayout.addWidget(self.lableInput)
		playLayout.addWidget(self.playBtn)
		playLayout.addWidget(self.undoBtn)
		playLayout.addWidget(self.clearBtn)

		self.waveWidget = WaveWidget(self, background='default', name='Wave Widget')
		self.waveWidget.setMinimumHeight(350)
		self.waveWidget.setStyleSheet("background-color:black;")
		self.waveWidget.setLabelInput(self.lableInput)
		self.waveWidget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))		

		mediaLayout = QHBoxLayout()
		mediaLayout.addWidget(self.waveWidget)
		mediaLayout.addLayout(playLayout)


		self.forwardBtn = PicButton('./icons/forward.png', self)
		self.backwardBtn = PicButton('./icons/back.png', self)
		self.slider = QSlider(Qt.Horizontal)
		self.leftLabel = QLabel('0:00')
		self.rightLabel = QLabel('5:00')
		timeLayout = QHBoxLayout()
		timeLayout.addWidget(self.backwardBtn)
		timeLayout.addWidget(self.leftLabel)
		timeLayout.addWidget(self.slider)
		timeLayout.addWidget(self.rightLabel)
		timeLayout.addWidget(self.forwardBtn)

		self.quitBtn = QPushButton('Quit', self)
		self.quitBtn.clicked.connect(self.close)
		quitLayout = QHBoxLayout()
		quitLayout.addWidget(self.quitBtn)
		quitLayout.addStretch()

		mainLayout = QVBoxLayout()
		mainLayout.addLayout(inputLayout)
		mainLayout.addLayout(outputLayout)
		mainLayout.addLayout(mediaLayout)
		mainLayout.addLayout(timeLayout)
		mainLayout.addLayout(quitLayout)


		self.centralWidget = QWidget()
		self.centralWidget.setLayout(mainLayout)
		self.setCentralWidget(self.centralWidget)

		self.statusBar().showMessage('Ready')
		self.show()

	def on_inputBtn_clicked(self):
		fname, ftype = QFileDialog.getOpenFileName(self, 'Open file', './',"Audio files (*.m4a)")
		if fname:
			self.inputLine.setText(fname)
			self.save_settings()
			self.load_wave()

	def on_outputBtn_clicked(self):
		fname = QFileDialog.getExistingDirectory(self, 'Select directory', './')
		if fname:
			self.outputLine.setText(fname)
			self.save_settings()

	def move_center(self):        
		frame = self.frameGeometry()
		ctr = QDesktopWidget().availableGeometry().center()
		frame.moveCenter(ctr)
		self.move(frame.topLeft())

	def on_playBtn_clicked(self):
		self.pause = not self.pause
		# self.waveWidget.play(True)

	def on_undoBtn_clicked(self):
		self.waveWidget.undoLabel()

	def on_clearBtn_clicked(self):
		self.waveWidget.clearLabel()

	def load_settings(self):
		settings = QSettings('star', 'wavemarker', self)
		input_file = settings.value('input_file', type=str)
		output_file = settings.value('output_file', type=str)
		self.inputLine.setText(input_file)
		self.outputLine.setText(output_file)
		self.load_wave()

	def save_settings(self):
		settings = QSettings('star', 'wavemarker', self)
		settings.setValue('input_file', self.inputLine.text())
		settings.setValue('output_file', self.outputLine.text())

	def load_wave(self):
		if self.inputLine.text():
			self.waveWidget.setSource(self.inputLine.text(), 48000)

	# def closeEvent(self, event):
	# 	reply = QMessageBox.question(self, 'Message',
	# 		"Are you sure to quit?", QMessageBox.Yes | 
	# 		QMessageBox.No, QMessageBox.No)

	# 	if reply == QMessageBox.Yes:
	# 		event.accept()
	# 	else:
	# 		event.ignore()  


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = App()
	sys.exit(app.exec_())