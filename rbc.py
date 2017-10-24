from dateutil.parser import parse
from openpyxl import Workbook
from openpyxl import load_workbook
import sys
import argparse


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


def excel(wb_path, verbose=False):
    headers = ['Date', 'Description', 'Price']

    wb = load_workbook('files/2016.xlsx')
    ws = wb['2016']

    out_ws = wb.create_sheet(title='2016 - Visa')
    out_ws['A1'].value = headers[0]
    out_ws['B1'].value = headers[1]
    out_ws['C1'].value = headers[2]

    i = 1
    row = 2
    while i<ws.max_row:
        words = ws.cell(column=1,row=i).value.split()
        if is_date(words[0]):
            date = ' '.join(words[:2])
            if words[-1][0] == '$' or words[-1][0] == '-': # if 1 liner
                price = words[-1]
                description =  ' '.join(words[4:-1])
            else:
                description =  ' '.join(words[4:])
                i+=2
                price = ws.cell(column=1,row=i).value
        elif words[0] == 'NEW':
            description = "NEW BALANCE"
            date = ""
            price = words[-1]
        else:
            print("error", ws.cell(column=1,row=i).value)
            i+=1
            continue
        if verbose:
            print("data: {}, description: {}, price: {}".format(
                date, description, price))
        out_ws.cell(column=1, row=row).value = date
        out_ws.cell(column=2, row=row).value = description
        out_ws.cell(column=3, row=row).value = price
        row+=1
        i+=1
    wb.save('files/2016.xlsx')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse rbc statements')
    parser.add_argument('wb_path', action="store")
    parser.add_argument('-v', help='verbose',default=False, dest='verbose', action="store_true")
    options = parser.parse_args()
    excel(**vars(options))

#'files/2016.xlsx'
# excel()
#parse_excel(strs2)
#extract(strs[:3])



