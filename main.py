if __name__ == '__main__':
    from YtDownloader import *
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    gc.collect()
    sys.exit(app.exec_())

