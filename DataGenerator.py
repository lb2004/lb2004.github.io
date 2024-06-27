import numpy as np
import pandas as pd
import random
import re
import os
import datetime as dt
from sys import platform

#### Text Generation Libraries ####
import markovify
from faker import Faker
import string
#########################

#### Tkinter Imports ####
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
if platform == 'darwin':
    from tkmacosx import Button
else:
    from tkinter import Button
#########################


class StringInput:

    def __init__(self, prompt, separator):
        assert isinstance(prompt, str) and isinstance(separator, str)
        self.prompt = prompt
        self.separator = separator
        self.input_string = input(prompt)

    def list(self):
        if self.separator != ' ':
            return self.input_string.replace(' ', '').split(self.separator)
        return self.input_string.split(self.separator)

    def length(self):
        return len(self.list())


def input_window():
    def submit_text():
        user_input = text_entry.get("1.0", "end-1c")
        root.quit()
        return user_input

    # Initialize the root window
    root = tk.Tk()
    root.title("Input Window")

    style = ThemedStyle(root)
    style.set_theme("arc")

    # Set the size of the window
    root.geometry("600x400")  # Width x Height

    prompt_label = ttk.Label(root, text="Please enter your input below:", font=("Arial", 14, 'bold'), background='#323232', foreground='#a7adba')
    prompt_label.pack(pady=(20, 10))

    # Create a text entry widget with text wrapping enabled
    text_entry = tk.Text(root, height=20, width=70, wrap=tk.WORD)
    text_entry.pack(padx=10, pady=10)

    # Create a submit button
    submit_button = Button(root, text="Submit", command=submit_text, bg='#272727', fg='#a7adba')
    submit_button.pack(pady=5)

    # Run the main loop to display the window
    root.mainloop()

    root.withdraw()

    return submit_text()

def createint(dlen = 100):
    dist = ''
    while True:
        try:
            dist = input('Choose a Distribution (by number):\n 1. Uniform\n 2. Normal\n 3. Triangular\n 4. Bernoulli\n 5. Exponential\n').replace('.','')
            _ = int(dist)
            break
        except:
            print('Invalid entry.')
    if int(dist) in [1, 3]:
        lb, ub, peak = 0, 0, 0
        while True:
            try:
                lb = int(input('Insert a lower bound: '))
                ub = int(input('Insert an upper bound: '))
                if int(dist) == 3:
                    peak = int(input('Pick a peak between lower and upper bound (inclusive): '))
                    assert peak >= lb and peak <= ub
                break
            except:
                print('Must be a valid integer!')
        if dist == '1':
            return pd.Series(np.random.randint(lb, ub, dlen))
        else:
            return pd.Series(np.round(np.random.triangular(lb, peak, ub, dlen), decimals=0)).astype(int)
    if dist == '2':
        mn, std = 0, 1
        while True:
            try:
                mn = int(input('Insert a mean: '))
                std = int(input('Insert a standard deviation: '))
                break
            except:
                print('Must be a valid integer!')
        return pd.Series(np.round(np.random.normal(mn, std, dlen), decimals = 0)).astype(int)
    if dist == '4':
        prob = 0.5
        while True:
            try:
                prob = float(input('Probability (As percentage): '))/100
                break
            except:
                print('Must be a valid integer!')
        return pd.Series(np.random.binomial(1, prob, dlen))
    if dist == '5':
        scale = 1
        while True:
            try:
                scale = float(input('Scale Factor: '))
                break
            except:
                print('Must be a valid integer!')
        return pd.Series(np.round(np.random.exponential(scale, dlen), decimals = 0)).astype(int)

def createfloat(dlen = 100):
    dist = ''
    while True:
        try:
            dist = input('Choose a Distribution (by number):\n 1. Uniform\n 2. Normal\n 3. Triangular\n 4. Exponential\n').replace('.','')
            _ = int(dist)
            break
        except:
            print('Invalid entry.')
    if int(dist) in [1, 3]:
        lb, ub, peak = 0, 0, 0
        while True:
            try:
                lb = float(input('Insert a lower bound: '))
                ub = float(input('Insert an upper bound: '))
                if int(dist) == 3:
                    peak = float(input('Pick a peak between lower and upper bound (inclusive): '))
                    assert peak >= lb and peak <= ub
                break
            except:
                print('Must be a valid integer!')
        if dist == '1':
            return pd.Series(np.random.uniform(lb, ub, dlen))
        else:
            return pd.Series(np.random.triangular(lb, peak, ub, dlen))
    if dist == '2':
        mn, std = 0, 1
        while True:
            try:
                mn = float(input('Insert a mean: '))
                std = float(input('Insert a standard deviation: '))
                break
            except:
                print('Must be a valid integer!')
        return pd.Series(np.random.normal(mn, std, dlen))
    if dist == '4':
        scale = 1
        while True:
            try:
                scale = float(input('Scale Factor: '))
                break
            except:
                print('Must be a valid integer!')
        return pd.Series(np.random.exponential(scale, dlen))

