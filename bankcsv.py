#!python

# Convert bank CSV files for appending to my Excel sheet

import csv
import argparse
import os

fieldnames = ['Account', 'Date', 'Description', 'Category', 'Detail', 'Amount']

# TODO: Reorganize it in tables
def categorize(row):
    '''Fill in Category or Detail field based on Description'''

    desc = row['Description']

    if 'Transfer To Loan 02' in desc:
        row['Category'] = 'Automobile'
        row['Detail'] = 'Legacy'
    elif 'Transfer To Loan 03' in desc:
        row['Category'] = 'Automobile'
        row['Detail'] = 'Santa Fe'
    elif 'Transfer To Loan 04' in desc:
        row['Category'] = 'Automobile'
        row['Detail'] = 'Legacy'
    elif 'Transfer From Loan' in desc or 'Transfer To Loan' in desc:
        row['Category'] = '$ Loan Xfer'
    if 'AMD INC.' in desc:
        row['Category'] = 'Salary'
    if 'ADVANCED MICRO D' in desc:
        row['Category'] = 'Business Travel'
        row['Detail'] = 'reim'
    if 'AMERICAN EXPRESS TYPE: ONLINE PMT' in desc or 'AUTOPAY PAYMENT' in desc:
        row['Category'] = '$ Pay AmEx'
    if 'TARGET.COM' in desc or 'TJ MAXX' in desc:
        row['Category'] = 'Housewares'
        row['Detail'] = 'Amazon'
    if 'TMOBILE' in desc or 'T-MOBILE' in desc:
        row['Category'] = 'Utilities'
        row['Detail'] = 'Cell Phone'
    if 'AMAZON.COM*' in desc and float(row['Amount']) > -300.0:
        row['Category'] = 'Housewares'
        row['Detail'] = 'Amazon'
    if ("AMAZON MARKEPLACE" in desc or "AMAZON.COM" in desc) and float(row['Amount']) > -250.0:
        row['Category'] = 'Housewares'
        row['Detail'] = 'Amazon'
    if 'CAROLLYNN' in desc:
        row['Category'] = 'Education'
        row['Detail'] = 'Piano'
    if 'COSTCO WHSE' in desc and float(row['Amount']) > -250.0:
        row['Category'] = 'Groceries'
    if 'COSTCO BY INSTACART' in desc or "MACEY'S HOLL" in desc or "WALMART.COM" in desc or "WAL-MART" in desc or "HARMONS" in desc:
        row['Category'] = 'Groceries'
    if 'DOORDASH' in desc:
        row['Category'] = 'Dining'
    if 'DTV*DIRECTV SERVICE' in desc:
        row['Category'] = 'Utilities'
        row['Detail'] = 'DirecTV'
    if 'Draft 3' in desc and float(row['Amount']) == -250.0:
        row['Category'] = 'Housewares'
        row['Detail'] = 'Nora Jimenez Cleaning'
    if 'ELECTRONIC PAYMENT RECEIVED' in desc:
        row['Category'] = '$ Pay AmEx'
    if 'From DLT' in desc:
        row['Category'] = 'Capital Xfer'
    if 'From MCALLISTER' in desc:
        row['Category'] = 'Capital Xfer'
    if 'GOOGLE*FIBER' in desc or 'GOOGLE *FIBER' in desc:
        row['Category'] = 'Utilities'
        row['Detail'] = 'Internet'
    if 'LEDINGHAM PROPER' in desc:
        row['Category'] = 'Rental Income'
    if 'LOANCARE' in desc or 'SLS' in desc or 'MORTGAGE' in desc or 'SPECIALIZED LOAN' in desc:
        row['Category'] = 'Mortgage'
    if "MACEY'S EXPRESS HLD" in desc or "CHEVRON" in desc or "JIFFY LUBE" in desc or "CHUCKS SERVICE" in desc or "HOLIDAY OIL" in desc:
        row['Category'] = 'Automobile'
    if "MCDONALD'S" in desc or "WENDY'S" in desc or "WENDYS" in desc or "LITTLE CAESAR" in desc or "RED 8 ASIAN" in desc or "TAQUERIA" in desc:
        row['Category'] = 'Dining'
    if "MEIERS PHARMACY" in desc:
        row['Category'] = 'Medical'
    if "MILLCREEK GARDENS" in desc:
        row['Category'] = 'Yard'
    if "PACIFICORP" in desc:
        row['Category'] = 'Utilities'
        row['Detail'] = 'Power'
    if "PENN MUTUAL" in desc:
        row['Category'] = '$ Life Ins'
        row['Detail'] = 'Penn Mutual'
    if "Mobile Deposit" in desc and "rent" in desc:
        row['Category'] = 'Rental Income Net'
    if "QUESTAR GAS" in desc:
        row['Category'] = 'Utilities'
        row['Detail'] = 'Gas'
    if "VALLEY WIDE COOP" in desc:
        row['Category'] = 'Utilities'
        row['Detail'] = 'Propane'
    if "VILLAGE TOWNHOME" in desc:
        row['Category'] = 'HOA Dues'
    if "VOYA" in desc:
        row['Category'] = '$ Life Ins'
        row['Detail'] = 'Voya'
    if "WASATCH FRONT WA" in desc or "WASATCH WASTE" in desc:
        row['Category'] = 'Utilities'
        row['Detail'] = 'Trash'
    if "ZIONS BANK TYPE: ONLINE PMT" in desc:
        row['Category'] = 'Zions Interest'
    if "APPLE.COM" in desc or "NETFLIX" in desc or "PRIME VIDEO" in desc or "VIDANGEL" in desc or "FANDANGO" in desc:
        row['Category'] = 'Entertainment'
    if "BALANCEDBODY" in desc:
        row['Category'] = 'Medical'
    # if "" in desc:
    #     row['Category'] = ''
    #     row['Detail'] = ''
    # if "" in desc:
    #     row['Category'] = ''
    #     row['Detail'] = ''
    # if "" in desc:
    #     row['Category'] = ''
    #     row['Detail'] = ''

    # print(row['Category'])

    return row

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

