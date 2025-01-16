#!python

# Convert bank CSV files for appending to my Excel sheet

import csv
import argparse
import os

# Positive amounts are income. Negative amounts are outflows.

fieldnames = ['Account', 'Date', 'Description', 'cat', 'det', 'Amount']

substitutions = [
# {'str': 'ADVANCED MICRO D', 'cat': 'Business Travel', 'det': 'reim'},
# {'str': 'AMD INC.', 'cat': 'Salary'},
{'str': "MACEY'S EXPRESS HLD", 'cat': 'Automobile'},
{'str': "MACEY'S HOLL", 'cat': 'Groceries'},
{'str': 'SPROUTS', 'cat': 'Groceries'},
{'str': "MCDONALD'S", 'cat': 'Dining'},
{'str': "SCHWAN'S HOME SERVIC", 'cat': 'Groceries', 'det': 'Schwans'},
{'str': 'ASPEN RIDGE MAN', 'cat': 'Education', 'det': 'Jonathan Rent'},
{'str': "WENDY'S", 'cat': 'Dining'},
{'str': '7-ELEVEN', 'cat': 'Automobile', 'min': -25},
{'str': '7-ELEVEN', 'cat': 'Dining', 'max': -25},
{'str': 'MAVERIK', 'cat': 'Automobile', 'min': -25},
{'str': 'MAVERIK', 'cat': 'Dining', 'max': -25},
{'str': 'ACE HARDWARE', 'cat': 'Repairs'},
{'str': 'ACTIVESKIN', 'cat': 'Medical'},
{'str': 'AFGHAN KITCHEN', 'cat': 'Dining'},
{'str': 'MY PIE P', 'cat': 'Dining'},
{'str': 'AMAZON MARKEPLACE', 'cat': 'Housewares', 'det': 'Amazon', 'max': -250.0},
{'str': 'AMAZON.COM', 'cat': 'Housewares', 'det': 'Amazon', 'max': -250.0},
{'str': 'AMAZON.COM*', 'cat': 'Housewares', 'det': 'Amazon', 'max': -250.0},
{'str': 'AMERICAN EXPRESS TYPE: ONLINE PMT', 'cat': '$ Pay AmEx'},
{'str': 'AMEX EPAYMENT TYPE: ONLINE PMT', 'cat': '$ Pay AmEx'},
{'str': 'APPLE.COM', 'cat': 'Entertainment'},
{'str': 'AUTO PARTS', 'cat': 'Automobile'},
{'str': 'AMEX RIDESHARE CREDIT', 'cat': 'Automobile'},
{'str': 'AUTOPAY PAYMENT', 'cat': '$ Pay AmEx'},
{'str': 'BALANCEDBODY', 'cat': 'Medical'},
{'str': 'UTAHTAXRFD', 'cat': 'Taxes'},
{'str': 'BYU', 'cat': 'Education'},
{'str': 'CAFE RIO', 'cat': 'Dining'},
{'str': 'HONEST E', 'cat': 'Dining'},
{'str': 'COSTA V', 'cat': 'Dining'},
{'str': 'ARCTIC CIRCLE', 'cat': 'Dining'},
{'str': 'CAROLLYNN', 'cat': 'Education', 'det': 'Piano'},
{'str': 'CARRINGTON', 'cat': 'Mortgage'},
{'str': 'CHEVRON', 'cat': 'Automobile'},
{'str': "O'REILLY AUTO PARTS", 'cat': 'Automobile'},
{'str': 'CHUCKS SERVICE', 'cat': 'Automobile'},
{'str': 'COSTA VIDA', 'cat': 'Dining'},
{'str': 'COSTCO BY INSTACART', 'cat': 'Groceries'},
{'str': 'COSTCO WHSE', 'cat': 'Groceries', 'max': -250.0},
{'str': 'COTTONWOOD ID', 'cat': 'Utilities', 'det': 'Sewer'},
{'str': 'DAIRY QUEEN', 'cat': 'Dining'},
{'str': 'DOLLAR TREE', 'cat': 'Housewares'},
{'str': 'ENBRIDGE', 'cat': 'Utilities', 'det': 'Gas'},
{'str': 'DOORDASH', 'cat': 'Dining'},
{'str': 'DOWNEAST', 'cat': 'Housewares'},
{'str': 'DTV*DIRECTV SERVICE', 'cat': 'Utilities', 'det': 'DirecTV'},
{'str': 'ELECTRONIC PAYMENT RECEIVED', 'cat': '$ Pay AmEx'},
{'str': 'EXXONMOBIL', 'cat': 'Automobile'},
{'str': 'HERTZ CAR RENTAL', 'cat': 'Business Travel'},
{'str': 'FANDANGO', 'cat': 'Entertainment'},
{'str': 'From DLT', 'cat': 'Capital Xfer'},
{'str': 'From MCALLISTER', 'cat': 'Capital Xfer'},
{'str': 'IRS T', 'cat': 'Taxes'},
{'str': 'GEICO AUTO', 'cat': 'Automobile'},
{'str': 'GOOGLE *FIBER', 'cat': 'Utilities', 'det': 'Internet'},
{'str': 'HOLLIDAY WATER CO', 'cat': 'Utilities', 'det': 'Water'},
{'str': 'GOOGLE*FIBER', 'cat': 'Utilities', 'det': 'Internet'},
{'str': "STUDIOL", 'cat': 'Personal Care'},
{'str': "CLAIRE'S BTQ", 'cat': 'Personal Care'},
{'str': 'GREAT CLIPS', 'cat': 'Personal Care'},
{'str': 'GREAT HARVEST', 'cat': 'Groceries'},
{'str': 'HALE CENTRE', 'cat': 'Entertainment'},
{'str': 'HARMONS', 'cat': 'Groceries'},
{'str': 'HOLIDAY OIL', 'cat': 'Automobile'},
{'str': 'IHOP', 'cat': 'Dining'},
{'str': 'INTERMOUNTAIN HEALTH', 'cat': 'Medical'},
{'str': 'JIFFY LUBE', 'cat': 'Automobile'},
{'str': 'JOANNE', 'cat': 'Housewares'},
{'str': 'JUST.INGREDIENTS', 'cat': 'Housewares'},
{'str': 'KFC', 'cat': 'Dining'},
{'str': 'KINDLE SVCS', 'cat': 'Entertainment'},
{'str': 'KOHLS', 'cat': 'Housewares'},
{'str': 'LABCORP', 'cat': 'Medical'},
{'str': 'LEDINGHAM PROPER', 'cat': 'Rental Income'},
{'str': 'LES SCHWAB', 'cat': 'Automobile'},
{'str': 'LILLIAN FARRIS', 'cat': 'Medical', 'det': 'Hazel'},
{'str': 'LITTLE CAESAR', 'cat': 'Dining'},
{'str': 'TOP IT FROZEN', 'cat': 'Dining'},
{'str': 'SUBWAY', 'cat': 'Dining'},
{'str': 'LOANCARE', 'cat': 'Mortgage'},
{'str': 'LUME DEODORANT', 'cat': 'Housewares'},
{'str': 'JOANN STORES', 'cat': 'Housewares'},
{'str': 'MARSHALLS', 'cat': 'Housewares'},
{'str': 'MEIERS PHARMACY', 'cat': 'Medical'},
{'str': 'MILLCREEK GARDENS', 'cat': 'Yard'},
{'str': 'MORTGAGE', 'cat': 'Mortgage'},
{'str': 'MT OLYMPUS IMPROVE', 'cat': 'Utilities', 'det': 'Sewer'},
{'str': 'NAYAX WASH', 'cat': 'Automobile'},
{'str': 'PARKING', 'cat': 'Automobile'},
{'str': 'NETFLIX', 'cat': 'Entertainment'},
{'str': 'ODP Fee', 'cat': 'Bank Fees'},
{'str': 'OHSWEBSTOR', 'cat': 'Education'},
{'str': 'FONS-SARAHJANEWATTS', 'cat': 'Education', 'det': 'Caroline voice'},
{'str': 'OLYMPUS CLINIC', 'cat': 'Medical'},
{'str': 'OLYMPUS FAMILY MED', 'cat': 'Medical'},
{'str': 'PACIFICORP', 'cat': 'Utilities', 'det': 'Power'},
{'str': 'PEDIATRIC', 'cat': 'Medical'},
{'str': 'PENN MUTUAL', 'cat': '$ Life Ins', 'det': 'Penn Mutual'},
{'str': 'PIZZA', 'cat': 'Dining'},
{'str': 'PIZZERIA', 'cat': 'Dining'},
{'str': 'PRELOVED', 'cat': 'Housewares'},
{'str': 'PRIMARY CHILDREN', 'cat': 'Medical'},
{'str': 'PRIME VIDEO', 'cat': 'Entertainment'},
{'str': 'QUESTAR GAS', 'cat': 'Utilities', 'det': 'Gas'},
{'str': 'RANCHERITO', 'cat': 'Dining'},
{'str': 'RED 8 ASIAN', 'cat': 'Dining'},
{'str': 'ROSS DRESS FOR LESS', 'cat': 'Housewares'},
{'str': 'ROSS STORES', 'cat': 'Housewares'},
{'str': 'SALTLAKECOUNTYLIBRARYS', 'cat': 'Entertainment'},
{'str': 'SHARONS CAFE', 'cat': 'Dining'},
{'str': 'SIZZLER', 'cat': 'Dining'},
{'str': 'SLS', 'cat': 'Mortgage'},
{'str': 'SMILES', 'cat': 'Medical', 'det': 'Dental'},
{'str': 'SMITHS FOOD', 'cat': 'Groceries'},
{'str': 'SMITHS MRKTPL', 'cat': 'Housewares'},
{'str': 'SNAPFISH', 'cat': 'Housewares'},
{'str': 'SPECIALIZED LOAN', 'cat': 'Mortgage'},
{'str': 'SPEEDWAY', 'cat': 'Automobile'},
{'str': 'STEAM GAMES', 'cat': 'Entertainment'},
{'str': 'SUBARU', 'cat': 'Automobile'},
{'str': 'SUMMIT FINANCIAL', 'cat': 'Legal and Prof Fees', 'det': 'Tax prep'},
{'str': 'SWEETALY', 'cat': 'Dining'},
{'str': 'TROPICAL SMOOTHIE CA', 'cat': 'Dining'},
{'str': 'SWINYER WOSETH', 'cat': 'Medical'},
{'str': 'SWITCH SALON', 'cat': 'Personal Care'},
{'str': 'T J MAXX', 'cat': 'Housewares'},
{'str': 'T-MOBILE', 'cat': 'Utilities', 'det': 'Cell Phone'},
{'str': 'TAQUERIA', 'cat': 'Dining'},
{'str': 'TARGET PLUS', 'cat': 'Housewares', 'max': -250.0},
{'str': 'TARGET.COM', 'cat': 'Housewares'},
{'str': 'TICKETMAST', 'cat': 'Entertainment'},
{'str': 'TJ MAXX', 'cat': 'Housewares'},
{'str': 'TMOBILE', 'cat': 'Utilities', 'det': 'Cell Phone'},
{'str': 'Transfer From Loan', 'cat': '$ Loan Xfer'},
{'str': 'Transfer To Loan 02', 'cat': 'Automobile', 'det': 'Legacy'},
{'str': 'Transfer To Loan 03', 'cat': 'Automobile', 'det': 'Santa Fe'},
{'str': 'Transfer To Loan 05', 'cat': 'Automobile', 'det': 'Impreza'},
{'str': 'Transfer To Loan 09', 'cat': '$ Loan Xfer'},
{'str': 'Transfer To Loan 10', 'cat': '$ Loan Xfer'},
{'str': 'Transfer To MCALLISTER', 'cat': 'Capital Xfer'},
{'str': 'U OF U MY CHART', 'cat': 'Medical'},
{'str': 'UNGRICHT PARKER', 'cat': 'Medical'},
{'str': 'UPTOWN CHEAPSKATE', 'cat': 'Housewares'},
{'str': 'USPS', 'cat': 'Housewares'},
{'str': 'UTAH CORPORATIONS', 'cat': 'Legal and Prof Fees'},
{'str': 'UTAH-DMV', 'cat': 'Automobile'},
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
{'str': 'WYZE LABS', 'cat': 'Legal and Prof Fees'},
{'str': 'ZEST FOR LIFE', 'cat': 'Medical'},
{'str': 'ZIONS BANK TYPE: ONLINE PMT', 'cat': 'Zions Interest'},
]

