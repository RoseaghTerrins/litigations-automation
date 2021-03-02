import pandas as pd
from sqlalchemy import create_engine, MetaData, Table,  String, Column, DateTime, Numeric, Float, CheckConstraint, Integer
import sqlalchemy
from datetime import datetime
import glob
import os
import shutil
import settings
from xlrd import open_workbook
from Database_Import.send_import_email import send_email

global file_type, name, sender, newest


def create_table(file):
    Server = 'Just-Win10VM\SQLEXPRESS'
    Database = 'RM_Files'
    Driver = 'ODBC Driver 17 for SQL Server'
    Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
    engine = create_engine(Database_Con)
    engine.connect()
    metadata = MetaData()
    table = Table(file, metadata,
                  Column('ClientReference', Integer(), nullable=True),
                  Column('CustomerName', String(225)),
                  Column('Salutation', String(225)),
                  Column('FirstName', String(225)),
                  Column('Surname', String(225)),
                  Column('DateOfBirth', DateTime()),
                  Column('MailingAddressLine1', String(225)),
                  Column('MailingAddressLine2', String(225)),
                  Column('MailingAddressLine3', String(225)),
                  Column('MailingAddressLine4', String(225)),
                  Column('MailingAddressLine5', String(225)),
                  Column('MailingAddressPostcode', String(225)),
                  Column('SupplyAddressLine1', String(225)),
                  Column('SupplyAddressLine2', String(225)),
                  Column('SupplyAddressLine3', String(225)),
                  Column('SupplyAddressLine4', String(225)),
                  Column('SupplyAddressLine5', String(225)),
                  Column('SupplyAddressLine5', String(225)),
                  Column('SupplyAddressPostcode', String(225)),
                         Column('Telephone1', sqlalchemy.types.NVARCHAR(length=225)),
                         Column('Telephone2',sqlalchemy.types.NVARCHAR(length=225)),
                         Column('Telephone3', sqlalchemy.types.NVARCHAR(length=225)),
                         Column('E-mail', String(225)),
                         Column('Balance', Float()),
                         Column('OutstandingBalance', Float()),
                         Column('LPC/FeesAddedtoBalance', Float()),
                         Column('DefaultDate', DateTime()),
                         Column('LastPaymentDate', DateTime()),
                         Column('LastPaymentAmount', Float()),
                         Column('ProductName', String(225)),
                         Column('ProductType', String(225)),
                         Column('SupplyDateFrom', DateTime()),
                         Column('SupplyDateTo', DateTime()),
                         Column('VulnerabilityIdentified', String(225)),
                         Column('AccountStatus', String(225)),
                         Column('FinalInvoiceNumber', sqlalchemy.types.NVARCHAR(length=225)),
                         Column('FinalBillIssueDate', DateTime()),
                         Column('FinalBillFromDate', DateTime()),
                         Column('FinalBillToDate', DateTime()),
                         Column('FinalBillVATAmount', Float()),
                         Column('LastBroughtFWDAmount', Float()),
                         Column('PrepaymentAccount', String(225)),
                         Column('ContactSupplyAddress', String(225)),
                         Column('MPANNumber', sqlalchemy.types.NVARCHAR(length=225)),
                         Column('MPRNNumber',sqlalchemy.types.NVARCHAR(length=225)),
                         Column('DisconnectionNoticeDate',  DateTime()),
                         Column('DisconnectionDate',  DateTime()),
                         Column('DisconnectionReason', String(225)),
                         Column('VacatedDate',  DateTime()),
                         Column('ParentAccountID', String(225)),
                         Column('TerminationReason', String(225)),
                         Column('ToleranceCharge', String(225)),
                         Column('AccountSource', String(225))
                         )
    metadata.create_all(engine)


def import_file_to_db(file):
    Server = 'Just-Win10VM\SQLEXPRESS'
    Database = 'RM_Files'
    Driver = 'ODBC Driver 17 for SQL Server'
    Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
    engine = create_engine(Database_Con)
    engine.connect()
    name = os.path.basename(file)
    name = name.replace('.csv', '')
    data = pd.read_csv(file, skip_blank_lines=False, encoding='gbk')
    df = pd.DataFrame(data)
    df = df.dropna(how='all')
    df.to_sql(name, con=engine, index=False, if_exists='append')


