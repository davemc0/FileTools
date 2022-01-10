#!python

# Convert bank CSV files for appending to my Excel sheet

import csv
import argparse
import os

def replaceLoop(content, oldt, newt, verbose, printNL):
    replCnt = content.count(oldt)
    while replCnt > 0:
        if verbose:
            print(replCnt, end=' ')
        content = content.replace(oldt, newt)
        replCnt = content.count(oldt)
    if verbose:
        print(replCnt, end=printNL)

    return content

def removeStars(content):
    '''Remove prefixes separated by punctuation from descriptions'''

    # *
    prefixes = ['ACT', 'AMZ', 'BT', 'FS', 'GG', 'PAYPAL', 'PTI', 'SP', 'TST', 'WPY']

    segs = content.split('*')
    if len(segs) > 2:
        print(segs)
    if segs[0].strip() in prefixes:
        content = ('*'.join(segs[1:])).strip()
        print('Replaced with:', content)

    # .
    prefixes = ['WWW',]

    segs = content.split('.')
    if len(segs) > 2:
        print(segs)
    if segs[0].strip() in prefixes:
        content = ('.'.join(segs[1:])).strip()
        print('Replaced with:', content)

    # space
    prefixes = ['WWW',]

    segs = content.split(' ')
    if len(segs) > 2:
        print(segs)
    if segs[0].strip() in prefixes:
        content = (' '.join(segs[1:])).strip()
        print('Replaced with:', content)

    return content

def process_uucu_file(file_path):
    '''Transactions_S-90.csv is from UUCU'''

    # Clean up line ends, etc.
    with open(file_path, 'rb') as open_file:
        content = open_file.read()

    print(
        content.count(b'\n'), 'CRLF,',
        content.count(b'\r'), 'CR,',
        content.count(b'\n '), 'LF,',
        content.count(b'\t'), 'TAB.')

    content = content.replace(b'\n', b' ')
    content = content.replace(b'\r ', b'\r')

    content = replaceLoop(content, b'  ', b' ', False, '\n') # Remove multiple spaces
    content = replaceLoop(content, b' \r', b'\r', False, '\n') # Remove trailing spaces

    content = content.replace(b'\r', b'\r\n')

    with open('tmp.csv', 'wb') as open_file:
        open_file.write(content)

    rows = []

    # Clean up columns, etc.
    with open('tmp.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            row.pop('Balance')

            print(row['Description'])

            for chop in ['Withdrawal by', 'Deposit by', 'Withdrawal', 'Deposit', 'BUSINESS DEBIT', 'Visa Debit', 'Bill Payment']:
                if row['Description'] != 'Withdrawal' and row['Description'] != 'Deposit':
                    row['Description'] = row['Description'].replace(chop, '')

            print(row['Description'])

            row['Description'] = row['Description'].replace('THE HOME DEPOT', 'HOME DEPOT')
            row['Description'] = row['Description'].replace('The Home Depot', 'HOME DEPOT')

            while len(row['Description']) and row['Description'][0] in list('#0123456789 '):
                row['Description'] = row['Description'][1:]

            row['Description'] = replaceLoop(row['Description'], '  ', ' ', False, '\n')

            if 'Transfer From Loan' in row['Description'] or 'Transfer To Loan' in row['Description']:
                row['Note'] = '$ Loan Xfer'
            rows.append(row)

    os.remove('tmp.csv')

    fieldnames = [key for key in rows[0]]

    with open('uucu.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def process_amex_file(file_path):
    '''activity.csv is from AmEx'''

    rows = []

    # Clean up columns, etc.
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            acct = 'DaveAcct' if '-6' in row['Account #'] else 'TiffAcct'
            row['Account'] = acct + '-' + row['Card Member']

            if 'Category' in row:
                row['Detail'] = row['Category']
                row.pop('Category')
            else:
                row['Detail'] = ''
            row.pop('Account #')
            row.pop('Card Member')
            if 'Type' in row:
                row.pop('Type')
            if 'Reference' in row:
                row.pop('Reference')

            # Clean up description
            row['Description'] = row['Description'].replace('AplPay ', '')
            row['Description'] = row['Description'].replace('1112 DOWNEAST', 'DOWNEAST')
            row['Description'] = row['Description'].replace('THE HOME DEPOT', 'HOME DEPOT')
            row['Description'] = replaceLoop(row['Description'], '  ', ' ', False, '\n')
            row['Description'] = removeStars(row['Description'])

            row['Amount'] = str(-float(row['Amount'])) # Negate the amount for AmEx

            # Automatic categorization
            if 'ELECTRONIC PAYMENT RECEIVED' in row['Description']:
                row['Category'] = '$ Pay AmEx'

            rows.append(row)

    fieldnames = ['Account', 'Date', 'Description', 'Category', 'Detail', 'Amount']

    with open('amex.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print('Done with AmEx')

def main():
    parser = argparse.ArgumentParser(
        description='bankcsv.py - Fix up CSV files from banks')

    parser.add_argument('fname',
                        nargs='+',
                        help='Files to convert')

    args = parser.parse_args()

    for fname in args.fname:
        print(fname)
        if 'Transac' in fname:
            process_uucu_file(fname)
        elif 'activity' in fname:
            process_amex_file(fname)
        else:
            print('Unrecognized filename', fname)

if __name__ == "__main__":
    main()
