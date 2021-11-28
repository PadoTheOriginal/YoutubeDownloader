from PyQt5.QtCore import QThread, pyqtSignal
import webscrapping as wb
import re
import gc
from youtube_dl import YoutubeDL
from pyperclip import paste
import math
from time import sleep


def convert_bytes_to_readable(size_bytes):
   if size_bytes == 0 or size_bytes is None:
       return "0B"

   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return f"{s} {size_name[i]}"


# ""
class Download(QThread):
    str_signal = pyqtSignal(str)
    tuple_signal = pyqtSignal(tuple)

    def __init__(self, url, name, parent, ydl_opts):
        """
        :param url: string
        :param name: string
        :param parent: PyQt5 Object (parent)
        :param ydl_opts: Dictionary
        """

        QThread.__init__(self, parent=parent)
        self.url = url
        self.name = name
        self.ydl_opts = ydl_opts
        self.num = 1
        self.isQueue = True if re.search("list=", url) else False
        self.failed = False


    def run(self):
        self.ydl_opts['progress_hooks'] = [self.progress]
        self.ydl_opts['addmetadata'] = True
        self.ydl_opts["ignoreerrors"] = True #if self.isQueue else False



        with YoutubeDL(self.ydl_opts) as ydl:
            ydl.cache.remove()
            r = ydl.download([self.url])

            if r == 1:
                title = self.name
                status = "Erro"
                data = (title, None, None, None, status)
                self.tuple_signal.emit(data)
                self.failed = True



        if self.failed is False:
            data = (self.name, None, None, None, "Baixado(a)")
            self.tuple_signal.emit(data)

    def progress(self, d):
        """
        {'status': 'downloading',
        'downloaded_bytes': 2048,
        'total_bytes': 191646212,
        'eta': 562,
        'speed': 340816.32248849387,
        '_eta_str': '09:22',
        '_percent_str': '  0.0%',
        '_speed_str': '332.83KiB/s',
        '_total_bytes_str': '182.77MiB'}
        """

        if d["status"] == "downloading":
            title = self.name
            size = convert_bytes_to_readable(d["total_bytes"]) if "total_bytes" in d else convert_bytes_to_readable(d['total_bytes_estimate'])
            speed = convert_bytes_to_readable(d["speed"])
            downloaded = d["downloaded_bytes"]
            status = f"Baixando ({self.num})" if self.isQueue else "Baixando"

            if downloaded:
                downloaded = convert_bytes_to_readable(downloaded)

            data = (title, size, speed, downloaded, status)
            self.tuple_signal.emit(data)
            self.failed = False

        elif d["status"] == "error":
            title = self.name
            status = f"Erro({self.num})" if self.isQueue else "Erro"
            data = (title, None, None, None, status)
            self.tuple_signal.emit(data)
            self.failed = True


        elif d["status"] == "finished":
            title = self.name
            size = None
            speed = None
            p = None
            status = f"Convertendo ({self.num})" if self.isQueue else "Convertendo"
            data = (title, size, speed, p, status)
            self.tuple_signal.emit(data)
            self.num += 1

# ""
def is_link(data):
    regex = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    return re.search(regex, data)

# ""
class DetectClipChanges(QThread):
    str_signal = pyqtSignal(str)
    def __init__(self, parent):
        QThread.__init__(self, parent=parent)


    def run(self):

        last_data = paste()

        while True:

            data = paste()

            if data != last_data:
                if re.search(r"(https://|http://)(www.youtube|youtu.be)(.com|/)", data):
                    self.str_signal.emit(data)

                last_data = paste()



            sleep(0.1)

# ""
class FreeRAM(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent=parent)


    def run(self):
        while True:
            gc.collect()
            sleep(20)

# ""
class SearchLink(QThread):
    str_signal = pyqtSignal(str)
    def __init__(self, url: str, parent):
        QThread.__init__(self, parent=parent)
        self.url = url


    def run(self):
        try:
            title = wb.video_title(self.url)
            self.str_signal.emit(title)
        except Exception as e:
            self.str_signal.emit("error")

# ""
class SearchYt(QThread):
    tuple_signal = pyqtSignal(tuple)
    def __init__(self, name, num, parent):
        QThread.__init__(self, parent=parent)
        self.name = name
        self.num = num


    def run(self):
        text = self.name

        try:
            yttitles, ytlinks, ytthumbnails = wb.yt_search(text, self.num)
            self.tuple_signal.emit((1, (yttitles, ytlinks, ytthumbnails)))

        except Exception as e:
            self.tuple_signal.emit((2, []))
