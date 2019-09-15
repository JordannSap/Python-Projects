from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Data_proccess as dt
import os
from getpass import getpass
from selenium.common import exceptions as ex

clear = lambda: os.system('cls') #to clear cmd








def click_rare_message_box(msg): # This messagebox appears rarely
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '(//textarea[@name="message_body"])')))
    element.send_keys(msg)

def click_send_rare(): # In case rare msgbox appears
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '(//button[@type="submit"])')))
    element.click()


def click_usual_msg_box(msg): #The most common msgbox
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '(//div[@role="combobox"])[1]')))
    element.send_keys(msg)
    return element


def click_profile_name(): #Clicks the first profile
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '(//div[@class="fsl fwb fcb"])')))
    element.click()


def click_all_messages(): #Clicks messages tab
    element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '(//div[@class="_4kny"])[4]')))
    element.click()


def click_my_profile():
    element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "_2s25")))
    element.click()


def click_friends_tab():
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '(//a[@data-tab-key="friends"])')))
    element.click()


def friends_search(name):
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'inputtext')))
    element.send_keys(name)


def click_msg_in_profile(): #Click the send msg button in a specific profile
    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '(//a[@class ="_42ft _4jy0 _4jy4 _517h _51sy"])')))
    element.click()

def close_chat():
    print('-----Wait...-----')
    element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@class ="_7jbw _4vu4 button"]')))
    element.click()

def home_page():
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "_19eb")))
    element.click()


#Iterator used to find more than one elements with the same class
#Condition is used so that the driver will not wait long after finding the first element as probably the element that
#causes a long wait doesnt exist

def find_last_msg_sent(i):
    if i == 1:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '(//div[@class="_1ijj"])[%s]' % i)))
    else:
        element = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, '(//div[@class="_1ijj"])[%s]' % i)))

    return element.get_attribute("innerHTML")

def find_time_sent(i):
    if i == 1:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '(//abbr[@class="timestamp"])[%s]' % i)))
    else:
        element = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, '(//abbr[@class="timestamp"])[%s]' % i)))

    return element.get_attribute("innerHTML")

def find_sent_msg_box(i): #Box that contains a sent or received message
    if i == 1:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '(//span[@class="_5yl5"])[%s]' % i)))
    else:
        element = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, '(//span[@class="_5yl5"])[%s]' % i)))

    return element.get_attribute('innerHTML')

def click_send_button(): #Not used but just in case Keys.ENTER doesnt work
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '(//a[@class="_6gb _6wm4 _6987"])')))
    element.click()




def send_msg(msg):
    element = click_usual_msg_box(msg)
    sleep(0.1)
    #click_send_button() if enter doesnt work
    element.send_keys(Keys.ENTER)
    sleep(0.1)



def search_friends(name):
    click_my_profile()
    click_friends_tab()
    friends_search(name)
    try:
        click_profile_name()
        print('-----Found in friends-----')
        print('-----Sending message-----')

        sleep(2)
        attempts = 0
        while attempts < 2:
            try:
                click_msg_in_profile()
                attempts = 3
            except:
                attempts += 1
    except:
        print('-----Not found in friends list-----')
        return 0



def write_msg(msg):
    try:
        sleep(0.1)
        click_rare_message_box(msg)
        sleep(0.2)
        click_send_rare()
        print('-----Successfully sent-----')

    except:
        sleep(0.1)
        send_msg(msg)



def find_name(name):
    if name == '':
        return 0
    if name in names:
        for i in range(0,len(names)):
            if name == names[i]:
                elements[i].click()
                return True
    else:
        return False

def send():
    get_last_names()
    name = input('-----name: ')
    msg = input('-----message: ')
    if name != '' and msg != '':
        found = find_name(name)
        if found:
            print('-----found-----')
            send_msg(msg)
            print('-----Successfully sent-----')
            close_chat()

        elif found != 0:
            print('-----Not found in recent messages-----')
            print('\n-----Searching in friends list-----')
            if search_friends(name) != 0:
                write_msg(msg)
                print('-----Successfully sent-----')
                close_chat()
    else:
        print('Type name and message')

    home_page()


def correct_chat_log():
    for i in range(1, 13):
        try:

            show = find_sent_msg_box(i)
            if 'img' in show:
                show = dt.correct_emoji(show)

            else:
                show = show.replace('<span>', '')
                show = show.replace('</span>', "")
            print(show)
        except:
            break


def chat_log():
    get_last_names()
    name = input('-----name: ')
    found = find_name(name)
    if found:
        correct_chat_log()
        close_chat()

    elif found != 0:
        print('-----Not found in recent messages-----')
        print('\n-----Searching in friends list-----')
        found = search_friends(name)
        if found != 0:
            correct_chat_log()
            close_chat()

    home_page()


def whole_chat_log():
    print('\n-----chat log-----')
    get_last_names()
    print('-----The list of your last contacts-----\n',names)
    for i in range(1, len(names)):
        print('\n')
        msg = find_last_msg_sent(i)
        msg_time = find_time_sent(i)
        dt.combine_all(names[i-1], msg, msg_time)
    print('-----Wait...-----')
    home_page()


def get_last_names():
    click_all_messages()
    unread = ''
    del names[:],elements[:]
    for i in range(1, 12):
        try:
            if i == 1:
                name_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '(//div[contains(@class, "author")])[%s]' % i))) #class changes after click
            else:
                name_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '(//div[contains(@class, "author")])[%s]' % i)))  # class changes after click

            name = name_element.get_attribute("innerHTML")
            name, not_seen = dt.correct_msg_name(name)
            names.append(name)
            if not_seen:
                unread += name + '\n'
            elements.append(name_element)
        except ex.TimeoutException:
            pass
    return unread

def check_unread():
    unread = get_last_names()
    if len(unread) == 0:
        print('You have no unread messages')
    else:
        print('You have unread messages from:\n' + unread)
    home_page()


# These lists will be used to save names and elements
names = []
elements = []

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(chrome_options=options)


def start():
    driver.get('https://facebook.com')
    print('Loading.....')
    sleep(1)
    email = input('Email: ')
    show = input("Show password? (Y/N)")
    if show == 'Y':
        password = input('Password: ')
    else:
        password = getpass('Password: ')

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
    element.send_keys(email)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'pass')))
    element.send_keys(password)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginbutton")))
    element.click()
    try:
        home_page()
        print('\n-----login successful-----')
    except:
        print('-----Wrong password or username-----')
        start()
start()






print('\n\n')
def commands():
    print('send()              send message\nexit()              exit code\nclear()             clear console')
    print('whole_chat_log()    list of last names and messages\nchat_log()          specific name chat log')
    print('commands()          show all commands\ncheck_unread()      check if you have unread messages')
commands()


while True:
    print('\n')
    command = input('-----enter command  ')
    try:
        exec(command)
    except NameError:
        print('Command not recognised')


