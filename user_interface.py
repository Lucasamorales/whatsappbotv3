
import mysql.connector


MyDB= mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    password='E3UPD3Db',
    database='whatsappbot'
)
MyCursor = MyDB.cursor()
def retrieve_info(phone):
    SQlSentence= "SELECT status,timeStamp From images2  where number = '{0}'"
    MyCursor.execute(SQlSentence.format(str(phone)))
    MyResult = MyCursor.fetchone()[:]
    print(MyResult)

phone_number = input('ingrese el numero de telefono que desea buscar: ')
retrieve_info(phone_number)
