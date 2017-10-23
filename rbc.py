from dateutil.parser import parse
from openpyxl import Workbook
from openpyxl import load_workbook


strs = [
    "10 Dec Interac purchase - 0644 KABOB HUT 7.89 1,415.33",
    "14 Dec Interac purchase - 3342 KABOB HUT 7.89",
    "Interac purchase - 6243 SUBWAY # 2969 8.76 1,398.68",
    "15 Dec Interac purchase - 2953 UW BRUBAKERS SL 6.22 1,392.46",
    "23 Dec Online Banking payment - 8933",
    "BELL CANADA 69.87 1,247.28"
]

strs2 = [
    "AUG 11 AUG 12 MCDONALD'S #8975 TORONTO ON",
    "7.40645E+22",
    "$1.46",
    "SEP 01 SEP 01 ANNUAL FEE $39.00",
    "SEP 01 SEP 01 ANNUAL FEE REBATE -$39.00",
    "SEP 02 SEP 06 FOOD BASICS #654 WATERLOO ON",
    "7.453E+22",
    "$52.38",
    "SEP 04 SEP 06 TIM HORTONS 0770 QTH CAMBRIDGE ON",
    "7.47034E+22",
    "$7.20",
]

def is_date(string):
    try:
        parse(string)
        return True
    except ValueError:
        return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def extract(strs):
    balance = None
    withdrawals = None
    desc = None

    for s in strs:
        s = s.split()
        left,right = 0,0

        if is_number(s[-1]) and is_number(s[-2]):
            balance = s[-1]
            withdrawals = s[-2]
            right = len(s) - 2
        elif s[-1].isdigit():
            balance = balance #prev
            withdrawals = s[-1]
            right = len(s) - 1

        if s[0].isdigit():
            date = s[0] + s[1]
            left = 1

        #desc = s[left:right]
        #if desc[-1].isdigit(): # 2 liners
        #    pass

        print(balance,withdrawals,desc)


def parse_excel(l):
    i = 0
    while i<len(l):
        words = l[i].split()
        if is_date(words[0]):
            date = ' '.join(words[:2])
            if words[-1][0] == '$' or words[-1][0] == '-': # if 1 liner
                price = words[-1]
                location =  ' '.join(words[4:-1])
                i+=1
            else:
                location =  ' '.join(words[4:])
                i+=2
                price = l[i]
                i+=1
            if price[0] == "(" or price[0] == '-':
                credit = True
            else:
                credit = False
            print("data: {}, location: {}, price: {}".format(
                  date,location, price))
        else:
            print("error", l[i])
            i+=1


def excel():
    headers = ['Date', 'Description', 'Price']

    wb = load_workbook('files/2016.xlsx')
    ws = wb['2016']

    i = 1
    while i<ws.max_row:
        words = ws.cell(column=1,row=i).value.split()
        if is_date(words[0]):
            date = ' '.join(words[:2])
            if words[-1][0] == '$' or words[-1][0] == '-': # if 1 liner
                price = words[-1]
                location =  ' '.join(words[4:-1])
            else:
                location =  ' '.join(words[4:])
                i+=2
                price = ws.cell(column=1,row=i).value

            print("data: {}, location: {}, price: {}".format(
                  date,location, price))
        elif words[0] == 'NEW':
            location = "NEW BALANCE"
            price = words[-1]
            print("data: {}, location: {}, price: {}".format(
                date, location, price))
        else:
            print("error", ws.cell(column=1,row=i).value)
        i+=1


excel()
#parse_excel(strs2)
#extract(strs[:3])



