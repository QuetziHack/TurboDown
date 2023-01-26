import youtube_dl

class Video:
	def __main__(self,url):
		self.url = url
		self.options = {
			'format':'bestaudio/best',
		}

	def genFilename(self,codec):
		self.info = youtube_dl.YoutubeDL().extract_info(self.url,download=False)
		self.filename = f"{self.info['title']}.{codec}"
		self.options['outtmpl']=filename

	

	def downloadmp3(self):
		


def download_ytvid_as_mp3():
    video_url = input("enter url of youtube video:")
    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
    filename = f"{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))
download_ytvid_as_mp3()

