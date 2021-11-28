import urllib.request

from PyQt5.QtWidgets import QMessageBox
from mainGUI import *
import os
from _pickle import dump, load
from notifierP import Notification
from threadClasses import *

ytlinks = []
yttitles = []
ytsearches = {}
downloads = {}
threads = []

""" 
- More stuff on menuBar
"""

# ""
class Ui(QtWidgets.QMainWindow, Ui_MainWindow):

    file_name = "/%(title)s.%(ext)s"
    queue_path = ""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": queue_path,
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
        "keepvideo": False
    }

    # ""
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        #uic.loadUi('YtExtraFiles/mainGUI.ui', self)

        self.toggle_window_btn.triggered.connect(self.control_window)
        self.reset_folders_btn.triggered.connect(self.reset_folder_save)
        self.search_btn.clicked.connect(self.get_user_data)
        self.folder_btn.clicked.connect(self.select_folder)
        self.search_input.textChanged.connect(self.check_link)
        self.qualities_box.activated.connect(self.change_quality)
        self.folders_box.activated.connect(self.change_queue_path)
        self.downloadBtn.clicked.connect(self.download_chosen_file)
        self.reset_suggestions_btn.triggered.connect(self.reset_suggestions)
        self.download_widget.hide()

        thread = DetectClipChanges(self)
        thread.str_signal.connect(self.add_value_to_input)
        thread.start()
        threads.append(thread)

        thread_2 = FreeRAM(self)
        thread_2.start()
        threads.append(thread_2)

        self.name = ""
        self.url = ""
        self.index = ""
        self.currentTitle = ""
        self.notification = Notification()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.close_notify)

        self.dirs = []
        self.search_quantity = 5
        self.qualities_index = 6
        self.on_front = False
        self.suggestions = []

        try:
            with open("YtExtraFiles/data.pickle", "rb") as f:
                self.search_quantity, \
                self.dirs,\
                self.queue_path,\
                self.qualities_index,\
                self.on_front, \
                self.suggestions = load(f)

            self.search_spinbox.setValue(self.search_quantity)
            self.qualities_box.setCurrentText(self.qualities_box.itemText(self.qualities_index))
            self.change_quality(self.qualities_index)
            if self.dirs:
                self.folders_box.addItems(self.dirs)

            if self.queue_path:
                self.ydl_opts["outtmpl"] = self.queue_path + self.file_name

            if self.suggestions:
                self.update_suggestions()

            self.folders_box.setCurrentText(self.queue_path)

        except Exception as e:
            print(e)

        if self.on_front:
            self.window_on_front()

        else:
            self.window_on_back()

    # ""
    def closeEvent(self, e):
        if len(threads) > 0:
            self.close_all_threads()

        self.save()

    # ""
    def close_all_threads(self):
        for thread in threads:
            try:
                thread.terminate()

            except:
                pass

    # ""
    def save(self):
        try:
            with open("YtExtraFiles/data.pickle", "wb") as f:
                data = (self.search_spinbox.value(), self.dirs, self.queue_path,
                        self.qualities_index, self.on_front, self.suggestions)
                dump(data, f)


        except:
            pass

    # ""
    def update_suggestions(self):
        completer = QtWidgets.QCompleter(self.suggestions)
        completer.popup().setStyleSheet("background-color: #202020; color: rgb(200, 200, 200);")
        self.search_input.setCompleter(completer)

    # ""
    def reset_suggestions(self):
        self.suggestions = []
        self.update_suggestions()

    # ""
    def window_on_front(self):
        # bring window to top and act like a "normal" window!
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # set always on top flag, makes window disappear
        self.show()  # makes window reappear, but it's ALWAYS on top
        self.toggle_window_btn.setText("Ficar atrás")
        self.on_front = True

    # ""
    def window_on_back(self):
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)  # clear always on top flag, makes window disappear
        self.show()  # makes window reappear, acts like normal window now (on top now but can be underneath if you raise another window)
        self.toggle_window_btn.setText("Ficar na frente")
        self.on_front = False

    # ""
    def control_window(self):
        if self.on_front:
            self.window_on_back()
            return 0

        self.window_on_front()

    # ""
    def notify(self, title, message, timeout=10):
        self.timer.stop()
        self.notification.doubleClick.connect(self.doubleClickedNotify)
        self.notification.set_notify(title, message)
        self.timer.start(timeout*1000)

    # ""
    def active_window(self):
        self.activateWindow()
        self.showNormal()

    # ""
    def close_notify(self):
        try:
            self.notification = Notification()

        except:
            pass

        self.timer.stop()

    # ""
    def doubleClickedNotify(self):
        self.close_notify()
        self.active_window()

    # ""
    def add_value_to_input(self, value):
        self.active_window()
        self.search_input.setText(value)

    # ""
    def check_link(self):
        data = self.search_input.text()

        if is_link(data):
            self.search_btn.setText("Baixar link")
            self.search_spinbox.hide()
            self.download_widget.hide()
            return 0

        self.search_btn.setText("Procurar")
        self.search_spinbox.show()

    # ""
    def download_to_table(self, data):
        downloads_list = list(downloads)
        title, _, _, _, status = data

        if title in downloads_list:
            i = downloads_list.index(title)

            for c, e in enumerate(data):
                self.download_table.setItem(i, c, QtWidgets.QTableWidgetItem(e))

        if status == "Baixado(a)":
            self.notify("Download Terminado", f"{title} Terminou de baixar", timeout=5)
            self.active_window()

        header = self.download_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        #gc.collect()
        
    # ""
    def warning_queue(self):
        self.window_on_back()
        popup = QMessageBox()
        popup.setWindowTitle("Playlist detectada")
        popup.setWindowIcon(QtGui.QIcon("YtExtraFiles/YtDownloader.png"))
        popup.setText("Uma playlist foi detectada, deseja baixar ela inteira?")
        popup.setInformativeText("(Pode haver errors, ou utilizar muita memória)")
        popup.setIcon(QMessageBox.Question)
        popup.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        popup.setDefaultButton(QMessageBox.Yes)
        popup.buttonClicked.connect(self.playlist_handle)
        popup.exec_()

    # ""
    def playlist_handle(self, i):
        if i.text() == "&Yes":
            if self.queue_path == "":
                self.select_folder()

            try:
                self.url = "https://www.youtube.com" + ytsearches[self.currentTitle]
            except:
                self.url = self.url

            self.name = self.currentTitle

            if self.name in downloads:
                old_name = self.name
                n = 1
                while True:
                    if self.name in downloads:
                        self.name = f"({n}) {old_name}"
                    else:
                        break

                    n += 1

            row_position = self.download_table.rowCount()
            self.download_table.insertRow(row_position)
            downloads[self.name] = self.url

            data = (self.name, None, None, None, "Preparando para baixar")
            self.download_to_table(data)
            self.notify("Preparando", "Preparando para baixar", timeout=2)
            thread = Download(self.url, self.name, self, self.ydl_opts)
            thread.tuple_signal.connect(self.download_to_table)
            thread.start()
            threads.append(thread)
            return 0

        self.name = self.currentTitle

        if self.name in downloads:
            old_name = self.name
            n = 1
            while True:
                if self.name in downloads:
                    self.name = f"({n}) {old_name}"
                else:
                    break

                n += 1

        row_position = self.download_table.rowCount()
        self.download_table.insertRow(row_position)
        downloads[self.name] = self.url
        data = (self.name, None, None, None, "Cancelada")
        self.download_to_table(data)

    # ""
    def select_folder(self):
        try:
            home = os.path.join(os.environ["HOMEPATH"], "Desktop")
        except:
            try:
                home = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            except:
                home = ""

        self.window_on_back()
        file_dialog = str(QtWidgets.QFileDialog.getExistingDirectory(caption="Baixar arquivo em...", directory=home))
        if file_dialog:
            self.queue_path = file_dialog
            self.ydl_opts["outtmpl"] = self.queue_path + self.file_name

            if not self.queue_path in self.dirs:
                self.dirs.append(self.queue_path)

            self.folders_box.clear()
            self.folders_box.addItems(self.dirs)
            self.folders_box.setCurrentText(self.queue_path)
            self.save()

    # ""
    def change_queue_path(self, i):
        item = self.folders_box.itemText(i)
        self.queue_path = item
        self.ydl_opts["outtmpl"] = self.queue_path + self.file_name

    # ""
    def download_chosen_file(self):
        global ytsearches
        global downloads

        title = self.searchBox.currentText()

        if re.search("list=", ytsearches[title]):
            self.currentTitle = title
            self.warning_queue()
            return 0

        self.url = "https://www.youtube.com" + ytsearches[title]
        if self.queue_path == "":
            self.select_folder()

        if self.queue_path != "":

            if title in downloads:
                old_name = title
                n = 1
                while True:
                    if title in downloads:
                        title = f"({n}){old_name}"
                    else:
                        break

                    n += 1

                ytsearches[title] = ytsearches[old_name]

            row_position = self.download_table.rowCount()
            self.download_table.insertRow(row_position)
            downloads[title] = self.url

            data = (title, None, None, None, "Preparando para baixar")
            self.download_to_table(data)
            self.notify("Preparando", "Preparando para baixar", timeout=2)
            thread = Download(self.url, title, self, self.ydl_opts)
            thread.tuple_signal.connect(self.download_to_table)
            thread.start()
            threads.append(thread)

    # ""
    def searches_show(self, info):
        global yttitles
        global ytlinks
        global ytsearches

        i, data = info
        if i == 2:
            self.window_on_back()
            popup = QMessageBox()
            popup.setWindowTitle("Erro")
            popup.setWindowIcon(QtGui.QIcon("YtExtraFiles/YtDownloader.png"))
            popup.setText("Ouve algum problema na sua conecção")
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            return 0

        yttitles, ytlinks, ytthumbnails = data
        for title, link in zip(yttitles, ytlinks):
            ytsearches[title] = link

        self.download_widget.show()

        for title, url in zip(yttitles, ytthumbnails):
            with urllib.request.urlopen(url) as response:
                data = response.read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(data)
            icon = QtGui.QIcon(pixmap)
            self.searchBox.addItem(icon, title)

    # ""
    def link_show(self, info):
        if info == "error":
            self.window_on_back()
            popup = QMessageBox()
            popup.setWindowTitle("Erro")
            popup.setWindowIcon(QtGui.QIcon("YtExtraFiles/YtDownloader.png"))
            popup.setText("Ouve algum problema na sua conecção")
            popup.setIcon(QMessageBox.Critical)
            popup.exec_()
            return 0

        elif is_link(info) and not re.search(r"(https://)(www\.youtube\.com/watch|youtu\.be/(?!v/).*)", info):
            self.currentTitle = info
            self.name = self.currentTitle

            if self.queue_path == "":
                self.select_folder()

            if self.queue_path != "":

                if self.name in downloads:
                    old_name = self.name
                    n = 1
                    while True:
                        if self.name in downloads:
                            self.name = f"({n}){old_name}"
                        else:
                            break

                        n += 1


                row_position = self.download_table.rowCount()
                self.download_table.insertRow(row_position)
                downloads[self.name] = self.url

                data = (self.name, None, None, None, "Preparando para baixar")
                self.download_to_table(data)
                self.notify("Preparando", "Preparando para baixar", timeout=2)
                thread = Download(self.url, self.name, self, self.ydl_opts)
                thread.tuple_signal.connect(self.download_to_table)
                thread.start()
                threads.append(thread)

            return 0


        self.currentTitle = info
        self.name = self.currentTitle

        if re.search("list=", self.url):
            self.warning_queue()

        else:
            if self.queue_path == "":
                self.select_folder()

            if self.queue_path != "":

                if self.name in downloads:
                    old_name = self.name
                    n = 1
                    while True:
                        if self.name in downloads:
                            self.name = "(%s) %s" % (n, old_name)
                        else:
                            break

                        n += 1

                row_position = self.download_table.rowCount()
                self.download_table.insertRow(row_position)
                downloads[self.name] = self.url

                data = (self.name, None, None, None, "Preparando para baixar")
                self.download_to_table(data)
                thread = Download(self.url, self.name, self, self.ydl_opts)
                thread.tuple_signal.connect(self.download_to_table)
                thread.start()
                threads.append(thread)

    # ""
    def get_user_data(self):
        global ytsearches
        global yttitles
        global ytlinks

        text = self.search_input.text()
        if text not in self.suggestions:
            self.suggestions.append(text)
            self.update_suggestions()

        self.search_input.setText("")

        if text.replace(" ", "") == "":
            return 0

        self.download_widget.hide()

        if is_link(text):
            self.url = text

            self.notify("Verificando", "Verificando se há como baixar", timeout=3)
            if re.search(r"(https://)(www\.youtube\.com/watch|youtu\.be/(?!v/).*)", self.url):
                if not text.startswith("https://"):
                    self.url = "https://" + text

                else:
                    self.url = text


                thread = SearchLink(self.url, self)
                thread.str_signal.connect(self.link_show)
                thread.start()
                threads.append(thread)


            else:

                self.link_show(self.url)

            return 0

        yttitles, ytlinks, ytsearches = [], [], {}
        self.searchBox.clear()
        self.notify(title="Pesquisando", message=f"Pesquisando {text}", timeout=3)

        thread = SearchYt(text, self.search_spinbox.value(), self)
        thread.tuple_signal.connect(self.searches_show)
        thread.start()
        threads.append(thread)

    # ""
    def reset_folder_save(self):
        self.queue_path = ""
        self.dirs = []
        self.folders_box.clear()
        self.save()

    # ""
    def remove_pp(self):
        self.ydl_opts["outtmpl"] = self.queue_path + self.file_name
        try:
            del self.ydl_opts["postprocessors"]

        except:
            pass

    # ""
    def change_quality(self, s):
        self.qualities_index = self.qualities_box.currentIndex()
        if s == 0:
            self.ydl_opts["format"] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            self.remove_pp()

        elif s == 1:
            self.ydl_opts[
                "format"] = 'bestvideo[height<=?1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=?1080][ext=mp4]'
            self.remove_pp()

        elif s == 2:
            self.ydl_opts["format"] = 'bestvideo[height<=?720][ext=mp4]+bestaudio[ext=m4a]/best[height<=?720][ext=mp4]'
            self.remove_pp()

        elif s == 3:
            self.ydl_opts["format"] = 'bestvideo[height<=?480][ext=mp4]+bestaudio[ext=m4a]/best[height<=?480][ext=mp4]'
            self.remove_pp()

        elif s == 4:
            self.ydl_opts["format"] = 'bestvideo[height<=?360][ext=mp4]+bestaudio[ext=m4a]/best[height<=?360][ext=mp4]'
            self.remove_pp()

        elif s == 5:
            self.ydl_opts["format"] = "worst"
            self.remove_pp()

        elif s == 6:
            self.ydl_opts["format"] = "bestaudio/best"
            self.ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
