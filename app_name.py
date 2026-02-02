#Libralis
import shutil
import pathlib
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication, QPushButton, QLabel,QFileDialog
from PySide6 import QtCore, QtWidgets, QtGui
import os
from PySide6.QtCore import QThread

#Main class
class App(QtWidgets.QWidget, QtCore.QThread):
    #__init__
    def __init__(self):
        super().__init__()
        #none direction
        self.direction = ""
        #creating thread
        self.thread = QtCore.QThread()
        #Initialization UI
        self.UI()
        self.dark_theme()
    
    #Layout
    def UI(self):
        
        #Ui components
        self.progressbar = QtWidgets.QProgressBar(value=0, maximum=100)
        self.direction_button = QtWidgets.QPushButton("Choose directory")
        self.copy_button = QtWidgets.QPushButton("Copy")
        self.label = QtWidgets.QLabel("choose direction",
                                     alignment=QtCore.Qt.AlignCenter)
        #creating layout
        self.layout = QtWidgets.QVBoxLayout(self)
        #adding widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progressbar)
        self.layout.addWidget(self.direction_button)
        self.layout.addWidget(self.copy_button)
        #button clicked
        if not self.thread.isRunning():
            self.copy_button.clicked.connect(self.Clone_thread)
            #self.copy_button.clicked.connect(self.Clone_thread)
        self.direction_button.clicked.connect(self.get_direction)
        
    def dark_theme(self):
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: white;}""")
        self.direction_button.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: white;}""")
        self.setStyleSheet("background-color:#111111")
    #Runing and starting cloning thread
    @QtCore.Slot()
    def Clone_thread(self):
        self.label.setText("Coping..")
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
            #creating PATHS.txt
            file_name = "PATHS.txt"
            file_path = os.path.join(destination, file_name)

            with open(file_path, "w") as f:
                f.write("""This file contain path to copied files
             
-Desktop_theme:
/usr/share/plasma/desktoptheme/

-Look and feel:
.local/share/plasma/look-and-feel/

-Config files:
.config/

-Icons:
.local/share/icons/
                    
-Plasmoids:
.local/share/plasma/plasmoids/""")
            self.progressbar.setValue(5)
            #coping desktoptheme
            desktoptheme = pathlib.Path("/usr/share/plasma/desktoptheme/")
            desktoptheme_folder = os.path.join(destination, "desktop_theme")
            os.makedirs(desktoptheme_folder, exist_ok=True)
            self.progressbar.setValue(10)
            shutil.copytree(desktoptheme, desktoptheme_folder, dirs_exist_ok=True)
            self.progressbar.setValue(15)

            #coping look and feel 
            look_and_feel_folder = os.path.join(destination, "look-and-feel")
            look_and_feel = pathlib.Path(f"{home_dir}/.local/share/plasma/look-and-feel/")
            os.makedirs(look_and_feel_folder, exist_ok=True)
            self.progressbar.setValue(20)
            shutil.copytree(look_and_feel, look_and_feel_folder, dirs_exist_ok=True)
            self.progressbar.setValue(30)

            #coping config files
            kdeglobals = pathlib.Path(f"{home_dir}/.config/kdeglobals")
            appletsrc = pathlib.Path(f"{home_dir}/.config/plasma-org.kde.plasma.desktop-appletsrc")
            plasmarc = pathlib.Path(f"{home_dir}/.config/plasmarc")
            config_folder = os.path.join(destination, "Config")
            os.makedirs(config_folder, exist_ok=True)
            self.progressbar.setValue(40)
            shutil.copy(kdeglobals, config_folder)
            shutil.copy(plasmarc, config_folder)
            shutil.copy(appletsrc, config_folder)
            self.progressbar.setValue(55)

            #coping icons
            icons  = pathlib.Path(f"{home_dir}/.local/share/icons/")
            icons_folder = os.path.join(destination, "Icons")
            os.makedirs(icons_folder, exist_ok=True)
            self.progressbar.setValue(65)
            shutil.copytree(icons, icons_folder, dirs_exist_ok=True)
            self.progressbar.setValue(80)
            
            #copying plasmoids
            plasmoid = pathlib.Path(f"{home_dir}/.local/share/plasma/plasmoids/")
            plasmoid_folder = os.path.join(destination, "plasmoid")
            os.makedirs(plasmoid_folder, exist_ok=True)
            self.progressbar.setValue(90)
            shutil.copytree(plasmoid, plasmoid_folder, dirs_exist_ok=True)
            self.progressbar.setValue(100)

            
            self.label.setText("Done")
        self.finished.emit()



#starting app
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = App()
    widget.resize(300, 200)
    widget.show()

    sys.exit(app.exec())
    