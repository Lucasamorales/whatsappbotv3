from requests import session
from selenium import webdriver

driver = webdriver.Chrome( executable_path='drivers/chromedriver.exe')
executor_url = driver.command_executor._url
session_id = driver.session_id
driver.get('https://web.whatsapp.com')

print('Session ID ' + session_id)
print('Executor_URL: ' + executor_url) 

with open('Resources/Whatsapp_Session.txt', mode="w") as text_file:
    text_file.write("{}\n".format(executor_url))
    text_file.write(session_id)

#crea una sesion para mantener el bot funcionando 
def Create_driver_session(session_id,excecutor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    org_command_excecute = RemoteWebDriver.execute

    def new_command_execute(self,command,params=None):
        if command == "newSession":
            return { 'succes':0, 'value':None,'sessionId': session_id}
        else:
            return org_command_excecute(self, command, params)
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={}) 
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_excecute

    return new_driver

driver2 = Create_driver_session(session_id,executor_url)
print("Driver 2 URL" + driver2.current_url)


