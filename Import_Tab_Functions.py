import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from datetime import date
import datetime
import glob
import os
from SQLQUERYS.YU_TO_FIRSTLOCATE.YU_TO_FIRST_LOCATE_ASSIGNMENT_FILE import process_nb
from SQLQUERYS.YU_TO_FIRSTLOCATE.YU_TO_FIRST_LOCATE_ADJUSTMENT_PAY_BILLS import process_trans_adjustment
from SQLQUERYS.YU_TO_FIRSTLOCATE.YU_CLIENT_RECALL import process_client_recall
from SQLQUERYS.YU_TO_FIRSTLOCATE.DCA_NFU_INSERT import process_dca_nfu
from SQLQUERYS.YU_TO_FIRSTLOCATE.DCA_TRANSACTION_INSERT import process_dca_transaction
from SQLQUERYS.YU_TO_FIRSTLOCATE.FIRST_LOCATE_ACTIVITY_FILE import process_first_locate_ACTIVITY
from SQLQUERYS.YU_TO_FIRSTLOCATE.FIRST_LOCATE_AGMT_FILE import process_first_locate_AGMT
from SQLQUERYS.YU_TO_FIRSTLOCATE.FIRST_LOCATE_CLIENT_RECALL_RESPONSE import process_client_recall_dca_response
from SQLQUERYS.YU_TO_FIRSTLOCATE.FIRST_LOCATE_QUERY_FILE import process_first_locate_query
from SQLQUERYS.YU_TO_FIRSTLOCATE.YU_QUERY_RESPONSE import process_yu_query_response
from SQLQUERYS.TO_AJJB_PAY import process_to_ajjb_pay
from SQLQUERYS.TO_AJJB_CLOSURE import process_to_ajjb_closure
from SQLQUERYS.TO_AJJB_BALANCEUPDATE import process_to_ajjb_balanceupdate
from SQLQUERYS.AJJB_PAYMENT import process_ajjb_payment
from SQLQUERYS.AJJB_NFU import process_ajjb_nfu
from SQLQUERYS.AJJB_CLOSURES import process_ajjb_closures
from SQLQUERYS.AJJB_ACTIVITY import process_ajjb_activity
from SQLQUERYS.AJJB_QUERY import process_ajjb_query
import settings


def update_db(data, name):
    df = pd.DataFrame(data)

    Server = 'Just-Win10VM\SQLEXPRESS'
    Database = 'RM_Reports'
    Driver = 'ODBC Driver 17 for SQL Server'
    Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
    engine = create_engine(Database_Con)
    engine.connect()
    df.to_sql(name, con=engine, index=False, if_exists='append')
    table = pd.read_sql(f'select * from {name}', con=engine)
    table = table.sort_values(by='Last_Update')
    table['Flag'] = table.duplicated('File_Name', keep='last')
    for index, row in table.iterrows():
        if row["File_Name"] == 'NULL':
            table = table.drop(index=index)
        elif row['Flag']:
            table = table.drop(index=index)
        else:
            pass
    table = table.drop('Flag', axis=1)
    table.to_sql(name, con=engine, index=False,if_exists='replace')



def pull_report_to_csv():
    from datetime import datetime
    today_date = str(datetime.now().strftime("%d/%m/%Y"))
    Server = 'Just-Win10VM\SQLEXPRESS'
    Database = 'RM_Reports'
    Driver = 'ODBC Driver 17 for SQL Server'
    Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
    engine = create_engine(Database_Con)
    engine.connect()
    table = pd.read_sql(f"select * from RM_Reports.dbo.Reports where Last_Update LIKE '%{today_date}%'", con=engine)
    today_date = str(datetime.now().strftime("%d%m%Y"))
    table.to_csv(f'{settings.DAILY_REPORTS}\\Daily RM Report {today_date}.csv', index=False)


def exception_cleaner(exception):
    exception = exception.replace("[42S02] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]", '')
    exception = exception.replace("('42S02',", '')
    exception = exception.replace("'. (208) (SQLExecDirectW)", '')
    exception = exception.replace("3701(SQLExecDirectW",'')
    exception = exception.replace('"', '')
    exception = exception.replace(')', '')
    exception = exception.replace("'", '')
    return exception


