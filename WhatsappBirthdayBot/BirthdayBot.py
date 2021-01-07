import datetime 
import json 
from selenium import webdriver 
import time 

def GetBirthdayWishMessage(name): 
    return "Happy Birthday " + name.split(" ")[0] + "!!"

def GetJsonData(file, personName, personBirthMonth, personBirthDay, currentMonth, currentDay): 
    contactsInfo = json.load(file) 
    contactsList = contactsInfo["Contacts"]
    greetingList =[]  
    for element in contactsList: 
        if(element[personBirthMonth]== currentMonth and element[personBirthDay]== currentDay): 
           greetingList.append(element[personName]) 
    return greetingList 

def GetGreetingNameList(birthdayJsonFile):
    dataFile = open(birthdayJsonFile, "r") 
    try:
        currentDate = datetime.datetime.now() 
        currentGreetingList = GetJsonData(dataFile, "name", "birth_month", "birth_date", 
                                      str(currentDate.month), str(currentDate.day)) 
    except json.decoder.JSONDecodeError: 
        print(ex)
    return currentGreetingList

def GetBrowserConfiguration(configurationJsonFile):
    dataFile = open(configurationJsonFile, "r") 
    try:
        configuration = json.load(dataFile)
        browserConfiguration = configuration["BrowserConfiguration"]
    except json.decoder.JSONDecodeError: 
        print(ex)
    return browserConfiguration["FirefoxProfilePath"], browserConfiguration["DriverPath"]

def GetWebAppConfiguration(configurationJsonFile):
    dataFile = open(configurationJsonFile, "r") 
    try:
        configuration = json.load(dataFile)
        webAppConfiguration = configuration["WebAppInformation"]
    except json.decoder.JSONDecodeError: 
        print(ex)
    return webAppConfiguration["TextBox"], webAppConfiguration["MessageContent"], webAppConfiguration["SendButton"]

def GetFirefoxDriver(firefoxProfilePath, driverPath):
    firefoxopt = webdriver.FirefoxProfile(profilePath) 
    driver = webdriver.Firefox(executable_path = driverPath,  
                               firefox_profile = firefoxopt) 
    return driver

def OpenWebWhatsApp(currentDriver):
    currentDriver.get("https://web.whatsapp.com/")
    print("Loading Web WhatsApp!")
    time.sleep(25)

def GetContactConversationButton(currentDriver, personName):
    try: 
        contactConversationButton = currentDriver.find_element_by_xpath('//span[@title ="{}"]'.format(personName)) 
    except Exception as ex: 
        print(ex)
    return contactConversationButton

def ClickOnTextBox(textBoxName):
    print("Clicking the Text Box")
    textBox = driver.find_element_by_class_name(textBoxName) 
    time.sleep(1) 
    textBox.click()

def WriteGreetingOnTextBox(textBoxName, textBoxContentName, personName):
    print("Writing Whishing message for {}".format(personName))
    textBox = driver.find_element_by_class_name(textBoxName) 
    textBoxContent = textBox.find_element_by_class_name(textBoxContentName)
    time.sleep(1)
    textBoxContent.send_keys(GetBirthdayWishMessage(personName)) 

def SendGreetingMessage(sendButtonName):
    eleSND = driver.find_element_by_class_name(sendButtonName) 
    # eleSND.click()

print("Script Running") 

currentGreetingList = GetGreetingNameList("ContactsBirthdayGreetingInfo.json")
profilePath, driverPath = GetBrowserConfiguration("configuration.json")
textBoxClassName, messageTextClassName, sendButtonClassName = GetWebAppConfiguration("configuration.json")
driver = GetFirefoxDriver(profilePath, driverPath) 
OpenWebWhatsApp(driver)

for person in currentGreetingList: 
    contactConverButton = GetContactConversationButton(currentDriver = driver, 
                                                       personName=person)
    if contactConverButton is not None:
        contactConverButton.click()
    else:
        continue
    ClickOnTextBox(textBoxClassName)
    WriteGreetingOnTextBox(textBoxClassName, messageTextClassName, person)
    SendGreetingMessage(sendButtonClassName)