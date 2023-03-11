#!python

# Convert bank CSV files for appending to my Excel sheet

import csv
import argparse
import os

fieldnames = ['Account', 'Date', 'Description', 'cat', 'det', 'Amount']

substitutions = [
{'str': "MACEY'S EXPRESS HLD", 'cat': 'Automobile'},
{'str': "MACEY'S HOLL", 'cat': 'Groceries'},
{'str': "MCDONALD'S", 'cat': 'Dining'},
{'str': "SCHWAN'S HOME SERVIC", 'cat': 'Groceries', 'det': 'Schwans'},
{'str': "WENDY'S", 'cat': 'Dining'},
{'str': 'ADVANCED MICRO D', 'cat': 'Business Travel', 'det': 'reim'},
{'str': 'AMAZON MARKEPLACE', 'cat': 'Housewares', 'det': 'Amazon', 'lmt': -250.0},
{'str': 'AMAZON.COM', 'cat': 'Housewares', 'det': 'Amazon', 'lmt': -250.0},
{'str': 'AMAZON.COM*', 'cat': 'Housewares', 'det': 'Amazon', 'lmt': -250.0},
{'str': 'AMD INC.', 'cat': 'Salary'},
{'str': 'AMERICAN EXPRESS TYPE: ONLINE PMT', 'cat': '$ Pay AmEx'},
{'str': 'APPLE.COM', 'cat': 'Entertainment'},
{'str': 'AUTOPAY PAYMENT', 'cat': '$ Pay AmEx'},
{'str': 'BALANCEDBODY', 'cat': 'Medical'},
{'str': 'CAROLLYNN', 'cat': 'Education', 'det': 'Piano'},
{'str': 'CHEVRON', 'cat': 'Automobile'},
{'str': 'CHUCKS SERVICE', 'cat': 'Automobile'},
{'str': 'COSTCO BY INSTACART', 'cat': 'Groceries'},
{'str': 'COSTCO WHSE', 'cat': 'Groceries', 'lmt': -250.0},
{'str': 'DOORDASH', 'cat': 'Dining'},
{'str': 'DTV*DIRECTV SERVICE', 'cat': 'Utilities', 'det': 'DirecTV'},
{'str': 'ELECTRONIC PAYMENT RECEIVED', 'cat': '$ Pay AmEx'},
{'str': 'FANDANGO', 'cat': 'Entertainment'},
{'str': 'From DLT', 'cat': 'Capital Xfer'},
{'str': 'From MCALLISTER', 'cat': 'Capital Xfer'},
{'str': 'GOOGLE *FIBER', 'cat': 'Utilities', 'det': 'Internet'},
{'str': 'GOOGLE*FIBER', 'cat': 'Utilities', 'det': 'Internet'},
{'str': 'HARMONS', 'cat': 'Groceries'},
{'str': 'HOLIDAY OIL', 'cat': 'Automobile'},
{'str': 'JIFFY LUBE', 'cat': 'Automobile'},
{'str': 'JUST.INGREDIENTS', 'cat': 'Housewares'},
{'str': 'LEDINGHAM PROPER', 'cat': 'Rental Income'},
{'str': 'LITTLE CAESAR', 'cat': 'Dining'},
{'str': 'LOANCARE', 'cat': 'Mortgage'},
{'str': 'LUME DEODORANT', 'cat': 'Housewares'},
{'str': 'MEIERS PHARMACY', 'cat': 'Medical'},
{'str': 'MILLCREEK GARDENS', 'cat': 'Yard'},
{'str': 'MORTGAGE', 'cat': 'Mortgage'},
{'str': 'NETFLIX', 'cat': 'Entertainment'},
{'str': 'OHSWEBSTOR', 'cat': 'Education'},
{'str': 'OLYMPUS FAMILY MED', 'cat': 'Medical'},
{'str': 'PACIFICORP', 'cat': 'Utilities', 'det': 'Power'},
{'str': 'PEDIATRIC', 'cat': 'Medical'},
{'str': 'PENN MUTUAL', 'cat': '$ Life Ins', 'det': 'Penn Mutual'},
{'str': 'PIZZA', 'cat': 'Dining'},
{'str': 'PIZZERIA', 'cat': 'Dining'},
{'str': 'PRIME VIDEO', 'cat': 'Entertainment'},
{'str': 'QUESTAR GAS', 'cat': 'Utilities', 'det': 'Gas'},
{'str': 'RED 8 ASIAN', 'cat': 'Dining'},
{'str': 'ROSS DRESS FOR LESS', 'cat': 'Housewares'},
{'str': 'SALTLAKECOUNTYLIBRARYS', 'cat': 'Entertainment'},
{'str': 'SHARONS CAFE', 'cat': 'Dining'},
{'str': 'SIZZLER', 'cat': 'Dining'},
{'str': 'SLS', 'cat': 'Mortgage'},
{'str': 'BYU', 'cat': 'Education'},
{'str': 'SMILES', 'cat': 'Medical', 'det': 'Dental'},
{'str': 'SMITHS MRKTPL', 'cat': 'Housewares'},
{'str': 'SNAPFISH', 'cat': 'Housewares'},
{'str': 'SPECIALIZED LOAN', 'cat': 'Mortgage'},
{'str': 'SPEEDWAY', 'cat': 'Automobile'},
{'str': 'STEAM GAMES', 'cat': 'Entertainment'},
{'str': 'SUBARU', 'cat': 'Automobile'},
{'str': 'SWEETALY', 'cat': 'Dining'},
{'str': 'SWINYER WOSETH', 'cat': 'Medical'},
{'str': 'U OF U MY CHART', 'cat': 'Medical'},
{'str': 'USPS', 'cat': 'Housewares'},
{'str': 'UTAH-DMV', 'cat': 'Automobile'},
{'str': 'SWITCH SALON', 'cat': 'Personal Care'},
{'str': 'T-MOBILE', 'cat': 'Utilities', 'det': 'Cell Phone'},
{'str': 'TAQUERIA', 'cat': 'Dining'},
{'str': 'TICKETMAST', 'cat': 'Entertainment'},
{'str': 'TARGET PLUS', 'cat': 'Housewares', 'lmt': -250.0},
{'str': 'TARGET.COM', 'cat': 'Housewares'},
{'str': 'TJ MAXX', 'cat': 'Housewares'},
{'str': 'TMOBILE', 'cat': 'Utilities', 'det': 'Cell Phone'},
{'str': 'Transfer From Loan', 'cat': '$ Loan Xfer'},
{'str': 'Transfer To Loan 02', 'cat': 'Automobile', 'det': 'Legacy'},
{'str': 'Transfer To Loan 03', 'cat': 'Automobile', 'det': 'Santa Fe'},
{'str': 'Transfer To Loan 04', 'cat': 'Automobile', 'det': 'Legacy'},
{'str': 'Transfer To Loan 10', 'cat': '$ Loan Xfer'},
{'str': 'VALLEY WIDE COOP', 'cat': 'Utilities', 'det': 'Propane'},
{'str': 'VIDANGEL', 'cat': 'Entertainment'},
{'str': 'VILLAGE TOWNHOME', 'cat': 'HOA Dues'},
{'str': 'VOYA', 'cat': '$ Life Ins', 'det': 'Voya'},
{'str': 'WAL-MART', 'cat': 'Groceries'},
{'str': 'WALMART.COM', 'cat': 'Groceries'},
{'str': 'WASATCH FRONT WA', 'cat': 'Utilities', 'det': 'Trash'},
{'str': 'WASATCH WASTE', 'cat': 'Utilities', 'det': 'Trash'},
{'str': 'WENDYS', 'cat': 'Dining'},
{'str': 'WINKWELL', 'cat': 'Housewares'},
{'str': 'ZIONS BANK TYPE: ONLINE PMT', 'cat': 'Zions Interest'},
# {'str': 'SUMMIT FINANCIAL', 'cat': 'Taxes', 'det': 'Tax Prep'},
# {'str': '', 'cat': ''},
]

def categorize(row):
    '''Fill in Category or Detail field based on Description'''

    desc = row['Description']

    for item in substitutions:
        if item['str'] in desc:
            if 'lmt' in item and float(row['Amount']) <= item['lmt']:
                continue
            row['cat'] = item['cat']
            if 'det' in item:
                row['det'] = item['det']
            return row

    # Special cases
    if 'Draft 3' in desc and float(row['Amount']) == -250.0:
        row['cat'] = 'Housewares'
        row['det'] = 'Nora Jimenez Cleaning'
    if 'Mobile Deposit' in desc and 'rent' in desc:
        row['cat'] = 'Rental Income Net'

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
    content = removeOnePrefix(content, ' ', ['WWW', 'SP'])
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
            row['det'] = row['Check']
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
                row['det'] = desc.split('MEMO: ')[1]

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
            row['cat'] = ''
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

            if 'cat' in row:
                row['det'] = row['cat']
                row.pop('cat')
            else:
                row['det'] = ''
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
            row['cat'] = ''
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
