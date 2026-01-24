#Libralis
import shutil
import pathlib
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication, QPushButton, QLabel,QFileDialog
from PySide6 import QtCore, QtWidgets, QtGui
import os


#Main class
class App(QtWidgets.QWidget, QtCore.QThread):
    progress =  QtCore.Signal()
    finished = QtCore.Signal()
    #Layout
    def __init__(self):
        super().__init__()
        #none direction
        self.direction = ""
        self.value = 0
        self.UI()
    
    def UI(self):
        #Ui components
        self.progressbar = QtWidgets.QProgressBar(value=self.value, maximum=100)
        self.direction_button = QtWidgets.QPushButton("Choose directory")
        self.copy_button = QtWidgets.QPushButton("Copy")
        self.label = QtWidgets.QLabel("choose direction",
                                     alignment=QtCore.Qt.AlignCenter)
        #creating layout
        self.layout = QtWidgets.QVBoxLayout(self)
        #adding widgets to layout
        self.layout.addWidget(self.direction_button)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.copy_button)
        self.layout.addWidget(self.progressbar)
        #button clicked
        self.direction_button.clicked.connect(self.get_direction)
        self.copy_button.clicked.connect(self.Clone_thread)

    @QtCore.Slot()
    def Clone_thread(self):
        self.thread = QtCore.QThread()
        self.thread.run = self.cloning
        self.thread.start()
    #geting copy direction
    @QtCore.Slot()
    def get_direction(self):
        self.direction = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "choose folder for copy"
        )
        
    
    #cloning files
    @QtCore.Slot()
    def cloning(self):
        
        home_dir = Path.home()
        destination = self.direction
        if (destination == ""):
            alert = QtWidgets.QLabel("Please choose folder")
            alert.show()
        else:
            desktoptheme = pathlib.Path("/usr/share/plasma/desktoptheme/")
            desktoptheme_folder = os.path.join(destination, "desktop_theme")
            os.makedirs(desktoptheme_folder, exist_ok=True)
            shutil.copytree(desktoptheme, desktoptheme_folder, dirs_exist_ok=True)
            self.value = 15

            look_and_feel_folder = os.path.join(destination, "look-and-feel")
            look_and_feel = pathlib.Path(f"{home_dir}/.local/share/plasma/look-and-feel/")
            os.makedirs(look_and_feel_folder, exist_ok=True)
            shutil.copytree(look_and_feel, look_and_feel_folder, dirs_exist_ok=True)
            self.value = 35

            kdeglobals = pathlib.Path(f"{home_dir}/.config/kdeglobals")
            appletsrc = pathlib.Path(f"{home_dir}/.config/plasma-org.kde.plasma.desktop-appletsrc")
            plasmarc = pathlib.Path(f"{home_dir}/.config/plasmarc")
            config_folder = os.path.join(destination, "Config")
            os.makedirs(config_folder, exist_ok=True)
            shutil.copy(kdeglobals, config_folder)
            shutil.copy(plasmarc, config_folder)
            shutil.copy(appletsrc, config_folder)
            self.value = 70

            icons  = pathlib.Path(f"{home_dir}/.local/share/icons/")
            icons_folder = os.path.join(destination, "Icons")
            os.makedirs(icons_folder, exist_ok=True)
            shutil.copytree(icons, icons_folder, dirs_exist_ok=True)
            self.value = 85
            
            plasmoid = pathlib.Path(f"{home_dir}/.local/share/plasma/plasmoids/")
            plasmoid_folder = os.path.join(destination, "plasmoid")
            os.makedirs(plasmoid_folder, exist_ok=True)
            shutil.copytree(plasmoid, plasmoid_folder, dirs_exist_ok=True)
            self.value = 100
            
            self.label.setText("Done")
        self.finished.emit()





#starting app
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
    