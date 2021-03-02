import pyodbc
import pandas as pd


def process_ajjb_nfu(incoming_file, outgoing_file):
    """This function processes the NFU file which comes form the litigator AJJB"""

    cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server= Just-Win10VM\SQLEXPRESS;"
                "Database=RM;"
                "Trusted_Connection=yes;")

    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    cursor.execute(f'''select *
                    into rm_files.dbo.[AJJB_NFU_TEMP]
                    FROM RM_FILES.DBO.{incoming_file}
                    ''')

    cnxn.commit()

    cursor.execute(f'''Execute AJJB_NFU''')

    cnxn.commit()

    cursor.execute(f'''	
    select *
    into rm_files.dbo.[{outgoing_file}]
    from rm_files.dbo.YU_NFU_TEMP cl''')

    cnxn.commit()

    cursor.execute('''drop table RM_FILES.dbo.[AJJB_NFU_TEMP]''')

    cnxn.commit()

    cursor.execute('''drop table RM_FILES.dbo.YU_NFU_TEMP''')

    cnxn.commit()


    data = pd.read_sql(f"SELECT * FROM RM_Files.[dbo].[{outgoing_file}]", cnxn)


    data.to_csv(
        f'C:\\Users\\justvm\\Documents\\RM_Litigations_Files\\Client\\YU\\From_Just\\NFU_Files\\{outgoing_file}.csv',
        index=False)
