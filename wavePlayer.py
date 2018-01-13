from PyQt5.QtCore import QThread
import sounddevice as sd

class WavePlayer(QThread):
	def __init__(self, parent=None):
		super(WavePlayer, self).__init__(parent)
		self.wave = []
		self.sr = 48000
		self.scale = 1
		self.is_pause = True
		self.tStart = None
		self.tEnd = None

	def run(self):
		print 'started'

	def setSource(self, wave, sr, scale):
		self.wave = wave
		self.sr = sr
		self.scale = scale

	def play(self, pause):
		if pause:
			sd.stop()
		else:
			start = self.tStart * self.sr / self.scale
			end = self.tEnd * self.sr / self.scale
			sd.play(self.wave[start:end], self.sr)


	def setPlayRange(self, playRange):
		self.tStart, self.tEnd = playRange

	def setStart(self, start):
		self.tStart = start

	def setEnd(self, end):
		self.tEnd = end