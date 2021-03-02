import shutil
import subprocess
from Database_Import.send_import_email import send_email_to_credit_safe
from UI import Ui_MainWindow
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from Import_Tab_Functions import *
from SQLQUERYS.PLACEMENT_PROCESS_1 import func
from SQLQUERYS.PLACEMENT_PROCESS_2 import func_2
from SQLQUERYS.PLACEMENT_PROCESS_3 import func_3
from datetime import datetime
import os
import pandas as pd


class ImportTab(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(lambda: self.clicked_process())
        self.ui.pushButton_3.clicked.connect(lambda: self.client_clicked_export())
        self.ui.pushButton_2.clicked.connect(lambda: self.DCA_clicked_process())
        self.ui.pushButton_4.clicked.connect(lambda: self.DCA_clicked_export())
        self.ui.pushButton_7.clicked.connect(lambda: self.to_enrichment())
        self.ui.pushButton_9.clicked.connect(lambda: self.from_enrichment())
        self.ui.pushButton_10.clicked.connect(lambda: self.from_enrichment_2())
        self.ui.pushButton_11.clicked.connect(lambda: self.litigation_clicked_process())
        self.ui.pushButton_6.clicked.connect(lambda: self.litigation_clicked_export())
        self.ui.pushButton_5.clicked.connect(lambda: self.process_from_litigation_to_just())
        self.ui.pushButton_8.clicked.connect(lambda: self.to_enrichment_2())

    def select_file(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the process files from client tab"""
        file_list = []
        client_index = self.ui.comboBox_5.currentIndex()
        check_box_list = [self.ui.checkBox_4.isChecked(), self.ui.checkBox_5.isChecked(), self.ui.checkBox.isChecked(), self.ui.checkBox_2.isChecked()]
        check_box_file_translation = ['NB', 'QR', 'Client Recall', 'Adjustment File']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if client_index == 0 and check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def clicked_process(self):
        """This function executes the process button on the process files from client tab"""
        now = datetime.now()
        file_list = self.select_file()
        client_index = self.ui.comboBox_5.currentIndex()
        DCA_index = self.ui.comboBox_9.currentIndex()
        if client_index == 0 and DCA_index == 0:
            file_paths = process_selected_yu_file(file_list)
            for file in file_paths:
                try:
                    if file == 'No File':
                        msg = QMessageBox()
                        msg.setWindowTitle("Processing Error")
                        msg.setText("There is no file to process in the directory")
                        x = msg.exec_()
                    else:
                        process_yu_to_first_locate(file)
                        status = 'File has been successfully processed'
                        self.process_from_client_update_table(file, client_index, status)
                except Exception as e:
                    exception_detail = exception_cleaner(str(e))
                    msg = QMessageBox()
                    msg.setWindowTitle("Processing Error")
                    msg.setText("There has been an error processing this file ")
                    x = msg.exec_()
                    status = f'File processing has failed: {exception_detail}'
                    self.process_from_client_update_table(file, client_index, status)
        elif client_index == 0 and DCA_index == 1:
            pass
        else:
            pass
        data = self.pull_process_client_data()
        update_db(data, 'Reports')
        pull_report_to_csv()


    def select_file_for_processing_From_DCA(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the process files for DCA tab"""
        file_list = []
        client_index = self.ui.comboBox_6.currentIndex()
        check_box_list = [self.ui.checkBox_6.isChecked(), self.ui.checkBox_7.isChecked(),
                          self.ui.checkBox_9.isChecked(),
                          self.ui.checkBox_17.isChecked(), self.ui.checkBox_18.isChecked(), self.ui.checkBox_8.isChecked() ]
        check_box_file_translation = ['NFU', 'Transaction',  'Closure', 'Activity', 'AGMT', 'Query']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if client_index == 0 and check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def DCA_clicked_process(self):
        "This function controls the process file button on the process DCA files tab"
        file_list = self.select_file_for_processing_From_DCA()
        client_index = self.ui.comboBox_6.currentIndex()
        if client_index == 0:
            file_paths = process_selected_1st_locate_file(file_list)
            for file in file_paths:
                try:
                    if file == 'No File':
                        msg = QMessageBox()
                        msg.setWindowTitle("Processing Error")
                        msg.setText("There is no file to process in the directory")
                        x = msg.exec_()
                    else:
                        process_1st_locate_file(file)
                        status = 'File has been successfully processed'
                        self.process_from_DCA_update_table(file, client_index, status)
                except Exception as e:
                    exception_detail = exception_cleaner(str(e))
                    msg = QMessageBox()
                    msg.setWindowTitle("Processing Error")
                    msg.setText("There has been an error processing this file ")
                    x = msg.exec_()
                    status = f'File processing has failed: {exception_detail}'
                    self.process_from_DCA_update_table(file, client_index, status)
        elif client_index == 1:
            pass
        else:
            pass
        data = self.pull_process_dca_data()
        update_db(data, 'Reports')
        pull_report_to_csv()

    def process_from_client_update_table(self, file, clientindex, status):
        """This function updates the table on the process file from client tab providing information data on the files"""
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        if 'NB' in file:
            try:
                name = os.path.basename(file)
                file_name = name.replace('.csv', '')
                self.ui.tableWidget.setItem(0, 0, QTableWidgetItem(file_name))
                self.ui.tableWidget.setItem(0, 2, QTableWidgetItem('New Business' + ' ' + status))
                self.ui.tableWidget.setItem(0, 3, QTableWidgetItem(now_str))
                self.ui.tableWidget.setItem(0, 5, QTableWidgetItem(''))
                if clientindex == 0:
                    self.ui.tableWidget.setItem(0, 1, QTableWidgetItem('Inbound: Yu Energy'))
            except Exception as e:
                print(e)
            else:
                pass
        elif 'Query' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget.setItem(1, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget.setItem(1, 2, QTableWidgetItem(
                'Query' + ' ' + status))
            self.ui.tableWidget.setItem(1, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget.setItem(1, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget.setItem(1, 1, QTableWidgetItem('Inbound: Yu Energy'))
            else:
                pass
        elif 'Closure' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            print(file_name)
            self.ui.tableWidget.setItem(2, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget.setItem(2, 2, QTableWidgetItem(
                'Client Recall/Closure' + ' ' + status))
            self.ui.tableWidget.setItem(2, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget.setItem(2, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget.setItem(2, 1, QTableWidgetItem('Inbound: Yu Energy'))
            else:
                pass
        elif 'Adjustment' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget.setItem(3, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget.setItem(3, 2, QTableWidgetItem(
                'Adjustment' + ' ' + status))
            self.ui.tableWidget.setItem(3, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget.setItem(3, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget.setItem(3, 1, QTableWidgetItem('Inbound: Yu Energy'))
            else:
                pass
        else:
            pass

    def process_from_DCA_update_table(self, file, clientindex, status):
        """This function updates the table on the process files from DCA Tab providing information data on the files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        if 'NFU' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_2.setItem(0, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_2.setItem(0, 2, QTableWidgetItem('Non Financial Updates' + ' ' + status))
            self.ui.tableWidget_2.setItem(0, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_2.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_2.setItem(0, 1, QTableWidgetItem('Inbound: 1st Locate'))
            else:
                pass
        elif 'Transaction' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_2.setItem(1, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_2.setItem(1, 2, QTableWidgetItem('Transaction' + ' ' + status))
            self.ui.tableWidget_2.setItem(1, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_2.setItem(1, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_2.setItem(1, 1, QTableWidgetItem('Inbound: 1st Locate'))
            else:
                pass
        elif 'Activity' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_2.setItem(4, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_2.setItem(4, 2, QTableWidgetItem(
                'Activity' + ' ' + status))
            self.ui.tableWidget_2.setItem(4, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget_2.setItem(4, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_2.setItem(4, 1, QTableWidgetItem('Inbound: 1st Locate'))
            else:
                pass
        elif 'AGMT' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_2.setItem(5, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_2.setItem(5, 2, QTableWidgetItem(
                'AGMTS' + ' ' + status))
            self.ui.tableWidget_2.setItem(5, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget_2.setItem(5, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_2.setItem(5, 1, QTableWidgetItem('Inbound: 1st Locate'))
            else:
                pass
        elif 'Closure' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_2.setItem(3, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_2.setItem(3, 2, QTableWidgetItem(
                'Closure' + ' ' + status))
            self.ui.tableWidget_2.setItem(3, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget_2.setItem(3, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_2.setItem(3, 1, QTableWidgetItem('Inbound: 1st Locate'))
        elif 'Query' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_2.setItem(6, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_2.setItem(6, 2, QTableWidgetItem(
                'Query' + ' ' + status))
            self.ui.tableWidget_2.setItem(6, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget_2.setItem(6, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_2.setItem(6, 1, QTableWidgetItem('Inbound: 1st Locate'))
            else:
                pass
        else:
            pass

    def pull_process_client_data(self):
        """This function pulls data from the table on the process client files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(5), columns=range(5))
        rowCount = self.ui.tableWidget.rowCount()
        columnCount = self.ui.tableWidget.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
        df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
        df = df.dropna(how='any', axis=0)
        return df

    def pull_process_dca_data(self):
        """This function pulls data from the table on the process DCA files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(5), columns=range(5))
        rowCount = self.ui.tableWidget_2.rowCount()
        columnCount = self.ui.tableWidget_2.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_2.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
        df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
        df = df.dropna(how='any', axis=0)
        return df

    def select_file_for_exporting_to_DCA(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the TO DCA TAB"""
        file_list = []
        client_index = self.ui.comboBox_8.currentIndex()
        check_box_list = [self.ui.checkBox_14.isChecked(), self.ui.checkBox_15.isChecked(), self.ui.checkBox_3.isChecked(), self.ui.checkBox_16.isChecked(), self.ui.checkBox_19.isChecked()]
        check_box_file_translation = ['Assignment', 'QR', 'Pay', 'Bill', 'Recall']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if client_index == 0 and check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def DCA_clicked_export(self):
        "This process controls the Export button on the Export Files to DCA Tab"
        global name, status
        file_list = self.select_file_for_exporting_to_DCA()
        client_index = self.ui.comboBox_6.currentIndex()
        if client_index == 0:
            file_paths = export_selected_1st_locate_file(file_list)
            for file in file_paths:
                try:
                    if 'Assignment' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FIRST_LOCATE_ASSIGNMENT_DIRECTORY}\\*.csv'), key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FIRST_LOCATE_ASSIGNMENT_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_DCA_update_table(name, client_index, status)
                    elif 'Bill' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FIRST_LOCATE_BILL_DIRECTORY}\\*.csv'), key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FIRST_LOCATE_BILL_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_DCA_update_table(name, client_index, status)
                    elif 'Pay' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FIRST_LOCATE_PAY_DIRECTORY}\\*.csv'), key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FIRST_LOCATE_PAY_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_DCA_update_table(name, client_index, status)
                    elif 'Recall' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FIRST_LOCATE_RECALL_DIRECTORY}\\*.csv'), key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FIRST_LOCATE_RECALL_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_DCA_update_table(name, client_index, status)
                    elif 'Query_Response' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FIRST_LOCATE_QueryRESPONSE_Directory}\\*.csv'), key=os.path.getmtime)
                        print(newest)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FIRST_LOCATE_QueryRESPONSE_Directory + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_DCA_update_table(name, client_index, status)
                    else:
                        pass
                except Exception as e:
                    if str(e) == 'max() arg is an empty sequence':
                        msg = QMessageBox()
                        msg.setWindowTitle("Exporting Error")
                        msg.setText("Directory is empty - there is no file to export")
                        x = msg.exec_()
                        status = 'export failed as there was no file in the directory'
                    else:
                        exception_detail = exception_cleaner(str(e))
                        msg = QMessageBox()
                        msg.setWindowTitle("Exporting Error")
                        msg.setText(f"Error exporting this file to the DCA SFTP: {exception_detail}")
                        x = msg.exec_()
                        status = 'export has failed'
                        self.export_from_DCA_update_table(name, client_index, status)
        else:
            pass
        data = self.pull_export_dca_data()
        update_db(data, 'Reports')
        pull_report_to_csv()

    def export_from_DCA_update_table(self, file, clientindex, status):
        """This function updates the table on the export files from DCA Tab providing information data on the files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        if 'ASS' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_5.setItem(0, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_5.setItem(0, 2, QTableWidgetItem('Assignment File' + ' ' + status))
            self.ui.tableWidget_5.setItem(0, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_5.setItem(0, 1, QTableWidgetItem('Outbound: 1st Locate'))
            else:
                pass
        elif 'QR' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_5.setItem(1, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_5.setItem(1, 2, QTableWidgetItem('Query Response' + ' ' + status))
            self.ui.tableWidget_5.setItem(1, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(1, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_5.setItem(1, 1, QTableWidgetItem('Outbound: 1st Locate'))
            else:
                pass
        elif 'Bill' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_5.setItem(3, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_5.setItem(3, 2, QTableWidgetItem('Bill File' + ' ' +status))
            self.ui.tableWidget_5.setItem(3, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(1, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_5.setItem(3, 1, QTableWidgetItem('Outbound: 1st Locate'))
            else:
                pass
        elif 'CLS' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_5.setItem(4, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_5.setItem(4, 2, QTableWidgetItem('Client Recall File' + ' ' +status))
            self.ui.tableWidget_5.setItem(4, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(1, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_5.setItem(4, 1, QTableWidgetItem('Outbound: 1st Locate'))
        else:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_5.setItem(2, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_5.setItem(2, 2, QTableWidgetItem('Pay File' + ' ' + status))
            self.ui.tableWidget_5.setItem(2, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(1, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_5.setItem(2, 1, QTableWidgetItem('Outbound: 1st Locate'))


    def pull_export_dca_data(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(5), columns=range(5))
        rowCount = self.ui.tableWidget_5.rowCount()
        columnCount = self.ui.tableWidget_5.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_5.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
        df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
        df = df.dropna(how='any', axis=0)
        return df

    def select_file_for_exporting_to_client(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the TO Client
        TAB """
        file_list = []
        client_index = self.ui.comboBox_7.currentIndex()
        check_box_list = [self.ui.checkBox_10.isChecked(), self.ui.checkBox_11.isChecked(),
                          self.ui.checkBox_12.isChecked(), self.ui.checkBox_13.isChecked(),
                          self.ui.checkBox_20.isChecked()]
        check_box_file_translation = ['NFU', 'Transaction', 'Adjustment', 'Closure', 'Query']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if client_index == 0 and check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def client_clicked_export(self):
        "This process controls the Export button on the Export Files to Client Tab"
        global name, status
        file_list = self.select_file_for_exporting_to_client()
        client_index = self.ui.comboBox_7.currentIndex()
        if client_index == 0:
            file_paths = export_selected_client_file(file_list)
            for file in file_paths:
                try:
                    if 'NFU' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.YU_NFU_DIRECTORY}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.YU_NFU_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_client_update_table(name, client_index, status)
                    elif 'Transaction' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.YU_TRANSACTION_DIRECTORY}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.YU_TRANSACTION_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_client_update_table(name, client_index, status)
                    elif 'Closure' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.YU_CLOSURE_DIRECTORY}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.YU_CLOSURE_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_client_update_table(name, client_index, status)
                    elif 'Query' in file:
                        subprocess.call(file)
                        newest = max(glob.glob(f'{settings.YU_QUERY_DIRECTORY}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.YU_QUERY_DIRECTORY + '\\Processed\\')
                        status = 'successfully exported to client SFTP'
                        self.export_from_client_update_table(name, client_index, status)
                except Exception as e:
                    if str(e) == 'max() arg is an empty sequence':
                        msg = QMessageBox()
                        msg.setWindowTitle("Exporting Error")
                        msg.setText("Directory is empty - there is no file to export")
                        x = msg.exec_()
                        status = 'export failed as there was no file in the directory'
                    else:
                        exception_detail = exception_cleaner(str(e))
                        msg = QMessageBox()
                        msg.setWindowTitle("Exporting Error")
                        msg.setText(f"Error exporting this file to the DCA SFTP: {exception_detail}")
                        x = msg.exec_()
                        status = 'export has failed'
                        self.export_from_client_update_table(name, client_index, status)
        else:
            pass
        data = self.pull_export_client_data()
        update_db(data, 'Reports')
        pull_report_to_csv()

    def export_from_client_update_table(self, file, clientindex, status):
        """This function updates the table on the export files from client Tab providing information data on the
        files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        if 'NFU' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_4.setItem(0, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_4.setItem(0, 2, QTableWidgetItem('Non-Financial Updates' + ' ' + status))
            self.ui.tableWidget_4.setItem(0, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_4.setItem(0, 1, QTableWidgetItem('Outbound: Yu Energy'))
            else:
                pass
        elif 'PAY' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_4.setItem(1, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_4.setItem(1, 2, QTableWidgetItem('Transaction' + ' ' + status))
            self.ui.tableWidget_4.setItem(1, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_4.setItem(1, 1, QTableWidgetItem('Outbound: Yu Energy'))
            else:
                pass
        elif 'CLS' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_4.setItem(3, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_4.setItem(3, 2, QTableWidgetItem('Closure' + ' ' + status))
            self.ui.tableWidget_4.setItem(3, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_4.setItem(3, 1, QTableWidgetItem('Outbound: Yu Energy'))
            else:
                pass
        elif 'QRY' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_4.setItem(4, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_4.setItem(4, 2, QTableWidgetItem('Query' + ' ' + status))
            self.ui.tableWidget_4.setItem(4, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_4.setItem(4, 1, QTableWidgetItem('Outbound: Yu Energy'))
            else:
                pass
        else:
            pass



    def pull_export_client_data(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(5), columns=range(5))
        rowCount = self.ui.tableWidget_4.rowCount()
        columnCount = self.ui.tableWidget_4.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_4.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
            df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
            df = df.dropna(how='any', axis=0)
            return df


    def to_enrichment(self):
        "This function controls the collating and exporting of files to Transunion and Credit Safe"
        global files
        if self.ui.checkBox_32.isChecked():
            tu_flag = 1
        else:
            tu_flag = 0
        if self.ui.checkBox_33.isChecked():
            cs_flag = 1
        else:
            cs_flag = 0
        try:
            func(cs_flag, tu_flag)
            files = export_enrichment_file(tu_flag, cs_flag)
            print(files)
            status = "has been successfully created and is ready to be exported."
            self.export_from_enrichment_table(files, status)
        except Exception as e:
            print(str(e))
            exception_detail = exception_cleaner(str(e))
            status = "have failed to be created:" + "" + exception_detail
            self.export_from_enrichment_table(files, status)
            msg = QMessageBox()
            msg.setWindowTitle("File Creation Error")
            msg.setText("There has been an error creating files for enrichment")
            x = msg.exec_()

        data = self.pull_enrichment_data()
        update_db(data, 'Reports')
        pull_report_to_csv()


    def export_from_enrichment_table(self, files, status):
        """This function updates the table on the export files from client Tab providing information data on the
        files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        for file in files:
            print(file)
            if 'TU' in file:
                name = os.path.basename(file)
                file_name = name.replace('.csv', '')
                self.ui.tableWidget_7.setItem(0, 0, QTableWidgetItem(file_name))
                self.ui.tableWidget_7.setItem(0, 2, QTableWidgetItem('Litigation Cases File for Transunion'+ ' ' + status))
                self.ui.tableWidget_7.setItem(0, 3, QTableWidgetItem(now_str))
                # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
                if  self.ui.checkBox_32.isChecked():
                    self.ui.tableWidget_7.setItem(0, 1, QTableWidgetItem('Outbound: Transunion'))
                else:
                    pass
            elif 'CS' in file:
                name = os.path.basename(file)
                file_name = name.replace('.csv', '')
                self.ui.tableWidget_7.setItem(1, 0, QTableWidgetItem(file_name))
                self.ui.tableWidget_7.setItem(1, 2, QTableWidgetItem('Litigation Cases File for Credit Safe' + ' ' + status))
                self.ui.tableWidget_7.setItem(1, 3, QTableWidgetItem(now_str))
                # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
                if  self.ui.checkBox_33.isChecked():
                    self.ui.tableWidget_7.setItem(1, 1, QTableWidgetItem('Outbound: Credit Safe'))
                else:
                    pass
            else:
                pass


    def pull_enrichment_data(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(2), columns=range(5))
        rowCount = self.ui.tableWidget_7.rowCount()
        columnCount = self.ui.tableWidget_7.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_7.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
            df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
            df = df.dropna(how='any', axis=0)
            return df

    def select_file_for_exporting_to_enrichment_2(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the TO Client
        TAB """
        file_list = []

        check_box_list = [self.ui.checkBox_34.isChecked(), self.ui.checkBox_35.isChecked()]
        check_box_file_translation = ['TU', 'CS']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def to_enrichment_2(self):
        "This function controls the collating and exporting of files to Transunion and Credit Safe"
        global files
        file_list = self.select_file_for_exporting_to_enrichment_2()
        try:
            files = export_enrichment_file_2(file_list)
            for file in files:
                subprocess.call(file)
                if 'CreditSafe' in file:
                    send_email_to_credit_safe('roseagh.terrins@therobotexchange.com')
            status = "has been successfully exported to the necessary SFTP location."
            self.export_from_enrichment_table_2(files, status )
        except Exception as e:
            print(str(e))
            exception_detail = exception_cleaner(str(e))
            status = "have failed to be created:" + "" + exception_detail
            self.export_from_enrichment_table_2(files, status)
            msg = QMessageBox()
            msg.setWindowTitle("File Export Error")
            msg.setText("There has been an error exporting files for enrichment")
            x = msg.exec_()

        data = self.pull_enrichment_data_2()
        update_db(data, 'Reports')
        pull_report_to_csv()


    def export_from_enrichment_table_2(self, files, status):
        """This function updates the table on the export files from client Tab providing information data on the
        files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        for file in files:
            if 'TransUnion' in file:
                name = os.path.basename(file)
                file_name = name.replace('.csv', '')
                self.ui.tableWidget_8.setItem(0, 0, QTableWidgetItem(file_name))
                self.ui.tableWidget_8.setItem(0, 2, QTableWidgetItem('Litigation Cases File for Transunion'+ ' ' + status))
                self.ui.tableWidget_8.setItem(0, 3, QTableWidgetItem(now_str))
                # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
                if  self.ui.checkBox_34.isChecked():
                    self.ui.tableWidget_8.setItem(0, 1, QTableWidgetItem('Outbound: Transunion'))
                else:
                    pass
            elif 'CreditSafe' in file:
                name = os.path.basename(file)
                file_name = name.replace('.csv', '')
                self.ui.tableWidget_8.setItem(1, 0, QTableWidgetItem(file_name))
                self.ui.tableWidget_8.setItem(1, 2, QTableWidgetItem('Litigation Cases File for Credit Safe' + ' ' + status))
                self.ui.tableWidget_8.setItem(1, 3, QTableWidgetItem(now_str))
                # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
                if  self.ui.checkBox_35.isChecked():
                    self.ui.tableWidget_8.setItem(1, 1, QTableWidgetItem('Outbound: Credit Safe'))
                else:
                    pass
            else:
                pass


    def pull_enrichment_data_2(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(2), columns=range(5))
        rowCount = self.ui.tableWidget_8.rowCount()
        columnCount = self.ui.tableWidget_8.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_8.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
            df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
            df = df.dropna(how='any', axis=0)
            return df


    def from_enrichment(self):
        "This function controls the collating and exporting of files from Transunion and Credit Safe"
        if self.ui.checkBox_36.isChecked() and self.ui.checkBox_37.isChecked():
            try:
                name = func_2()
                status = "Placement File for review has been successfully created - please review this file and make " \
                         "changes, if required."
                self.from_enrichment_table(name, status )
                msg = QMessageBox()
                msg.setWindowTitle("Placement File - Creation Success")
                msg.setText("Placement File for review has been created - please review this file and make any "
                            "changes prior to exporting to Litigation Provider, if required.")
                x = msg.exec_()
            except Exception as e:
                print(str(e))
                exception_detail = exception_cleaner(str(e))
                status = "Placement File for review has failed to be created:" + "" + exception_detail
                self.from_enrichment_table(name, status)
                msg = QMessageBox()
                msg.setWindowTitle("File Creation Error")
                msg.setText("There has been an error creating the list of accounts required for placement.")
                x = msg.exec_()

        data = self.pull_from_enrichment_data()
        update_db(data, 'Reports')
        pull_report_to_csv()


    def from_enrichment_table(self, name, status):
        """This function updates the table on the export files from client Tab providing information data on the
        files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")

        self.ui.tableWidget_9.setItem(0, 0, QTableWidgetItem(name))
        self.ui.tableWidget_9.setItem(0, 2, QTableWidgetItem('Litigation Cases File for Transunion'+ ' ' + status))
        self.ui.tableWidget_9.setItem(0, 3, QTableWidgetItem(now_str))
        self.ui.tableWidget_9.setItem(0, 1, QTableWidgetItem('Outbound: AJJB'))


    def pull_from_enrichment_data(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(2), columns=range(4))
        rowCount = self.ui.tableWidget_9.rowCount()
        columnCount = self.ui.tableWidget_9.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_9.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
            df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update']
            df = df.dropna(how='any', axis=0)
            return df




    def from_enrichment_2(self):
        "This function controls the collating and exporting of files from Transunion and Credit Safe"
        if self.ui.checkBox_31.isChecked():
            try:
                name = func_3()
                status = "Placement File been successfully created and is not ready to exported to AJJB"
                self.from_enrichment_table_2(name, status)
                msg = QMessageBox()
                msg.setWindowTitle("Finalised Placement File - Creation Success")
                msg.setText("Placement File has been created - this file is now ready to be exported to the relevant litigation provider")
                x = msg.exec_()
            except Exception as e:
                print(str(e))
                exception_detail = exception_cleaner(str(e))
                status = "Finalised Placement File has failed to be created:" + "" + exception_detail
                self.from_enrichment_table_2(name, status)
                msg = QMessageBox()
                msg.setWindowTitle("File Creation Error")
                msg.setText("There has been an error creating the finalised list of accounts required for placement.")
                x = msg.exec_()

        data = self.pull_from_enrichment_data_2()
        update_db(data, 'Reports')
        pull_report_to_csv()


    def from_enrichment_table_2(self, name, status):
        """This function updates the table on the export files from client Tab providing information data on the
        files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")

        self.ui.tableWidget_10.setItem(0, 0, QTableWidgetItem(name))
        self.ui.tableWidget_10.setItem(0, 2, QTableWidgetItem(status))
        self.ui.tableWidget_10.setItem(0, 3, QTableWidgetItem(now_str))
        self.ui.tableWidget_10.setItem(0, 1, QTableWidgetItem('Outbound: AJJB'))


    def pull_from_enrichment_data_2(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(2), columns=range(4))
        rowCount = self.ui.tableWidget_10.rowCount()
        columnCount = self.ui.tableWidget_10.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_10.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
            df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update']
            df = df.dropna(how='any', axis=0)
            return df

    def select_file_for_creating_to_litigator(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the TO Client
        TAB """
        file_list = []
        client_index = self.ui.comboBox_13.currentIndex()
        check_box_list = [self.ui.checkBox_38.isChecked(), self.ui.checkBox_40.isChecked(),
                          self.ui.checkBox_41.isChecked()]
        check_box_file_translation = ['Transaction', 'Balance Update', 'Closure']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if client_index == 0 and check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def litigation_clicked_process(self):
        "This function controls the process file button on the process DCA files tab"
        global file, file_path
        file_list = self.select_file_for_creating_to_litigator()
        print(file_list)
        for file in file_list:
            try:
                file_path = ""
                file_path = process_to_litgation(file)
                print(file_path)
                status = 'File for litigation has been successfully processed'
                self.create_litigation_table(file, file_path, status)
            except Exception as e:
                print(str(e))
                exception_detail = exception_cleaner(str(e))
                msg = QMessageBox()
                msg.setWindowTitle("File Creation Error")
                msg.setText(f"There has been an error creating the {file} file ")
                x = msg.exec_()
                status = f'File creation has failed: {exception_detail}'
                self.create_litigation_table(file, file_path, status)

        data = self.pull_create_litigation_data()
        update_db(data, 'Reports')
        pull_report_to_csv()


    def create_litigation_table(self, file, file_path, status):
        """This function updates the table on the export files from client Tab providing information data on the
        files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        if 'Transaction' in file:
            name = os.path.basename(file_path)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_11.setItem(0, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_11.setItem(0, 2, QTableWidgetItem('Transaction' + ' ' + status))
            self.ui.tableWidget_11.setItem(0, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if self.ui.checkBox_38.isChecked():
                self.ui.tableWidget_11.setItem(0, 1, QTableWidgetItem('Outbound: AJJB'))
            else:
                pass
        elif 'Balance Update' in file:
            name = os.path.basename(file_path)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_11.setItem(1, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_11.setItem(1, 2,QTableWidgetItem('Balance Update' + ' ' + status))
            self.ui.tableWidget_11.setItem(1, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if self.ui.checkBox_40.isChecked():
                self.ui.tableWidget_11.setItem(1, 1, QTableWidgetItem('Outbound: AJJB'))
            else:
                pass
        elif 'Closure' in file:
            name = os.path.basename(file_path)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_11.setItem(2, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_11.setItem(2, 2,
                                              QTableWidgetItem('Closure' + ' ' + status))
            self.ui.tableWidget_11.setItem(2, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if self.ui.checkBox_41.isChecked():
                self.ui.tableWidget_11.setItem(2, 1, QTableWidgetItem('Outbound: AJJB'))
            else:
                pass
        else:
            pass


    def pull_create_litigation_data(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(3), columns=range(5))
        rowCount = self.ui.tableWidget_11.rowCount()
        columnCount = self.ui.tableWidget_11.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_11.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
            df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
            df = df.dropna(how='any', axis=0)
            return df

    def select_file_for_exporting_to_litigation(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the TO Client
        TAB """
        file_list = []
        client_index = self.ui.comboBox_13.currentIndex()
        check_box_list = [self.ui.checkBox_24.isChecked(), self.ui.checkBox_25.isChecked(),
                          self.ui.checkBox_26.isChecked(), self.ui.checkBox_30.isChecked()]
        check_box_file_translation = ['Transaction', 'Balance Update','Closure', 'Placement']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if client_index == 0 and check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def litigation_clicked_export(self):
        "This process controls the Export button on the Export Files to Client Tab"
        global name, status
        file_list = self.select_file_for_exporting_to_litigation()
        print(file_list)
        client_index = self.ui.comboBox_13.currentIndex()
        if client_index == 0:
            file_paths = export_selected_litigation_file(file_list)
            print(file_paths)
            for file in file_paths:
                try:
                    if 'Transaction' in file:
                        # subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FROM_JUST_AJJB_PAY}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FROM_JUST_AJJB_PAY + '\\Processed\\')
                        status = 'successfully exported to AJJB SFTP'
                        self.export_to_litigator_table(name, client_index, status)
                        print('here')
                    elif 'Balance Update' in file:
                        # subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FROM_JUST_AJJB_BU}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FROM_JUST_AJJB_BU + '\\Processed\\')
                        status = 'successfully exported to AJJB SFTP'
                        self.export_to_litigator_table(name, client_index, status)
                    elif 'Closure' in file:
                        # subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FROM_JUST_AJJB_CLOSURE}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FROM_JUST_AJJB_CLOSURE + '\\Processed\\')
                        status = 'successfully exported to AJJB SFTP'
                        self.export_to_litigator_table(name, client_index, status)
                    elif 'Placement' in file:
                        # subprocess.call(file)
                        newest = max(glob.glob(f'{settings.FROM_JUST_AJJB_PLACEMENT}\\*.csv'),
                                     key=os.path.getmtime)
                        name = os.path.basename(newest)
                        name.replace('.csv', '')
                        shutil.move(newest, settings.FROM_JUST_AJJB_PLACEMENT+ '\\Processed\\')
                        status = 'successfully exported to AJJB SFTP'
                        self.export_to_litigator_table(name, client_index, status)
                except Exception as e:
                    if str(e) == 'max() arg is an empty sequence':
                        msg = QMessageBox()
                        msg.setWindowTitle("Exporting Error")
                        msg.setText("Directory is empty - there is no file to export")
                        x = msg.exec_()
                        status = 'export failed as there was no file in the directory'
                    else:
                        exception_detail = exception_cleaner(str(e))
                        msg = QMessageBox()
                        msg.setWindowTitle("Exporting Error")
                        msg.setText(f"Error exporting this file to the AJJB SFTP: {exception_detail}")
                        x = msg.exec_()
                        status = 'export has failed'
                        self.export_to_litigator_table(name, client_index, status)
        else:
            pass
        data = self.pull_export_litigator_data()
        update_db(data, 'Reports')
        pull_report_to_csv()

    def export_to_litigator_table(self, file, clientindex, status):
        """This function updates the table on the export files from client Tab providing information data on the
        files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        if 'PAY' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_6.setItem(0, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_6.setItem(0, 2, QTableWidgetItem('Transaction' + ' ' + status))
            self.ui.tableWidget_6.setItem(0, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_6.setItem(0, 1, QTableWidgetItem('Outbound: AJJB'))
            else:
                pass
        elif 'BU' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_6.setItem(1, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_6.setItem(1, 2, QTableWidgetItem('Balance Update' + ' ' + status))
            self.ui.tableWidget_6.setItem(1, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_6.setItem(1, 1, QTableWidgetItem('Outbound: AJJB'))
            else:
                pass
        elif 'CLOSURE' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_6.setItem(2, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_6.setItem(2, 2, QTableWidgetItem('Closure' + ' ' + status))
            self.ui.tableWidget_6.setItem(2, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_6.setItem(2, 1, QTableWidgetItem('Outbound: AJJB'))
            else:
                pass
        elif 'Placement' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_6.setItem(3, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_6.setItem(3, 2, QTableWidgetItem('Placement' + ' ' + status))
            self.ui.tableWidget_6.setItem(3, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_5.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_6.setItem(3, 1, QTableWidgetItem('Outbound: AJJB'))
            else:
                pass
        else:
            pass


    def pull_export_litigator_data(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(5), columns=range(5))
        rowCount = self.ui.tableWidget_6.rowCount()
        columnCount = self.ui.tableWidget_6.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_6.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
            df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
            df = df.dropna(how='any', axis=0)
            return df


    def select_file_for_processing_From_litigation(self):
        """This function returns a list of the selected files input by the user using the checkboxes on the process files for DCA tab"""
        file_list = []
        client_index = self.ui.comboBox_11.currentIndex()
        check_box_list = [self.ui.checkBox_21.isChecked(), self.ui.checkBox_22.isChecked(),
                          self.ui.checkBox_23.isChecked(),
                          self.ui.checkBox_27.isChecked(), self.ui.checkBox_29.isChecked()]
        check_box_file_translation = ['NFU', 'Transaction',  'Closure', 'Activity',  'Query']
        counter = 0
        for check_box in check_box_list:
            counter = counter + 1
            if client_index == 0 and check_box:
                value = check_box_file_translation[counter - 1]
                file_list.append(value)
            else:
                pass
        return file_list

    def process_from_litigation_to_just(self):
        "This function controls the process file button on the process DCA files tab"
        file_list = self.select_file_for_processing_From_litigation()
        client_index = self.ui.comboBox_11.currentIndex()
        if client_index == 0:
            file_paths = process_selected_litigation(file_list)
            for file in file_paths:
                try:
                    if file == 'No File':
                        msg = QMessageBox()
                        msg.setWindowTitle("Processing Error")
                        msg.setText("There is no file to process in the directory")
                        x = msg.exec_()
                    else:
                        process_litigation_file(file)
                        status = 'File has been successfully processed'
                        self.process_from_AJJB_update_table(file, client_index, status)
                except Exception as e:
                    exception_detail = exception_cleaner(str(e))
                    msg = QMessageBox()
                    msg.setWindowTitle("Processing Error")
                    msg.setText("There has been an error processing this file ")
                    x = msg.exec_()
                    status = f'File processing has failed: {exception_detail}'
                    self.process_from_AJJB_update_table(file, client_index, status)
        elif client_index == 1:
            pass
        else:
            pass
        data = self.pull_process_litigation_data()
        update_db(data, 'Reports')
        pull_report_to_csv()


    def process_from_AJJB_update_table(self, file, clientindex, status):
        """This function updates the table on the process files from DCA Tab providing information data on the files """
        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        if 'NFU' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_3.setItem(0, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_3.setItem(0, 2, QTableWidgetItem('Non Financial Updates' + ' ' + status))
            self.ui.tableWidget_3.setItem(0, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_2.setItem(0, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_3.setItem(0, 1, QTableWidgetItem('Inbound: AJJB'))
            else:
                pass
        elif 'Payment' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_3.setItem(1, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_3.setItem(1, 2, QTableWidgetItem('Payment' + ' ' + status))
            self.ui.tableWidget_3.setItem(1, 3, QTableWidgetItem(now_str))
            # self.ui.tableWidget_2.setItem(1, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_3.setItem(1, 1, QTableWidgetItem('Inbound: AJJB'))
            else:
                pass
        elif 'Activity' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_3.setItem(3, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_3.setItem(3, 2, QTableWidgetItem(
                'Activity' + ' ' + status))
            self.ui.tableWidget_3.setItem(3, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget_3.setItem(3, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_3.setItem(3, 1, QTableWidgetItem('Inbound: AJJB'))
            else:
                pass
        elif 'Closure' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_3.setItem(2, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_3.setItem(2, 2, QTableWidgetItem(
                'Closure' + ' ' + status))
            self.ui.tableWidget_3.setItem(2, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget_3.setItem(2, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_3.setItem(2, 1, QTableWidgetItem('Inbound: AJJB'))
        elif 'Query' in file:
            name = os.path.basename(file)
            file_name = name.replace('.csv', '')
            self.ui.tableWidget_3.setItem(4, 0, QTableWidgetItem(file_name))
            self.ui.tableWidget_3.setItem(4, 2, QTableWidgetItem(
                'Query' + ' ' + status))
            self.ui.tableWidget_3.setItem(4, 3, QTableWidgetItem(now_str))
            self.ui.tableWidget_3.setItem(4, 5, QTableWidgetItem(''))
            if clientindex == 0:
                self.ui.tableWidget_3.setItem(4, 1, QTableWidgetItem('Inbound: AJJB'))
            else:
                pass
        else:
            pass

    def pull_process_litigation_data(self):
        """This function pulls data from the table on the export dca files tab in a dataframe to push to database"""
        df = pd.DataFrame(index=range(5), columns=range(5))
        rowCount = self.ui.tableWidget_3.rowCount()
        columnCount = self.ui.tableWidget_3.columnCount()
        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.ui.tableWidget_3.item(row, column)
                if (widgetItem and widgetItem.text):
                    df.loc[row, column] = widgetItem.text()
                else:
                    df.loc[row, column] = 'NULL'
        df.columns = ['File_Name', 'Client', 'File_Status', 'Last_Update', 'SLA_Breached']
        df = df.dropna(how='any', axis=0)
        return df
if __name__ == "__main__":
    import sys

    app = qtw.QApplication(sys.argv)
    widget = ImportTab()
    widget.show()

    sys.exit(app.exec_())
