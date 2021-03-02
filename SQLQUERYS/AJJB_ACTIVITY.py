import pyodbc


def process_ajjb_activity(incoming_file):
    """This fucntion processes the activity file which comes form the litigator AJJB"""

    cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server= Just-Win10VM\SQLEXPRESS;"
                "Database=RM;"
                "Trusted_Connection=yes;")

    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    cursor.execute(f'''select *
                    into #activity
                    from rm_files.[dbo].{incoming_file}''')

    cnxn.commit()

    cursor.execute(f'''Execute AJJB_ACTIVITY''')



