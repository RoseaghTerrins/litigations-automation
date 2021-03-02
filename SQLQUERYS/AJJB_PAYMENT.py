import pyodbc


def process_ajjb_payment(incoming_file):
    """This function processes the payment file which comes form the litigator AJJB"""

    cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server= Just-Win10VM\SQLEXPRESS;"
                "Database=RM;"
                "Trusted_Connection=yes;")

    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    cursor.execute(f'''select *
                  into #Transaction
                  FROM  rm_files.dbo.{incoming_file}
                    ''')

    cnxn.commit()

    cursor.execute(f'''Execute AJJB_PAYMENT''')