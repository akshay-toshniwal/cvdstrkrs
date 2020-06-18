from flask import Flask, render_template
import speech_recognition as sr
import pyttsx3
import re
from googletrans import Translator
from playsound import playsound
import csv
from csv import writer
import os
import sys
from werkzeug.utils import redirect
import recognizer

ans = []
fans = []


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def finalAnswer(result):
    fans.append(result)


def acceptnoofppl(flag1):
    if flag1 == 0:
        playsound('mignop.wav')

    MyText = recognizer.recognizekar()
    translator = Translator()
    MyText1 = (translator.translate(MyText, src='hi'))
    x = MyText1.text.upper()
    print("Did you say " + x)
    numbers = []
    flag = 0
    for word in x.split():
        if word.isdigit():
            numbers.append(int(word))
            flag = 1
    if flag == 1:
        age = numbers[0]
        finalAnswer(age)
    else:
        acceptnoofppl(0)




def playAccept(audiofile):
    playsound(audiofile)
    readAudio(audiofile)


def readText(inp,audiofile):
    temp = inp
    if len(temp) != 0:
        x1 = temp.split()
        if len(x1) != 0:
            f = open('ctydr.csv')
            csv_f = csv.reader(f)
            city = None
            for column in csv_f:
                for y in x1:
                    y = y.capitalize()
                    if y == column[0]:
                        city = y
                        finalAnswer(city)

            if city == None:
                playsound('migwncty.wav')
                readAudio(audiofile)


        else:
            pass

    else:
        playsound('migwncty.wav')
        readAudio(audiofile)


def readAudio(audiofile):
    x=recognizer.recognizekar()
    print('DID YOOU SAY __ '+x)
    if x== "unknown error occured":
        playAccept(audiofile)
    readText(x,audiofile)




app = Flask(__name__)


@app.route('/')
def main1():

    fnm = ['migsrc.wav', 'migdest.wav']

    playsound('migtitle.wav')
    acceptnoofppl(0)

    for i in range(len(fnm)):
        audiofile = fnm[i]
        print(audiofile)
        playAccept(audiofile)

    print(fans)
    append_list_as_row("migdb.csv", fans)
    playsound("migvot.wav")
    print("!!!After approval from government side you will be notified by text message!!!")
    return redirect('home1')


"""os.system('main.py')"""


@app.route('/home1')
def main2():
    engine = pyttsx3.init()

    engine.say(
        'As per provided info you want to travel from {fans1} to {fans2} with {fans0} people.'.format(fans1=fans[1],
                                                                                                      fans2=fans[2],
                                                                                                      fans0=fans[0]))

    engine.runAndWait()

    return render_template('home1.html', fans=fans)


if __name__ == '__main__':
    app.run(debug=True)
