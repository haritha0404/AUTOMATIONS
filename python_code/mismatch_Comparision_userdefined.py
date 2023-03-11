import pyodbc
import xlsxwriter
from xlsxwriter import Workbook
#server1 = 'ebitg-hpi-adbsvr-abcr.database.windows.net'
#database1 = 'ebitg-hpi-adb-abcr'
#username1 = 'srvc_rapid_radical_reader'
#password1 = '{Admin@007}'   
driver1= '{ODBC Driver 17 for SQL Server}'
print("Enter the server1")
server1 = input()
print("Enter the database1")
database1 =  input()
print("Enter the username1")
username1 = input()
print("Enter the password1")
password1 = input()
print("Enter the server2")
server2 = input()
print("Enter the database2")
database2 = input()
print("Enter the username2")
username2 = input()
print("Enter the password2")
password2 = input()
print("Enter the type (schema/table/view)")
table_or_schema = input()
print("Enter the schema ")
schema = input()
print("Enter the table of a list separated by space ")
table = input()
 conn1 = pyodbc.connect('DRIVER='+driver1+
                      ';SERVER='+server1+
                      ';PORT=1433;DATABASE='+database1+
                      ';UID='+username1+
                      ';PWD='password1+
                      )
  conn2 = pyodbc.connect('DRIVER='+driver1+
                      ';SERVER='+server2+
                      ';PORT=1433;DATABASE='+database2+
                      ';UID='+username2+
                      ';PWD='password2+
                      )

print(conn1)
print(conn2)
user_list = table.split()
import pandas as pd
import numpy as np
# print list
print('list: ', user_list)
# pass each item to query
writer= pd.ExcelWriter('D://mismatch_excel.xlsx') 
for i in range(len(user_list)):
    print('list: ', user_list[i])
    if (table_or_schema == 'schema'):
        sql_query1 = pd.read_sql_query('''select a.TABLE_NAME, b.COLUMN_NAME,b.DATA_TYPE,b.CHARACTER_MAXIMUM_LENGTH from INFORMATION_SCHEMA.TABLES a inner join INFORMATION_SCHEMA.COLUMNS b on  a.TABLE_NAME = b.TABLE_NAME where b.TABLE_SCHEMA like '%'''+schema+'''%' and a.TABLE_NAME like '%'''+user_list[i]+'''%' order by b.COLUMN_NAME asc''',conn1) # here, the 'conn' is the variable that contains your database connection information from step 2
        sql_query2 = pd.read_sql_query('''select a.TABLE_NAME, b.COLUMN_NAME,b.DATA_TYPE,b.CHARACTER_MAXIMUM_LENGTH from INFORMATION_SCHEMA.TABLES a inner join INFORMATION_SCHEMA.COLUMNS b on  a.TABLE_NAME = b.TABLE_NAME where b.TABLE_SCHEMA like '%'''+schema+'''%'  and a.TABLE_NAME like '%'''+user_list[i]+'''%' order by b.COLUMN_NAME asc''',conn2) # here, the 'conn' is the variable that contains your database connection information from step 2
        df1 = pd.DataFrame(sql_query1)
        print(df1)
        df2 = pd.DataFrame(sql_query2)
        print(df2)
        ##compare both the files
        df3 = pd.merge(df1, df2, on=['TABLE_NAME','COLUMN_NAME','DATA_TYPE','CHARACTER_MAXIMUM_LENGTH'], how='outer', indicator=True)
        print(df3)
        # selecting rows based on condition
        rslt_df = df3[df3['_merge'] != 'both']
        rslt_df['server'] = np.where(rslt_df['_merge'] == 'left_only', server1, server2)
        print(rslt_df)
        # Write DataFrame to Excel file with sheet name
        sheetname = user_list[i]
        
        rslt_df.to_excel(writer, sheet_name=sheetname[0:30],index=False)
        
        
writer.close()
