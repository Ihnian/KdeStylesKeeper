#Libralis
import shutil
import pathlib
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication, QPushButton, QLabel,QFileDialog
from PySide6.QtCore import Slot
from PySide6 import QtCore, QtWidgets, QtGui
import os

#Main class
class App(QtWidgets.QWidget):
    #Layout
    #github bug
    def __init__(self):
        super().__init__()
        #none direction
        self.direction = ""
        #Ui components
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
        #button clicked
        self.direction_button.clicked.connect(self.get_direction)
        self.copy_button.clicked.connect(self.cloning)

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
        print
        desktoptheme = pathlib.Path("/usr/share/plasma/desktoptheme/")
        look_and_feel = pathlib.Path(f"{home_dir}/.local/share/plasma/look-and-feel/")
        kdeglobals = pathlib.Path(f"{home_dir}/.config/kdeglobals")
        plasmarc = pathlib.Path(f"{home_dir}/.config/plasmarc")
        
        desktoptheme_folder = os.path.join(destination, "desktop_theme")
        os.makedirs(desktoptheme_folder, exist_ok=True)
        look_and_feel_folder = os.path.join(destination, "look-and-feel")
        os.makedirs(look_and_feel_folder, exist_ok=True)
        config_folder = os.path.join(destination, "Config")
        os.makedirs(config_folder, exist_ok=True)
        if (destination == ""):
            alert = QtWidgets.QLabel("Please choose folder")
            alert.show()
        
        shutil.copy(kdeglobals, config_folder)
        shutil.copy(plasmarc, config_folder)
        shutil.copytree(desktoptheme, desktoptheme_folder, dirs_exist_ok=True)
        shutil.copytree(look_and_feel, look_and_feel_folder, dirs_exist_ok=True)
        
        self.label.setText("Done")





#starting app
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = App()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
    