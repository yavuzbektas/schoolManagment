# ============================================================================
# ==================== Library  ==================================
import sys, os, shutil
import MySQLdb
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, Slot, QDate
from PySide2.QtUiTools import QUiLoader
from xlrd import *
from xlsxwriter import *
import PySide2.QtXml
# ============================================================================
# ==================== import UI files ==================================
from MainWindow import Ui_MainWindow
from Login import Ui_Dialog
import students
import firms
import internship
import quota

# ============================================================================
# ================   GLOBALS    ===================================
global UserID
global student_id
global firm_id
global quota_id
global internship_id
global absent_id
global hostName_db
global port_db
global username_db
global password_db
global database_db
internship_id = 0
quota_id = 0
firm_id = 0
absent_id= 0
# ============================================================================
# ================   SETTINGS     ===================================
BASE_PATH = os.getcwd()
IMAGE_DIR = (BASE_PATH + '\\staticfiles\\bioImages\\')
FILE_DIR = (BASE_PATH + '\\staticfiles\\CVFiles\\')
REPORT_DIR = (BASE_PATH + '\\staticfiles\\Reports\\')
STUDENT_IMAGES_DIR = (BASE_PATH + '\\staticfiles\\student_images\\')
print('Resim Dosyalar : {} klasöründe ve  CV Dosyları : {} kalasöründe yer almaktadır. '.format(IMAGE_DIR, FILE_DIR))

# ============================================================================
# ================ INTERNSHIP DIALOG ===================================
class InternshipWindow(QDialog, internship.Ui_Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(InternshipWindow, self).__init__(parent, *args, **kwargs)
        self.ui = internship.Ui_Dialog()

        self.ui.setupUi(self)
        self.setWindowTitle('Staj Yapan Öğrenci Seçim Seçim Sayfası')
        self.handle_button()
        self.internshipDialog = parent
        self.internship_search()

    def handle_button(self):
        self.ui.tableWidget_7.itemClicked.connect(self.internship_callback)
        self.ui.comboBox_14.currentIndexChanged.connect(self.internship_search)
        self.ui.comboBox_12.currentIndexChanged.connect(self.internship_search)
        self.ui.comboBox.currentIndexChanged.connect(self.internship_search)
        self.ui.pushButton.clicked.connect(self.turn_mainwindow)
        self.ui.pushButton_3.clicked.connect(self.internship_search)
        self.ui.pushButton_2.clicked.connect(lambda x: InternshipWindow.close(self))

    def internship_search(self):
        session = self.ui.comboBox_14.currentText()
        internship_type = self.ui.comboBox_12.currentText()
        filter_val = self.ui.lineEdit.text()
        index_val = str(self.ui.comboBox.currentIndex())
        header = {'0': 'firms.name', '1': 'students.name','2': 'students.surname', '3': 'students.school_number'}
        if filter_val:
            sql = "SELECT internship.id, internship_capacity.session,internship_capacity.internship_type,firms.name," \
                  "students.name,students.surname,internship.notes " \
                  "FROM internship " \
                  "INNER JOIN students ON internship.student_id=students.id " \
                  "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
                  "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
                  "WHERE internship_capacity.session={} AND internship_capacity.internship_type='{}' AND {} LIKE '{}%'".format(
                session, internship_type, header[index_val], filter_val)
        else:
            sql = "SELECT internship.id, internship_capacity.session,internship_capacity.internship_type,firms.name," \
                  "students.name,students.surname,internship.notes " \
                  "FROM internship " \
                  "INNER JOIN students ON internship.student_id=students.id " \
                  "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
                  "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
                  "WHERE internship_capacity.session={} AND internship_capacity.internship_type='{}'".format(
                session, internship_type)


        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_7.setRowCount(0)
            self.ui.tableWidget_7.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_7.rowCount()
                self.ui.tableWidget_7.insertRow(row_pos)
        else:
            self.ui.tableWidget_7.clearContents()

    def internship_callback(self):
        global internship_id
        global student_id
        global quota_id
        global firm_id
        internship_id = self.ui.tableWidget_7.item(self.ui.tableWidget_7.currentRow(), 0).text()

        self.db_connect()
        sql = "SELECT internship_capacity.session,internship_capacity.internship_type,firms.name," \
              "students.name,students.surname, students.tc_no,students.school_number," \
              "students.departure,students.class_level, students.class,students.image_link," \
              "internship.notes,internship.username_id, " \
              "internship_capacity.firm_id,internship.quota_id,internship.student_id, " \
              "internship_capacity.capacity_girl,internship_capacity.capacity_boy " \
              "FROM internship " \
              "INNER JOIN students ON internship.student_id=students.id " \
              "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
              "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
              "WHERE internship.id='{}'".format(internship_id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.ui.lineEdit_98.setText(data[0])
            self.ui.lineEdit_99.setText(data[1])
            self.ui.lineEdit_95.setText(data[2])
            self.ui.lineEdit_104.setText(data[3])
            self.ui.lineEdit_103.setText(data[4])
            self.ui.lineEdit_105.setText(data[6])
            self.ui.lineEdit_106.setText(data[7])
            self.ui.lineEdit_107.setText(str(data[8]))
            self.ui.lineEdit_108.setText(data[9])
            self.ui.textEdit_10.setPlainText(data[11])

            student_id = data[15]
            quota_id = data[14]
            firm_id = data[13]
            self.db.close()
            new_file_name = data[10]
            pic_path = STUDENT_IMAGES_DIR + new_file_name

            picture = QPixmap(pic_path)
            self.ui.label_152.setPixmap(picture)
            self.ui.label_152.setScaledContents(True)
            self.ui.lineEdit_36.setText(str(internship_id))

    def turn_mainwindow(self):
        global internship_id
        self.hide()
        self.internshipDialog.internship_dialog_turn_window(internship_id)


    def db_connect(self):
        global hostName_db
        global port_db
        global username_db
        global password_db
        global database_db

        try:
            self.db = MySQLdb.connect(host=hostName_db, port=port_db, user=username_db, passwd=password_db,
                                      db=database_db,
                                      charset="utf8")
            self.cur = self.db.cursor()
            info = self.db.get_host_info()

            return (info)
        except:
            warning = QMessageBox.warning(self, 'Bağlantı Hatası', 'Lütfen DB Ayarlarını Kontrol Edin', QMessageBox.Ok)

# ============================================================================
# ================ QUOTA DIALOG ===================================
class QuotaWindow(QDialog, internship.Ui_Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(QuotaWindow, self).__init__(parent, *args, **kwargs)
        self.ui = quota.Ui_Dialog()

        self.ui.setupUi(self)
        self.setWindowTitle('Staj Yeri Seçim Seçim Sayfası')
        self.handle_button()
        self.quotaDialog = parent
        self.quota_search()

    def handle_button(self):
        self.ui.tableWidget_7.itemClicked.connect(self.quota_callback)
        self.ui.comboBox_14.currentIndexChanged.connect(self.quota_search)
        self.ui.comboBox_12.currentIndexChanged.connect(self.quota_search)
        self.ui.pushButton.clicked.connect(self.turn_mainwindow)
        self.ui.pushButton_2.clicked.connect(lambda x: QuotaWindow.close(self))

    def quota_search(self):
        session = self.ui.comboBox_14.currentText()
        internship_type = self.ui.comboBox_12.currentText()

        sql = "SELECT internship_capacity.id,internship_capacity.session,internship_capacity.internship_type,firms.name,internship_capacity.capacity_girl,internship_capacity.capacity_boy," \
              "internship_capacity.username_id FROM internship_capacity INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
              "WHERE session='{}' AND  internship_capacity.internship_type='{}'  order by id desc".format(session,
                                                                                                          internship_type)

        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_7.setRowCount(0)
            self.ui.tableWidget_7.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_7.rowCount()
                self.ui.tableWidget_7.insertRow(row_pos)

    def quota_callback(self):
        global quota_id
        global firm_id
        quota_id = self.ui.tableWidget_7.item(self.ui.tableWidget_7.currentRow(), 0).text()
        self.db_connect()
        sql = "SELECT * FROM internship_capacity WHERE id={} order by id DESC".format(quota_id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()
            firm_id = data[3]
            self.ui.lineEdit_25.setText(str(data[0]))
            self.ui.lineEdit_79.setText(data[4])
            self.ui.lineEdit_80.setText(data[5])
            self.ui.lineEdit_77.setText(str(data[6]))
            self.ui.lineEdit_81.setText(str(data[7]))
            self.ui.textEdit_8.setPlainText(data[8])
            self.ui.textEdit_9.setPlainText(data[9])

            self.db.close()
        self.quota_firm_datail_upload(firm_id)

    def turn_mainwindow(self):
        global quota_id
        self.hide()
        self.quotaDialog.quota_dialog_turn_window(quota_id)

    def quota_firm_datail_upload(self, id):

        global firm_id
        self.db_connect()
        sql = "SELECT * FROM firms WHERE id={}".format(id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()
            firm_id = data[0]
            self.ui.lineEdit_69.setText(data[2])
            self.ui.lineEdit_71.setText(data[6])
            self.ui.textEdit_6.setPlainText(data[3])

            self.db.close()
            return data
        else:
            firm_id = 0
            self.db.close()
            return None

    def db_connect(self):
        global hostName_db
        global port_db
        global username_db
        global password_db
        global database_db

        try:
            self.db = MySQLdb.connect(host=hostName_db, port=port_db, user=username_db, passwd=password_db,
                                      db=database_db,
                                      charset="utf8")
            self.cur = self.db.cursor()
            info = self.db.get_host_info()

            return (info)
        except:
            warning = QMessageBox.warning(self, 'Bağlantı Hatası', 'Lütfen DB Ayarlarını Kontrol Edin', QMessageBox.Ok)


# ============================================================================
# ================ FIRMS DIALOG ===================================
class FirmWindow(QDialog, firms.Ui_Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(FirmWindow, self).__init__(parent, *args, **kwargs)
        self.ui = firms.Ui_Dialog()

        self.ui.setupUi(self)
        self.setWindowTitle('Firma Seçim Sayfası')
        self.handle_button()
        self.firmDialog = parent

    def handle_button(self):
        self.ui.pushButton_22.clicked.connect(self.firm_search)
        self.ui.tableWidget_5.itemClicked.connect(self.firm_callback)
        self.ui.pushButton_2.clicked.connect(self.turn_mainwindow)
        self.ui.pushButton_3.clicked.connect(lambda x: FirmWindow.close(self))

    def turn_mainwindow(self):

        self.hide()

        # self.window3=MainWindow()
        self.firmDialog.quota_firm_datail_upload(firm_id)

    def firm_search(self):

        filter_val = self.ui.lineEdit_76.text()
        index_val = str(self.ui.comboBox_10.currentIndex())
        header = {'0': 'name', '1': 'cari_code', '2': 'adress', '3': 'hr_name'}
        if filter_val:
            sql = "SELECT id,cari_code,name,adress,city,state,telephone,fax,web,sector_code,sector_desc,hr_name,hr_telephone,hr_email,notes FROM firms WHERE {} LIKE '{}%'".format(
                header[index_val], filter_val)
        else:
            sql = "SELECT id,cari_code,name,adress,city,state,telephone,fax,web,sector_code,sector_desc,hr_name,hr_telephone,hr_email,notes FROM firms"

        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_5.setRowCount(0)
            self.ui.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_5.rowCount()
                self.ui.tableWidget_5.insertRow(row_pos)

    def firm_callback(self):
        global firm_id  # #selected cell value.
        firm_id = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 0).text()
        caricode = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 1).text()
        name = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 2).text()
        adress = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 3).text()
        city = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 4).text()
        state = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 5).text()
        telephone = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 6).text()
        fax = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 7).text()
        web = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 8).text()
        sectorCode = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 9).text()
        sector_desc = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 10).text()
        hr_name = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 11).text()
        hr_phone = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 12).text()
        hr_email = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 13).text()
        notes = self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 14).text()

        self.ui.lineEdit_45.setText(caricode)
        self.ui.lineEdit_39.setText(name)
        self.ui.textEdit_4.setPlainText(adress)
        self.ui.lineEdit_53.setText(city)
        self.ui.lineEdit_52.setText(state)
        self.ui.lineEdit_46.setText(telephone)
        self.ui.lineEdit_47.setText(fax)
        self.ui.lineEdit_51.setText(web)
        self.ui.lineEdit_50.setText(sectorCode)
        self.ui.lineEdit_55.setText(sector_desc)
        self.ui.lineEdit_48.setText(hr_name)
        self.ui.lineEdit_49.setText(hr_phone)
        self.ui.lineEdit_54.setText(hr_email)

    def db_connect(self):
        global hostName_db
        global port_db
        global username_db
        global password_db
        global database_db

        try:
            self.db = MySQLdb.connect(host=hostName_db, port=port_db, user=username_db, passwd=password_db,
                                      db=database_db,
                                      charset="utf8")
            self.cur = self.db.cursor()
            info = self.db.get_host_info()

            return (info)
        except:
            warning = QMessageBox.warning(self, 'Bağlantı Hatası', 'Lütfen DB Ayarlarını Kontrol Edin', QMessageBox.Ok)


# ============================================================================
# ================ STUDENT DIALOG ===================================
class StudentWindow(QDialog, students.Ui_Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(StudentWindow, self).__init__(parent, *args, **kwargs)
        self.ui = students.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Öğrenci Seçim Sayfası')
        self.studentDialog = parent
        self.student_search()
        self.handle_button()

    def handle_button(self):
        self.ui.pushButton.clicked.connect(self.student_search)
        self.ui.tableWidget.itemClicked.connect(self.student_callback)
        self.ui.pushButton_2.clicked.connect(self.turn_mainwindow)
        self.ui.pushButton_3.clicked.connect(lambda x: StudentWindow.close(self))

    def turn_mainwindow(self):

        self.close()

        # self.window3=MainWindow()
        self.studentDialog.student_detail_upload()

    def student_search(self):
        name = self.ui.lineEdit.text()
        surname = self.ui.lineEdit_2.text()
        level = self.ui.comboBox_2.currentText()
        class_name = self.ui.comboBox.currentText()
        if (name or surname) and level and class_name:
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link FROM students WHERE name LIKE '{}%' AND surname LIKE '{}%' AND class LIKE '{}%' AND class_level  LIKE '{}%' ORDER BY id DESC".format(
                name, surname, class_name, level)
        else:

            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link FROM students WHERE  class LIKE '{}%' AND class_level  LIKE '{}%' ORDER BY id DESC".format(
                class_name, level)
        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_pos)
        self.db.close()

    def student_callback(self):
        global student_id  # #selected cell value.
        student_id = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text()
        name = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 1).text()
        surname = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text()
        tc_no = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 3).text()
        class_no = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 4).text()
        class_level = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 5).text()
        class_name = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 6).text()
        new_file_name = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 7).text()
        self.ui.lineEdit_3.setText(name)
        self.ui.lineEdit_4.setText(surname)
        self.ui.lineEdit_5.setText(tc_no)
        self.ui.lineEdit_6.setText(class_no)
        self.ui.lineEdit_7.setText(class_level)
        self.ui.lineEdit_8.setText(class_name)
        pic_path = STUDENT_IMAGES_DIR + new_file_name
        picture = QPixmap(pic_path)
        self.ui.label_11.setPixmap(picture)
        self.ui.label_11.setScaledContents(True)

    def db_connect(self):
        global hostName_db
        global port_db
        global username_db
        global password_db
        global database_db

        try:
            self.db = MySQLdb.connect(host=hostName_db, port=port_db, user=username_db, passwd=password_db,
                                      db=database_db,
                                      charset="utf8")
            self.cur = self.db.cursor()
            info = self.db.get_host_info()

            return (info)
        except:
            warning = QMessageBox.warning(self, 'Bağlantı Hatası', 'Lütfen DB Ayarlarını Kontrol Edin', QMessageBox.Ok)


