
import csv
import datetime
import time
date_format = '%Y-%m-%d %H:%M:%S'

class Event:
        def __init__(self,ho,mi,da,mo,name,ye,st):
            self.date = datetime.datetime(year=ye,month=mo,day=da,hour=ho,minute=mi)
            self.name = name
            self.st = st
            now = datetime.datetime.now()
            self.diff = (self.date - now)

        def __str__(self):
            return self.date

        @classmethod
        def by_datetime(cls,alter_name,alter_date,st):
            d = datetime.datetime.strptime(alter_date, date_format)
            return cls(d.hour,d.minute,d.day,d.month,alter_name,d.year,st)

        def name_and_date(self):
            return "{}: {}".format(self.name,self.date)

        def show(self):
            return "{}+{}+{}".format(self.name,self.date,self.st)

        def update_diff(self):
            now = datetime.datetime.now()
            self.diff = (self.date - now)

        def show_diff(self):
            self.update_diff()
            now = datetime.datetime.now()
            if self.date < now:
                return "It's already over."
            hours = int(self.diff.seconds/3600)
            minutes =  int((self.diff.seconds - hours*3600)/60)
            return ("{} days, {} hours and {} minutes.".format(self.diff.days,hours,minutes))

        def save_to_file(self,events_file):
            f = open(events_file, "a")
            f.write(self.show()+"\n")
            f.close()


from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QLabel
import sys

class Load(QMainWindow):
    def __init__(self):
        super(Load, self).__init__()
        loadUi("load.ui", self)
        self.load.clicked.connect(self.load_a_file)
        self.give_name.setText("")
        self.events_file = ""

    def load_a_file(self):
        if self.give_name.text()!="":
            self.events_file=self.give_name.text()
            self.events_file+=".txt"
            try:
                existing_file = open(self.events_file,'r')
                existing_file.close()
            except FileNotFoundError:
                new_file=open(self.events_file,'a')
                new_file.writelines(["0", "\n"])
                new_file.close()
            self.move_to_main()
    def move_to_main(self):
        mainwindow = Main(self.events_file)
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        mainwindow.update(False)

class Add(QMainWindow):
        def __init__(self,ef,mainwindow):
            super(Add,self).__init__()
            loadUi("add.ui",self)
            self.mainwindow=mainwindow
            self.number_of_events=0
            self.input_warning.hide()
            self.events_file=ef
            self.go_back.clicked.connect(self.goback)
            self.pushadd.clicked.connect(self.add_event)

        def goback(self):
            widget.setCurrentIndex(widget.currentIndex() - 1)
            self.warning.hide()
            self.input_warning.hide()
            self.mainwindow.update(False)

        def add_event(self):
                self.input_warning.hide()
                self.warning.hide()
                with open(self.events_file, "r") as f1:
                    previous = f1.readlines()
                f1.close()
                events_number = int(previous[0])
                if events_number<9:
                    bad_stuff = ["ł", "Ł", "ę", "ó", "ą", "ś", "ż", "ź", "ć", "ń", 'Ł', "Ę", "Ó", "Ą", "Ś", "Ż", "Ź",
                                 "Ć", "Ń"]
                    na = (self.name.text())
                    da= int(self.day.text())
                    mo = int(self.month.text())
                    ho = int(QtCore.QTime.hour(self.thetime.time()))
                    mi = int(QtCore.QTime.minute(self.thetime.time()))
                    ye=int(self.year.text())
                    st = self.sample.styleSheet()
                    message=""
                    if(da<1 or da>31):
                        message+="Incorrect day.\n"
                    if(mo<1 or mo>12):
                        message+="Incorrect month.\n"
                    if(ho < 0 or ho > 24 or mi < 0 or mi >60):
                        message+="Incorrect time.\n"
                    if na=="":
                        message+="Provide a name.\n"
                    if "," in na or "+" in na:
                        message+="Provide a name without '+' and ','"
                    for stuff in bad_stuff:
                        if stuff in na:
                            message+="I don't speak polish...\n"
                            break
                    if ye<0:
                        message+="Don't try being funny with the year...\n"
                    if message=="":
                        events_number += 1
                        new = [str(events_number), "\n"]
                        counter = 0
                        for stuff in previous:
                            if counter > 0:
                                new.append(stuff)
                            counter += 1
                        with open(self.events_file, "w") as f:
                            f.writelines(new)

                        new_event = Event(ho,mi,da,mo,na,ye,st)
                        new_event.save_to_file(self.events_file)
                    else:
                        self.input_warning.setText(message)
                        self.input_warning.show()
                else:
                    self.warning.show()

