import numpy as np
import pyqtgraph as pg
import librosa
import sounddevice as sd

class WaveWidget(pg.PlotWidget):
	def __init__(self, parent=None, background='default', **kargs):
		super(WaveWidget, self).__init__(parent, background, **kargs)
		self.setLabel('left', 'Value', units='V')
		self.setLabel('bottom', 'Time', units='s')
		self.setLimits(xMin=0, yMin=-1, yMax=1)
		self.setMouseEnabled(y=False)


	def setSource(self, path, sr):
		self.path = path
		self.sr = sr

		self.wave, self.sr = librosa.load(self.path, sr=self.sr)
		x = np.arange(len(self.wave)) / float(self.sr)
		self.plot(y=self.wave, x=x)
		self.setLimits(xMax=max(x))
		print x



