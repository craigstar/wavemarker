import numpy as np
import pyqtgraph as pg
import librosa
# import sounddevice as sd
from wavePlayer import WavePlayer


class WaveWidget(pg.PlotWidget):
	def __init__(self, parent=None, background='default', **kargs):
		super(WaveWidget, self).__init__(parent, background, **kargs)
		
		self.setLimits(xMin=0, yMin=-1, yMax=1)
		self.setMouseEnabled(y=False)
		self.setLabel('left', 'Value', units='V')
		self.setLabel('bottom', 'Time', units='ms')
		self.play_line = self.addLine(x=0, pen='r', name='play_line')
		self.play_line.setZValue(1)
		self.player = WavePlayer(self)
		self.player.start()
		self.input_widget = None
		self.start_line = None
		self.current_rect = None
		self.current_text = None
		self.rects = []
		self.texts = []

	def setSource(self, path, sr):
		self.path = path
		self.sr = sr
		self.scale = 1000

		self.wave, self.sr = librosa.load(path, sr=sr)
		x = np.arange(len(self.wave)) / float(self.sr) * self.scale
		self.setLimits(xMax=max(x))
		self.wave_plot = self.plot(y=self.wave, x=x)
		self.wave_plot.setZValue(0)
		self.player.setSource(self.wave, self.sr, self.scale)

	def mouseDoubleClickEvent(self, event):
		super(WaveWidget, self).mouseDoubleClickEvent(event)
		
		x = self.mapToView(event.pos()).x()
		if not self.start_line and not self.current_rect:
			self.start_line = self.addLine(x=x, pen='g', name='start_line', movable=True)
		elif not self.current_rect:
			start = self.start_line.value()
			self.current_rect = pg.LinearRegionItem(values=[start, x], brush=(0,255,0, 100))
			self.addItem(self.current_rect)
			self.removeItem(self.start_line)
			self.start_line = None
			self.player.setPlayRange((start, x))
		else:
			left, right = self.current_rect.getRegion()
			if x < left:
				self.current_rect.setRegion((x, right))
				self.player.setPlayRange((x, right))
			elif x > right:
				self.current_rect.setRegion((left, x))
				self.player.setPlayRange((left, x))
			else:
				self.setWaveLabel()

	def setWaveLabel(self):
		if not self.input_widget:
			return
		self.input_widget.setDisabled(False)
		self.input_widget.setFocus()

	def pushRect(self):
		if not self.input_widget.text():
			return
		self.current_rect.setMovable(False)
		self.current_rect.setBrush((0,0,255, 100))
		
		left, right = self.current_rect.getRegion()
		mid = (left + right) / 2
		self.current_text = pg.TextItem(text=self.input_widget.text(), color='r', anchor=(0.5, 0.5))
		self.current_text.setPos(mid, 0)
		self.addItem(self.current_text)

		self.rects.append(self.current_rect)
		self.texts.append(self.current_text)
		self.current_rect = None
		self.current_text = None

		self.input_widget.clear()
		self.input_widget.clearFocus()

	def setLabelInput(self, input_widget):
		self.input_widget = input_widget
		self.input_widget.editingFinished.connect(self.on_focus_out)
		self.input_widget.returnPressed.connect(self.pushRect)

	def on_focus_out(self):
		self.input_widget.setDisabled(True)

	def undoLabel(self):
		if self.texts:
			self.removeItem(self.texts.pop())
		if self.rects:
			self.removeItem(self.rects.pop())

	def clearLabel(self):
		while self.texts:
			self.removeItem(self.texts.pop())

		while self.rects:
			self.removeItem(self.rects.pop())

	def play(self, pause):
		self.player.play(pause)





