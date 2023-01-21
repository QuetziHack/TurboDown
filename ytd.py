import pytube as pt
import sys

class Video:
	def __init__(self,url, codec="mp3"):
		self.url=url
		self.codec=codec
		self.video=pt.YouTube(input("Ingresa la url del video: ")

	def descarga_mp3(self):
		mp3 = self.video.streams.

