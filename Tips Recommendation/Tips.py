
import requests
from bs4 import BeautifulSoup
import random
import tkinter as tk
from tkinter import messagebox
def datastructres():
    url = "https://www.interviewbit.com/data-structure-interview-questions/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    division = soup.find(id='freshers')
    QAS = division.findAll('section')
    index = random.randrange(0, len(QAS))
    str=''
    for i in QAS[index].stripped_strings:
        str+=i
    return str


def basics():
    url = "https://www.interviewbit.com/computer-science-interview-questions/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    division = soup.find(id='freshers')
    division2=soup.find(id="experienced")
    # print(division)
    QAS1 = division.findAll('section')
    QAS2= division2.findAll('section')
    QAS=QAS1+QAS2
    index = random.randrange(0, len(QAS))
    str=''
    for i in QAS[index].stripped_strings:
        str+=i
    return str

def OOPs():
    url = "https://www.interviewbit.com/oops-interview-questions/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    division = soup.find(id='basic-oops-interview-questions')
    division2=soup.find(id="advanced-oops-interview-questions")
    # print(division)
    QAS1 = division.findAll('section')
    QAS2= division2.findAll('section')
    QAS=QAS1+QAS2
    index = random.randrange(0, len(QAS))
    str=''
    for i in QAS[index].stripped_strings:
        str+=i
    return str


def messageBox(string):
    window = tk.Tk()
    window.withdraw()  # Hide the main window
    window.config(bg='#5FB691')
    res = messagebox.askquestion('TIP OF THE DAY', string)
    if res == 'yes':
        display()
    elif res == 'no':
        window.quit()




def display():
    num = random.randrange(1, 4)
    match num:
        case 1:
            string = datastructres()
            messageBox(string)

        case 2:
            string = OOPs()
            messageBox(string)

        case 3:
            string = basics()
            messageBox(string)



if __name__=="__main__":

    display()