from PyQt5 import QtWidgets
import sys
from yt_dlp import YoutubeDL

class Ui(QtWidgets.QMainWindow):
    queue_path = ""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "verbose": False,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "ffmpeg_location": "YtExtraFiles",
        "ignoreerrors": True,
        "continue": True,
        "nooverwrites": True,
        "no_warnings": True,
        "noprogress": True,
        "keepvideo": False
    }

    # ""
    def __init__(self):
        super(Ui, self).__init__()

        self.search_btn = QtWidgets.QPushButton(self)
        self.search_btn.clicked.connect(self.test_download)

    def test_download(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(['https://music.youtube.com/watch?v=MxEjnYdfLXU'])
        
app = QtWidgets.QApplication(sys.argv)

window = Ui()
window.show()

app.exec()

