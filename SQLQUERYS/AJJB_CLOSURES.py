import pyodbc


def process_ajjb_closures(incoming_file):
    """This function processes the closures file which comes from the litigator AJJB"""

    cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server= Just-Win10VM\SQLEXPRESS;"
                "Database=RM;"
                "Trusted_Connection=yes;")

    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    cursor.execute(f'''select *
                    into ##Closures
                    FROM RM_FILES.DBO.{incoming_file}
                    ''')

    cnxn.commit()

    cursor.execute(f'''Execute AJJB_CLOSURE''')


# process_ajjb_closures('JUST_Closures_17022021')