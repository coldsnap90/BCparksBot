#program is a bot which auto books camp site for you when you allocate user defined variables
#also uses various python libraries including speech recognition to beat googles anti-bot software
from time import sleep
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver import firefox
from selenium.webdriver.common import action_chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import speech_recognition as SR
import urllib
import urllib.request
import pydub
import ffmpy
import os
import selectors

browser = webdriver.Firefox()
browser.maximize_window()
action = ActionChains(browser)
recog = SR.Recognizer()  
urllib.request.urlcleanup()

#error message  
def exceptPrint():
    print('could not be located')
 
#auto enter text you want at a speed a human could
def typeSpeed(element: WebElement,text:str):

    delay = 0.2
    for char in text:
        element.send_keys(char)
        sleep(delay)


#looks for captcha iframe 
def captchaChecker(check):
    print('captcha check')
    browser.implicitly_wait(3)
    try:
       browser.find_element(By.TAG_NAME,'iframe')
       wait(browser,10).until(EC.presence_of_element_located((By.TAG_NAME,'iframe')))
       return True
       
    except:
        return False
    
#defeats captcha by listening to the sound saving it and manipulating the sound to text modules to
#type in the soubnd
def captchaCrush():
    browser.implicitly_wait(3)
    frame=[]
    
    print('CAPTCHA CRUSH')
    frame = browser.find_elements(By.TAG_NAME,'iframe')
    browser.implicitly_wait(5)
    wait(browser,10).until(EC.frame_to_be_available_and_switch_to_it((frame[2])))
    print('frame found')
    itemX = browser.find_element(By.ID,'recaptcha-audio-button')
    clicked = wait(browser,10).until(EC.presence_of_element_located((By.ID,'recaptcha-audio-button'))).click()
    print(clicked,' 1 ')
    itemX.click()
    browser.implicitly_wait(4)
    print('Part 2')
    play = browser.find_element(By.XPATH,'/html/body/div/div/div[7]/a').get_attribute('href')
    wait(browser,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div[7]/a')))
    urllib.request.urlretrieve(play,'audio.mp3')
    os.path.join('audio.mp3')
    path_wav = os.path.join('audio.wav')
    sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\audio.mp3")
    sound.export(path_wav,format='wav')
    sample_sound = SR.AudioFile(path_wav)
    
    #enters the recorded sound translated to text
    with sample_sound as source:
        audio = recog.record(source)
        key = recog.recognize_google(audio)
        print('speech: '+key)
    print('Waiting for input.....')
   
    try:
        words = browser.find_element(By.CSS_SELECTOR,'#audio-response')
        wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#audio-response')))
        typeSpeed(words,key)
        print('Verifying....')
        
    
    except:print('Fail to verify')
    #clicks enter captcha text after its verified
    enter = browser.find_element(By.CSS_SELECTOR,'#recaptcha-verify-button')
    wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#recaptcha-verify-button'))).click()
    browser.switch_to.default_content()
    
#enters billing info into payment processor
def creditDetails():
    browser.implicitly_wait(3)
    name = ''
    number = ''
    verification = ''
    billingAddress = ''
    province = ''
    city = ''
    postal = ''
    
    #finds name input and inputs name
    cardName = browser.find_element(By.CSS_SELECTOR,'#txtCreditCardName')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#txtCreditCardName')))
    typeSpeed(cardName,name)
    browser.implicitly_wait(3)
    
    #finds element and inputs card type
    cardType = browser.find_element(By.CSS_SELECTOR,'#ddlCardType')
    wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#ddlCardType > option:nth-child(4)'))).click()
    
    #finds element and inputs cardtype
    cardNumber = browser.find_element(By.CSS_SELECTOR,'#txtCreditCardNumber')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#txtCreditCardNumber')))
    typeSpeed(cardNumber,number)
    browser.implicitly_wait(3)
    
    #finds element for expiry month and inputs
    expiryMonth = browser.find_element(By.CSS_SELECTOR,'#ddlExpMonth')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ddlExpMonth')))
    browser.find_element(By.CSS_SELECTOR,'#ddlExpMonth > option:nth-child(3)').click()
    browser.implicitly_wait(3)
    
   #finds element for expiry year and inputs
    expiryYear = browser.find_element(By.CSS_SELECTOR,'#ddlExpYear')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ddlExpYear')))
    browser.find_element(By.CSS_SELECTOR,'#ddlExpYear > option:nth-child(3)').click()
    browser.implicitly_wait(3)
    
    #finds element for verification number for card
    verCode = browser.find_element(By.CSS_SELECTOR,'#txtCreditCardVerificationCode')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#txtCreditCardVerificationCode')))
    typeSpeed(verCode,verification)
    browser.implicitly_wait(3)
    

    #finds element for billing address and inputs
    billing = browser.find_element(By.CSS_SELECTOR,'#txtBillingAddress1')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#txtBillingAddress1')))
    typeSpeed(billing,billingAddress)
    browser.implicitly_wait(3)
   
    #finds element for city and inputs
    billingCity = browser.find_element(By.CSS_SELECTOR,'#txtBillingCity')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#txtBillingCity')))
    typeSpeed(billingCity,city)
    browser.implicitly_wait(3)
    
    #finds element for bill province and inputs
    billingProvince = browser.find_element(By.CSS_SELECTOR,'#txtBillingState')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#txtBillingState')))
    typeSpeed(billingProvince,province)
    browser.implicitly_wait(3)
    
    #finds element for postal code and inputs
    billingPostal = browser.find_element(By.CSS_SELECTOR,'#txtBillingZip')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#txtBillingZip')))
    typeSpeed(billingPostal,postal)
   
    #complete print message
    print('** BOOKING COMPLETE **')
    
#gets bcparks site
web = browser.get('https://www.discovercamping.ca/bccweb/')
browser.implicitly_wait(3)

#finds login into user account account
browser.find_element(By.CSS_SELECTOR,'#aLogin')
wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#aLogin'))).click()

#enter email and password for user account
email = ''
password = ''
emailLogin = browser.find_element(By.XPATH,'//*[@id="txtUserName"]')
wait(browser,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="txtUserName"]')))
wait(browser,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="txtUserName"]')))
typeSpeed(emailLogin,email)
browser.implicitly_wait(3)

#finds element for passwork and inputs
pLogin = browser.find_element(By.ID,'txtPassword')
wait(browser,10).until(EC.presence_of_element_located((By.ID,'txtPassword')))
typeSpeed(pLogin,password)
#finds button to sign in an clicks
signIn = browser.find_element(By.CSS_SELECTOR,'#divOnlyLogin')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#divOnlyLogin')))
signIn.click()
browser.implicitly_wait(3)

check = bool
if captchaChecker(check) == True: #captcha's are annoying, this checks for the captcha
    print('** CAPTCHA PRESENT **')
    captchaCrush()

browser.refresh()
browser.implicitly_wait(3)
siteEntryText = '' #selection for which campsite you want to stay
siteEntry = browser.find_element(By.ID,'txtSearchparkautocomplete')
siteEntryLoader = wait(browser,10).until(EC.presence_of_element_located((By.ID,'txtSearchparkautocomplete')))
typeSpeed(siteEntry,siteEntryText) #enters site chosen

#clicks on campsite from the dropdown menu
siteEntryMenu = browser.find_element(By.CLASS_NAME,'Park-icon')
siteEntryMenuLoader = wait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'Park-icon')))
siteEntryMenu.click() #clicks park chosen
browser.implicitly_wait(3)

