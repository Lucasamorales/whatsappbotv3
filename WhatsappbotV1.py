
from asyncio.windows_events import NULL
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import re 
from unicodedata import normalize
from selenium.webdriver.common.by import By
import mysql.connector
from image_storage import RetrieveBlob

filepath = "Resources/Whatsapp_session.txt"
driver = webdriver
global ID, number
ID=0
number=NULL
#crea una sesion de whatsapp y la mantiene abierta para que el bot actue 
def create_driver_session():
    with open(filepath) as fp:
        for cnt,line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line 


    def new_command_execute(self,command,params=None):
        if command == "newSession":
            return{'succes':0, 'value':None,'sessionId':session_id}
        else:
            return org_command_execute(self,command,params)
    
    org_command_execute = RemoteWebDriver.execute

    new_driver = webdriver.Remote(command_executor=executor_url,desired_capabilities={})
    new_driver.session_id =session_id

    return new_driver

#Crea una base de datos en Mysql y utiiza una funcion para traer las imagenes de la misma
def database(ID: int):
    MyDB= mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    password='E3UPD3Db',
    database='whatsappbot'
)      
    MyCursor = MyDB.cursor()

    MyCursor.execute("CREATE TABLE IF NOT EXISTS images(id INTEGER(45) NOT NULL AUTO_INCREMENT PRIMARY KEY, photo LONGBLOB NOT NULL, number LONGTEXT,status LONGTEXT,timeStamp LONGTEXT)")

    #decodifica las imagenes de la base de datos
    RetrieveBlob(ID) 

#consigue el numero del remitente
def retrieve_number():
    user=driver.find_element(By.CLASS_NAME,'_21nHd')
    user.click()
    user_num=  WebDriverWait(driver, timeout=5).until(lambda driver: driver.find_element(By.CLASS_NAME,'AjtLy._1FXE6._1lF7t').get_attribute("innerHTML"))
    number=str(user_num.replace(" ", ""))
    print(user_num.replace)
    time.sleep(5)
    close_user = driver.find_element(By.CLASS_NAME,'_18eKe')
    time.sleep(2)
    close_user.click()
    time.sleep(0.5)
    return number

#sube el numero de telefono a la base de datos
def upload_number(number:str,ID:int):

    MyDB= mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    password='E3UPD3Db',
    database='whatsappbot'
)      
    MyCursor = MyDB.cursor()
    SQLStatement = "UPDATE images SET number  = %s WHERE id = '{0}'"
    MyCursor.execute(SQLStatement.format(str(ID)), (number, ))
    MyDB.commit()

#sube el estado de la imagen (enviado, entregado y  leido) enviada y la hora a la que se envio a la base de datos 
def upload_status(ID:int,msg_status:str,time_stamp:str):
    MyDB= mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    password='E3UPD3Db',
    database='whatsappbot'
)      
    MyCursor = MyDB.cursor()
    SQLStatement = "UPDATE images SET status = %s,timestamp = %s WHERE id = '{0}'"
    MyCursor.execute(SQLStatement.format(str(ID)), ((msg_status,time_stamp)))
    MyDB.commit()

#busca los chats para contestarles
def search_chats():
    print('searching chats..')
    if len(driver.find_elements(By.CLASS_NAME,"zaKsw"))==0:
        print('open chat')
        message = identify_message()
        if message != None:
            return True 
        

    chats = driver.find_elements(By.CLASS_NAME,'lhggkp7q.ln8gz9je.rx9719la')
    
    for chat in chats:
        print('detecting unread messages')

        chat_messages = chat.find_elements(By.CLASS_NAME,'l7jjieqr.cfzgl7ar.ei5e7seu.h0viaqh7.tpmajp1w.c0uhu3dl.riy2oczp.dsh4tgtl.sy6s5v3r.gz7w46tb.lyutrhe2.qfejxiq4.fewfhwl7.ovhn1urg.ap18qm3b.ikwl5qvt.j90th5db.aumms1qt')

        if len(chat_messages) == 0:
            print('all read')
            continue
        

        element_name= chat.find_elements(By.CLASS_NAME,'ggj6brxn.gfz4du6o.r7fjleex.g0rxnol2.lhj4utae.le5p0ye3.l7jjieqr.i0jNr')
        name = element_name[0].text.upper().strip()

        print('identifing contact')

        with open('Resources/Authorized users.txt',mode='r',encoding='utf-8') as file:
            contacts= [line.rstrip() for line in file]  
            if name not in contacts:
                print('unauthorized contact: ',name)
                continue
        
        print(name,'authorizedfor bot assistance')

        chat.click()
        
        return True
    return False