def createdate(dlen = 100):
    print('Datetime format examples:\
          \n     MM-DD-YYYY\
          \n     D/M/YY\
          \n     YYYY-MM-DD hh:mm:ss.cccc\
          \n Datetimes can be separated by \'-\' or \'/\' for days, months, and years; or by \':\' and \'.\' for hour/minute/second/subsecond.\
          \n Please ensure to separate the day from the time with at minimum a single space.')
    format = ''
    while True:
        format = input('Write datetime format (case sensitive):')
        try:
            format = format.replace('YYYY', '%Y').replace('YY', '%y').replace('MM', '%m').replace('M', '%m')\
                        .replace('DD', '%d').replace('D', '%d').replace('hh', '%H').replace('mm', '%M')\
                        .replace('ss', '%S')
            format = re.sub(r'c+', '%f', format)
            break
        except:
            print('Invalid date format. Please try again.\n')
    sd, ed = '', ''
    while True:
        sd = input('Start Date (formatted): ')
        ed = input('End Date (formatted): ')
        try:
            sd = pd.to_datetime(sd, format = format)
            ed = pd.to_datetime(ed, format = format)
            break
        except:
            print('Date improperly inputted.')
    return pd.to_datetime(pd.Series(np.random.randint(sd.timestamp(), ed.timestamp(), int(dlen))*(10**9)))

def createcatint(dlen = 100):
    lb, ub = 0, 0
    while True:
        try:
            lb = int(input('Insert a lower bound: '))
            ub = int(input('Insert an upper bound: '))
            break
        except:
            print('Must be a valid integer!')
    return pd.Series(np.random.choice(range(lb, ub), size=int(dlen), replace=True))

def createtext(dlen = 100):
    print('\nTo create sentences about a topic, you will need to provide a set of example sentences about it.\
            \nSpecificity is key. The better the quality of the sentences provided, the better the quality of the sentences outputted.\
            \nFor example, if this data is for a classification model, you will have to make sure there is some overlap in the examples. Otherwise,\
            \nthe data will be too easy to classify. Input quality = Output quality.\n')
    def gen_text(clen=50, api=False):
        if api:
            api_opt = input('Use google bard API to get topic sentences? (Y/N): ')
        while True:
            try:
                sample_text = input_window()
                assert len(re.findall('\.', sample_text)) > 7
                break
            except:
                'Text is too short! Unique sentences will not be generated. Please try again.'
        text_model = markovify.Text(sample_text, state_size=1)
        empt = []
        for i in range(clen):
            empt.append(text_model.make_sentence())
        return empt
    cats = input('Does the text need to obey categories? (Y/N): ')
    if 'y' in cats.lower():
        catname = input('Name the category column: ')
        cats, weights = [], []
        while True:
            try:
                tups = input('List categories with weights/probabilities as tuples (i.e. (Spam, 0.4), (Ham, 0.6)) separated by commas: ')
                cats = re.findall(r'\(([^\,]+)', tups)
                weights = list(map(float, re.findall(r'\,\W*([\d.]+)', tups)))
                assert len(cats) == len(weights) > 0
                break
            except:
                print('Invalid input. Please try again.')
        sent_list, cat_list = [], []
        for i in range(len(cats)):
            print(f'Generate example sentences for category: {cats[i]}')
            listlen = int(np.round(weights[i]*int(dlen)))
            sent_list.extend(gen_text(clen=listlen))
            cat_list.extend([cats[i]]*listlen)
        shufdf = pd.DataFrame({'text':sent_list, 'cat':cat_list}).sample(frac=1)
        return [shufdf['text'], shufdf['cat'], catname]
    return(pd.Series(gen_text(clen=int(dlen))))

def createrandtext(dlen = 100):
    def genrand_word(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))
    fake = Faker()
    dist = ''
    while True:
        try:
            dist = input('Choose a type of fake text (by number):\
                         \n 1. Random String of Characters\
                         \n 2. Random String of Words\
                         \n 3. Random Sentence\
                         \n 4. Random Paragraph\
                         \n 5. Random Names\n').replace('.','')
            assert int(dist) < 6
            break
        except:
            print('Invalid entry.')
    randt = []
    for _ in range(int(dlen)):
        rand_text = ''
        if dist == '1':
            rand_text = genrand_word(random.randint(50, 100))
        elif dist == '2':
            rand_text = fake.text(max_nb_chars=200)
        elif dist == '3':
            rand_text = fake.sentence()
        elif dist == '4':
            rand_text = fake.text(max_nb_chars=1200)
        elif dist == '5':
            rand_text = fake.name()
        randt.append(rand_text)
    return pd.Series(randt)