#enters arrival date in the menu
siteEntryDate = browser.find_element(By.ID,'mainContent_txtArrivalDate')
siteEntryDateLoader = wait(browser,10).until(EC.presence_of_element_located((By.ID,'mainContent_txtArrivalDate')))
siteEntryDate.click()
browser.implicitly_wait(3)

#month and day of your trip
month = ''
day = ''
siteEntryMonthText=[]
flag = True
#keeps clicking the arrow for the month you want till it appears
while flag == True:
    siteEntryMonth = browser.find_element(By.CSS_SELECTOR,'.ui-datepicker-month')
    siteEntryMonthText = browser.find_elements(By.CSS_SELECTOR,'.ui-datepicker-month')
    siteEntryMonthLoader = wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.ui-datepicker-month')))
    siteEntryMonthNext = browser.find_element(By.CSS_SELECTOR,'.ui-datepicker-next[data-original-title="Next Month"]')
    for text in siteEntryMonthText:
        print(text.text)
        if(text.text == month): #loops through month text
            text.click()
            flag = False
            break
        if(text.text != month):
            siteEntryMonthNext.click()

flag = True
siteEntryDateText=[]
#scans the days until it finds the day enteredn much like the month
while flag == True :
    siteEntryDateText = browser.find_elements(By.CSS_SELECTOR,'.ui-datepicker-calendar > tbody > tr > td')
    wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.ui-datepicker-calendar > tbody > tr > td ')))
    for date in siteEntryDateText:
        if(date.text == day):
            print(date.text)
            date.click()
            flag = False
            break