class Main(QMainWindow):
        def __init__(self,ef):
            super(Main, self).__init__()
            self.events_file=ef
            loadUi("view.ui", self)
            self.aac.clicked.connect(self.adding)
            self.up.clicked.connect(lambda:self.update(False))
            self.deleting.clicked.connect(lambda:self.update(True))
            self.version.clicked.connect(self.version_info)
            self.version_info_existence = False
            self.author.clicked.connect(self.author_info)
            self.author_info_existence = False

        def author_info(self):
            if self.author_info_existence == False:
                self.author_info_existence = True
                self.info_button2 = QPushButton(widget)
                self.info_button2.setStyleSheet('font: 7pt "MS Shell Dlg 2";color: rgb(255, 255, 255);background-color: rgb(57, 57, 86);')
                self.info_button2.setGeometry(370, 35, 200, 160)
                self.info_button2.setText("Main Designer and\nProgrammer: Ami\n\nOne color scheme\nDesigner: Wik\n\n(press to hide)")
                self.info_button2.show()
                self.info_button2.clicked.connect(self.hide_author_info)


        def version_info(self):
            if self.version_info_existence == False:
                self.version_info_existence = True
                self.info_button = QPushButton(widget)
                self.info_button.setGeometry(30,35,200,160)
                self.info_button.setStyleSheet('font: 7pt "MS Shell Dlg 2";color: rgb(255, 255, 255);background-color: rgb(57, 57, 86);')
                self.info_button.setText("\nEvents file:\n{}\n\n(press to hide)".format(self.events_file))
                self.info_button.show()
                self.info_button.clicked.connect(self.hide_version_info)

        def hide_version_info(self):
            self.version_info_existence = False
            self.info_button.hide()

        def hide_author_info(self):
            self.author_info_existence = False
            self.info_button2.hide()

        def adding(self):
            adding = Add(self.events_file,self)
            widget.addWidget(adding)
            now = datetime.datetime.now()
            widget.setCurrentIndex(widget.currentIndex() + 1)
            adding.warning.hide()
            adding.name.setText("")
            adding.day.setText(str(now.day))
            adding.month.setText(str(now.month))
            adding.year.setText(str(now.year))
            adding.thetime.setTime(QtCore.QTime(now.hour,now.minute))
            adding.s1.clicked.connect(lambda: self.style_sample(adding, adding.s1.styleSheet()))
            adding.s2.clicked.connect(lambda: self.style_sample(adding,adding.s2.styleSheet()))
            adding.s3.clicked.connect(lambda: self.style_sample(adding, adding.s3.styleSheet()))
            adding.s4.clicked.connect(lambda: self.style_sample(adding, adding.s4.styleSheet()))
            adding.s5.clicked.connect(lambda: self.style_sample(adding, adding.s5.styleSheet()))
            adding.s6.clicked.connect(lambda: self.style_sample(adding, adding.s6.styleSheet()))
            adding.s7.clicked.connect(lambda: self.style_sample(adding, adding.s7.styleSheet()))



        def delete_a_button(self,which_one):
            which_one.hide()
            button_text = (which_one.text())
            split_text = button_text.split(":")
            with open(self.events_file,"r") as file:
                events_content = file.readlines()
            events_number = int(events_content[0])
            events_number-=1
            del events_content[0]
            list_of_contents = []
            list_of_contents.append(str(events_number))
            list_of_contents.append("\n")
            for stuff in events_content:
                list_of_contents.append(stuff)
            counter=0
            for content in list_of_contents:
                if counter>1:
                    split_content = content.split("+")
                    if split_text[0]==split_content[0]:
                        list_of_contents[counter] = "\n"
                        break
                counter+=1
            with open(self.events_file,"w") as file_again:
                file_again.writelines(list_of_contents)
            file.close()
            self.update(False)

        def style_sample(self,what,style):
            what.sample.setStyleSheet(style)

        def update(self,do_we_delete):
            classes = []
            buttons = []
            buttons2 = []
            self.deleting.disconnect()
            self.deleting.clicked.connect(lambda: self.update(True))
            self.deleting.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(57, 57, 86);")
            import os
            if os.stat(self.events_file).st_size != 0:
                with open(self.events_file, "r") as file1:
                    reader = csv.reader(file1,delimiter='+')
                    counter = 0
                    buttons2= []
                    for stuff in reader:
                            if len(stuff) > 1 and counter>0:
                                current_name = stuff[0]
                                current_date = stuff[1]
                                current_st = stuff[2]
                                classes.append(Event.by_datetime(current_name, current_date,current_st))
                                buttons.append(QPushButton(widget))
                                buttons2.append("")
                                buttons[-1].setStyleSheet(current_st)
                            counter+=1
                    counter=0
                    classes2 = sorted(classes,key=lambda x:x.date)
                    for u in range(0,len(buttons)):
                        i = classes2.index(classes[u])
                        buttons2[i] = buttons[u]
                    for button in buttons2:
                            buttons2[counter].setGeometry(30, 80 + 100 * counter, 540, 80)
                            buttons2[counter].setText("{}: {}".format(classes2[counter].name, classes2[counter].show_diff()))
                            buttons2[counter].show()
                            counter+=1
                    magic_curtain = QLabel(widget)
                    magic_curtain.setGeometry(30,80+100*counter,540,80)
                    magic_curtain.setStyleSheet('background-color: rgb(85, 85, 127);')
                    magic_curtain.show()
                if do_we_delete is True:
                        time.sleep(0.3)
                        self.deleting.disconnect()
                        self.deleting.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(255, 0, 0);")
                        self.deleting.clicked.connect(lambda: self.update(False))
                        if counter > 0:
                            buttons2[0].clicked.connect(lambda:self.delete_a_button(buttons2[0]))
                        if counter > 1:
                            buttons2[1].clicked.connect(lambda:self.delete_a_button(buttons2[1]))
                        if counter > 2:
                            buttons2[2].clicked.connect(lambda:self.delete_a_button(buttons2[2]))
                        if counter > 3:
                            buttons2[3].clicked.connect(lambda:self.delete_a_button(buttons2[3]))
                        if counter > 4:
                            buttons2[4].clicked.connect(lambda:self.delete_a_button(buttons2[4]))
                        if counter > 5:
                            buttons2[5].clicked.connect(lambda:self.delete_a_button(buttons2[5]))
                        if counter > 6:
                            buttons2[6].clicked.connect(lambda:self.delete_a_button(buttons2[6]))
                        if counter > 7:
                            buttons2[7].clicked.connect(lambda:self.delete_a_button(buttons2[7]))
                        if counter > 8:
                            buttons2[8].clicked.connect(lambda:self.delete_a_button(buttons2[8]))
                else:
                    if len(buttons)>0:
                        buttons[0].clicked.connect(lambda: self.change_view(buttons[0], classes[0]))
                    if len(buttons)>1:
                        buttons[1].clicked.connect(lambda: self.change_view(buttons[1], classes[1]))
                    if len(buttons) > 2:
                        buttons[2].clicked.connect(lambda: self.change_view(buttons[2], classes[2]))
                    if len(buttons) > 3:
                        buttons[3].clicked.connect(lambda: self.change_view(buttons[3], classes[3]))
                    if len(buttons) > 4:
                        buttons[4].clicked.connect(lambda: self.change_view(buttons[4], classes[4]))
                    if len(buttons) > 5:
                        buttons[5].clicked.connect(lambda: self.change_view(buttons[5], classes[5]))
                    if len(buttons) > 6:
                        buttons[6].clicked.connect(lambda: self.change_view(buttons[6], classes[6]))
                    if len(buttons) > 7:
                        buttons[7].clicked.connect(lambda: self.change_view(buttons[7], classes[7]))
                    if len(buttons) > 8:
                        buttons[8].clicked.connect(lambda: self.change_view(buttons[8], classes[8]))
                file1.close()

        def change_view(self,current,new):
            if current.text()==new.name_and_date():
                current.setText("{}: {}".format(new.name, new.show_diff()))
            else:
                current.setText(new.name_and_date())



app = QApplication(sys.argv)
app.setApplicationName("CountdownToSomething")
loadwindow = Load()
widget = QtWidgets.QStackedWidget()
widget.addWidget(loadwindow)
widget.setFixedWidth(600)
widget.setFixedHeight(1000)
widget.show()
app.exec_()