# ============================================================================
# ================LOGIN PAGE===================================
class LoginWindow(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Kullanıcı Giriş Sayfası')
        self.handle_button()
        self.db_settings()
        self.invisible_objects()
    def handle_button(self):
        self.ui.pushButton.clicked.connect(self.user_check)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.tabWidget.tabBar().setVisible(False)

        self.ui.pushButton_4.clicked.connect(lambda x:self.ui.tabWidget.setCurrentIndex(1))
        self.ui.pushButton_5.clicked.connect(lambda x: self.ui.tabWidget.setCurrentIndex(0))
        self.ui.pushButton_61.clicked.connect(self.db_connect)
    def user_check(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        self.db_connect()
        sql = ''' SELECT * FROM user'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        data_count = len(data)
        row_count = 0
        for row in data:

            if username == row[0] and password == row[2]:
                global UserID
                UserID = username
                self.window2 = MainWindow()
                self.close()
                self.window2.show()

                break
            row_count += 1
        if data_count <= row_count:
            warning = QMessageBox.warning(self, 'Veri Hatası', 'Lütfen Verilerinizi Kontrol Ediniz', QMessageBox.Ok)
            self.ui.label_4.setText('Kullanıcı Girişi Hatalı Lütfen Kontrol ediniz.')

        self.db.close()

    def db_connect(self):
        global hostName_db
        global port_db
        global username_db
        global password_db
        global database_db
        self.db_settings()
        try :
            self.db = MySQLdb.connect(host=hostName_db, port=port_db, user=username_db, passwd=password_db, db=database_db,
                                  charset="utf8")
            self.cur = self.db.cursor()
            info=self.db.get_host_info()
            print(info)
            self.ui.label_179.setVisible(True)
            self.ui.label_178.setVisible(False)
            return (info)
        except:
            warning = QMessageBox.warning(self, 'Bağlantı Hatası', 'Lütfen DB Ayarlarını Kontrol Edin', QMessageBox.Ok)
            self.ui.label_179.setVisible(False)
            self.ui.label_178.setVisible(True)
            print("Host Name:{} , Port = {} , Username = {} , DataBase Name ={} ".format(hostName_db,port_db,username_db,database_db))
    def invisible_objects(self):
        self.ui.label_179.setVisible(False)
        self.ui.label_178.setVisible(False)
    def db_settings(self):
        global hostName_db
        global port_db
        global username_db
        global password_db
        global database_db
        hostName_db=self.ui.lineEdit_114.text()
        port_db=int(self.ui.lineEdit_119.text())
        username_db=self.ui.lineEdit_120.text()
        password_db=str(self.ui.lineEdit_122.text())
        database_db=self.ui.lineEdit_121.text()


# ============================================================================
# ================MAIN PAGE===================================================
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user_init()
        self.handle_button()
        self.studentDialog = StudentWindow(self)
        self.student_invisible_objects()
        self.firm_invisible_objects()
        self.quota_invisible_objects()
        self.internship_invisible_objects()
        self.absent_invisible_objects()
        self.firmDialog = FirmWindow(self)
        self.quotaDialog = QuotaWindow(self)
        self.internshipDialog = InternshipWindow(self)

        self.setWindowTitle('Ana Sayfa')



    # ================ TABS CONTROL  ===========================================
    def teacher_tab(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget_2.setCurrentIndex(0)

    def student_tab(self):
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.tabWidget_3.setCurrentIndex(0)
        self.student_show_last_record()

    def report_tab(self):
        self.ui.tabWidget.setCurrentIndex(4)

    def internship_tab(self):
        self.ui.tabWidget.setCurrentIndex(3)
        self.ui.tabWidget_4.setCurrentIndex(0)
        self.firm_showAll()
        self.quota_showAll()
        self.quotaDialog.quota_search()
        self.internship_showAll()

    def settings_tab(self):
        self.ui.tabWidget.setCurrentIndex(5)

    def lessons_tab(self):
        self.ui.tabWidget.setCurrentIndex(2)

    # ================ HANDLE BUTTONS  ===========================================
    def handle_button(self):

        # ================  tabs ==========================
        self.ui.pushButton_4.clicked.connect(self.student_tab)
        self.ui.pushButton.clicked.connect(self.lessons_tab)
        self.ui.pushButton_3.clicked.connect(self.internship_tab)
        self.ui.pushButton_5.clicked.connect(self.report_tab)
        self.ui.pushButton_6.clicked.connect(self.settings_tab)
        self.ui.pushButton_2.clicked.connect(self.teacher_tab)
        self.ui.tabWidget.tabBar().setVisible(False)
        self.ui.actionHakk_nda.triggered.connect(lambda x:self.ui.tabWidget.setCurrentIndex(6))

        # ================  themes ==========================
        self.ui.pushButton_35.clicked.connect(self.theme_1)
        self.ui.pushButton_39.clicked.connect(self.theme_2)
        self.ui.pushButton_40.clicked.connect(self.theme_3)

        # ================  users ==========================
        self.ui.pushButton_10.clicked.connect(self.logout_window)
        self.ui.pushButton_8.clicked.connect(self.password_check)
        self.ui.pushButton_11.clicked.connect(self.image_file_dialog_open)
        self.ui.pushButton_12.clicked.connect(self.cv_file_dialog_open)
        self.ui.pushButton_13.clicked.connect(self.cv_file_open)
        self.ui.pushButton_7.clicked.connect(self.teacher_show_All)
        self.ui.pushButton_14.clicked.connect(self.export_teacher)

        # ================  students ==========================
        self.ui.pushButton_15.clicked.connect(self.student_field_check)
        self.ui.pushButton_16.clicked.connect(self.student_delete)
        self.ui.pushButton_17.clicked.connect(self.student_image_open)
        self.ui.pushButton_30.clicked.connect(self.student_window_call)
        self.ui.pushButton_29.clicked.connect(self.student_screen_clear)
        self.ui.pushButton_21.clicked.connect(self.student_showAll)
        self.ui.tableWidget_6.itemClicked.connect(self.student_detail_upload_fromtable)
        self.ui.pushButton_45.clicked.connect(self.student_classtlist_showAll)
        self.ui.dateEdit_2.dateChanged.connect(self.student_birth_date_time)
        self.ui.pushButton_20.clicked.connect(self.export_student)
        # ================  firms  ==========================
        self.ui.pushButton_18.clicked.connect(self.firm_field_check)
        self.ui.pushButton_32.clicked.connect(self.firm_screen_clear)
        self.ui.pushButton_22.clicked.connect(self.firm_showAll)
        self.ui.tableWidget_5.itemClicked.connect(self.firm_callback)
        self.ui.pushButton_19.clicked.connect(self.firm_delete)
        self.ui.pushButton_26.clicked.connect(self.quota_firm_window_call)

        # ================   Quota ==========================
        self.ui.pushButton_36.clicked.connect(self.quota_field_check)
        self.ui.comboBox_14.currentIndexChanged.connect(self.quota_showAll)
        self.ui.tableWidget_7.itemClicked.connect(self.quota_detail_upload_table)
        self.ui.pushButton_37.clicked.connect(self.quota_screen_clear)
        self.ui.pushButton_23.clicked.connect(self.export_internship_list)
        self.ui.pushButton_38.clicked.connect(self.quota_delete)
        # ================  Internship ==========================
        self.ui.pushButton_34.clicked.connect(self.quota_dialog_window_call)
        self.ui.pushButton_27.clicked.connect(self.internship_field_check)
        self.ui.pushButton_25.clicked.connect(self.student_window_call)
        self.ui.pushButton_33.clicked.connect(self.internship_screen_clear)
        self.ui.pushButton_60.clicked.connect(self.internship_unassigned_list_show)
        self.ui.tableWidget_4.itemClicked.connect(self.internship_detail_upload_table)
        self.ui.dateEdit_3.dateChanged.connect(self.internship_start_date_time)
        self.ui.dateEdit_4.dateChanged.connect(self.internship_finish_date_time)
        self.ui.pushButton_24.clicked.connect(self.internship_list_showall)
        self.ui.pushButton_28.clicked.connect(self.internship_delete)
        # ================  Calculations  ==========================
        self.ui.comboBox_15.currentIndexChanged.connect(self.cal_total_quota)
        self.ui.pushButton_31.clicked.connect(self.cal_total_quota)
        self.ui.tableWidget_4.itemClicked.connect(self.cal_total_quota)

        # ================  Absent ==========================
        self.ui.pushButton_50.clicked.connect(self.absent_dialog_window_call)
        self.ui.pushButton_52.clicked.connect(self.absent_field_check)
        self.ui.dateEdit_5.dateChanged.connect(self.absent_date_time)
        self.ui.tableWidget_3.itemClicked.connect(self.absent_detail_from_table_call)
        self.ui.pushButton_53.clicked.connect(self.absent_screen_clear)
        self.ui.pushButton_51.clicked.connect(self.export_absent_for_student)
        self.ui.textEdit_10.createStandardContextMenu()
        self.ui.pushButton_54.clicked.connect(self.absent_delete)

    # ============================================================================
    # ================ DATABASE SETTING ==========================================


    def db_connect(self):
        global hostName_db
        global port_db
        global username_db
        global password_db
        global database_db

        try:
            self.db = MySQLdb.connect(host=hostName_db, port=port_db, user=username_db, passwd=password_db,
                                      db=database_db,
                                      charset="utf8")
            self.cur = self.db.cursor()
            info = self.db.get_host_info()

            return (info)
        except:
            warning = QMessageBox.warning(self, 'Bağlantı Hatası', 'Lütfen DB Ayarlarını Kontrol Edin', QMessageBox.Ok)

    # ============================================================================
    def input_mask_override(self):
        self.ui.lineEdit_66.setInputMask('99/99/9999')
        self.ui.lineEdit_66.setMaxLength(10)

    def image_file_dialog_open(self):
        filepath, _ = QFileDialog.getOpenFileName(filter='Resim Dosyası *.png')
        filename = QFileInfo(filepath).fileName()
        new_file_name = self.ui.lineEdit_7.text() + self.ui.lineEdit_11.text() + '.png'
        if filename:

            self.ui.lineEdit_19.setText(new_file_name)
            pic_path = IMAGE_DIR + new_file_name
            shutil.copyfile(filepath, IMAGE_DIR + new_file_name)
            picture = QPixmap(pic_path)
            self.ui.label_22.setPixmap(picture)
            self.ui.label_22.setScaledContents(True)

    def cv_file_dialog_open(self):
        filepath, _ = QFileDialog.getOpenFileName(filter='CV Dosyası *.pdf')
        filename = QFileInfo(filepath).fileName()

        if filename:
            new_file_name = self.ui.lineEdit_7.text() + self.ui.lineEdit_11.text() + '.pdf'
            self.ui.lineEdit_20.setText(new_file_name)
            cv_path = FILE_DIR + new_file_name
            shutil.copyfile(filepath, cv_path)

            self.ui.label_24.setText(cv_path)

    def cv_file_open(self):
        filename = self.ui.lineEdit_20.text()
        if filename:
            cv_path = FILE_DIR + filename
            os.startfile(cv_path)
            self.statusBar().showMessage('CV dosyası açıldı ')
        else:
            warning = QMessageBox.warning(self, 'Dosya Bulunamadı', 'Lütfen Dosya Ekleyin', QMessageBox.Ok)
            self.statusBar().showMessage('Dosya Bulunamadı ')

    def password_check(self):
        pasw1 = self.ui.lineEdit_3.text()
        pasw2 = self.ui.lineEdit_4.text()
        if pasw1 == pasw2:
            self.teacher_update()
        else:
            warning = QMessageBox.warning(self, 'Şifre Hatası', 'Lütfen Şifreyi Kontrol Ediniz', QMessageBox.Ok)
            self.statusBar().showMessage('Şifreler Uyumsuz ')

    def user_init(self):

        try:
            self.db_connect()
            username = UserID

            sql = ''' SELECT * FROM user WHERE username = %s'''
            self.cur.execute(sql, [(UserID)])
            data = self.cur.fetchone()

            self.ui.lineEdit_5.setText(data[0])  # username
            self.ui.lineEdit_11.setText(data[0])  # username
            self.ui.lineEdit.setText(data[4])  # name and surname
            self.ui.lineEdit_2.setText(data[1])  # email
            self.ui.lineEdit_7.setText(str(data[3]))  # TC no
            self.ui.lineEdit_3.setText(data[2])  # sifre
            if data[6] == 'E':
                self.ui.comboBox_3.setCurrentText('E')  # admin

            else:
                self.ui.comboBox_3.setCurrentText('H')  # admin
                self.admin_control_dactivate()

            sql2 = ''' SELECT * FROM teacher_detail WHERE username = %s'''
            self.cur.execute(sql2, [(username)])
            data2 = self.cur.fetchone()
            if data2:
                self.ui.comboBox.setCurrentText(data2[2])
                self.ui.comboBox_2.setCurrentText(data2[3])
                self.ui.lineEdit_14.setText(data2[4])
                self.ui.lineEdit_10.setText(data2[5])
                self.ui.textEdit.setPlainText(data2[6])
                self.ui.lineEdit_13.setText(data2[7])
                self.ui.lineEdit_12.setText(data2[8])
                self.ui.lineEdit_8.setText(data2[9])
                self.ui.lineEdit_9.setText(data2[10])
                self.ui.lineEdit_19.setText(data2[11])
                self.ui.lineEdit_20.setText(data2[12])
                self.ui.lineEdit_15.setText(data2[13])
                self.ui.lineEdit_16.setText(data2[14])
                self.ui.lineEdit_17.setText(data2[15])
                self.ui.lineEdit_18.setText(data2[16])
                pic_path = IMAGE_DIR + data2[11]
                picture = QPixmap(pic_path)
                self.ui.label_23.setPixmap(picture)
                self.ui.label_23.setScaledContents(True)

                cv_path = FILE_DIR + data2[12]
                if self.ui.lineEdit_20.text():
                    self.ui.label_24.setText(cv_path)
                else:
                    self.ui.label_24.setText('')
                self.db.close()
        except:
            warning = QMessageBox.warning(self, 'Bağlantı Hatası', 'Lütfen DB Ayarlarını Kontrol Edin', QMessageBox.Ok)

    def admin_control_dactivate(self):
        self.ui.pushButton_9.setEnabled(0)
        self.ui.comboBox_3.setEnabled(0)



    def logout_window(self):
        self.window2 = LoginWindow()
        self.close()
        self.window2.show()
        self.statusBar().showMessage('Login sayfasına Dönüldü')

    # ============================================================================
    # ================ TEACHERS BLOCKS ===========================================
    def teacher_update(self):

        departure = self.ui.comboBox.currentText()
        status = str(self.ui.comboBox_2.currentText())
        start_year = self.ui.lineEdit_14.text()
        state = str(self.ui.lineEdit_10.text())
        adress = self.ui.textEdit.toPlainText()
        pers_email = self.ui.lineEdit_13.text()
        telephone = self.ui.lineEdit_12.text()
        university = self.ui.lineEdit_8.text()
        uni_departure = self.ui.lineEdit_9.text()
        profile_image = self.ui.lineEdit_19.text()
        cv_file = self.ui.lineEdit_20.text()
        fb_link = self.ui.lineEdit_15.text()
        linkedin_link = self.ui.lineEdit_16.text()
        blog_link = self.ui.lineEdit_17.text()
        other_link = self.ui.lineEdit_18.text()

        self.db_connect()
        username = UserID
        sql2 = ''' SELECT * FROM teacher_detail WHERE username = %s'''
        self.cur.execute(sql2, [(username)])
        data2 = self.cur.fetchone()
        if data2:

            sql = '''UPDATE teacher_detail SET 
            username=%s,
            departure=%s,
            status=%s,
            start_year=%s,
            state=%s,
            adress=%s,
            pers_email=%s,
            telephone=%s,
            university=%s,
            uni_departure=%s,
            profile_image=%s,
            cv_file=%s,
            fb_link=%s,
            linkedin_link=%s,
            blog_link=%s,
            other_link=%s
            
            WHERE username = %s
                        '''
            self.cur.execute(sql, (
                username, departure, status, start_year, state, adress, pers_email, telephone, university,
                uni_departure,
                profile_image, cv_file, fb_link, linkedin_link, blog_link, other_link, username))

            self.db.commit()
            self.statusBar().showMessage('Öğretmen Bilgileri Güncellendi')
            self.db.close()

        else:
            self.teacher_add()
        pic_path = IMAGE_DIR + self.ui.lineEdit_19.text()
        picture = QPixmap(pic_path)
        self.ui.label_23.setPixmap(picture)
        self.ui.label_23.setScaledContents(True)

        new_file_name = self.ui.lineEdit_20.text()
        cv_path = FILE_DIR + new_file_name
        if self.ui.lineEdit_20.text():
            self.ui.label_24.setText(cv_path)
        else:
            self.ui.label_24.setText('')

        self.ui.lineEdit_4.setText('')

    def teacher_delete(self):
        pass

    def teacher_add(self):
        departure = self.ui.comboBox.currentText()
        status = str(self.ui.comboBox_2.currentText())
        start_year = self.ui.lineEdit_14.text()
        state = str(self.ui.lineEdit_10.text())
        adress = self.ui.textEdit.toPlainText()
        pers_email = self.ui.lineEdit_13.text()
        telephone = self.ui.lineEdit_12.text()
        university = self.ui.lineEdit_8.text()
        uni_departure = self.ui.lineEdit_9.text()
        profile_image = self.ui.lineEdit_19.text()
        cv_file = self.ui.lineEdit_20.text()
        fb_link = self.ui.lineEdit_15.text()
        linkedin_link = self.ui.lineEdit_16.text()
        blog_link = self.ui.lineEdit_17.text()
        other_link = self.ui.lineEdit_18.text()

        self.db_connect()
        username = UserID
        sql = '''INSERT INTO teacher_detail 
                (username,
                departure,
                status,
                start_year,
                state,
                adress,
                pers_email,
                telephone,
                university,
                uni_departure,
                profile_image,
                cv_file,
                fb_link,
                linkedin_link,
                blog_link,
                other_link)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

        self.cur.execute(sql, (
            username, departure, status, start_year, state, adress, pers_email, telephone, university, uni_departure,
            profile_image, cv_file, fb_link, linkedin_link, blog_link, other_link))

        self.db.commit()
        self.statusBar().showMessage('Öğretmen Bilgileri Eklendi')

        pic_path = IMAGE_DIR + self.ui.lineEdit_19.text()
        picture = QPixmap(pic_path)
        self.ui.label_23.setPixmap(picture)
        self.ui.label_23.setScaledContents(True)

        new_file_name = self.ui.lineEdit_20.text()
        cv_path = FILE_DIR + new_file_name
        if self.ui.lineEdit_20.text():
            self.ui.label_24.setText(cv_path)
        else:
            self.ui.label_24.setText('')

        self.db.close()
        self.ui.lineEdit_4.setText('')

    def teacher_show_All(self):

        header_list = ['username', 'departure', 'status', 'start_year', 'state', 'adress', 'pers_email', 'telephone',
                       'university', 'uni_departure', 'profile_image', 'cv_file', 'fb_link', 'linkedin_link',
                       'blog_link', 'other_link']
        indexn = 1
        sayi = len(header_list)
        for field in range(sayi):
            if field == self.ui.comboBox_4.currentIndex():
                header = header_list[self.ui.comboBox_4.currentIndex()]

                break
        self.db_connect()
        if self.ui.lineEdit_21.text():
            sql = "SELECT * FROM teacher_detail WHERE {} LIKE '{}%'".format(header, self.ui.lineEdit_21.text())
        else:
            sql = "SELECT * FROM teacher_detail"

        # sql = "SELECT * FROM teacher_detail WHERE username = 'ed'"

        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget.setRowCount(0)
            self.ui.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_pos)
        else:
            self.ui.tableWidget.clearContents()

        self.db.close()
        return data

    def export_teacher(self):
        wb = Workbook(REPORT_DIR + '\\report.xlsx', )
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Kullanıcı Adı')
        sheet1.write(0, 1, 'Kullanıcı Adı')
        sheet1.write(0, 2, 'Bolum')
        sheet1.write(0, 3, 'Durum')
        sheet1.write(0, 4, 'Baslangıc Yılı')
        sheet1.write(0, 5, 'İlçe')
        sheet1.write(0, 6, 'Adres')
        sheet1.write(0, 7, 'Kişisel Email')
        sheet1.write(0, 8, 'Telefon')
        sheet1.write(0, 9, 'Universite')
        sheet1.write(0, 10, 'Universite Bölümü')
        sheet1.write(0, 11, 'Profil Resmi')
        sheet1.write(0, 12, 'CV Adı')
        sheet1.write(0, 13, 'FB Link')
        sheet1.write(0, 14, 'Linkdn Link')
        sheet1.write(0, 15, 'Blog Link')
        sheet1.write(0, 16, 'Other Link')
        sheet1.write(0, 17, 'Kayıt Zamanı')

        data = self.teacher_show_All()
        row_number = 1
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_number, column_num, str(item))
                column_num += 1
            row_number += 1

        wb.close()
        info = QMessageBox.information(self, 'İşlem Tamamlandı',
                                      'Excel Dosyası  Başarıyla oluşturuldu\n {} \nadresinde dosyayı görebilirsiniz. '.format(REPORT_DIR),
                                      QMessageBox.Ok)

        self.statusBar().showMessage('Excel Dosyası oluşturuldu ')

    # ============================================================================
    # ================ STUDENT BLOCKS ================================================
    def student_invisible_objects(self):
        self.ui.label_71.setVisible(False)
        self.ui.label_76.setVisible(False)
        self.ui.label_106.setVisible(False)
        self.ui.label_107.setVisible(False)
        self.ui.label_108.setVisible(False)
        self.ui.label_109.setVisible(False)
        self.ui.label_110.setVisible(False)
        self.ui.label_111.setVisible(False)
        self.ui.label_112.setVisible(False)
        self.ui.label_113.setVisible(False)


    def student_birth_date_time(self):
        day = self.ui.dateEdit_2.date().day()
        month = self.ui.dateEdit_2.date().month()
        year = self.ui.dateEdit_2.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))

        self.ui.lineEdit_33.setText(str(date))

    def student_field_check(self):

        if (not self.ui.lineEdit_31.text() or
                not self.ui.lineEdit_30.text() or
                not self.ui.lineEdit_32.text() or
                not self.ui.lineEdit_33.text() or
                self.ui.comboBox_20.currentIndex()==0 or
                not self.ui.lineEdit_35.text() or
                not self.ui.lineEdit_42.text() or
                not self.ui.lineEdit_43.text() or

                # self.ui.lineEdit_29.text() or
                not self.ui.lineEdit_37.text()):
            warning = QMessageBox.warning(self, 'Eksik Veri Hatası',
                                          'Girilmesi zorunlu olan veriler bulunmaktadır. Lütfen eksik tüm alanları doldurun',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Eksik Veri hatası ')
            self.student_visible_objects()
            return (False)
        else:
            self.student_visible_objects()
            self.student_add()
            return (True)

    def student_visible_objects(self):

        if self.ui.lineEdit_31.text() == '':
            self.ui.label_71.setVisible(True)
        else:
            self.ui.label_71.setVisible(False)

        if self.ui.lineEdit_30.text() == '':
            self.ui.label_76.setVisible(True)
        else:
            self.ui.label_76.setVisible(False)

        if self.ui.lineEdit_32.text() == '':
            self.ui.label_106.setVisible(True)
        else:
            self.ui.label_106.setVisible(False)

        if self.ui.lineEdit_33.text() == '':
            self.ui.label_107.setVisible(True)
        else:
            self.ui.label_107.setVisible(False)

        if self.ui.lineEdit_35.text() == '':
            self.ui.label_108.setVisible(True)
        else:
            self.ui.label_108.setVisible(False)

        if self.ui.lineEdit_42.text() == '':
            self.ui.label_109.setVisible(True)
        else:
            self.ui.label_109.setVisible(False)

        if self.ui.lineEdit_43.text() == '':
            self.ui.label_110.setVisible(True)
        else:
            self.ui.label_110.setVisible(False)

        if self.ui.comboBox_20.currentIndex() == 0:
            self.ui.label_111.setVisible(True)
        else:
            self.ui.label_111.setVisible(False)


        if self.ui.lineEdit_37.text() == '':
            self.ui.label_112.setVisible(True)
        else:
            self.ui.label_112.setVisible(False)

        # if self.ui.lineEdit_29.text()=='':
        #     self.ui.label_113.setVisible(True)
        # else:
        #     self.ui.label_113.setVisible(False)

    def student_add(self):

        profil_image = self.ui.lineEdit_29.text()
        student_name = self.ui.lineEdit_31.text()
        student_surname = self.ui.lineEdit_30.text()
        tc_no = self.ui.lineEdit_32.text()
        birthday = self.ui.lineEdit_33.text()
        email = self.ui.lineEdit_40.text()
        telephone = self.ui.lineEdit_35.text()
        partner_name = self.ui.lineEdit_42.text()
        partner_phone = self.ui.lineEdit_43.text()
        register_date = self.ui.comboBox_20.currentText()
        student_num = self.ui.lineEdit_37.text()
        departure = self.ui.comboBox_7.currentText()
        class_level = self.ui.comboBox_6.currentText()
        class_name = self.ui.comboBox_9.currentText()
        city = self.ui.lineEdit_44.text()
        state = self.ui.lineEdit_34.text()
        adress = self.ui.textEdit_2.toPlainText()
        note = self.ui.textEdit_3.toPlainText()
        sexual=self.ui.comboBox_5.currentText()
        id = self.existing_student_check()
        if id:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu TC Kimlik Numaralı Öğrenci Sistemde Mevcuttur.\nMevcut kaydı güncellemek için lütfen\n- SaveAll -  butonuna çıkmak için  -Cancel-  tusuna basın")
            msgBox.setWindowTitle("DİKKAT - Veriler Güncellenecek")
            msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.SaveAll)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            self.statusBar().showMessage('DİKKAT - Veriler Güncellenecek')
            if returnValue == QMessageBox.SaveAll:
                print('Save All clicked')
                self.student_update(id)
                return None

        else:

            self.db_connect()

            sql = '''INSERT INTO students (name,surname,birthday, tc_no,email,telephone,parent_name,parent_telephone,city,
                            state,adress,register_date,school_number,departure,class_level,class,image_link,notes,sexual) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''

            self.cur.execute(sql, (
                student_name, student_surname, birthday, tc_no, email, telephone, partner_name, partner_phone, city,
                state, adress, register_date,
                student_num, departure, class_level, class_name, profil_image, note,sexual))

            self.db.commit()
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu {} Kimlik Numaralı, {} {} adlı Öğrencinin  Bilgileri Sisteme Başarıyla Kaydedilmiştir.\nDevam Etmek için OK tuşuna basın".format(
                    tc_no, student_name, student_surname))
            msgBox.setWindowTitle("DİKKAT - Veriler Sisteme Eklendi")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.student_screen_clear()
            self.statusBar().showMessage('Öğrenci Bilgileri Eklendi')
            self.db.close()
            self.student_show_last_record()

    def student_window_call(self):

        self.studentDialog.show()
        self.studentDialog.student_search()

    def student_detail_upload_fromtable(self):
        global student_id
        student_id = int(self.ui.tableWidget_6.item(self.ui.tableWidget_6.currentRow(), 0).text())
        self.student_detail_upload()
    def student_detail_upload(self):
        global student_id
        self.db_connect()

        sql = ''' SELECT * FROM students WHERE id = %s'''
        self.cur.execute(sql, [(student_id)])
        data = self.cur.fetchone()
        student_id=data[0]
        self.ui.lineEdit_22.setText(str(data[0]))
        self.ui.lineEdit_29.setText(data[17])
        self.ui.lineEdit_31.setText(data[1])
        self.ui.lineEdit_30.setText(data[2])
        self.ui.lineEdit_32.setText(str(data[4]))
        self.ui.lineEdit_33.setText(data[3])
        self.ui.lineEdit_40.setText(data[5])
        self.ui.lineEdit_35.setText(str(data[6]))
        self.ui.lineEdit_42.setText(data[7])
        self.ui.lineEdit_43.setText(data[8])
        self.ui.comboBox_20.setCurrentText(data[12])
        self.ui.lineEdit_37.setText(data[13])
        self.ui.comboBox_7.setCurrentText(data[14])
        self.ui.comboBox_6.setCurrentText(str(data[15]))
        self.ui.comboBox_9.setCurrentText(data[16])
        self.ui.lineEdit_44.setText(data[9])
        self.ui.lineEdit_34.setText(data[10])
        self.ui.textEdit_2.setPlainText(data[11])
        self.ui.textEdit_3.setPlainText(data[18])
        self.ui.comboBox_5.setCurrentText(data[20])
        new_file_name = data[17]
        pic_path = STUDENT_IMAGES_DIR + new_file_name

        picture = QPixmap(pic_path)
        self.ui.label_35.setPixmap(picture)
        self.ui.label_35.setScaledContents(True)
        self.internship_student_call(student_id)
        self.ui.label_130.setVisible(True)
        self.ui.label_128.setVisible(False)

    def student_update(self, id):
        profil_image = self.ui.lineEdit_29.text()
        student_name = self.ui.lineEdit_31.text()
        student_surname = self.ui.lineEdit_30.text()
        tc_no = self.ui.lineEdit_32.text()
        birthday = self.ui.lineEdit_33.text()
        email = self.ui.lineEdit_40.text()
        telephone = self.ui.lineEdit_35.text()
        partner_name = self.ui.lineEdit_42.text()
        partner_phone = self.ui.lineEdit_43.text()
        register_date = self.ui.comboBox_20.currentText()
        student_num = self.ui.lineEdit_37.text()
        departure = self.ui.comboBox_7.currentText()
        class_level = self.ui.comboBox_6.currentText()
        class_name = self.ui.comboBox_9.currentText()
        city = self.ui.lineEdit_44.text()
        state = self.ui.lineEdit_34.text()
        adress = self.ui.textEdit_2.toPlainText()
        note = self.ui.textEdit_3.toPlainText()
        sexual = self.ui.comboBox_5.currentText()
        id = self.existing_student_check()
        self.ui.lineEdit_22.setText(str(id))
        self.db_connect()

        sql = (
            "UPDATE students SET name=%s,surname=%s,birthday=%s, tc_no=%s,email=%s,telephone=%s,parent_name=%s,parent_telephone=%s,city=%s,state=%s,adress=%s,register_date=%s,school_number=%s,departure=%s,class_level=%s,class=%s,image_link=%s,notes=%s,sexual=%s WHERE id=%s")

        self.cur.execute(sql, (
            student_name, student_surname, birthday, tc_no, email, telephone, partner_name, partner_phone, city, state,
            adress, register_date, student_num, departure, class_level, class_name, profil_image, note,sexual, id))

        self.db.commit()

        self.db.close()
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(
            "Bu {} Kimlik Numaralı, {} {} adlı Öğrencinin  Bilgileri Güncellendi.\nDevam Etmek için OK tuşuna basın".format(
                tc_no, student_name, student_surname))
        msgBox.setWindowTitle("DİKKAT - Veriler Güncellendi")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
        returnValue = msgBox.exec()
        self.statusBar().showMessage('Öğrenci Bilgileri Güncellendi')
        self.student_show_last_record()

    def student_screen_clear(self):
        self.ui.lineEdit_29.setText('')
        self.ui.lineEdit_31.setText('')
        self.ui.lineEdit_30.setText('')
        self.ui.lineEdit_32.setText('')
        self.ui.lineEdit_33.setText('')
        self.ui.lineEdit_40.setText('')
        self.ui.lineEdit_35.setText('')
        self.ui.lineEdit_42.setText('')
        self.ui.lineEdit_43.setText('')

        self.ui.comboBox_20.setCurrentIndex(0)
        self.ui.lineEdit_37.setText('')
        self.ui.comboBox_7.setCurrentText('')
        self.ui.comboBox_6.setCurrentText('')
        self.ui.comboBox_9.setCurrentText('')
        self.ui.lineEdit_44.setText('')
        self.ui.lineEdit_34.setText('')
        self.ui.textEdit_2.setPlainText('')
        self.ui.textEdit_3.setText('')
        self.ui.lineEdit_34.setText('')
        self.ui.label_35.setPixmap(None)
        self.ui.lineEdit_22.setText('')
        self.ui.comboBox_9.setCurrentText('E')
        self.student_invisible_objects()

        self.statusBar().showMessage('Tüm sayfa temizlendi yeni kayıt eklenebilir')

    def student_delete(self):
        global student_id


        student_name = self.ui.lineEdit_31.text()
        student_surname = self.ui.lineEdit_30.text()

        if self.ui.lineEdit_22.text() != '':

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                " {} {} adlı Öğrenciye ait {} Nolu kayıt siliniecektir.\nDevam Etmek için Discard tuşuna basın".format(
                    student_name, student_surname,student_id))
            msgBox.setWindowTitle("DİKKAT - Veri Silinecek")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(lambda x: print(" Silme Butonu Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Discard:
                self.db_connect()

                sql = "DELETE FROM students WHERE id={}".format(student_id)

                self.cur.execute(sql)

                self.db.commit()
                self.statusBar().showMessage(
                    " {} {} adlı Öğrenciye ait {} Nolu kayıt siliniecektir.\nDevam Etmek için Discard tuşuna basın".format(
                    student_name, student_surname,student_id))
                self.db.close()
                self.ui.lineEdit_22.setText('')
                student_id = 0
                self.ui.tableWidget_6.clearContents()
                self.student_screen_clear()
                self.student_showAll()
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("Silmek için önce  tablodan bir kayıt seçmelisiniz")
            msgBox2.setWindowTitle("DİKKAT - Veri Seçimi yapılmadı")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            msgBox2.buttonClicked.connect(lambda x: print(" OK Butonu Tıklandı"))
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" Kayıt Seçimi yapılmadı")

    def existing_student_check(self):
        tc_no = self.ui.lineEdit_32.text()

        self.db_connect()
        sql = "SELECT id,tc_no FROM students WHERE tc_no={}".format(tc_no)
        if self.cur.execute(sql):
            id, data = self.cur.fetchone()

            self.statusBar().showMessage('Kayıt Bulundu.')
            self.db.close()
            return id
        else:
            self.db.close()
            return None

    def student_image_open(self):

        if not self.ui.lineEdit_32.text():
            warning = QMessageBox.warning(self, 'Veri Eksik', ' Önce TC Kimlik numarasını giriniz', QMessageBox.Ok)
            self.statusBar().showMessage('Veri Eksik ')
        else:

            filepath, _ = QFileDialog.getOpenFileName(filter='Resim Dosyası *.png')
            filename = QFileInfo(filepath).fileName()
            new_file_name = self.ui.lineEdit_32.text() + '_' + 'resim' + '.png'
            if filename:
                self.ui.lineEdit_29.setText(new_file_name)
                pic_path = STUDENT_IMAGES_DIR + new_file_name
                shutil.copyfile(filepath, pic_path)
                picture = QPixmap(pic_path)
                self.ui.label_35.setPixmap(picture)
                self.ui.label_35.setScaledContents(True)
        return pic_path

    def student_showAll(self):
        register_date=self.ui.comboBox_21.currentText()
        filter_val = self.ui.lineEdit_41.text()
        index_val = str(self.ui.comboBox_8.currentIndex())
        header = {'0': 'name', '1': 'surname', '2': 'school_number', '3': 'class_level', '4': 'class' , '5': 'departure','6': 'sexual'}
        if filter_val and register_date=='':
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link,departure,sexual,register_date FROM students  WHERE {} LIKE '{}%' ".format(
                header[index_val], filter_val)
        elif filter_val and register_date:
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link,departure,sexual,register_date FROM students  WHERE {} LIKE '{}%' AND register_date={}".format(
                header[index_val], filter_val,register_date)
        elif filter_val=='' and register_date:
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link,departure,sexual,register_date FROM students WHERE register_date={}".format(
                register_date)
        else:
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link,departure,sexual,register_date FROM students ORDER BY record_date DESC"
        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_2.setRowCount(0)
            self.ui.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_2.rowCount()
                self.ui.tableWidget_2.insertRow(row_pos)
            self.statusBar().showMessage('Kayıtlar Getirili')
        else:
            self.statusBar().showMessage('Kayıt Bulunamadı. Arama kriterlerini değiştirin')

            self.ui.tableWidget_2.clearContents()

        return data

    def student_classtlist_showAll(self):
        register_date=self.ui.comboBox_17.currentText()
        class_level = self.ui.comboBox_19.currentText()
        class_name = self.ui.comboBox_18.currentText()

        if register_date:
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link,departure,sexual,register_date FROM students  WHERE register_date={} AND class_level='{}' AND class='{}'".format(
                register_date, class_level,class_name)

        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_8.setRowCount(0)
            self.ui.tableWidget_8.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_8.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_8.rowCount()
                self.ui.tableWidget_8.insertRow(row_pos)
            self.statusBar().showMessage('Kayıtlar Getirili')
        else:
            self.statusBar().showMessage('Kayıt Bulunamadı. Arama kriterlerini değiştirin')

            self.ui.tableWidget_8.clearContents()

        self.db.close()
        return data

    def student_show_last_record(self):

        sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link FROM students ORDER BY record_date DESC LIMIT 5"

        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_6.setRowCount(0)
            self.ui.tableWidget_6.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_6.rowCount()
                self.ui.tableWidget_6.insertRow(row_pos)
            self.statusBar().showMessage('Kayıtlar Getirili')
        else:
            self.statusBar().showMessage('Kayıt Bulunamadı. Arama kriterlerini değiştirin')

    def export_student(self):
        wb = Workbook(REPORT_DIR + '\\report_student.xlsx', )
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Kayıt No')
        sheet1.write(0, 1, 'Öğrenci Adı')
        sheet1.write(0, 2, 'Öğrenci Soyadı')
        sheet1.write(0, 3, 'TC No')
        sheet1.write(0, 4, 'Sınıf No')
        sheet1.write(0, 5, 'Sınıf')
        sheet1.write(0, 6, 'Sube')
        sheet1.write(0, 7, 'Resim Link')
        # sheet1.write(0, 8, 'Telefon')
        # sheet1.write(0, 9, 'Universite')
        # sheet1.write(0, 10, 'Universite Bölümü')
        # sheet1.write(0, 11, 'Profil Resmi')
        # sheet1.write(0, 12, 'CV Adı')
        # sheet1.write(0, 13, 'FB Link')
        # sheet1.write(0, 14, 'Linkdn Link')
        # sheet1.write(0, 15, 'Blog Link')
        # sheet1.write(0, 16, 'Other Link')
        # sheet1.write(0, 17, 'Kayıt Zamanı')

        data = self.student_showAll()
        row_number = 1
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_number, column_num, str(item))
                column_num += 1
            row_number += 1

        wb.close()
        info = QMessageBox.information(self, 'İşlem Tamamlandı',
                                       'Excel Dosyası  Başarıyla oluşturuldu\n {} \nadresinde dosyayı görebilirsiniz. '.format(
                                           REPORT_DIR),
                                       QMessageBox.Ok)

        self.statusBar().showMessage('Excel Dosyası oluşturuldu ')
    # ============================================================================
    # ================ FIRM BLOCKS ============================================
    def firm_invisible_objects(self):
        self.ui.label_114.setVisible(False)
        self.ui.label_115.setVisible(False)
        self.ui.label_116.setVisible(False)
        self.ui.label_117.setVisible(False)
        self.ui.label_118.setVisible(False)
        self.ui.label_119.setVisible(False)
        self.ui.label_120.setVisible(False)

    def firm_field_check(self):
        if (not self.ui.lineEdit_45.text() or
                not self.ui.lineEdit_50.text() or
                not self.ui.lineEdit_39.text() or
                not self.ui.lineEdit_46.text() or
                not self.ui.lineEdit_52.text() or
                not self.ui.lineEdit_53.text() or

                not self.ui.textEdit_4.toPlainText()):
            warning = QMessageBox.warning(self, 'Eksik Veri Hatası',
                                          'Girilmesi zorunlu olan veriler bulunmaktadır. Lütfen eksik tüm alanları doldurun',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Eksik Veri hatası ')
            self.firm_visible_objects()
            return (False)
        else:
            self.firm_visible_objects()
            self.firm_add()
            return (True)

    def firm_visible_objects(self):

        if self.ui.lineEdit_45.text() == '':
            self.ui.label_114.setVisible(True)
        else:
            self.ui.label_114.setVisible(False)

        if self.ui.lineEdit_50.text() == '':
            self.ui.label_115.setVisible(True)
        else:
            self.ui.label_115.setVisible(False)

        if self.ui.lineEdit_39.text() == '':
            self.ui.label_116.setVisible(True)
        else:
            self.ui.label_116.setVisible(False)

        if self.ui.lineEdit_46.text() == '':
            self.ui.label_117.setVisible(True)
        else:
            self.ui.label_117.setVisible(False)

        if self.ui.lineEdit_53.text() == '':
            self.ui.label_118.setVisible(True)
        else:
            self.ui.label_118.setVisible(False)

        if self.ui.lineEdit_52.text() == '':
            self.ui.label_119.setVisible(True)
        else:
            self.ui.label_119.setVisible(False)

        if self.ui.textEdit_4.toPlainText() == '':
            self.ui.label_120.setVisible(True)
        else:
            self.ui.label_120.setVisible(False)

    def firm_add(self):
        caricode = self.ui.lineEdit_45.text()
        name = self.ui.lineEdit_39.text()
        adress = self.ui.textEdit_4.toPlainText()
        city = self.ui.lineEdit_53.text()
        state = self.ui.lineEdit_52.text()
        telephone = self.ui.lineEdit_46.text()
        fax = self.ui.lineEdit_47.text()
        web = self.ui.lineEdit_51.text()
        sectorCode = self.ui.lineEdit_50.text()
        sector_desc = self.ui.lineEdit_55.text()
        hr_name = self.ui.lineEdit_48.text()
        hr_phone = self.ui.lineEdit_49.text()
        hr_email = self.ui.lineEdit_54.text()
        notes = self.ui.textEdit_5.toPlainText()
        firm_id = self.firm_existing_check()

        if firm_id:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu Cari Kodlu Firma Sistemde KAyıtlıdır.\nMevcut kaydı güncellemek için lütfen\n- SaveAll -  butonuna çıkmak için  -Cancel-  tusuna basın")
            msgBox.setWindowTitle("DİKKAT - Veriler Güncellenecek")
            msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.SaveAll)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            self.statusBar().showMessage('DİKKAT - Veriler Güncellenecek')
            if returnValue == QMessageBox.SaveAll:
                print('Save All clicked')
                self.firm_update(firm_id)
                return None

        else:

            self.db_connect()

            sql = '''INSERT INTO firms (cari_code,name,adress,city,state,telephone,fax,web,sector_code,sector_desc,hr_name,hr_telephone,hr_email,notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            self.cur.execute(sql, (
                caricode, name, adress, city, state, telephone, fax, web, sectorCode, sector_desc, hr_name, hr_phone,
                hr_email, notes))

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu {} Cari Kodlu , {} adlı Firmanın  Bilgileri Sisteme Başarıyla Kaydedilmiştir.\nDevam Etmek için OK tuşuna basın".format(
                    caricode, name))
            msgBox.setWindowTitle("DİKKAT - Veriler Sisteme Eklendi")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.firm_screen_clear()
            self.db.commit()
            self.statusBar().showMessage('Firma  Bilgileri Eklendi')
            self.db.close()
            self.firm_showAll()
            self.ui.lineEdit_23.setText(str(firm_id))

    def firm_callback(self):
        global firm_id
        firm_id = int(self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 0).text())


        self.db_connect()
        sql = "SELECT * FROM firms WHERE id={}".format(firm_id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()
            firm_id = data[0]
            self.ui.lineEdit_45.setText(data[1])
            self.ui.lineEdit_39.setText(data[2])
            self.ui.textEdit_4.setPlainText(data[3])
            self.ui.lineEdit_53.setText(data[4])
            self.ui.lineEdit_52.setText(data[5])
            self.ui.lineEdit_46.setText(data[6])
            self.ui.lineEdit_47.setText(data[7])
            self.ui.lineEdit_51.setText(data[8])
            self.ui.lineEdit_50.setText(data[9])
            self.ui.lineEdit_55.setText(data[10])
            self.ui.lineEdit_48.setText(data[11])
            self.ui.lineEdit_49.setText(data[12])
            self.ui.lineEdit_54.setText(data[13])
            self.ui.textEdit_5.setPlainText(data[14])
            self.ui.lineEdit_23.setText(str(firm_id))

            self.db.close()
            return data
        else:
            firm_id = 0
            self.db.close()
            return None

    def firm_update(self, firm_id):
        caricode = self.ui.lineEdit_45.text()
        name = self.ui.lineEdit_39.text()
        adress = self.ui.textEdit_4.toPlainText()
        city = self.ui.lineEdit_53.text()
        state = self.ui.lineEdit_52.text()
        telephone = self.ui.lineEdit_46.text()
        fax = self.ui.lineEdit_47.text()
        web = self.ui.lineEdit_51.text()
        sectorCode = self.ui.lineEdit_50.text()
        sector_desc = self.ui.lineEdit_55.text()
        hr_name = self.ui.lineEdit_48.text()
        hr_phone = self.ui.lineEdit_49.text()
        hr_email = self.ui.lineEdit_54.text()
        notes = self.ui.textEdit_5.toPlainText()
        firm_id = self.firm_existing_check()

        self.db_connect()

        sql = (
            "UPDATE firms SET cari_code=%s,name=%s,adress=%s,city=%s,state=%s,telephone=%s,fax=%s,web=%s,sector_code=%s,sector_desc=%s,hr_name=%s,hr_telephone=%s,hr_email=%s,notes=%s WHERE id=%s")

        self.cur.execute(sql, (
            caricode, name, adress, city, state, telephone, fax, web, sectorCode, sector_desc, hr_name, hr_phone,
            hr_email,
            notes, firm_id))

        self.db.commit()

        self.db.close()
        self.ui.lineEdit_23.setText(str(firm_id))
        self.firm_showAll()
        self.statusBar().showMessage('Firma Bilgileri Güncellendi')

    def firm_screen_clear(self):
        self.ui.lineEdit_45.setText('')
        self.ui.lineEdit_39.setText('')
        self.ui.textEdit_4.setPlainText('')
        self.ui.lineEdit_53.setText('')
        self.ui.lineEdit_52.setText('')
        self.ui.lineEdit_46.setText('')
        self.ui.lineEdit_47.setText('')
        self.ui.lineEdit_51.setText('')
        self.ui.lineEdit_50.setText('')
        self.ui.lineEdit_55.setText('')
        self.ui.lineEdit_48.setText('')
        self.ui.lineEdit_49.setText('')
        self.ui.lineEdit_54.setText('')
        self.ui.textEdit_5.setPlainText('')
        self.ui.lineEdit_23.setText('')
        self.statusBar().showMessage('Yeni Firma Ekleme')

    def firm_delete(self):

        global firm_id
        global quota_id

        firm_name = self.ui.lineEdit_39.text()

        if self.ui.lineEdit_23.text() != '':

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                " {} Nolu kayda ait {} firmanın kaydı siliniecektir.\nDevam Etmek için Discard tuşuna basın".format(
                     firm_id,firm_name))
            msgBox.setWindowTitle("DİKKAT - Veri Silinecek")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(lambda x: print(" Silme Butonu Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Discard:
                self.db_connect()

                sql = "DELETE FROM firms WHERE id={}".format(firm_id)

                self.cur.execute(sql)

                self.db.commit()
                self.statusBar().showMessage(
                    " {} Nolu kayda ait {} firmanın kaydı siliniecektir.\nDevam Etmek için Discard tuşuna basın".format(
                     firm_id,firm_name))
                self.db.close()
                self.ui.lineEdit_23.setText('')
                firm_id = 0
                self.ui.tableWidget_5.clearContents()
                self.firm_screen_clear()
                self.firm_showAll()
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("Silmek için önce  tablodan bir kayıt seçmelisiniz")
            msgBox2.setWindowTitle("DİKKAT - Veri Seçimi yapılmadı")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            msgBox2.buttonClicked.connect(lambda x: print(" OK Butonu Tıklandı"))
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" Kayıt Seçimi yapılmadı")

    def firm_existing_check(self):
        caricode = self.ui.lineEdit_45.text()

        self.db_connect()
        sql = "SELECT id,cari_code FROM firms WHERE cari_code={}".format(caricode)
        if self.cur.execute(sql):
            id, data = self.cur.fetchone()

            self.db.close()
            return id
        else:
            self.db.close()
            return None

    def firm_showAll(self):
        filter_val = self.ui.lineEdit_76.text()
        index_val = str(self.ui.comboBox_10.currentIndex())
        header = {'0': 'name', '1': 'cari_code', '2': 'adress', '3': 'hr_name'}
        if filter_val:
            sql = "SELECT id,cari_code,name,adress,city,state,telephone,fax,web,sector_code,sector_desc,hr_name,hr_telephone,hr_email,notes FROM firms WHERE {} LIKE '{}%'".format(
                header[index_val], filter_val)
        else:
            sql = "SELECT id,cari_code,name,adress,city,state,telephone,fax,web,sector_code,sector_desc,hr_name,hr_telephone,hr_email,notes FROM firms ORDER BY record_date DESC LIMIT 100"

        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_5.setRowCount(0)
            self.ui.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_5.rowCount()
                self.ui.tableWidget_5.insertRow(row_pos)
            self.statusBar().showMessage('Kayıtlar Getirili')
        else:
            self.statusBar().showMessage('Kayıt Bulunamadı. Arama kriterlerini değiştirin')

            self.ui.tableWidget_5.clearContents()

    # ============================================================================
    # ================ QUOTA BLOCKS ================================================
    def quota_invisible_objects(self):
        self.ui.label_121.setVisible(False)
        self.ui.label_122.setVisible(False)
        self.ui.label_123.setVisible(False)
        self.ui.label_124.setVisible(False)

    def quota_field_check(self):
        if (not self.ui.lineEdit_79.text() or
                not self.ui.lineEdit_77.text() or
                not self.ui.lineEdit_81.text() or

                not self.ui.textEdit_9.toPlainText()):
            warning = QMessageBox.warning(self, 'Eksik Veri Hatası',
                                          'Girilmesi zorunlu olan veriler bulunmaktadır. Lütfen eksik tüm alanları doldurun',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Eksik Veri hatası ')
            self.quota_visible_objects()
            return (False)
        else:
            self.quota_visible_objects()
            self.quota_add()
            return (True)

    def quota_firm_datail_upload(self, id):

        global firm_id
        self.db_connect()
        sql = "SELECT * FROM firms WHERE id={}".format(id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()
            firm_id = data[0]
            self.ui.lineEdit_70.setText(data[1])
            self.ui.lineEdit_75.setText(data[9])
            self.ui.lineEdit_78.setText(data[10])
            self.ui.lineEdit_69.setText(data[2])
            self.ui.lineEdit_71.setText(data[6])
            self.ui.lineEdit_72.setText(data[7])
            self.ui.lineEdit_68.setText(data[4])
            self.ui.lineEdit_67.setText(data[5])
            self.ui.textEdit_6.setPlainText(data[3])

            self.db.close()
            return data
        else:
            firm_id = 0
            self.db.close()
            return None

    def quota_visible_objects(self):

        if self.ui.textEdit_9.toPlainText() == '':
            self.ui.label_121.setVisible(True)
        else:
            self.ui.label_121.setVisible(False)

        if self.ui.lineEdit_79.text() == '':
            self.ui.label_122.setVisible(True)
        else:
            self.ui.label_122.setVisible(False)

        if self.ui.lineEdit_77.text() == '':
            self.ui.label_123.setVisible(True)
        else:
            self.ui.label_123.setVisible(False)

        if self.ui.lineEdit_81.text() == '':
            self.ui.label_124.setVisible(True)
        else:
            self.ui.label_124.setVisible(False)

    def quota_firm_window_call(self):
        global quota_id
        quota_id=0
        self.ui.lineEdit_24.setText('')
        self.firmDialog.show()


    def quota_add(self):
        global firm_id
        global quota_id

        caricoode = self.ui.lineEdit_70.text()
        sector_code = self.ui.lineEdit_75.text()
        sector_desc = self.ui.lineEdit_78.text()
        firm_name = self.ui.lineEdit_69.text()
        firm_telephone = self.ui.lineEdit_71.text()
        firm_fax = self.ui.lineEdit_72.text()
        city = self.ui.lineEdit_68.text()
        state = self.ui.lineEdit_67.text()
        adress = self.ui.textEdit_6.toPlainText()
        staff_name = self.ui.lineEdit_79.text()
        staff_title = self.ui.lineEdit_80.text()
        skills_req = self.ui.textEdit_8.toPlainText()
        session = self.ui.comboBox_14.currentText()
        internship_type = self.ui.comboBox_12.currentText()
        capacity_girl = self.ui.lineEdit_77.text()
        capacity_boy = self.ui.lineEdit_81.text()
        report = self.ui.textEdit_9.toPlainText()
        username_id = self.ui.lineEdit_5.text()

        if quota_id:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu Staj Yeri Kaydı Sistemde Kayıtlıdır.\nMevcut kaydı güncellemek için lütfen\n- SaveAll -  butonuna çıkmak için  -Cancel-  tusuna basın")
            msgBox.setWindowTitle("DİKKAT - Veriler Güncellenecek")
            msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.SaveAll)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            self.statusBar().showMessage('DİKKAT - Veriler Güncellenecek')
            if returnValue == QMessageBox.SaveAll:
                print('Save All clicked')
                self.quota_update(quota_id)
                return None
                self.quota_update(quota_id)
        else:

            self.db_connect()

            sql = '''INSERT INTO internship_capacity (session,internship_type,firm_id,firm_staff_name,firm_staff_title,capacity_girl,capacity_boy,skills_req,report,username_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            self.cur.execute(sql, (
                session, internship_type, firm_id, staff_name, staff_title, capacity_girl, capacity_boy, skills_req,
                report, username_id))

            self.db.commit()
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu {} Nolu Kayıt   , {} adlı Firmaaya Ait Staj Bilgileri Sisteme Başarıyla Kaydedilmiştir.\nDevam Etmek için OK tuşuna basın".format(
                    quota_id, firm_name))
            msgBox.setWindowTitle("DİKKAT - Veriler Sisteme Eklendi")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.quota_screen_clear()

            self.statusBar().showMessage('Yeni Kayıt oluşturuldu ve Staj Yeri Blgileri Eklendi')
            self.db.close()
            self.quota_showAll()

    def quota_update(self, quota_id):
        # caricoode = self.ui.lineEdit_70.text()
        # sector_code = self.ui.lineEdit_75.text()
        # sector_desc = self.ui.lineEdit_78.text()
        firm_name = self.ui.lineEdit_69.text()
        # firm_telephone = self.ui.lineEdit_71.text()
        # firm_fax = self.ui.lineEdit_72.text()
        # city = self.ui.lineEdit_68.text()
        # state = self.ui.lineEdit_67.text()
        # adress = self.ui.textEdit_6.toPlainText()
        staff_name = self.ui.lineEdit_79.text()
        staff_title = self.ui.lineEdit_80.text()
        skills_req = self.ui.textEdit_8.toPlainText()
        session = self.ui.comboBox_14.currentText()
        internship_type = self.ui.comboBox_12.currentText()
        capacity_girl = self.ui.lineEdit_77.text()
        capacity_boy = self.ui.lineEdit_81.text()
        report = self.ui.textEdit_9.toPlainText()
        username_id = self.ui.lineEdit_5.text()
        self.db_connect()

        sql = (
            "UPDATE internship_capacity SET session=%s,internship_type=%s,firm_id=%s,firm_staff_name=%s,firm_staff_title=%s,capacity_girl=%s,capacity_boy=%s,skills_req=%s,report=%s,username_id=%s WHERE id=%s")

        self.cur.execute(sql, (
            session, internship_type, firm_id, staff_name, staff_title, capacity_girl, capacity_boy, skills_req, report,
            username_id, quota_id))

        self.db.commit()

        self.db.close()
        self.quota_showAll()
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(
            "Bu {}  Nolu Kayıt   , {} adlı Firmaaya Ait Staj Bilgileri Güncellenmiştir .\nDevam Etmek için OK tuşuna basın".format(
                quota_id, firm_name))
        msgBox.setWindowTitle("DİKKAT - Veriler Başarıyla Güncellendi")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
        returnValue = msgBox.exec()
        self.statusBar().showMessage('Staj Yeri Bilgileri Güncellendi')

    def quota_delete(self):
        global internship_id
        global absent_id
        global quota_id
        session=self.ui.comboBox_14.currentText()
        internship_type=self.ui.lineEdit_69.text()
        firm_name = self.ui.comboBox_12.currentText()

        if self.ui.lineEdit_24.text() != '':

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "{} nolu Döneme ait ve {}  Staj Türünü olan  {} firmanın {} kaydı siliniecektir.\nDevam Etmek için Discard tuşuna basın".format(
                    session, internship_type, firm_name, quota_id))
            msgBox.setWindowTitle("DİKKAT - Veri Silinecek")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(lambda x: print(" Silme Butonu Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Discard:
                self.db_connect()

                sql = "DELETE FROM internship_capacity WHERE id={}".format(quota_id)

                self.cur.execute(sql)

                self.db.commit()
                self.statusBar().showMessage(
                    "{} nolu Döneme ait ve {}  Staj Türünü olan  {} firmanın {} kayıt Silinmiştir ".format(
                    session, internship_type, firm_name, quota_id))
                self.db.close()
                self.ui.lineEdit_24.setText('')
                quota_id = 0
                self.ui.tableWidget_7.clearContents()
                self.quota_screen_clear()
                self.quota_showAll()
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("Silmek için önce  tablodan bir kayıt seçmelisiniz")
            msgBox2.setWindowTitle("DİKKAT - Veri Seçimi yapılmadı")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            msgBox2.buttonClicked.connect(lambda x: print(" OK Butonu Tıklandı"))
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" KAyıt Seçimi yapılmadı")

    def quota_screen_clear(self):
        global quota_id
        caricoode = self.ui.lineEdit_70.setText('')
        sector_code = self.ui.lineEdit_75.setText('')
        sector_desc = self.ui.lineEdit_78.setText('')
        firm_name = self.ui.lineEdit_69.setText('')
        firm_telephone = self.ui.lineEdit_71.setText('')
        firm_fax = self.ui.lineEdit_72.setText('')
        city = self.ui.lineEdit_68.setText('')
        state = self.ui.lineEdit_67.setText('')
        adress = self.ui.textEdit_6.setPlainText('')
        staff_name = self.ui.lineEdit_79.setText('')
        capacity_girl = self.ui.lineEdit_77.setText('')
        capacity_boy = self.ui.lineEdit_81.setText('')
        staff_title = self.ui.lineEdit_80.setText('')
        skills_req = self.ui.textEdit_8.setPlainText('')
        quota_id = self.ui.lineEdit_24.setText('')
        report = self.ui.textEdit_9.setPlainText('')

    def quota_detail_upload_table(self):
        global quota_id
        global firm_id
        quota_id = self.ui.tableWidget_7.item(self.ui.tableWidget_7.currentRow(), 0).text()
        self.db_connect()
        sql = "SELECT * FROM internship_capacity WHERE id={} order by id DESC".format(quota_id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()
            firm_id = data[3]
            self.ui.lineEdit_24.setText(str(data[0]))
            self.ui.lineEdit_79.setText(data[4])
            self.ui.lineEdit_80.setText(data[5])
            self.ui.textEdit_8.setPlainText(data[8])
            self.ui.textEdit_9.setPlainText(data[9])
            self.ui.comboBox_14.setCurrentText(data[1])
            self.ui.lineEdit_77.setText(str(data[6]))
            self.ui.lineEdit_81.setText(str(data[7]))
            self.ui.comboBox_12.setCurrentText(data[2])

            self.db.close()
        self.quota_firm_datail_upload(firm_id)

    def quota_showAll(self):

        session = self.ui.comboBox_14.currentText()

        sql = "SELECT internship_capacity.id,internship_capacity.session,internship_capacity.internship_type,firms.name,internship_capacity.capacity_girl,internship_capacity.capacity_boy," \
              "internship_capacity.username_id, internship_capacity.report, internship_capacity.record_date FROM internship_capacity INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
              "WHERE session= {} order by internship_capacity.record_date desc".format(session)

        self.db_connect()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data:
            self.ui.tableWidget_7.setRowCount(0)
            self.ui.tableWidget_7.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_7.rowCount()
                self.ui.tableWidget_7.insertRow(row_pos)
            self.statusBar().showMessage('Kayıtlar Getirili')
        else:
            self.statusBar().showMessage('Kayıt Bulunamadı. Arama kriterlerini değiştirin')

            self.ui.tableWidget_7.clearContents()

    # ============================================================================
    # ================ INTERSHIP BLOCKS ================================================
    def internship_start_date_time(self):
        day = self.ui.dateEdit_3.date().day()
        month = self.ui.dateEdit_3.date().month()
        year = self.ui.dateEdit_3.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))

        self.ui.lineEdit_66.setText(str(date))

    def internship_finish_date_time(self):
        day = self.ui.dateEdit_4.date().day()
        month = self.ui.dateEdit_4.date().month()
        year = self.ui.dateEdit_4.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))

        self.ui.lineEdit_73.setText(str(date))

    def internship_invisible_objects(self):
        self.ui.label_125.setVisible(False)
        self.ui.label_126.setVisible(False)
        self.ui.label_127.setVisible(False)
        self.ui.label_128.setVisible(False)
        self.ui.label_129.setVisible(False)
        self.ui.label_130.setVisible(False)
        self.ui.label_131.setVisible(False)
        self.ui.label_164.setVisible(False)
        self.ui.label_165.setVisible(False)

    def internship_field_check(self):
        if (not self.ui.lineEdit_66.text() or
                not self.ui.lineEdit_73.text() or
                not self.ui.lineEdit_61.text() or
                not self.ui.lineEdit_25.text() or
                not self.ui.lineEdit_74.text()):
            warning = QMessageBox.warning(self, 'Eksik Veri veya Yanlış Seçim Hatası',
                                          'Lütfen Tüm bilgileri tekrar kontrol edin ve eksik tüm alanları doldurun',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Eksik Veri hatası ')
            self.internship_visible_objects()
            return (False)



        if  not ((self.ui.lineEdit_113.text()=='K' and int(self.ui.lineEdit_86.text())>0)or
                (self.ui.lineEdit_113.text()=='E' and int(self.ui.lineEdit_28.text())>0)):
            warning = QMessageBox.warning(self, 'Kontenjan Yetersiz ,Hatası',
                                          'Lütfen Kontenjan Bilgileri Kontrol Edin.\nFirma veya Öğrenci seçimini değiştirin.',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Yanlış Seçim Hatası ')
            self.internship_visible_objects()
            return (False)

        global internship_id
        global student_id

        session=self.ui.lineEdit_90.text()
        internship_type=self.ui.lineEdit_94.text()
        self.db_connect()
        sql = "SELECT COUNT(distinct student_id) " \
              "FROM internship " \
              "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
              "WHERE  internship_capacity.session='{}' AND internship_capacity.internship_type='{}' and internship.student_id={}".format(session,internship_type,student_id)
        if self.cur.execute(sql):
            data, = self.cur.fetchone()

            self.db.close()
            if data>=1:
                warning = QMessageBox.warning(self, 'Öğrenci Seçim Hatası',
                                              'Bu öğrenci Bu dönem için zaten kaydedilmiştir. \n Lütfen BAşka bir öğrenci seçin',
                                              QMessageBox.Ok)
                self.statusBar().showMessage('Yanlış Seçim Hatası ')
                self.internship_visible_objects()
                return (False)



        self.internship_visible_objects()
        self.internship_add()
        return (True)

    def internship_visible_objects(self):

        if self.ui.lineEdit_66.text() == '':
            self.ui.label_125.setVisible(True)
        else:
            self.ui.label_125.setVisible(False)

        if self.ui.lineEdit_73.text() == '':
            self.ui.label_126.setVisible(True)
        else:
            self.ui.label_126.setVisible(False)

        if self.ui.lineEdit_74.text() == '':
            self.ui.label_127.setVisible(True)
        else:
            self.ui.label_127.setVisible(False)

        if self.ui.lineEdit_61.text() == '':
            self.ui.label_128.setVisible(True)
            self.ui.label_130.setVisible(False)
        else:
            self.ui.label_128.setVisible(False)
            self.ui.label_131.setVisible(True)

        if self.ui.lineEdit_25.text() == '':
            self.ui.label_129.setVisible(True)
            self.ui.label_131.setVisible(False)
        else:
            self.ui.label_129.setVisible(False)
            self.ui.label_131.setVisible(True)

        if self.ui.lineEdit_113.text()=='E' or ( self.ui.lineEdit_113.text()=='K' and int(self.ui.lineEdit_86.text())>0):

            self.ui.label_164.setVisible(False)
        else:
            self.ui.label_164.setVisible(True)

        if self.ui.lineEdit_113.text()=='K' or ( self.ui.lineEdit_113.text()=='E' and int(self.ui.lineEdit_28.text())>0):
            self.ui.label_165.setVisible(False)
        else:
            self.ui.label_165.setVisible(True)

    def internship_student_call(self, id):

        self.db_connect()
        sql = "SELECT name,surname,tc_no,school_number,departure,class_level,class,sexual,image_link FROM students WHERE id={} order by id DESC".format(id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.ui.lineEdit_59.setText(data[0])        # öğrenci adı
            self.ui.lineEdit_58.setText(data[1])        # soyadı
            self.ui.lineEdit_61.setText(str(data[2]))   #TC No
            self.ui.lineEdit_62.setText(str(data[3]))   #okul No
            self.ui.lineEdit_63.setText(data[4])         #bolum
            self.ui.lineEdit_64.setText(str(data[5]))   #seviye
            self.ui.lineEdit_65.setText(data[6])        #  sube
            self.ui.lineEdit_113.setText(data[7])        # cinsiyet
            new_file_name = data[8]
            pic_path = STUDENT_IMAGES_DIR + new_file_name

            picture = QPixmap(pic_path)
            self.ui.label_67.setPixmap(picture)
            self.ui.label_67.setScaledContents(True)
            self.db.close()

    def quota_dialog_window_call(self):

        self.quotaDialog.show()

    def quota_dialog_turn_window(self, id):
        self.ui.lineEdit_25.setText(str(quota_id))

        global firm_id

        self.db_connect()
        sql = "SELECT internship_capacity.id,internship_capacity.session,internship_capacity.internship_type,firms.name,internship_capacity.capacity_girl,internship_capacity.capacity_boy," \
              "internship_capacity.username_id FROM internship_capacity INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
              "WHERE internship_capacity.id= '{}' order by id desc".format(quota_id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.ui.lineEdit_84.setText(data[3])
            self.ui.lineEdit_90.setText(data[1])
            self.ui.lineEdit_94.setText(data[2])
            self.ui.lineEdit_83.setText(str(data[4]))
            self.ui.lineEdit_82.setText(str(data[5]))
            self.ui.label_131.setVisible(True)
            self.ui.label_129.setVisible(False)
            self.db.close()
            self.cal_total_quota()

    def internship_add(self):
        global internship_id
        global student_id

        quota_id = self.ui.lineEdit_25.text()
        start_date = self.ui.lineEdit_66.text()
        finish_date = self.ui.lineEdit_73.text()
        internship_day = self.ui.lineEdit_74.text()
        note = self.ui.textEdit_7.toPlainText()
        username_id = self.ui.lineEdit_5.text()

        if internship_id:

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu {} Nolu Kayıt Ait Staj Bilgileri Sistemde Kayıtlı Görünmektedir.Tüm Bilgiler güncellenecektir.\nDevam Etmek için OK tuşuna basın".format(
                    internship_id))
            msgBox.setWindowTitle("DİKKAT - Veriler Güncellenecek")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.internship_update(internship_id)
        else:

            self.db_connect()

            sql = "INSERT INTO internship (student_id,quota_id,start_date,finish_date,internship_day,notes,username_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"

            self.cur.execute(sql, (student_id, quota_id, start_date, finish_date, internship_day, note, username_id))

            self.db.commit()
            self.statusBar().showMessage('Yeni Kayıt oluşturuldu ve Staj Yeri ilgili Öğrenciye Atandı')
            self.db.close()
            self.internship_showAll()
            self.cal_total_quota()
            self.ui.lineEdit_57.setText(str(internship_id))

    def internship_delete(self):
        global internship_id
        global absent_id
        student_name = self.ui.lineEdit_59.text()
        student_surname = self.ui.lineEdit_58.text()
        firm_name=self.ui.lineEdit_84.text()


        if self.ui.lineEdit_59.text() !='':

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu {} {}  Adlı Öğrenciye ve {} firmasına atanmaış  {} Nolu Kaydada ait tüm Bilgiler siliniecektir.\nDevam Etmek için Discard tuşuna basın".format(
                    student_name, student_surname, firm_name, internship_id))
            msgBox.setWindowTitle("DİKKAT - Veri Silinecek")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(lambda x: print(" Silme Butonu Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Discard:
                self.db_connect()

                sql = "DELETE FROM internship WHERE id={}".format(internship_id)

                self.cur.execute(sql)

                self.db.commit()
                self.statusBar().showMessage(
                    ' {} {} adlı öğrencinin ilgili devamsızlık kaydı silinmiştir.'.format(student_name,
                                                                                          student_surname))
                self.db.close()
                self.ui.lineEdit_25.setText('')
                internship_id = 0
                self.ui.tableWidget_4.clearContents()
                self.internship_screen_clear()
                self.internship_showAll()
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("Silmek için önce  tablodan bir kayıt seçmelisiniz")
            msgBox2.setWindowTitle("DİKKAT - Veri Seçimi yapılmadı")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            msgBox2.buttonClicked.connect(lambda x: print(" OK Butonu Tıklandı"))
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" KAyıt Seçimi yapılmadı")

    def internship_update(self, id):
        global internship_id
        global student_id
        global quota_id
        global firm_id

        quota_id = self.ui.lineEdit_25.text()
        start_date = self.ui.lineEdit_66.text()
        finish_date = self.ui.lineEdit_73.text()
        internship_day = self.ui.lineEdit_74.text()
        note = self.ui.textEdit_7.toPlainText()
        username_id = self.ui.lineEdit_5.text()
        if not self.ui.lineEdit_61.text() or not self.ui.lineEdit_25.text():
            warning = QMessageBox.warning(self, 'Veri Hatası',
                                          'Eksik veriler  görünmektedir.\n Lütfen bilgileri doldurunuz',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Veri hatası ')
            return None
        self.db_connect()

        sql = (
            "UPDATE internship SET student_id=%s,quota_id=%s,start_date=%s,finish_date=%s,internship_day=%s,notes=%s,username_id=%s WHERE id=%s")

        self.cur.execute(sql, (
            student_id, quota_id, start_date, finish_date, internship_day, note, username_id, internship_id))

        self.db.commit()

        self.db.close()
        self.internship_showAll()
        self.cal_total_quota()
        self.ui.lineEdit_57.setText(internship_id)
        self.statusBar().showMessage('Öğrencinin Staj Yeri Bilgileri Güncellendi')

    def internship_screen_clear(self):
        global internship_id
        global student_id
        global quota_id
        internship_id = 0
        student_id = 0
        quota_id = 0
        self.ui.lineEdit_25.setText('')
        start_date = self.ui.lineEdit_66.setText('')
        finish_date = self.ui.lineEdit_73.setText('')
        internship_day = self.ui.lineEdit_74.setText('')
        note = self.ui.textEdit_7.setPlainText('')
        self.ui.label_67.setPixmap(None)
        self.ui.lineEdit_59.setText('')
        self.ui.lineEdit_58.setText('')
        self.ui.lineEdit_61.setText('')
        self.ui.lineEdit_62.setText('')
        self.ui.lineEdit_63.setText('')
        self.ui.lineEdit_64.setText('')
        self.ui.lineEdit_65.setText('')
        self.ui.lineEdit_84.setText('')
        self.ui.lineEdit_90.setText('')
        self.ui.lineEdit_94.setText('')
        self.ui.lineEdit_83.setText('')
        self.ui.lineEdit_82.setText('')
        self.ui.lineEdit_113.setText('')
        self.ui.lineEdit_86.setText('')
        self.ui.lineEdit_28.setText('')
        self.ui.label_130.setVisible(False)
        self.ui.label_131.setVisible(False)
        self.ui.label_128.setVisible(False)
        self.ui.label_129.setVisible(False)
        self.ui.lineEdit_57.setText('')

    def internship_detail_upload_table(self):
        global internship_id
        global student_id
        global quota_id
        global firm_id
        internship_id = int(self.ui.tableWidget_4.item(self.ui.tableWidget_4.currentRow(), 0).text())

        self.db_connect()
        sql = "SELECT internship_capacity.session,internship_capacity.internship_type,firms.name," \
              "students.name,students.surname, students.tc_no,students.school_number," \
              "students.departure,students.class_level, students.class,students.image_link," \
              "internship.start_date,internship.finish_date,internship.internship_day,internship.notes,internship.username_id, " \
              "internship_capacity.firm_id,internship.quota_id,internship.student_id, " \
              "internship_capacity.capacity_girl,internship_capacity.capacity_boy,internship.id " \
              "FROM internship " \
              "INNER JOIN students ON internship.student_id=students.id " \
              "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
              "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
              "WHERE internship.id='{}'".format(internship_id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.ui.lineEdit_58.setText(data[4])
            self.ui.lineEdit_59.setText(data[3])
            self.ui.lineEdit_61.setText(str(data[5]))
            self.ui.lineEdit_62.setText(data[6])
            self.ui.lineEdit_63.setText(data[7])
            self.ui.lineEdit_64.setText(data[8])
            self.ui.lineEdit_65.setText(data[9])
            self.ui.lineEdit_66.setText(str(data[11]))
            self.ui.lineEdit_73.setText(str(data[12]))
            self.ui.lineEdit_74.setText(data[13])
            self.ui.lineEdit_25.setText(str(data[16]))
            self.ui.lineEdit_84.setText(data[2])
            self.ui.lineEdit_90.setText(data[0])
            self.ui.lineEdit_94.setText(data[1])
            self.ui.lineEdit_82.setText(str(data[20]))
            self.ui.lineEdit_83.setText(str(data[19]))
            self.ui.lineEdit_57.setText(str(data[21]))
            self.ui.textEdit_7.setPlainText(data[14])
            student_id = data[18]
            quota_id = data[17]
            firm_id = data[16]
            self.db.close()
            new_file_name = data[10]
            pic_path = STUDENT_IMAGES_DIR + new_file_name

            picture = QPixmap(pic_path)
            self.ui.label_67.setPixmap(picture)
            self.ui.label_67.setScaledContents(True)

            self.ui.label_130.setVisible(True)
            self.ui.label_131.setVisible(True)

    def internship_showAll(self):
        global internship_id
        global student_id
        global quota_id
        global firm_id

        self.db_connect()
        sql = "SELECT internship.id, internship_capacity.session,internship_capacity.internship_type,firms.name," \
              "students.name,students.surname, " \
              "internship.start_date,internship.finish_date,internship.notes,internship.username_id " \
              "FROM internship " \
              "INNER JOIN students ON internship.student_id=students.id " \
              "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
              "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
              "ORDER BY internship.record_date DESC "
        if self.cur.execute(sql):
            data = self.cur.fetchall()

            self.db.close()
            if data:
                self.ui.tableWidget_4.setRowCount(0)
                self.ui.tableWidget_4.insertRow(0)
                for row, form in enumerate(data):
                    for column, item in enumerate(form):
                        self.ui.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                    row_pos = self.ui.tableWidget_4.rowCount()
                    self.ui.tableWidget_4.insertRow(row_pos)
                self.statusBar().showMessage('Kayıtlar Getirili')
            else:
                self.statusBar().showMessage('Kayıt Bulunamadı. Arama kriterlerini değiştirin')

                self.ui.tableWidget_4.clearContents()

        self.ui.lineEdit_57.setText(str(internship_id))

    def internship_list_showall(self):
        global internship_id
        global student_id
        global quota_id
        global firm_id
        session=self.ui.comboBox_22.currentText()
        filter_val = self.ui.lineEdit_56.text()
        index_val = str(self.ui.comboBox_11.currentIndex())
        header = {'0': 'internship_capacity.internship_type', '1': 'firms.name', '2': 'students.name', '3': 'students.surname', '4': 'students.class_level', '5': 'students.class',
                  '6': 'students.sexual'}
        if filter_val:
            sql = "SELECT internship.id, internship_capacity.session,internship_capacity.internship_type,firms.name," \
                  "students.name,students.surname, " \
                  "internship.start_date,internship.finish_date,internship.notes,internship.username_id,students.sexual " \
                  "FROM internship " \
                  "INNER JOIN students ON internship.student_id=students.id " \
                  "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
                  "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
                  "WHERE internship_capacity.session={} AND {} LIKE '{}%'".format(
                session,header[index_val], filter_val)
        else:
            if session=='':
                sql = "SELECT internship.id, internship_capacity.session,internship_capacity.internship_type,firms.name," \
                      "students.name,students.surname, " \
                      "internship.start_date,internship.finish_date,internship.notes,internship.username_id " \
                      "FROM internship " \
                      "INNER JOIN students ON internship.student_id=students.id " \
                      "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
                      "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
                      "ORDER BY internship.record_date DESC "
            else:
                sql = "SELECT internship.id, internship_capacity.session,internship_capacity.internship_type,firms.name," \
                      "students.name,students.surname, " \
                      "internship.start_date,internship.finish_date,internship.notes,internship.username_id " \
                      "FROM internship " \
                      "INNER JOIN students ON internship.student_id=students.id " \
                      "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
                      "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
                      "WHERE  internship_capacity.session='{}'".format(session)

        self.db_connect()

        self.cur.execute(sql)
        data = self.cur.fetchall()

        self.db.close()
        if data:
            self.ui.tableWidget_9.setRowCount(0)
            self.ui.tableWidget_9.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_9.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_9.rowCount()
                self.ui.tableWidget_9.insertRow(row_pos)
        else:
            self.ui.tableWidget_9.clearContents()
        return data

    def internship_unassigned_list_show(self):
        global internship_id
        global student_id

        session = self.ui.comboBox_27.currentText()
        internship_type = self.ui.comboBox_28.currentText()
        class_level = str(self.ui.comboBox_25.currentText())
        class_name = self.ui.comboBox_26.currentText()


        sql = "SELECT name,surname,class_level,class FROM students " \
              "WHERE (class='{}' AND class_level='{}') AND " \
              "id NOT IN (SELECT student_id FROM internship " \
              "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
              "WHERE internship_capacity.session='{}' AND internship_capacity.internship_type='{}' )" \
              "".format(class_name, class_level,session,internship_type)
        self.db_connect()

        self.cur.execute(sql)
        data = self.cur.fetchall()

        self.db.close()
        if data:
            self.ui.tableWidget_11.setRowCount(0)
            self.ui.tableWidget_11.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.tableWidget_11.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_11.rowCount()
                self.ui.tableWidget_11.insertRow(row_pos)
        else:
            self.ui.tableWidget_11.clearContents()

    def export_internship_list(self):
        wb = Workbook(REPORT_DIR + '\\report_internship.xlsx', )
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Kayıt No')
        sheet1.write(0, 1, 'Donem')
        sheet1.write(0, 2, 'Staj Turu')
        sheet1.write(0, 3, 'Firma Adı')
        sheet1.write(0, 4, 'Öğrenci Adı')
        sheet1.write(0, 5, 'Öğrenci Soyadı')
        sheet1.write(0, 6, 'Staj Başlama Tarihi')
        sheet1.write(0, 7, 'Staj Bitirme Tarihi')
        sheet1.write(0, 8, 'Staj Notları')
        # sheet1.write(0, 9, 'Kaydeden Öğretmen')
        # sheet1.write(0, 10, 'Universite Bölümü')
        # sheet1.write(0, 11, 'Profil Resmi')
        # sheet1.write(0, 12, 'CV Adı')
        # sheet1.write(0, 13, 'FB Link')
        # sheet1.write(0, 14, 'Linkdn Link')
        # sheet1.write(0, 15, 'Blog Link')
        # sheet1.write(0, 16, 'Other Link')
        # sheet1.write(0, 17, 'Kayıt Zamanı')

        data = self.internship_list_showall()
        row_number = 1
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_number, column_num, str(item))
                column_num += 1
            row_number += 1

        wb.close()
        info = QMessageBox.information(self, 'İşlem Tamamlandı',
                                       'Excel Dosyası  Başarıyla oluşturuldu.\n {} \nadresindeki -report_internship.xlsx- dosyaya bakabilrsiniz. '.format(
                                           REPORT_DIR),
                                       QMessageBox.Ok)

        self.statusBar().showMessage('Excel Dosyası oluşturuldu ')

    # ============================================================================
    # ================ ABSENT BLOCKS ================================================
    def absent_date_time(self):
        day = self.ui.dateEdit_5.date().day()
        month = self.ui.dateEdit_5.date().month()
        year = self.ui.dateEdit_5.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))

        self.ui.lineEdit_92.setText(str(date))

    def absent_invisible_objects(self):
        self.ui.label_136.setVisible(False)
        self.ui.label_138.setVisible(False)
        self.ui.label_143.setVisible(False)
        self.ui.label_145.setVisible(False)

    def absent_field_check(self):
        if (not self.ui.lineEdit_92.text() or
                self.ui.comboBox_23.currentIndex()==0 or
                not self.ui.lineEdit_36.text() or
                not self.ui.lineEdit_104.text() or
                not self.ui.lineEdit_95.text()):
            warning = QMessageBox.warning(self, 'Eksik Veri Hatası',
                                          'Girilmesi zorunlu olan veriler bulunmaktadır. Lütfen eksik tüm alanları doldurun',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Eksik Veri hatası ')
            self.absent_visible_objects()
            return (False)
        else:
            self.absent_visible_objects()
            self.absent_add()
            return (True)

    def absent_visible_objects(self):

        if self.ui.lineEdit_92.text() == '':
            self.ui.label_143.setVisible(True)
        else:
            self.ui.label_143.setVisible(False)

        if self.ui.comboBox_23.currentIndex() == 0:
            self.ui.label_145.setVisible(True)
        else:
            self.ui.label_145.setVisible(False)

        if self.ui.lineEdit_36.text() == '':
            self.ui.label_136.setVisible(True)
            self.ui.label_138.setVisible(False)
        else:
            self.ui.label_136.setVisible(False)
            self.ui.label_138.setVisible(True)


    def absent_dialog_window_call(self):

        self.internshipDialog.show()

    def internship_dialog_turn_window(self,id):
        global internship_id
        global student_id
        global quota_id
        global firm_id

        self.absent_clear_for_new_record()
        self.db_connect()
        sql = "SELECT internship_capacity.session,internship_capacity.internship_type,firms.name," \
              "students.name,students.surname, students.tc_no,students.school_number," \
              "students.departure,students.class_level, students.class,students.image_link," \
              "internship.start_date,internship.finish_date,internship.internship_day,internship.notes,internship.username_id, " \
              "internship_capacity.firm_id,internship.quota_id,internship.student_id, " \
              "internship_capacity.capacity_girl,internship_capacity.capacity_boy " \
              "FROM internship " \
              "INNER JOIN students ON internship.student_id=students.id " \
              "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
              "INNER JOIN firms ON internship_capacity.firm_id=firms.id " \
              "WHERE internship.id='{}'".format(id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.ui.lineEdit_98.setText(data[0])
            self.ui.lineEdit_99.setText(data[1])
            self.ui.lineEdit_95.setText(data[2])
            self.ui.lineEdit_104.setText(data[3])
            self.ui.lineEdit_103.setText(data[4])
            self.ui.lineEdit_105.setText(data[6])
            self.ui.lineEdit_106.setText(data[7])
            self.ui.lineEdit_107.setText(str(data[8]))
            self.ui.lineEdit_108.setText(data[9])


            student_id = data[15]
            quota_id = data[14]
            firm_id = data[13]
            self.db.close()
            new_file_name = data[10]
            pic_path = STUDENT_IMAGES_DIR + new_file_name

            picture = QPixmap(pic_path)
            self.ui.label_152.setPixmap(picture)
            self.ui.label_152.setScaledContents(True)
            self.ui.lineEdit_36.setText(str(internship_id))
            self.ui.label_138.setVisible(True)
            self.ui.label_136.setVisible(False)
            self.absent_showAll(internship_id)

    def absent_add(self):
        global internship_id
        global student_id
        student_name=self.ui.lineEdit_104.text()
        student_surname=self.ui.lineEdit_103.text()
        internship_id = self.ui.lineEdit_36.text()
        absent_date = self.ui.lineEdit_92.text()
        absent_type = self.ui.comboBox_23.currentText()
        absent_report = self.ui.comboBox_24.currentText()
        note = self.ui.textEdit_10.toPlainText()
        username_id = self.ui.lineEdit_5.text()

        if absent_id:

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu {} {}  Adlı Öğrenciye Ait {} Nolu Kaydada ait tüm Bilgiler güncellenecektir.\nDevam Etmek için OK tuşuna basın".format(
                    student_name,student_surname,absent_id))
            msgBox.setWindowTitle("DİKKAT - Veriler Güncellenecek")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(lambda x: print("Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.absent_update(absent_id)
        else:

            self.db_connect()

            sql = "INSERT INTO absent (internship_id,username_id,abs_date,abs_type,note,report_invalid) VALUES (%s,%s,%s,%s,%s,%s)"

            self.cur.execute(sql, (internship_id,username_id,absent_date,absent_type,note,absent_report))

            self.db.commit()
            self.statusBar().showMessage('Yeni Kayıt oluşturuldu ve Devamsızlık Bİlgileri {} {} adlı öğrenciye eklendi'.format(student_name,student_surname))
            self.db.close()
            self.absent_showAll(internship_id)

    def absent_update(self,id):
        global internship_id
        global student_id
        global quota_id
        global firm_id

        student_name = self.ui.lineEdit_104.text()
        student_surname = self.ui.lineEdit_103.text()
        internship_id = self.ui.lineEdit_36.text()
        absent_date = self.ui.lineEdit_92.text()
        absent_type = self.ui.comboBox_23.currentText()
        absent_report = self.ui.comboBox_24.currentText()
        note = self.ui.textEdit_10.toPlainText()
        username_id = self.ui.lineEdit_5.text()

        if not self.ui.lineEdit_92.text() or not self.ui.comboBox_23.currentText():
            warning = QMessageBox.warning(self, 'Veri Hatası',
                                          'Eksik veriler  görünmektedir.\n Lütfen bilgileri doldurunuz',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Veri hatası ')
            return None
        self.db_connect()

        sql = (
            "UPDATE absent SET internship_id=%s,username_id=%s,abs_date=%s,abs_type=%s,note=%s,report_invalid=%s WHERE id=%s")

        self.cur.execute(sql, (internship_id,username_id,absent_date,absent_type,note,absent_report,absent_id))

        self.db.commit()
        self.db.close()
        self.absent_showAll(internship_id)
        self.statusBar().showMessage('Öğrencinin Devamsızlık Bilgileri Güncellendi')

    def absent_delete(self):
        global internship_id
        global absent_id
        student_name = self.ui.lineEdit_104.text()
        student_surname = self.ui.lineEdit_103.text()
        internship_id = self.ui.lineEdit_36.text()


        if absent_id>0:

            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(
                "Bu {} {}  Adlı Öğrenciye Ait {} Nolu Kaydada ait tüm Bilgiler siliniecektir.\nDevam Etmek için Discard tuşuna basın".format(
                    student_name, student_surname, absent_id))
            msgBox.setWindowTitle("DİKKAT - Veri Silinecek")
            msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(lambda x: print(" Silme Butonu Tıklandı"))
            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Discard:
                self.db_connect()

                sql = "DELETE FROM absent WHERE id={}".format(absent_id)

                self.cur.execute(sql)

                self.db.commit()
                self.statusBar().showMessage(
                    ' {} {} adlı öğrencinin ilgili devamsızlık kaydı silinmiştir.'.format(student_name,
                                                                                                          student_surname))
                self.db.close()
                self.ui.lineEdit_102.setText('')
                absent_id=0
                self.ui.tableWidget_3.clearContents()
                self.absent_showAll(internship_id)
                return True
        else:
            msgBox2 = QMessageBox(self)
            msgBox2.setIcon(QMessageBox.Information)
            msgBox2.setText("Silmek için önce  tablodan bir kayıt seçmelisiniz")
            msgBox2.setWindowTitle("DİKKAT - Veri Seçimi yapılmadı")
            msgBox2.setStandardButtons(QMessageBox.Ok)
            msgBox2.buttonClicked.connect(lambda x: print(" OK Butonu Tıklandı"))
            returnValue = msgBox2.exec()
            self.statusBar().showMessage(" KAyıt Seçimi yapılmadı")



    def absent_detail_from_table_call(self):
        global internship_id
        global student_id
        global quota_id
        global firm_id
        global absent_id
        absent_id = int(self.ui.tableWidget_3.item(self.ui.tableWidget_3.currentRow(), 0).text())

        self.db_connect()
        sql = "SELECT id, abs_date,abs_type,report_invalid,username_id,note " \
              "FROM absent " \
              "WHERE internship_id={} AND id={}".format(internship_id,absent_id)

        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.db.close()

        self.ui.lineEdit_102.setText(str(data[0]))
        self.ui.lineEdit_92.setText(data[1])
        self.ui.comboBox_23.setCurrentText(data[2])
        self.ui.comboBox_24.setCurrentText(data[3])

        self.ui.textEdit_10.setPlainText(data[5])

    def absent_showAll(self,id):
        global internship_id
        global student_id
        global quota_id
        global firm_id

        self.db_connect()
        sql = "SELECT id, abs_date,abs_type,report_invalid,username_id,note " \
              "FROM absent " \
              "WHERE internship_id={} " \
              "ORDER BY record_date DESC ".format(id)
        if self.cur.execute(sql):
            data = self.cur.fetchall()

            self.db.close()
            if data:
                self.ui.tableWidget_3.setRowCount(0)
                self.ui.tableWidget_3.insertRow(0)
                for row, form in enumerate(data):
                    for column, item in enumerate(form):
                        self.ui.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                        column += 1
                    row_pos = self.ui.tableWidget_3.rowCount()
                    self.ui.tableWidget_3.insertRow(row_pos)
                self.statusBar().showMessage('Kayıtlar Getirili')
            else:
                self.statusBar().showMessage('Kayıt Bulunamadı. Arama kriterlerini değiştirin')
                self.ui.tableWidget_3.clearContents()
            return data

    def absent_clear_for_new_record(self):


        global absent_id

        absent_id = 0
        student_name = self.ui.lineEdit_104.setText('')
        student_surname = self.ui.lineEdit_103.setText('')
        self.ui.lineEdit_36.setText('')
        absent_date = self.ui.lineEdit_92.setText('')
        absent_type = self.ui.comboBox_23.setCurrentText('')
        absent_report = self.ui.comboBox_24.setCurrentText('')
        note = self.ui.textEdit_10.setPlainText('')
        self.ui.lineEdit_105.setText('')
        self.ui.lineEdit_106.setText('')
        self.ui.lineEdit_107.setText('')
        self.ui.lineEdit_108.setText('')
        self.ui.lineEdit_36.setText('')
        self.ui.lineEdit_95.setText('')
        self.ui.lineEdit_98.setText('')
        self.ui.lineEdit_99.setText('')
        self.ui.lineEdit_102.setText('')
        self.ui.tableWidget_3.clearContents()

        self.ui.label_152.setPixmap(None)
        self.ui.label_136.setVisible(False)
        self.ui.label_143.setVisible(False)
        self.ui.label_136.setVisible(False)
        self.ui.label_138.setVisible(False)

    def absent_screen_clear(self):
        global internship_id
        global student_id
        global quota_id
        global absent_id

        absent_date = self.ui.lineEdit_92.setText('')
        absent_type = self.ui.comboBox_23.setCurrentText('')
        absent_report = self.ui.comboBox_24.setCurrentText('')
        note = self.ui.textEdit_10.setPlainText('')
        absent_id=0
        self.ui.lineEdit_102.setText('')


    def export_absent_for_student(self):
        global internship_id
        if not self.ui.lineEdit_36.text():
            warning = QMessageBox.warning(self, 'Eksik Veri Hatası',
                                          'Henüz Bir Öğrenci Seçmediniz. Lütfen Lütfen bir öürenci seçimi yapın',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Eksik Veri hatası ')
        student_name = self.ui.lineEdit_104.text()
        student_surname = self.ui.lineEdit_103.text()
        student_class=self.ui.lineEdit_108.text()
        student_class_level=self.ui.lineEdit_107.text()
        student_class_number = self.ui.lineEdit_105.text()
        firm_name=self.ui.lineEdit_95.text()
        internship_type=self.ui.lineEdit_99.text()
        session = self.ui.lineEdit_98.text()
        internship_id = self.ui.lineEdit_36.text()
        absent_date = self.ui.lineEdit_92.text()
        absent_type = self.ui.comboBox_23.currentText()
        absent_report = self.ui.comboBox_24.currentText()
        note = self.ui.textEdit_10.toPlainText()
        username_id = self.ui.lineEdit_5.text()



        wb = Workbook(REPORT_DIR + '\\report_devamsizlik_{}_{}.xlsx'.format(student_name, student_surname))
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'Öğrenci Adı :')
        sheet1.write(0, 1, student_name)
        sheet1.write(0, 2, student_surname)
        sheet1.write(1, 0, 'Firma Adı :')
        sheet1.write(1, 1, firm_name)
        sheet1.write(2, 0, 'Staj Türü :')
        sheet1.write(2, 1, internship_type)
        sheet1.write(2, 0, 'Staj Türü :')
        sheet1.write(2, 1, internship_type)
        sheet1.write(3, 0, 'Staj Dönemi :')
        sheet1.write(3, 1, session)
        sheet1.write(3, 0, 'Öğrencinin Sınıfı  :')
        sheet1.write(3, 1, student_class_level)
        sheet1.write(3, 2, student_class)
        sheet1.write(4, 0, 'Öğrenci Numarası  :')
        sheet1.write(4, 1, student_class_number)
        sheet1.write(5, 0, 'KAydı Alan Öğretmen  :')
        sheet1.write(5, 1, username_id)

        sheet1.write(6, 0, 'Kayıt No')
        sheet1.write(6, 1, 'Devamsızlık Günü')
        sheet1.write(6, 2, 'Devamsızlık Türü')
        sheet1.write(6, 3, 'Rapor Durumu')
        sheet1.write(6, 4, 'Kontrol Eden Öğretmen')
        sheet1.write(6, 5, 'Not')
        # sheet1.write(6, 6, 'Staj Başlama Tarihi')
        # sheet1.write(6, 7, 'Staj Bitirme Tarihi')
        # sheet1.write(6, 8, 'Staj Notları')
        # sheet1.write(0, 9, 'Kaydeden Öğretmen')
        # sheet1.write(0, 10, 'Universite Bölümü')
        # sheet1.write(0, 11, 'Profil Resmi')
        # sheet1.write(0, 12, 'CV Adı')
        # sheet1.write(0, 13, 'FB Link')
        # sheet1.write(0, 14, 'Linkdn Link')
        # sheet1.write(0, 15, 'Blog Link')
        # sheet1.write(0, 16, 'Other Link')
        # sheet1.write(0, 17, 'Kayıt Zamanı')

        data = self.absent_showAll(internship_id)
        row_number = 7
        for row in data:
            column_num = 0
            for item in row:
                sheet1.write(row_number, column_num, str(item))
                column_num += 1
            row_number += 1

        wb.close()
        info = QMessageBox.information(self, 'İşlem Tamamlandı',
                                       'Excel Dosyası  Başarıyla oluşturuldu.\n {} \nadresindeki -report_devamsizlik.xlsx- dosyaya bakabilrsiniz. '.format(
                                           REPORT_DIR),
                                       QMessageBox.Ok)

        self.statusBar().showMessage('Excel Dosyası oluşturuldu ')

    # ============================================================================
    # ================ THEMES ================================================

    def theme_1(self):
        style = open('staticfiles/themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def theme_2(self):
        style = open('staticfiles/themes/qdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def theme_3(self):
        style = open('staticfiles/themes/qdarkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    # ============================================================================
    # ================ CALCULATIONS ================================================
    def cal_total_quota(self):
        global firm_id
        self.db_connect()
        session = self.ui.comboBox_15.currentText()
        internship_type = self.ui.comboBox_13.currentText()

        sql1 = "SELECT SUM(capacity_girl) FROM internship_capacity WHERE session='{}' AND internship_type='{}'".format(
            session, internship_type)
        sql2 = "SELECT SUM(capacity_boy) FROM internship_capacity WHERE session='{}' AND internship_type='{}'".format(
            session, internship_type)
        sql3 = "SELECT count(internship.id) FROM internship " \
               "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
               "INNER JOIN students ON internship.student_id=students.id WHERE internship_capacity.internship_type='{}' AND  internship_capacity.session='{}' AND students.sexual='K'".format(
            internship_type,session)
        sql4 = "SELECT count(internship.id) FROM internship " \
               "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
               "INNER JOIN students ON internship.student_id=students.id WHERE internship_capacity.internship_type='{}' AND internship_capacity.session='{}' AND students.sexual='E'".format(
            internship_type,session)


        session_firm = self.ui.lineEdit_90.text()
        internship_type_firm=self.ui.lineEdit_94.text()
        sql7 = "SELECT count(internship.id) FROM internship " \
               "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
               "INNER JOIN students ON internship.student_id=students.id WHERE internship_capacity.internship_type='{}' AND internship_capacity.session='{}' AND students.sexual='K' AND firm_id={}".format(
            internship_type_firm,session_firm, firm_id)
        sql8 = "SELECT count(internship.id) FROM internship " \
               "INNER JOIN internship_capacity ON internship.quota_id=internship_capacity.id " \
               "INNER JOIN students ON internship.student_id=students.id WHERE internship_capacity.internship_type='{}' AND internship_capacity.session='{}' AND students.sexual='E' AND firm_id={}".format(
            internship_type_firm,session_firm, firm_id)


        self.cur.execute(sql1)
        total_girl_quota, = self.cur.fetchone()
        if total_girl_quota:
            pass
        else:
            total_girl_quota=0

        self.cur.execute(sql2)
        total_boy_quota, = self.cur.fetchone()
        if total_boy_quota:
            pass
        else:
            total_boy_quota=0

        print("{} sezonu toplam kontenjan sayısı Kız :{} ve Erkek :{}".format(session, total_girl_quota,
                                                                                  total_boy_quota))

        if total_girl_quota and total_boy_quota:
            self.ui.lineEdit_26.setText(str(total_girl_quota))
            self.ui.lineEdit_88.setText(str(total_boy_quota))
        else:
            self.ui.lineEdit_26.setText('0')
            self.ui.lineEdit_88.setText('0')

        self.cur.execute(sql3)
        total_girl_assigned, = self.cur.fetchone()
        if total_girl_assigned:
            pass
        else:
            total_girl_assigned=0
        self.cur.execute(sql4)
        total_boy_assigned, = self.cur.fetchone()
        if total_boy_assigned:
            pass
        else:
            total_boy_assigned=0
        print("{} sezonu  staj yeri atanan toplam kız:{} ve Erkek : {} ".format(session, total_girl_assigned,
                                                                                   total_boy_assigned))

        self.ui.lineEdit_60.setText(str(total_girl_assigned))
        self.ui.lineEdit_87.setText(str(total_boy_assigned))
        self.ui.lineEdit_27.setText(str(total_girl_quota - total_girl_assigned))
        self.ui.lineEdit_89.setText(str(total_boy_quota - total_boy_assigned))

        if self.ui.lineEdit_83.text():
            total_girl_firm_assign = int(self.ui.lineEdit_83.text())
        else:
            total_girl_firm_assign =0
        if self.ui.lineEdit_82.text():
            total_boy_firm_assign = int(self.ui.lineEdit_82.text())
        else:
            total_boy_firm_assign =0
        print("{} sezonu  bu firmaya atanacak toplam kız:{} ve Erkek : {} ".format(session,total_girl_firm_assign,total_boy_firm_assign))

        self.cur.execute(sql7)
        total_girl_firm_assigned, = self.cur.fetchone()
        if total_girl_firm_assigned:
            pass
        else:
            total_girl_firm_assigned=0

        self.cur.execute(sql8)
        total_boy_firm_assigned, = self.cur.fetchone()
        if total_boy_firm_assigned:
            pass
        else:
            total_boy_firm_assigned = 0


        self.ui.lineEdit_86.setText(str(total_girl_firm_assign - total_girl_firm_assigned))
        self.ui.lineEdit_28.setText(str(int(total_boy_firm_assign) - total_boy_firm_assigned))
        print("{} sezonu  bu firmada kalan kontenjan toplamı kız:{} ve Erkek : {} ".format(session,
                                                                                                 self.ui.lineEdit_86.text(),
                                                                                                 self.ui.lineEdit_28.text()))

        self.db.close()
        numbers=self.cal_total_students_for_each_class()
        print("{} sezonu  9. Sınıf Toplma  kız:{} ve Erkek : {}  sayıları".format(session, numbers[0],numbers[1]))
        print("{} sezonu  10. Sınıf Toplma  kız:{} ve Erkek : {}  sayıları".format(session, numbers[2], numbers[3]))
        print("{} sezonu  11. Sınıf Toplma  kız:{} ve Erkek : {}  sayıları".format(session, numbers[4], numbers[5]))
        print("{} sezonu  12. Sınıf Toplma  kız:{} ve Erkek : {}  sayıları".format(session, numbers[6], numbers[7]))
        self.ui.lineEdit_85.setText(str(numbers[0]))
        self.ui.lineEdit_96.setText(str(numbers[1]))
        self.ui.lineEdit_101.setText(str(numbers[2]))
        self.ui.lineEdit_100.setText(str(numbers[3]))
        self.ui.lineEdit_110.setText(str(numbers[4]))
        self.ui.lineEdit_109.setText(str(numbers[5]))
        self.ui.lineEdit_112.setText(str(numbers[6]))
        self.ui.lineEdit_111.setText(str(numbers[7]))
        if self.ui.comboBox_13.currentIndex()==0 or self.ui.comboBox_13.currentIndex()==2:
            self.ui.lineEdit_38.setText(str(numbers[2]-total_girl_assigned))
            self.ui.lineEdit_91.setText(str(numbers[3]-total_boy_assigned))
        elif self.ui.comboBox_13.currentIndex()==1 or self.ui.comboBox_13.currentIndex()==3:
            self.ui.lineEdit_38.setText(str(numbers[4] - total_girl_assigned))
            self.ui.lineEdit_91.setText(str(numbers[5] - total_boy_assigned))


    def cal_total_students_for_each_class(self):
        classes=['9','10','11','12']
        number=[]

        for class_level in classes:
            sql1 = "SELECT COUNT(id) FROM students  WHERE sexual='K' AND class_level='{}'".format(
                 class_level)
            sql2 = "SELECT COUNT(id) FROM students  WHERE sexual='E' AND class_level='{}'".format(
                class_level)
            self.db_connect()
            self.cur.execute(sql1)
            data,=self.cur.fetchall()
            number.append(data[0])
            self.cur.execute(sql2)
            data1, =self.cur.fetchall()
            number.append(data1[0])
            self.db.close()

        return (number)



    def export_report_year_for_allclass(self):
        pass




# ============================================================================
# ================ SHOW PAGES ================================================
def show_LoginPage():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Çıkılıyor")


def show_StudentPage():
    app = QApplication(sys.argv)
    window = StudentWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Çıkılıyor")


def show_mainPage():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Çıkılıyor")


# ============================================================================
# ============================================================================

if __name__ == "__main__":
    UserID = 'ed'  # bu silinecek sorrasında
    global hostName_db
    global port_db
    global username_db
    global password_db
    global database_db
    hostName_db = 'localhost'
    port_db = 3306
    username_db = 'root'
    password_db = '1234567890'
    database_db = 'shool_db'
    show_mainPage()  # bu show_login_page ile değiştirilecek


    # show_LoginPage() #bu show_login_page ile değiştirilecek