#drop down menu for how many nights you want
stay = browser.find_elements(By.ID,'ddlHomeNights') 
stayFound = wait(browser,10.).until(EC.presence_of_element_located((By.ID,'ddlHomeNights')))
stayNights = browser.find_element(By.CSS_SELECTOR,'#ddlHomeNights > option:nth-child(3)').click()

browser.implicitly_wait(4)

#type of trip
type = browser.find_element(By.CSS_SELECTOR,'#ddl_homeCategories > option:nth-child(2)')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ddl_homeCategories > option:nth-child(2)')))
type.click()

browser.implicitly_wait(4)
search = browser.find_element(By.CSS_SELECTOR,'.viewsearch > div:nth-child(2) > a:nth-child(1)')
wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.viewsearch > div:nth-child(2) > a:nth-child(1)')))
search.click()
browser.implicitly_wait(3)

#park choice
park = browser.find_element(By.CSS_SELECTOR,'#divParkTitle_104')
wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#divParkTitle_104')))
park.click()

#reserves the site you want
reserveSite = browser.find_element(By.CSS_SELECTOR,'.table_data_box > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.table_data_box > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')))
reserveSite.click()
#reserves the day
browser.implicitly_wait(4)
reserveDate = browser.find_element(By.CSS_SELECTOR,'#td_0_0')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#td_0_0')))
reserveDate.click()

browser.implicitly_wait(4)

#books site
browser.find_element(By.CSS_SELECTOR,'div.modal-body:nth-child(17)')
reserveBook = browser.find_element(By.CSS_SELECTOR,'#mainContent_UnitDetailPopup_bReserveCal')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_UnitDetailPopup_bReserveCal')))
wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainContent_UnitDetailPopup_bReserveCal')))
reserveBook.click()
browser.implicitly_wait(4)

#enters in information for num of people
adultSec = browser.find_element(By.CSS_SELECTOR,'#mainContent_ddlAdults > option:nth-child(3)')  
wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainContent_ddlAdults > option:nth-child(3)')))
adultSec.click()
browser.implicitly_wait(3)
#numbers of vehicles
vehicleCount = browser.find_element(By.CSS_SELECTOR,'#mainContent_ddlVehicles > option:nth-child(4)')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_ddlVehicles > option:nth-child(4)')))
vehicleCount.click()
browser.implicitly_wait(3)
#number of tents
tentCount = browser.find_element(By.CSS_SELECTOR,'#mainContent_ddlSleepingUnitType > option:nth-child(3)')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_ddlSleepingUnitType > option:nth-child(3)')))
tentCount.click()
#vehicle size
vehicleLength = browser.find_element(By.CSS_SELECTOR,'#mainContent_ddlPadLength > option:nth-child(3)')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_ddlPadLength > option:nth-child(3)')))
vehicleLength.click()
browser.implicitly_wait(3)

#reservation holder
person = ''
optionalPerson = browser.find_element(By.CSS_SELECTOR,'#mainContent_txtOptionalOccupant')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_txtOptionalOccupant')))
typeSpeed(optionalPerson,person)
browser.implicitly_wait(3)

#clicks you accept terms
terms = browser.find_element(By.CSS_SELECTOR,'#Lnksalecondition')
wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#Lnksalecondition'))).click()
browser.implicitly_wait(3)

#agree to terms
check = browser.find_element(By.CSS_SELECTOR,'.agree')
wait(browser,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.agree')))
check.click()

browser.implicitly_wait(3)
#reserving your site
reserveUnit = browser.find_element(By.CSS_SELECTOR,'#mainContent_bReserve')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_bReserve')))
reserveUnit.click()
browser.implicitly_wait(3)

#confirm
confirm = browser.find_element(By.CSS_SELECTOR,'#mainContent_chkAgree')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_chkAgree')))
confirm.click()
browser.implicitly_wait(3)

#enter payment
checkout = browser.find_element(By.CSS_SELECTOR,'#mainContent_aCheckOut')
wait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainContent_aCheckOut')))
checkout.click()

#funtion to enter credit card details
creditDetails()