def import_nb_file_to_db(file):
    Server = 'Just-Win10VM\SQLEXPRESS'
    Database = 'RM_Files'
    Driver = 'ODBC Driver 17 for SQL Server'
    Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
    engine = create_engine(Database_Con)
    engine.connect()
    name = os.path.basename(file)
    name = name.replace('.csv', '')
    create_table(name)
    data = pd.read_csv(file, skip_blank_lines=False, encoding='gbk')
    df = pd.DataFrame(data)
    df[["DateofBirth", "DefaultDate", "LastPaymentDate", "SupplyDateFrom", "SupplyDateTo", "FinalBillIssueDate", "FinalBillFromDate", "FinalBillToDate", "VacatedDate" ]] = df[["DateofBirth", "DefaultDate", "LastPaymentDate", "SupplyDateFrom", "SupplyDateTo", "FinalBillIssueDate", "FinalBillFromDate", "FinalBillToDate", "VacatedDate"]].apply(pd.to_datetime)
    df[["Telephone1", "Telephone2", "Telephone3", "MPANNumber", "MPRNNumber"]] = df[["Telephone1", "Telephone2", "Telephone3", "MPANNumber", "MPRNNumber"]].astype(str)
    df["MPANNumber"] = df["MPANNumber"].str.rstrip('0')
    df["MPRNNumber"] = df["MPRNNumber"].str.rstrip('0')
    df["Telephone1"] = df["Telephone1"].str.rstrip('0')
    df["Telephone2"] = df["Telephone2"].str.rstrip('0')
    df["Telephone3"] = df["Telephone3"].str.rstrip('0')
    df["MPANNumber"] = df["MPANNumber"].str.rstrip('.')
    df["MPRNNumber"] = df["MPRNNumber"].str.rstrip('.')
    df["Telephone1"] = df["Telephone1"].str.rstrip('.')
    df["Telephone2"] = df["Telephone2"].str.rstrip('.')
    df["Telephone3"] = df["Telephone3"].str.rstrip('.')
    df['Telephone1'] = "0" + df['Telephone1']
    df['Telephone2'] = "0" + df['Telephone2']
    df['Telephone3'] = "0" + df['Telephone3']

    df[["Telephone1", "Telephone2", "Telephone3", "MPANNumber", "MPRNNumber"]]= df[["Telephone1", "Telephone2", "Telephone3", "MPANNumber", "MPRNNumber"]].replace('0nan', 'NULL')
    df = df.dropna(how='all')
    df.to_sql(name, con=engine, index=False, if_exists='append')


directory_list = [
settings.YU_NB_Input_Directory,
                  settings.YU_QR_Input_Directory,
                  settings.YU_CLIENT_RECALL_Input_Directory,
                  settings.YU_CLIENT_ADJUSTMENT_Input_Directory,
                  settings.FIRST_LOCATE_Activity_Directory,
                  settings.FIRST_LOCATE_AGMTS_Directory,
                  settings.FIRST_LOCATE_Query_Directory,
                  settings.First_LOCATE_Closure_Input_Directory,
                  settings.First_LOCATE_NFU_Input_Directory,
                  settings.First_LOCATE_Transaction_Input_Directory,

                  settings.AJJB_ACTIVITY_Input_Directory,
                  settings.AJJB_CLOSURE_Input_Directory,
                  settings.AJJB_NFU_Input_Directory,
                  settings.AJJB_PAYMENT_Input_Directory,
                  settings.AJJB_QUERY_Input_Directory,

                  settings.FROM_CREDIT_SAFE,
                  settings.FROM_TRANSUNION
                  ]


def get_attr(item):
    """This function pulls data from the table on the import_to_just tab in a dataframe to push to database"""
    if 'Query Response' in item:
        file_type = 'Query Response File'
    elif 'Query' in item:
        file_type = 'Query File'
    elif 'Adjustment' in item:
        file_type = 'Adjustment File'
    elif 'Closure' in item:
        file_type = 'Closure File'
    elif 'Recall' in item:
        file_type = 'Client Recall File'
    elif 'NFU' in item:
        file_type = 'Non-Financial Updates File'
    elif 'Transaction' in item:
        file_type = 'Transaction File'
    elif 'NB' in item:
        file_type = 'New Business File'
    elif 'Activity' in item:
        file_type = 'Activity File'
    elif 'AGMT' in item:
        file_type = 'AGMTS File'
    elif 'Payment' in item:
        file_type = 'Payment File'
    elif 'CS' in item:
        file_type = 'Credit Safe Enrichment File'
    elif 'TU' in item:
        file_type = 'TransUnion Enrichment File'
    else:
        file_type = ''

    if '1st_Locate' in item:
        sender = '1st Locate'
    elif 'YU' in item:
        sender = 'Yu Energy'
    elif 'AJJB' in item:
        sender = 'AJJB'
    elif 'CS' in item:
        sender = 'Credit Safe'
    elif 'TU' in item:
        sender = 'TransUnion'
    else:
        sender = ''

    return file_type, sender