def removeOnePrefix(content, splitkey, prefixes):
    segs = content.split(splitkey)
    if segs[0].strip() in prefixes:
        content = (splitkey.join(segs[1:])).strip()

    return content

def removePrefixes(content):
    '''Remove prefixes separated by punctuation from descriptions'''

    before = content
    content = removeOnePrefix(content, '*', ['ACT', 'AMZ', 'BT', 'FS', 'GG', 'ICP', 'INT', 'PAYPAL', 'PTI', 'SP', 'SQ', 'TST', 'WPY'])
    content = removeOnePrefix(content, ' ', ['WWW'])
    content = removeOnePrefix(content, '.', ['WWW'])

    # if before != content:
    #     print('Replaced:', before, '=>', content)

    return content

def process_ufirstcu_file(file_path):
    '''AccountHistory.csv is from UFirstCU'''

    # Clean up line ends, etc.
    with open(file_path, 'rb') as open_file:
        content = open_file.read()

    print(
        content.count(b'\r\n'), 'CRLF,',
        content.count(b'\r'), 'CR,',
        content.count(b'\n'), 'LF,',
        content.count(b'\t'), 'TAB.')

    content = content.replace(b'\r\n', b'\r')
    content = content.replace(b'\n', b'\r')
    content = content.replace(b'\r\r', b'\r')

    content = replaceLoop(content, b'  ', b' ', False, '\n') # Remove multiple spaces
    content = replaceLoop(content, b'\r ', b'\r', False, '\n') # Remove leading spaces
    content = replaceLoop(content, b' \r', b'\r', False, '\n') # Remove trailing spaces

    content = content.replace(b'\r', b'\r\n')

    with open('tmp.csv', 'wb') as open_file:
        open_file.write(content)

    # Process file, row by row, clean up columns, etc.
    rows = []

    with open('tmp.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            if len(row) != 8:
                print('Bad row:', row)
                raise Exception('Improper row')

            row.pop('Balance')

            row['Account'] = row['Account Number']
            row.pop('Account Number')
            row['Date'] = row['Post Date']
            row.pop('Post Date')
            row['Detail'] = row['Check']
            row.pop('Check')
            row.pop('Status')
            desc = row['Description']

            for chop in ['Withdrawal by', 'Deposit by', 'Withdrawal', 'Deposit', 'BUSINESS DEBIT', 'Visa Debit', 'Bill Payment']:
                if desc != 'Withdrawal' and desc != 'Deposit' and 'Withdrawal at ATM' not in desc and 'Mobile Deposit' not in desc:
                    desc = desc.replace(chop, '')

            desc = desc.replace('THE HOME DEPOT', 'HOME DEPOT')
            desc = desc.replace('The Home Depot', 'HOME DEPOT')
            desc = desc.replace('MEMO:', ' MEMO:')
            desc = removePrefixes(desc)

            if 'in the amount' in desc:
                desc = 'Fee Withdrawal Overdrawn ' + desc

            if '/ Transfer' in desc:
                desc = desc.split('/ ')[1] + ' ' + desc.split('/ ')[0]

            if 'MEMO:' in desc:
                row['Detail'] = desc.split('MEMO: ')[1]

            if 'TYPE:' in desc and 'CO:' in desc:
                company = desc.split('CO: ')[1]
                company = company.replace('Entry Class Code', 'CODE')
                company = company.split(':')[0] + ':'
                company = company.replace(' NAME:', '')
                company = company.replace(' CODE:', '')
                company = company.replace(' DATA:', '')
                company = company.replace(':', '')
                desc = company + ' ' + desc

            # Eat initial digits
            if '7-11' not in desc:
                while len(desc) and desc[0] in list('#0123456789 '):
                    desc = desc[1:]

            desc = replaceLoop(desc, '  ', ' ', False, '\n')

            row['Description'] = desc

            if row['Debit'] != '':
                row['Amount'] = str(-float(row['Debit']))
            if row['Credit'] != '':
                row['Amount'] = str(float(row['Credit']))

            row.pop('Debit')
            row.pop('Credit')

            # Automatic categorization
            row['Category'] = ''
            row = categorize(row)

            rows.append(row)

    os.remove('tmp.csv')

    with open('ufirstcu.csv', 'w', newline='') as csvfile:
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
            desc = row['Description']

            desc = desc.replace('AplPay ', '')
            desc = desc.replace('1112 DOWNEAST', 'DOWNEAST')
            desc = desc.replace('THE HOME DEPOT', 'HOME DEPOT')

            # Eat initial digits
            if '7-ELEVEN' not in desc:
                while len(desc) and desc[0] in list('#0123456789 '):
                    desc = desc[1:]

            desc = replaceLoop(desc, '  ', ' ', False, '\n')
            desc = removePrefixes(desc)

            row['Description'] = desc
            row['Amount'] = str(-float(row['Amount'])) # Negate the amount for AmEx

            # Automatic categorization
            row['Category'] = ''
            row = categorize(row)

            rows.append(row)

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
        elif 'Account' in fname:
            process_ufirstcu_file(fname)
        elif 'activity' in fname:
            process_amex_file(fname)
        else:
            print('Unrecognized filename', fname)

if __name__ == "__main__":
    main()