def categorize(row):
    '''Fill in Category or Detail field based on Description'''

    desc = row['Description']

    for item in substitutions:
        if item['str'] in desc:
            if 'max' in item and float(row['Amount']) <= item['max']:
                continue
            if 'min' in item and float(row['Amount']) >= item['min']:
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
    content = removeOnePrefix(content, '*', ['ACT', 'AMZ', 'BT', 'EB', 'ETT', 'FS', 'GG', 'ICP', 'INT', 'PAYPAL', 'POS', 'PTI', 'PY', 'RAL', 'SP', 'SQ', 'TM', 'TST', 'WPY', 'YSI'])
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

            desc = desc.replace('UFirst RDC', 'UFirst Mobile Check Deposit')
            desc = desc.replace('THE HOME DEPOT', 'HOME DEPOT')
            desc = desc.replace('The Home Depot', 'HOME DEPOT')
            desc = desc.replace('MEMO:', ' MEMO:')
            desc = desc.replace('CO: Urban FT', '')
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
            if 'Account #' in row:
                acct = 'DaveDReserve'
                row['Account'] = acct + '-' + row['Card Member']
                row.pop('Account #')
                row.pop('Card Member')
            else:
                row['Account'] = 'DaveMarrBevy'

            if 'cat' in row:
                row['det'] = row['cat']
                row.pop('cat')
            else:
                row['det'] = ''

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
