import pyodbc
import pandas as pd
import settings
import shutil


def process_ajjb_query(file):
    """This function processes the query file which comes form the litigator AJJB"""

    cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server= Just-Win10VM\SQLEXPRESS;"
                "Database=RM;"
                "Trusted_Connection=yes;")

    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    cursor.execute(f'''	
           insert into rm.dbo.lit_queries
            select '{file}' as [file] 
    	    , * 
    	    , cast(getdate() as date) dtstamp
            from rm_files.dbo.[{file}]''')

    cnxn.commit()

    DF = pd.read_sql(f'''Select * from RM_FILES.dbo.[{file}]''', cnxn)
    DF.columns = ['DCA Ref', 'Account Number', 'Account Name', 'Query Type', 'Query Details', 'Attachment']
    DF['YU Energy Comments'] = ''

    settings.DCA_TOJUST_QUERY_DATABASE = settings.DCA_TOJUST_QUERY_DATABASE.strip('*')

    DF.to_csv(settings.DCA_TOJUST_QUERY_DATABASE + f'{file}.csv')

    shutil.copyfile(settings.DCA_TOJUST_QUERY_DATABASE + f'{file}.csv', settings.YU_QUERY_DIRECTORY + f'\\{file}.csv')
    shutil.copyfile(settings.FIRST_LOCATE_Query_Directory + f'\\Supplementary_Docs_Zip\\{file}.zip',
                    settings.YU_QUERY_DIRECTORY + f'\\{file}.zip')
    shutil.move(settings.FIRST_LOCATE_Query_Directory + '\\Supplementary_Docs_Zip\\' + f'{file}.zip',
                settings.DCA_TOJUST_QUERY_DATABASE + f'{file}.zip')