def process_selected_yu_file(files):
    file_paths = []
    for file in files:
        if file == 'NB':
            try:
                newest = max(glob.glob(f'{settings.YU_TOJUST_NB_DATABASE}\\*.csv'), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                file_paths.append('No File')
        elif file == 'QR':
            try:
                newest = max(
                    glob.glob(str(settings.YU_TOJUST_QR_DATABASE)),
                    key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                file_paths.append('No File')
        elif file == 'Client Recall':
            try:
                newest = max(
                    glob.glob(str(settings.YU_TOJUST_CLIENT_RECALL)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                file_paths.append('No File')
        elif file == 'Adjustment File':
            try:
                newest = max(
                    glob.glob(str(settings.YU_TOJUST_ADJUSTMENT)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                file_paths.append('No File')
        else:
            pass
        pass

    return file_paths


def process_yu_to_first_locate(file):
    today = date.today()
    today = str(today)
    today = today.replace('-', '')
    if 'NB' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_nb(file_name)
    elif 'Query_Response' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_yu_query_response(file_name)
    elif 'Recall' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_client_recall(file_name, f'{today}_JUST_CLS')
    elif 'Adjustment' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_trans_adjustment(file_name)
    else:
        pass


def process_selected_1st_locate_file(files):
    file_paths = []
    for file in files:
        if file == 'NFU':
            try:
                newest = max(glob.glob(str(settings.DCA_TOJUST_NFU_DATABASE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Transaction':
            try:
                newest = max(glob.glob(str(settings.DCA_TOJUST_TRANSACTION_DATABASE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Activity':
            try:
                newest = max(glob.glob(str(settings.DCA_TOJUST_ACTIVITY_DATABASE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'AGMT':
            try:
                newest = max(glob.glob(str(settings.DCA_TOJUST_AGMTS_DATABASE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Closure':
            try:
                newest = max(glob.glob(str(settings.DCA_TOJUST_CLOSURE_DATABASE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Query':
            try:
                newest = max(glob.glob(str(settings.DCA_TOJUST_QUERY_DATABASE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        else:
            pass
    return file_paths


def process_1st_locate_file(file):
    today = date.today()
    today = str(today)
    today = today.replace('-', '')
    if 'NFU' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_dca_nfu(file_name)
    elif 'Transaction' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_dca_transaction(file_name, f'YU_PAY{today}')
    elif 'Adjustment' in file:
        pass
    elif 'Closure' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_client_recall_dca_response(file_name, f'ToYU_{today}_JUST_CLS')
    elif 'Activity' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_first_locate_ACTIVITY(file_name)
    elif 'AGMT' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_first_locate_AGMT(file_name)
    elif 'Query' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_first_locate_query(file_name)
    else:
        pass


def export_selected_1st_locate_file(files):
    file_paths = []
    for file in files:
        if file == 'Assignment':
            try:
                newest = max(glob.glob(str(settings.ASSIGNMENT_FROM_JUST_TO_FIRST_LOCATE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Pay':
            try:
                newest = max(glob.glob(str(settings.PAY_FROM_JUST_TO_FIRST_LOCATE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Bill':
            try:
                newest = max(glob.glob(str(settings.BILL_FROM_JUST_TO_FIRST_LOCATE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Recall':
            try:
                newest = max(glob.glob(str(settings.RECALL_FROM_JUST_TO_FIRST_LOCATE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'QR':
            try:
                newest = max(glob.glob(str(settings.QR_FROM_JUST_TO_FIRST_LOCATE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        else:
            pass
    return file_paths


def export_selected_client_file(files):
    file_paths = []
    for file in files:
        if file == 'NFU':
            try:
                newest = max(glob.glob(str(settings.NFU_FROM_JUST_TO_YU)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Transaction':
            try:
                newest = max(glob.glob(str(settings.TRANSACTION_FROM_JUST_TO_YU)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Closure':
            try:
                newest = max(glob.glob(str(settings.CLOSURE_FROM_JUST_TO_YU)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Query':
            try:
                newest = max(glob.glob(str(settings.QUERY_FROM_JUST_TO_YU)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        else:
            pass
    return file_paths

def export_enrichment_file(tu_flag, cs_flag):
    file_paths = []
    if tu_flag == 1:
        try:
            newest = max(glob.glob(str(f'{settings.TO_TRANSUNION}\\*.csv')), key=os.path.getmtime)
            file_paths.append(newest)
        except ValueError:
            pass
    if cs_flag == 1:
        print('flag got here')
        try:
            newest = max(glob.glob(str(f'{settings.TO_CREDIT_SAFE}\\*.csv')), key=os.path.getmtime)
            file_paths.append(newest)
        except ValueError:
            pass
    return file_paths

def export_enrichment_file_2(file_list):
    file_paths = []
    for file in file_list:
        if file == 'TU':
            try:
                newest = max(glob.glob(str(settings.TO_TRANSUNION_BATCH_FILE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'CS':
            try:
                newest = max(glob.glob(str(settings.TO_CREDIT_SAFE_BATCH_FILE)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        else:
                pass
    return file_paths

def process_to_litgation(file):
    file_paths = []
    if file == 'Transaction':
        process_to_ajjb_pay()
        newest = max(glob.glob(str(f'{settings.FROM_JUST_AJJB_PAY}\\*.csv')), key=os.path.getmtime)
        file_paths.append(newest)
    elif file == 'Balance Update':
        process_to_ajjb_balanceupdate()
        newest = max(glob.glob(str(f'{settings.FROM_JUST_AJJB_BU}\\*.csv')), key=os.path.getmtime)
        file_paths.append(newest)
    elif file == 'Closure':
        process_to_ajjb_closure()
        newest = max(glob.glob(str(f'{settings.FROM_JUST_AJJB_CLOSURE}\\*.csv')), key=os.path.getmtime)
        file_paths.append(newest)
    else:
        pass
    return file_paths[0]


def export_selected_litigation_file(files):
    file_paths = []
    for file in files:
        if file == 'Transaction':
            try:
                newest = max(glob.glob(str(settings.FROM_JUST_AJJB_TRANSACTION_BATCH)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Balance Update':
            try:
                newest = max(glob.glob(str(settings.FROM_JUST_AJJB_BALANCE_UPDATE_BATCH)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Closure':
            try:
                newest = max(glob.glob(str(settings.FROM_JUST_AJJB_CLOSURE_BATCH)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Placement':
            try:
                newest = max(glob.glob(str(settings.FROM_JUST_AJJB_PLACEMENT_BATCH)), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        else:
            pass
    return file_paths

def process_litigation_file(file):
    today = date.today()
    today = str(today)
    today = today.replace('-', '')
    if 'NFU' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        print('here')
        process_ajjb_nfu(file_name, f'YU_NFU{today}')
    elif 'Transaction' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_ajjb_payment(file_name)
    elif 'Adjustment' in file:
        pass
    elif 'Closure' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_ajjb_closures(file_name)
    elif 'Activity' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_ajjb_activity(file_name)
    elif 'Query' in file:
        name = os.path.basename(file)
        file_name = name.replace('.csv', '')
        process_ajjb_query(file_name)
    else:
        pass


def process_selected_litigation(files):
    file_paths = []
    for file in files:
        if file == 'NFU':
            try:
                print('here')
                newest = max(glob.glob(str(f'{settings.AJJB_NFU_Input_Directory}\\Processed\\*.csv')), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Transaction':
            try:
                newest = max(glob.glob(str(f'{settings.AJJB_PAYMENT_Input_Directory}\\Processed\\*.csv')), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Activity':
            try:
                newest = max(glob.glob(str(f'{settings.AJJB_ACTIVITY_Input_Directory}\\Processed\\*.csv')), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Closure':
            try:
                newest = max(glob.glob(str(f'{settings.AJJB_CLOSURE_Input_Directory}\\Processed\\*.csv')), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        elif file == 'Query':
            try:
                newest = max(glob.glob(str(f'{settings.AJJB_QUERY_Input_Directory}\\Processed\\*.csv')), key=os.path.getmtime)
                file_paths.append(newest)
            except ValueError:
                pass
        else:
            pass
    return file_paths





def monday_check_sla_breach(file):
    # Monday SLA for New Business File
    today = datetime.date.today()
    x = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    y = today - datetime.timedelta(days=today.weekday())
    file_date = os.path.getmtime(file)
    date = datetime.datetime.fromtimestamp(file_date)
    date = date.strftime("%Y-%m-%d")
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date = date.date()

    if date == y:
        value = 'No'
    elif date < y:
        value = 'Yes'
    else:
        pass
    return value
