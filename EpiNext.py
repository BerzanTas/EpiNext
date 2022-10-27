from time import sleep
from requests_html import HTMLSession
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(700, 600)
        MainWindow.setAccessibleName("")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 130, 660, 350))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(18)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")

        self.labelepisodeinfo = QtWidgets.QLabel(self.frame)
        self.labelepisodeinfo.setGeometry(QtCore.QRect(10, 70, 650, 220))
        self.labelepisodeinfo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelepisodeinfo.setObjectName("labelepisodeinfo")
        self.labelepisodeinfo.setFont(QtGui.QFont("Segoe Print", 14))

        self.labelshowname = QtWidgets.QLabel(self.frame)
        self.labelshowname.setGeometry(QtCore.QRect(10, 10, 650, 50))
        self.labelshowname.setAlignment(QtCore.Qt.AlignCenter)
        self.labelshowname.setObjectName("labelshowname")

        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setEnabled(False)
        self.nextButton.setGeometry(QtCore.QRect(350, 480, 100, 40))
        self.nextButton.setObjectName("nextButton")

        self.prevButton = QtWidgets.QPushButton(self.centralwidget)
        self.prevButton.setEnabled(False)
        self.prevButton.setGeometry(QtCore.QRect(240, 480, 100, 40))
        self.prevButton.setObjectName("prevButton")

        self.searchbutton = QtWidgets.QPushButton(self.centralwidget)
        self.searchbutton.setGeometry(QtCore.QRect(530, 20, 90, 30))
        self.searchbutton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchbutton.setObjectName("searchbutton")

        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(250, 50, 90, 30))
        self.addButton.setObjectName("addbutton")

        self.removeButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeButton.setGeometry(QtCore.QRect(350, 50, 90, 30))
        self.removeButton.setObjectName("removebutton")

        self.titleBox = QtWidgets.QComboBox(self.centralwidget)
        self.titleBox.setGeometry(QtCore.QRect(160, 20, 360, 30))
        self.titleBox.setEditable(True)
        self.titleBox.setCurrentText("")
        self.titleBox.setObjectName("titleBox")
        self.titleBox.addItem("")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 20))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.labelepisodeinfo.setText("Welcome!\nIn this program you can check for\n the next airing date of your favourite TV Series!\nWarning:\nProgram does not work for Tv series that has been ended")
        self.labelepisodeinfo.setWordWrap(True)

        self.retranslateUi(MainWindow)
        self.titleBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Add items to titlebox
        with open("titles.txt", "r") as f:
            titlesList = f.read()

        titlesList = titlesList.split(",")
        del(titlesList[0]) #This code gets rid of the first comma, because it is causing an empty row in combobox.
        self.titleList = titlesList        
        self.titleBox.addItems(titlesList)

        #Connecting button with methods
        self.addButton.clicked.connect(self.addToList)
        self.removeButton.clicked.connect(self.removeFromList)
        self.searchbutton.clicked.connect(self.setText)
        self.prevButton.clicked.connect(self.prevEpisode)
        self.nextButton.clicked.connect(self.newEpisode)


        #Button description
        self.addButton.setToolTip("Write the Tv series name and click this button\nto add it to the list")
        self.removeButton.setToolTip("Write or choose the Tv series name and click this button\nto remove it from the list")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EpiNext"))
        self.searchbutton.setText(_translate("MainWindow", "Search"))
        self.addButton.setText(_translate("MainWindow", "Add To List"))
        self.titleBox.setItemText(0, _translate("MainWindow", "Write or choose a title"))
        self.nextButton.setText(_translate("MainWindow", "Next Episode"))
        self.prevButton.setText(_translate("MainWindow", "Prev Episode"))
        self.removeButton.setText(_translate("MainWindow", "Remove"))
        
    #This method is responsible for adding items to titleBox and to the titles.txt
    def addToList(self):

        #Here we check if the title already exists
        with open("titles.txt", "r") as d:
            dupcheck = d.read()
            dupcheck = dupcheck.split(",")
        currentText = self.titleBox.currentText()

        if str(currentText) not in dupcheck and str(currentText) != "Write or choose a title":
            self.titleBox.addItem(currentText)
            with open("titles.txt", "a") as f:
                f.write("," + currentText)
                

    #This code does the opposite of addToList().
    def removeFromList(self):

        currentText = self.titleBox.currentText()
        index1 = self.titleBox.findText(currentText)

        with open("titles.txt", "r") as f:
            current_titles = f.read()
            
        current_titles = current_titles.replace(f",{currentText}","")

        with open("titles.txt", "w") as f:
            f.write(current_titles)

        self.titleBox.removeItem(index1)

    #Scrapes show info from the website.
    def getShow(self):

        given_name = self.titleBox.currentText().replace(" ", "-") #Changes the user input for the url search.
    
        self.url = f'https://next-episode.net/{given_name}'
        self.session = HTMLSession()
        self.r = self.session.get(self.url)
        self.r.html.render(sleep=1)
        
            
        
    #Try's to display show name on the screen, if failed, error window pops out.
    def setText(self):
        
        self.getShow()

        try:
            self.show_name = str(self.r.html.find('div#showname_addremovestring div#show_name', first = True).text).upper()
            self.labelshowname.setText(self.show_name)
            self.newEpisode() #We call the newEpisode method so it displays new episode information on screen by default.
        except:
            wrong_name = self.titleBox.currentText()
            self.labelshowname.clear()
            self.labelepisodeinfo.clear()
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
            self.errorPopup(f"Wrong Title!\nCheck if '{wrong_name}' is correct!")

        

    #Takes information about the new episode from the HTML code.
    def newEpisode(self):
        try:
            self.next_episode_info = self.r.html.find('div#next_episode', first = True).text
            self.next_episode_info = str(self.next_episode_info)
            self.next_episode_info = self.next_episode_info.replace("Summary:", "").replace("Episode Summary", "") #I don't want the summary, so I replace it with nothing
        except:
            self.next_episode_info = "NO UPCOMING EPISODES:("


        self.labelepisodeinfo.setText(self.next_episode_info)
        self.prevButton.setEnabled(True)
        self.nextButton.setEnabled(False)
       
    #Takes information about the previous episode. 
    def prevEpisode(self):
        try:
            self.previous_episode_info = self.r.html.find('div#previous_episode', first = True).text
            self.previous_episode_info = str(self.previous_episode_info)
            self.previous_episode_info = self.previous_episode_info.replace("Summary:", "").replace("Episode Summary", "")
        except:
            self.previous_episode_info = "CAN'T FIND INFORMATION\nABOUT PREVIOUS EPISODE!"

        self.labelepisodeinfo.setText(self.previous_episode_info)
        self.prevButton.setEnabled(False)
        self.nextButton.setEnabled(True)



    #If user input is unknowed by the website, then error window occurs.
    def errorPopup(self, errorname):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ups!")
        msg.setText(errorname)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setStandardButtons(QtWidgets.QMessageBox.Retry|QtWidgets.QMessageBox.Cancel)
        x = msg.exec_()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
