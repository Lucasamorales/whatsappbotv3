import mysql.connector

MyDB= mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    password='E3UPD3Db',
    database='whatsappbot'
)

MyCursor = MyDB.cursor()

MyCursor.execute("CREATE TABLE IF NOT EXISTS images(id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, photo LONGBLOB NOT NULL, number LONGTEXT,status LONGTEXT,timeStamp LONGTEXT)")
#insertar imagenes en la base de datos como un BLOB
def InsertBlob(FilePath):
    with open (FilePath,'rb') as File:
        BinaryData = File.read()
    SQLStatement = "INSERT INTO images (photo) VALUES (%s)"
    MyCursor.execute(SQLStatement, (BinaryData, ))
    MyDB.commit()
#traer una imagen de tipo .jpg desde la base de datos a una carpeta
def RetrieveBlob(ID):
    SQLStatement2 = "SELECT * FROM images WHERE id = '{0}'"
    MyCursor.execute(SQLStatement2.format(str(ID)))
    MyResult = MyCursor.fetchone()[1]
    StoreFilepath = "image_outputs/img{0}.jpg".format(str(ID))
    print(MyResult)
    with open(StoreFilepath, 'wb') as File:
        File.write(MyResult)
        File.close()

# menu para hacer funcionar el codigo 
#print("1. insert image\n2. Read Image")
#MenuInput = input()
#if int(MenuInput) ==1:
 #   UserFilePath = input("Enter File Path:")
  #  InsertBlob(UserFilePath)
#elif int(MenuInput) ==2:
 #   UserIDChoice = input ("Enter ID:")
  #  RetrieveBlob(UserIDChoice)




