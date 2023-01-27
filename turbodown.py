import youtube_dl

class Video:
<<<<<<< HEAD
    def __init__(self,url) -> None: 
        self.url = url
        
    def generarnombre(self,codec):
        video_info = youtube_dl.YoutubeDL().extract_info(url = self.url,download=False)
        self.filename = f"{video_info['title']}.{codec}"

    def setMp3(self):
        self.options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        self.generarnombre('mp3')

    def setMp4(self):
        options = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        self.generarnombre('mp4')

    def descargar(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.url])
=======
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
		

>>>>>>> 562ea09453d43a67e7e042dcc41145e781bd5e78

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


#download_ytvid_as_mp3()

def main():
    url = input ("Ingresa la url del video, xfa: ")
    videoyt = Video(url)
    videoyt.setMp3()
    videoyt.descargar()

main()