def createcattext(dlen = 100):
    eqdist = input('Should groups be distributed evenly? (Y/N): ')
    if 'n' in eqdist.lower():
        cats, weights = [], []
        while True:
            try:
                tups = input('List categories with weights/probabilities as tuples (i.e. (Group 1, 0.4), (Group 2, 0.6)) separated by commas: ')
                cats = re.findall(r'\(([^\,]+)', tups)
                weights = list(map(float, re.findall(r'\,\W*([\d.]+)', tups)))
                assert len(cats) == len(weights) > 0
                break
            except:
                print('Invalid input. Please try again.')
        return pd.Series(random.choices(cats, weights=weights,k=int(dlen)))
    catnames = StringInput('List category names, separated by commas: ', ',')
    return pd.Series(np.random.choice(catnames.list(), size=int(dlen), replace=True))

def change(dframe, mdata, opt, passdict):
    if opt == 1:
        print('Columns: ', dframe.columns)
        col = ''
        while True:
            try:
                col = input('Choose column to remove: ')
                assert col in dframe.columns
                break
            except:
                print('Invalid Column.')
        return dframe.drop(col)
    elif opt == 2:
        print('Columns: ', dframe.columns)
        col = ''
        while True:
            try:
                col = input('Choose column to resample: ')
                assert col in dframe.columns
                break
            except:
                print('Invalid Column.')
        type = mdata[np.where(np.array(dframe.columns) == col)]
        dframe[col] = passdict[type](dframe.shape[0])
        return dframe
    elif opt == 3:
        print('Current DataFrame Length: ', dframe.shape[0])
        newlen = 0
        while True:
            try:
                newlen = int(input('New DataFrame Length'))
                assert newlen <= dframe.shape[0]
                break
            except:
                print('Invalid Length.')
        return dframe.sample(newlen, replace=False)
        

def datagenerator():

    print('Welcome to DataFrame Generator! Let\'s begin:')
    print('Step 1: Establish columns')
    colnames = StringInput('List column names, separated by commas: ', ',')

    print('Choose column types. Options: \
          \n integer(int) - integer numbers(randomly generated) \
          \n float - floating point numbers(randomly generated) \
          \n datetime(date) - dates in a certain range \
          \n Categorical integer(catint) - numbers as categories (or ordering) \
          \n text - string in specified language (can be about certain subject) \
          \n random text(randtext) - random string of words or characters, also works for random names \
          \n Categorical text(cattext) - categories given by strings. Can be random or given by user')
    
    coltypes = None
    while True:
        coltypes = StringInput('List out the column types, separated by commas: ', ',')
        if coltypes.length() == colnames.length():
            break
        else:
            print('Number of column types does not match number of columns! \n ')

    typedict = {'integer': createint,
                'int': createint,
                'float': createfloat,
                'datetime': createdate,
                'date': createdate,
                'categorical integer': createcatint,
                'catint': createcatint,
                'text': createtext,
                'random text': createrandtext,
                'randtext': createrandtext,
                'categorical text': createcattext,
                'cattext': createcattext}
    
    params = StringInput('List out the intended length (or \'rand\' for random) of the data and the output datatype (csv, xslx, tsv, df) separated by commas: ', ',')
    par_list = params.list()
    try:
        par_list[0] = int(params.list()[0])
    except:
        par_list[0] = random.randint(100, 5000)
    
    print('Data length: ', par_list[0])
    print('Output type: ', par_list[1])


    dframe = pd.DataFrame()
    metadata = []

    for i in range(colnames.length()):
        print(f'Making column: {colnames.list()[i]} \nColumn type: {coltypes.list()[i]} \n ')
        outputr = typedict[coltypes.list()[i].lower()](dlen = par_list[0])
        if isinstance(outputr, list):
            dframe[colnames.list()[i]] = outputr
            dframe[outputr[2]] = outputr[1]
            metadata.extend(['text', 'cattext'])
            continue
        dframe[colnames.list()[i]] = outputr
        metadata.append(coltypes.list()[i])

    print(dframe.head(10))
    while True:
        prompt1 = input('Are you satisfied with this output? (Y/N): ')
        if prompt1.lower() == 'n':
            print('Would you like to: \
                  \n 1. Remove a column \
                  \n 2. Resample a column \
                  \n 3. Change the data length \
                  \n 4. Restart the process \
                  \n 5. Cancel')
            while True:
                try:
                    prompt2 = input('Choose:').replace('.', '')
                    assert int(prompt2) < 6
                    break
                except:
                    print('Invalid input. Please Try Again')
            if int(prompt2) < 4:
                dframe = change(dframe, metadata, int(prompt2), typedict)
            elif prompt2 == '4':
                return datagenerator()
            else:
                break
        else:
            break
    
    outtype = params.list()[1].lower()
    if outtype == 'csv':
        print('New file created: ', os.getcwd(), '/', 'fakedata.csv')
        dframe.to_csv('fakedata.csv')
        return None
    elif outtype == 'xlsx':
        print('New file created: ', os.getcwd(), '/', 'fakedata.xlsx')
        dframe.to_excel('fakedata.xlsx')
        return None
    elif outtype == 'tsv':
        print('New file created: ', os.getcwd(), '/', 'fakedata.tsv')
        dframe.to_csv('fakedata.tsv', sep = '\t')
        return None
    else:
        return dframe

fakedata = datagenerator()

print('Final Output: \n', fakedata)