#normaliza los mensajes 
def Normalize(message :str):
    message = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", message), 0, re.I
    )
    return normalize( 'NFC', message)

#identifica los mensajes recibidos 
def identify_message():
    messages = driver.find_elements(By.CLASS_NAME,'_1-FMR')
    position = len(messages) -1
    message_type = messages[position].get_attribute('class')
    
    if  message_type == '_1-FMR message-out focusable-list-item':
        print("CHAT ATENDIDO")
        return
   
    element_message= messages[position].find_elements(By.CLASS_NAME,'_22Msk')
    message = element_message[0].text.upper().strip()
    print('message recived: ',message)
    return Normalize(message)

#envia una imagen de la base de datos 
def send_img(img: str):
    print("IMG :", img)
    WebDriverWait(driver, timeout= 3).until(lambda driver: driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')).click()
    file_image = WebDriverWait(driver, timeout= 10).until(lambda driver: driver.find_element(By.TAG_NAME,'input'))
    file_image.send_keys(img)
    WebDriverWait(driver, timeout= 10).until(lambda driver: driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div')).click()
    time.sleep(2)
    chatbox = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    chatbox.send_keys('.\n')
    time.sleep(5)

#consigue el estado y la hora de la imagen enviada
def retrieve_status():
    images=driver.find_elements(By.CLASS_NAME,"_1-FMR._3Zpy8.j-md4.message-out.focusable-list-item")
    position= len(images) - 1

    check_box = images[position].find_element(By.CLASS_NAME,'N4ItZ')
    msg_status=check_box.get_attribute('aria-label')
    msg_status=str(msg_status)

    time_stamp= images[position].find_element(By.CLASS_NAME,'l7jjieqr.fewfhwl7').text

    return msg_status,time_stamp

#prepara una respuesta dependiendo del remitente
def prepare_answer(message : str):
    print('preparing answer..')
    if message.__contains__('QUIEN CREO ESTE BOT'):
        response = "Fui creado por Lucas Morales \n"
    elif message.__contains__('QUE PROGRAMA USARON PARA CREARTE'):
        
        response ="me programaron utilizando python y la libreria de selenium\n"
    elif message.__contains__('QUE PODES HACER'):
        
        text1= open('Resources/bot_answers.txt', mode='r',encoding='utf-8')
        response = text1.read() 
        text1.close()
    elif message.__contains__("GRACIAS"):
        
        response = "ha sido un placer ayudarte\n" 
       
    else:
        response = "Hola soy un bot de whatsapp, preguntame que podes hacer \n"

    return response

#elije que tipo de mensaje enviar
def process_message(message: str):
    if message.__contains__('IMAGEN'):
        global ID
        
        ID+=1
        database(ID)
        send_img(f"image_outputs/img{ID}.jpg")
        retrieve_status()
        return ID
    else:
        chatbox = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
        response = prepare_answer(message)
        chatbox.send_keys(response)

#funcion principal   
def whatsapp_bot_init():
    global driver 
    driver = create_driver_session() 
    
    while True:
        if not search_chats():
            time.sleep(5)
            continue
        message = identify_message() 
        if number == NULL:   
            number = retrieve_number()
            continue
        
        if message == None: 
            continue

        process_message(message)
        if ID!=0 and number is not NULL:
            
            upload_number(number,ID) 
            
            msg_status,time_stamp=retrieve_status()

            upload_status(ID,msg_status,time_stamp)   
            continue
    
if __name__ == '__main__': 
    whatsapp_bot_init()