def func():
    global file_type, name, sender, newest
    data = []
    success_counter = 0
    now = str(datetime.now().strftime("%Y%m%d"))
    for item in directory_list:
        try:
            print(item)
            if 'Activity' and '1st_Locate' in item:
                newest = max(glob.glob(f'{item}\\*.xlsx'), key=os.path.getmtime)
                wb = open_workbook(newest, encoding_override='latin1')
                df = pd.read_excel(wb)
                os.remove(newest)
                name = f'1st_ACT_{now}.csv'
                path = item + '\\' + name
                df.to_csv(item + '\\' + name, index=False)
                import_file_to_db(item + '\\' + name)
                shutil.move(path, item + '\\Processed\\')
                status = 'Import Successful - This file is ready to process using the RM Application'
                file_type, sender = get_attr(item)
                data.append([file_type, name, sender, item, status])
                success_counter += 1
            elif 'Query_Response' in item:
                newest = max(glob.glob(f'{item}\\*.csv'), key=os.path.getmtime)
                newest = str(newest)
                name = os.path.basename(newest)
                name = name.replace('.csv', '_response')
                newest_2 = newest.replace('.csv', '_response.csv')
                os.rename(newest, newest_2)
                import_file_to_db(newest_2)
                shutil.move(newest_2, item + '\\Processed\\')
                status = 'Import Successful - This file is ready to process using the RM Application'
                file_type, sender = get_attr(item)
                data.append([file_type, name, sender, item, status])
                success_counter += 1
            elif 'NB_Files' in item:
                newest = max(glob.glob(f'{item}\\*.csv'), key=os.path.getmtime)
                name = os.path.basename(newest)
                name = name.replace('.csv', '')
                import_nb_file_to_db(newest)
                shutil.move(newest, item + '\\Processed\\' + name + ".csv")
                status = 'Import Successful - This file is ready to process using the RM Application'
                file_type, sender = get_attr(item)
                data.append([file_type, name, sender, item, status])
                success_counter += 1
            elif 'Query' in item and 'AJJB' in item:
                newest = max(glob.glob(f'{item}\\*.xlsx'), key=os.path.getmtime)
                wb = open_workbook(newest, encoding_override='latin1')
                df = pd.read_excel(wb)
                os.remove(newest)
                name = f'AJJBQueryReport{now}.csv'
                path = item + '\\' + name
                df.to_csv(item + '\\' + name, index=False)
                import_file_to_db(item + '\\' + name)
                shutil.move(path, item + '\\Processed\\')
                status = 'Import Successful - This file is ready to process using the RM Application'
                file_type, sender = get_attr(item)
                data.append([file_type, name, sender, item, status])
                success_counter += 1
            else:
                newest = max(glob.glob(f'{item}\\*.csv'), key=os.path.getmtime)
                name = os.path.basename(newest)
                name = name.replace('.csv', '')
                import_file_to_db(newest)
                shutil.move(newest, item + '\\Processed\\' + name + ".csv")
                status = 'Import Successful - This file is ready to process using the RM Application'
                file_type, sender = get_attr(item)
                data.append([file_type, name, sender, item, status])
                success_counter += 1
        except Exception as e:
            exception = str(e)
            print(exception)
            file_type, sender = get_attr(item)
            if 'already exists' in exception:
                status = 'Duplication Error: This file has already been imported into the database'
                data.append([file_type, name, sender, item, status])
                shutil.move(newest, item + '\\Processed\\' + name + ".csv")
            elif 'max() arg is an empty sequence' in exception:
                status = 'No New File to process in this directory'
                name = ''
                data.append([file_type, name, sender, item, status])
            else:
                pass
    return data, success_counter


now = str(datetime.now().strftime("%d-%m-%Y %H%M"))
data, success_counter = func()
df = pd.DataFrame(data)
df.columns = ['File_Type', 'File_Name', 'Sender', 'Directory Location/File Path', 'Status']
df = df.dropna(how='any', axis=0)
email_addresses = ["roseagh.terrins@therobotexchange.com"]
if success_counter >= 1:
    df.to_csv(f'{settings.IMPORT_REPORTS}\\DCA_Import_Report_{now}.csv', index=False)
    for email in email_addresses:
        send_email(now, email)
