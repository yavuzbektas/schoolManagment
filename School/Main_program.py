# ============================================================================
# ==================== Library  ==================================
import sys, os, shutil
import MySQLdb
import sqlite3

from PySide2.QtWidgets import QApplication, QMainWindow, QDialog
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, Slot, QDate
from PySide2.QtUiTools import QUiLoader
from xlrd import *
from xlsxwriter import *
# ============================================================================
# ==================== import UI files ==================================
from MainWindow import Ui_MainWindow
from Login import Ui_Dialog
import students
import firms
import internship

# ============================================================================
# ================   GLOBALS    ===================================
global UserID
global student_id
global firm_id
global quota_id
global internship_id
internship_id = 0
quota_id = 0
firm_id = 0
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
class QuotaWindow(QDialog, internship.Ui_Dialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(QuotaWindow, self).__init__(parent, *args, **kwargs)
        self.ui = internship.Ui_Dialog()

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
            self.ui.lineEdit_77.setText(data[6])
            self.ui.lineEdit_81.setText(data[7])
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
        self.db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234567890', db='shool_db',
                                  charset="utf8")
        self.cur = self.db.cursor()


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
        self.db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234567890', db='shool_db',
                                  charset="utf8")
        self.cur = self.db.cursor()


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
        print(name, surname, level, class_name)

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
        self.db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234567890', db='shool_db',
                                  charset="utf8")
        self.cur = self.db.cursor()


