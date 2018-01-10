import numpy as np
import pyqtgraph as pg
import librosa
# import sounddevice as sd

class WaveWidget(pg.PlotWidget):
	def __init__(self, parent=None, background='default', **kargs):
		super(WaveWidget, self).__init__(parent, background, **kargs)
		
		self.setLimits(xMin=0, yMin=-1, yMax=1)
		self.setMouseEnabled(y=False)
		self.setLabel('left', 'Value', units='V')
		self.setLabel('bottom', 'Time', units='s')
		self.play_line = self.addLine(x=0, pen='r', name='play_line')
		self.play_line.setZValue(1)


	def setSource(self, path, sr):
		self.path = path
		self.sr = sr

		self.wave, self.sr = librosa.load(path, sr=sr)
		x = np.arange(len(self.wave)) / float(self.sr)
		self.setLimits(xMax=max(x))

		self.wave_plot = self.plot(y=self.wave, x=x)
		self.wave_plot.setZValue(0)

		
	# def play(self, is_pause):