# ============================================================================
# ================LOGIN PAGE===================================
class LoginWindow(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(LoginWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('Kullanıcı Giriş Sayfası')
        self.handle_button()

    def handle_button(self):
        self.ui.pushButton.clicked.connect(self.user_check)
        self.ui.pushButton_2.clicked.connect(self.close)

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
        self.db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234567890', db='shool_db',
                                  charset="utf8")
        self.cur = self.db.cursor()


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
        self.firmDialog = FirmWindow(self)
        self.quotaDialog = QuotaWindow(self)

        self.setWindowTitle('Ana Sayfa')
        self.firm_showAll()
        self.quota_showAll()
        self.internship_showAll()

    # ================ TABS CONTROL  ===========================================
    def teacher_tab(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget_2.setCurrentIndex(0)

    def student_tab(self):
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.tabWidget_3.setCurrentIndex(0)

    def report_tab(self):
        self.ui.tabWidget.setCurrentIndex(4)

    def internship_tab(self):
        self.ui.tabWidget.setCurrentIndex(3)
        self.ui.tabWidget_4.setCurrentIndex(0)

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
        self.ui.pushButton_16.clicked.connect(self.student_show_last_record)
        self.ui.pushButton_17.clicked.connect(self.student_image_open)
        self.ui.pushButton_30.clicked.connect(self.student_window_call)
        self.ui.pushButton_29.clicked.connect(self.student_screen_clear)
        self.ui.pushButton_21.clicked.connect(self.student_showAll)
        self.ui.dateEdit.dateChanged.connect(self.student_record_date_time)
        self.ui.dateEdit_2.dateChanged.connect(self.student_birth_date_time)
        # ================  firms  ==========================
        self.ui.pushButton_18.clicked.connect(self.firm_field_check)
        self.ui.pushButton_32.clicked.connect(self.firm_screen_clear)
        self.ui.pushButton_22.clicked.connect(self.firm_showAll)
        self.ui.tableWidget_5.itemClicked.connect(self.firm_callback)

        self.ui.pushButton_26.clicked.connect(self.quota_firm_window_call)
        # ================   Quota ==========================
        self.ui.pushButton_36.clicked.connect(self.quota_field_check)
        self.ui.comboBox_14.currentIndexChanged.connect(self.quota_showAll)
        self.ui.tableWidget_7.itemClicked.connect(self.quota_detail_upload_table)
        self.ui.pushButton_37.clicked.connect(self.quota_screen_clear)

        # ================  Internship ==========================
        self.ui.pushButton_34.clicked.connect(self.quota_dialog_window_call)
        self.ui.pushButton_27.clicked.connect(self.internship_field_check)
        self.ui.pushButton_25.clicked.connect(self.student_window_call)
        self.ui.pushButton_33.clicked.connect(self.internship_screen_clear)
        self.ui.pushButton_28.clicked.connect(self.internship_showAll)
        self.ui.tableWidget_4.itemClicked.connect(self.internship_detail_upload_table)
        self.ui.dateEdit_3.dateChanged.connect(self.internship_start_date_time)
        self.ui.dateEdit_4.dateChanged.connect(self.internship_finish_date_time)

    def input_mask_override(self):
        self.ui.lineEdit_66.setInputMask('99/99/9999')
        self.ui.lineEdit_66.setMaxLength(10)

    def image_file_dialog_open(self):
        filepath, _ = QFileDialog.getOpenFileName(filter='Resim Dosyası *.png')
        filename = QFileInfo(filepath).fileName()
        new_file_name = self.ui.lineEdit_7.text() + self.ui.lineEdit_11.text() + '.png'
        if filename:
            print(new_file_name)
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
            print(cv_path)
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

    def admin_control_dactivate(self):
        self.ui.pushButton_9.setEnabled(0)
        self.ui.comboBox_3.setEnabled(0)

    def db_connect(self):
        self.db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='1234567890', db='shool_db',
                                  charset="utf8")
        self.cur = self.db.cursor()

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

        conn = sqlite3.connect('school_db.db')

        username = 'ed'
        sql2 = "SELECT * FROM teacher_detail WHERE username = '{}'"
        c = conn.cursor()
        c.execute(sql2.format(username))
        data2 =c.fetchone()
        conn.close()
        print(data2)
        # self.cur.execute(sql2, [(username)])
        # data2 = self.cur.fetchone()
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

            WHERE username = %s '''%(
                username, departure, status, start_year, state, adress, pers_email, telephone, university,
                uni_departure,
                profile_image, cv_file, fb_link, linkedin_link, blog_link, other_link, username)
            conn = sqlite3.connect('school_db.db')
            c = conn.cursor()
            c.execute(sql)
            # self.cur.execute(sql, (
            #     username, departure, status, start_year, state, adress, pers_email, telephone, university,
            #     uni_departure,
            #     profile_image, cv_file, fb_link, linkedin_link, blog_link, other_link, username))
            conn.commit()
            # self.db.commit()
            self.statusBar().showMessage('Öğretmen Bilgileri Güncellendi')
            # self.db.close()
            conn.close()
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

        conn = sqlite3.connect('school_db.db')
        c = conn.cursor()
        # self.db_connect()
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
        c.execute(sql %(
            username, departure, status, start_year, state, adress, pers_email, telephone, university, uni_departure,
            profile_image, cv_file, fb_link, linkedin_link, blog_link, other_link))
        # self.cur.execute(sql, (
        #     username, departure, status, start_year, state, adress, pers_email, telephone, university, uni_departure,
        #     profile_image, cv_file, fb_link, linkedin_link, blog_link, other_link))
        conn.commit()
        conn.close()

        # self.db.commit()
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

        # self.db.close()
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
        pass

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

    def student_record_date_time(self):
        day = self.ui.dateEdit.date().day()
        month = self.ui.dateEdit.date().month()
        year = self.ui.dateEdit.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))
        print(date)
        self.ui.lineEdit_36.setText(str(date))

    def student_birth_date_time(self):
        day = self.ui.dateEdit_2.date().day()
        month = self.ui.dateEdit_2.date().month()
        year = self.ui.dateEdit_2.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))
        print(date)
        self.ui.lineEdit_33.setText(str(date))

    def student_field_check(self):

        if (not self.ui.lineEdit_31.text() or
                not self.ui.lineEdit_30.text() or
                not self.ui.lineEdit_32.text() or
                not self.ui.lineEdit_33.text() or

                not self.ui.lineEdit_35.text() or
                not self.ui.lineEdit_42.text() or
                not self.ui.lineEdit_43.text() or
                not self.ui.lineEdit_36.text() or
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

        if self.ui.lineEdit_36.text() == '':
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
        register_date = self.ui.lineEdit_36.text()
        student_num = self.ui.lineEdit_37.text()
        departure = self.ui.comboBox_7.currentText()
        class_level = self.ui.comboBox_6.currentText()
        class_name = self.ui.comboBox_9.currentText()
        city = self.ui.lineEdit_44.text()
        state = self.ui.lineEdit_34.text()
        adress = self.ui.textEdit_2.toPlainText()
        note = self.ui.textEdit_3.toPlainText()
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
                            state,adress,register_date,school_number,departure,class_level,class,image_link,notes) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''

            self.cur.execute(sql, (
                student_name, student_surname, birthday, tc_no, email, telephone, partner_name, partner_phone, city,
                state, adress, register_date,
                student_num, departure, class_level, class_name, profil_image, note))

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

    def student_detail_upload(self):
        global student_id
        self.db_connect()

        sql = ''' SELECT * FROM students WHERE id = %s'''
        self.cur.execute(sql, [(student_id)])
        data = self.cur.fetchone()
        self.ui.lineEdit_22.setText(str(data[0]))
        self.ui.lineEdit_29.setText(data[17])
        self.ui.lineEdit_31.setText(data[1])
        self.ui.lineEdit_30.setText(data[2])
        self.ui.lineEdit_32.setText(data[4])
        self.ui.lineEdit_33.setText(data[3])
        self.ui.lineEdit_40.setText(data[5])
        self.ui.lineEdit_35.setText(data[6])
        self.ui.lineEdit_42.setText(data[7])
        self.ui.lineEdit_43.setText(data[8])
        self.ui.lineEdit_36.setText(data[12])
        self.ui.lineEdit_37.setText(data[13])
        self.ui.comboBox_7.setCurrentText(data[14])
        self.ui.comboBox_6.setCurrentText(data[15])
        self.ui.comboBox_9.setCurrentText(data[16])
        self.ui.lineEdit_44.setText(data[9])
        self.ui.lineEdit_34.setText(data[10])
        self.ui.textEdit_2.setPlainText(data[11])
        self.ui.textEdit_3.setPlainText(data[18])
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
        register_date = self.ui.lineEdit_36.text()
        student_num = self.ui.lineEdit_37.text()
        departure = self.ui.comboBox_7.currentText()
        class_level = self.ui.comboBox_6.currentText()
        class_name = self.ui.comboBox_9.currentText()
        city = self.ui.lineEdit_44.text()
        state = self.ui.lineEdit_34.text()
        adress = self.ui.textEdit_2.toPlainText()
        note = self.ui.textEdit_3.toPlainText()
        id = self.existing_student_check()
        self.ui.lineEdit_22.setText(str(id))
        self.db_connect()

        sql = (
            "UPDATE students SET name=%s,surname=%s,birthday=%s, tc_no=%s,email=%s,telephone=%s,parent_name=%s,parent_telephone=%s,city=%s,state=%s,adress=%s,register_date=%s,school_number=%s,departure=%s,class_level=%s,class=%s,image_link=%s,notes=%s WHERE id=%s")

        self.cur.execute(sql, (
            student_name, student_surname, birthday, tc_no, email, telephone, partner_name, partner_phone, city, state,
            adress, register_date, student_num, departure, class_level, class_name, profil_image, note, id))

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
        self.ui.lineEdit_36.setText('')
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
        self.student_invisible_objects()

    def student_delete(self):
        pass

    def existing_student_check(self):
        tc_no = self.ui.lineEdit_32.text()

        self.db_connect()
        sql = "SELECT id,tc_no FROM students WHERE tc_no={}".format(tc_no)
        if self.cur.execute(sql):
            id, data = self.cur.fetchone()

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
        filter_val = self.ui.lineEdit_41.text()
        index_val = str(self.ui.comboBox_8.currentIndex())
        header = {'0': 'name', '1': 'surname', '2': 'school_number', '3': 'class_level', '4': 'record_date'}
        if filter_val:
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link FROM students  WHERE {} LIKE '{}%'".format(
                header[index_val], filter_val)
        else:
            sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link FROM students ORDER BY record_date DESC"

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

    def student_show_last_record(self):

        sql = "SELECT id, name, surname,tc_no,school_number,class_level,class,image_link FROM students ORDER BY record_date DESC"

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
        self.ui.textEdit_5.setPlainText(notes)
        self.ui.lineEdit_23.setText(str(firm_id))

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
        pass

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
            sql = "SELECT id,cari_code,name,adress,city,state,telephone,fax,web,sector_code,sector_desc,hr_name,hr_telephone,hr_email,notes FROM firms ORDER BY record_date DESC"

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
        pass

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
            self.ui.lineEdit_77.setText(data[6])
            self.ui.lineEdit_81.setText(data[7])
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

    # ============================================================================
    # ================ INTERSHIP BLOCKS ================================================
    def internship_start_date_time(self):
        day = self.ui.dateEdit_3.date().day()
        month = self.ui.dateEdit_3.date().month()
        year = self.ui.dateEdit_3.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))
        print(date)
        self.ui.lineEdit_66.setText(str(date))

    def internship_finish_date_time(self):
        day = self.ui.dateEdit_4.date().day()
        month = self.ui.dateEdit_4.date().month()
        year = self.ui.dateEdit_4.date().year()

        date = (str(day) + '.' + str(month) + '.' + str(year))
        print(date)
        self.ui.lineEdit_73.setText(str(date))

    def internship_invisible_objects(self):
        self.ui.label_125.setVisible(False)
        self.ui.label_126.setVisible(False)
        self.ui.label_127.setVisible(False)
        self.ui.label_128.setVisible(False)
        self.ui.label_129.setVisible(False)
        self.ui.label_130.setVisible(False)
        self.ui.label_131.setVisible(False)

    def internship_field_check(self):
        if (not self.ui.lineEdit_66.text() or
                not self.ui.lineEdit_73.text() or
                not self.ui.lineEdit_61.text() or
                not self.ui.lineEdit_25.text() or
                not self.ui.lineEdit_74.text()):
            warning = QMessageBox.warning(self, 'Eksik Veri Hatası',
                                          'Girilmesi zorunlu olan veriler bulunmaktadır. Lütfen eksik tüm alanları doldurun',
                                          QMessageBox.Ok)
            self.statusBar().showMessage('Eksik Veri hatası ')
            self.internship_visible_objects()
            return (False)
        else:
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

    def internship_student_call(self, id):

        self.db_connect()
        sql = "SELECT * FROM students WHERE id={} order by id DESC".format(id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.ui.lineEdit_59.setText(data[1])
            self.ui.lineEdit_58.setText(data[2])
            self.ui.lineEdit_61.setText(data[4])
            self.ui.lineEdit_62.setText(data[13])
            self.ui.lineEdit_63.setText(data[14])
            self.ui.lineEdit_64.setText(data[15])
            self.ui.lineEdit_65.setText(data[16])

            new_file_name = data[17]
            pic_path = STUDENT_IMAGES_DIR + new_file_name

            picture = QPixmap(pic_path)
            self.ui.label_67.setPixmap(picture)
            self.ui.label_67.setScaledContents(True)
            self.db.close()

    def quota_dialog_window_call(self):

        self.quotaDialog.show()

    def quota_dialog_turn_window(self, id):
        self.ui.lineEdit_25.setText(quota_id)

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
            self.ui.lineEdit_83.setText(data[4])
            self.ui.lineEdit_82.setText(data[5])
            self.ui.label_131.setVisible(True)
            self.ui.label_129.setVisible(False)
            self.db.close()

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
            warning = QMessageBox.warning(self, 'Veri Hatası',
                                          'Bu Staj yeri sistemde kayıtlı görünmektedir.\nMevcut kaydı güncellemek için lütfen "SaveAll" butonuna çıkmak için "Cancel" tusuna basın',
                                          QMessageBox.Cancel | QMessageBox.SaveAll)
            self.statusBar().showMessage('Veri hatası ')
            if warning.SaveAll:
                self.internship_update(internship_id)
        else:

            self.db_connect()

            sql = "INSERT INTO internship (student_id,quota_id,start_date,finish_date,internship_day,notes,username_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"

            self.cur.execute(sql, (student_id, quota_id, start_date, finish_date, internship_day, note, username_id))

            self.db.commit()
            self.statusBar().showMessage('Yeni Kayıt oluşturuldu ve Staj Yeri ilgili Öğrenciye Atandı')
            self.db.close()
            self.internship_showAll()
            self.ui.lineEdit_57.setText(str(internship_id))

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
        self.ui.lineEdit_57.setText(internship_id)
        self.statusBar().showMessage('Öğrencinin Staj Yeri Bilgileri Güncellendi')

    def internship_screen_clear(self):
        global internship_id
        global student_id
        global quota_id
        internship_id = ''
        student_id = ''
        quota_id = ''
        quota_id = self.ui.lineEdit_25.setText('')
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
        internship_id = self.ui.tableWidget_4.item(self.ui.tableWidget_4.currentRow(), 0).text()

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
              "WHERE internship.id='{}'".format(internship_id)
        if self.cur.execute(sql):
            data = self.cur.fetchone()

            self.ui.lineEdit_58.setText(data[4])
            self.ui.lineEdit_59.setText(data[3])
            self.ui.lineEdit_61.setText(data[5])
            self.ui.lineEdit_62.setText(data[6])
            self.ui.lineEdit_63.setText(data[7])
            self.ui.lineEdit_64.setText(data[8])
            self.ui.lineEdit_65.setText(data[9])
            self.ui.lineEdit_66.setText(data[11])
            self.ui.lineEdit_73.setText(data[12])
            self.ui.lineEdit_74.setText(data[13])
            self.ui.lineEdit_25.setText(str(data[16]))
            self.ui.lineEdit_84.setText(data[2])
            self.ui.lineEdit_90.setText(data[0])
            self.ui.lineEdit_94.setText(data[1])
            self.ui.lineEdit_82.setText(data[20])
            self.ui.lineEdit_83.setText(data[19])

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
            self.ui.lineEdit_57.setText(str(internship_id))
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
            print(data, type(data))
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
        self.ui.lineEdit_57.setText(str(internship_id))

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
    show_mainPage()  # bu show_login_page ile değiştirilecek

    # show_LoginPage() #bu show_login_page ile değiştirilecek
