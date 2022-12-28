#!python

import os
import re
import multiprocessing
import hashlib
import math

skipFolders = {}

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

count = 0
emails = set()

TLDs = {'il', 'ink', 'llc', 'gi', 'sca', 'stc', 'moto', 'dm', 'fire', 'mm', 'tv', 'yun', 'bm', 'cam', 'mk', 'ltda', 'fit', 'tips', 'mobi', 'fo', 'gmo', 'blog', 'jo', 'ly', 'gp', 'gn', 'ag', 'de', 'xyz', 'to', 'co', 'silk', 'br', 'pink', 'fast', 'th', 'uz', 'buzz', 'itv', 'aq', 'pohl', 'kred', 'aol', 'new', 'hu', 'call', 'icbc', 'song', 'gu', 'like', 'lu', 'srl', 'biz', 'dvr', 'fans', 'vc', 'pe', 'py', 'pid', 'iq', 'zara', 'sk', 'you', 'ril', 'wiki', 'mo', 'gg', 'io', 'gr', 'aw', 'golf', 'md', 'ua', 'mls', 'gw', 'vip', 'au', 'tl', 'ice', 'cr', 'dish', 'ieee', 'jcb', 'mov', 'gmbh', 'data', 'cbs', 'bet', 'asia', 'pr', 'aig', 'gdn', 'er', 'tn', 'ug', 'rwe', 'jot', 'dhl', 'gop', 'nc', 'boo', 'cc', 'az', 'pwc', 'tr', 'lgbt', 'in', 'bbt', 'com', 'case', 'car', 're', 'wine', 'men', 'name', 'sale', 'gm', 'city', 'cw', 'fox', 'ltd', 'ma', 'talk', 'ist', 'si', 'food', 'kz', 'gy', 'ga', 'mlb', 'sohu', 'host', 'town', 'gay', 'sfr', 'farm', 'na', 'guru', 'arte', 'maif', 'ads', 'ke', 'fm', 'zm', 'edu', 'cy', 'ci', 'gal', 'here', 'bar', 'rw', 'bms', 'lb', 'sncf', 'us', 'loft', 'ses', 'zip', 'aaa', 'vana', 'so', 'cv', 'deal', 'pars', 'pf', 'fj', 'bcg', 'map', 'eat', 'gle', 'nyc', 'sm', 'tiaa', 'amex', 'saxo', 'diet', 'ir', 'arpa', 'mma', 'cfd', 'dj', 'ford', 'tel', 'cash', 'show', 'lat', 'dad', 'sj', 'ally', 'top', 'sbi', 'no', 'moe', 'tj', 'om', 'app', 'post', 'coop', 'desi', 'bi', 'gf', 'gh', 'bh', 'med', 'mom', 'bike', 'rs', 'bond', 'tm', 'bzh', 'gold', 'bz', 'gov', 'bo', 'wow', 'pm', 'pay', 'jobs', 'dnp', 'moi', 'page', 'ml', 'man', 'ms', 'porn', 'mn', 'blue', 'care', 'al', 'ren', 'red', 'ski', 'gea', 'ad', 'ooo', 'help', 'pro', 'ollo', 'ong', 'sn', 'ss', 'asda', 'cl', 'dot', 'cern', 'vi', 'life', 'prod', 'how', 'nra', 'tube', 'aco', 'phd', 'cat', 'itau', 'jnj', 'rsvp', 'dz', 'hr', 'ca', 'hot', 'shop', 'ht', 'cg', 'kids', 'ae', 'kpn', 'book', 'ntt', 'erni', 'rio', 'eg', 'law', 'voto', 'sarl', 'lk', 'lc', 'ky', 'luxe', 'vote', 'nico', 'aero', 'anz', 'teva', 'hbo', 'cab', 'hm', 'cool', 'pl', 'beer', 'goo', 'imdb', 'sony', 'ac', 'net', 'tax', 'sl', 'hiv', 'li', 'yt', 'bd', 'ups', 'ovh', 'wang', 'va', 'spot', 'uol', 'seat', 'nu', 'trv', 'pn', 'tz', 'bing', 'box', 'nhk', 'fly', 'run', 'sd', 'mx', 'afl', 'int', 'is', 'tt', 'se', 'ws', 'bw', 'ie', 'np', 'ai', 'toys', 'dk', 'as', 'cn', 'able', 'axa', 'goog', 'limo', 'cz', 'uy', 'cbre', 'fun', 'fund', 'dev', 'sg', 'rip', 'ping', 'jio', 'read', 'pg', 'next', 'live', 'wtc', 'za', 'wien', 'mba', 'art', 'info', 'bot', 'krd', 'fk', 'bt', 'id', 'ng', 'mh', 'jmp', 'nfl', 'xbox', 'foo', 'loan', 'pw', 'lol', 'bbc', 'la', 'pnc', 'je', 'vivo', 'pa', 'ceo', 'nab', 'cars', 'pk', 'fail', 'ki', 'ro', 'ge', 'skin', 'tui', 'docs', 'casa', 'sbs', 'chat', 'me', 'free', 'my', 'cd', 'ni', 'club', 'cm', 'fr', 'mp', 'pt', 'cba', 'cu', 'tjx', 'pru', 'sz', 'bank', 'hair', 'rest', 'st', 'am', 'fage', 'jeep', 'java', 'lidl', 'mc', 'cfa', 'tech', 'kn', 'game', 'sr', 'haus', 'spa', 'seek', 'wme', 'wf', 'ye', 'gd', 'cbn', 'guge', 'bf', 'kw', 'nr', 'zone', 'team', 'mt', 'crs', 'save', 'sas', 'xin', 'diy', 'sex', 'land', 'cf', 'star', 'sv', 'mtn', 'date', 'td', 'fi', 'play', 'dvag', 'qa', 'sina', 'mv', 'vn', 'ruhr', 'one', 'pin', 'ifm', 'hgtv', 'ing', 'nz', 'tk', 'bofa', 'vig', 'cafe', 'gl', 'cyou', 'eus', 'jm', 'lr', 'gent', 'gb', 'wtf', 'et', 'zero', 'lv', 'im', 'vg', 'kiwi', 'scb', 'fido', 'cal', 'taxi', 'audi', 'tf', 'bom', 'hk', 'pccw', 'zw', 'prof', 'win', 'bid', 'mg', 'shia', 'tc', 'baby', 'mint', 'vin', 'msd', 'visa', 'vu', 'plus', 'ggee', 'meet', 'army', 'icu', 'sb', 'jprs', 'inc', 'hsbc', 'joy', 'ru', 'open', 'sc', 'nf', 'ls', 'site', 'thd', 'do', 'hn', 'tci', 'esq', 'gift', 'fyi', 'scot', 'ba', 'pics', 'ngo', 'mil', 'room', 'kim', 'pet', 'qpon', 'lego', 'ps', 'immo', 'menu', 'xxx', 'aarp', 'got', 'ao', 'ck', 'hdfc', 'sew', 'gt', 'ec', 'bv', 'yoga', 'uno', 'by', 'kp', 'jp', 'gap', 'soy', 'bmw', 'ee', 'link', 'ar', 'love', 'jll', 'cpa', 'bb', 'rich', 'fish', 'cx', 'org', 'uk', 'onl', 'km', 'bcn', 'sexy', 'kpmg', 'mu', 'ax', 'sy', 'day', 'lpl', 'nrw', 'fiat', 'nba', 'aeg', 'band', 'eu', 'bj', 'ph', 'work', 'su', 'sa', 'vet', 'weir', 'ne', 'fan', 'tw', 'kh', 'mz', 'kia', 'mw', 'af', 'safe', 'now', 'moda', 'tdk', 'kr', 'dtv', 'frl', 'mr', 'ch', 'kfh', 'pub', 'tg', 'auto', 'it', 'akdn', 'citi', 'abb', 'mtr', 'ubs', 'shaw', 'kg', 'gq', 'obi', 'be', 'tab', 'best', 'meme', 'es', 'sh', 'mit', 'gbiz', 'news', 've', 'dclk', 'ibm', 'surf', 'tvs', 'ftr', 'lds', 'bbva', 'ott', 'viva', 'abc', 'bio', 'nike', 'sky', 'dell', 'kddi', 'eco', 'flir', 'mini', 'sx', 'bs', 'camp', 'bn', 'dds', 'sap', 'navy', 'hkt', 'bg', 'lt', 'gmx', 'arab', 'dog', 'rent', 'at', 'nec', 'buy', 'mq', 'film', 'aws', 'nl', 'gs', 'reit', 'llp', 'wed'}

def removeNonAscii(string):
    return string.encode('ascii', errors='ignore').decode()

def replaceLoop(content, oldt, newt, verbose = False, printNL = None):
    replCnt = content.count(oldt)
    while replCnt > 0:
        if verbose:
            print(replCnt, end=' ')
        content = content.replace(oldt, newt)
        replCnt = content.count(oldt)
    if verbose:
        print(replCnt, end=printNL)

    return content

def warnUnicode(content):
    i = 0
    didNL = False
    for b in content:
        if b >= 128:
            print(('' if didNL else '\n'), 'Bad byte:', b, 'offset:', i)
            didNL = True
        i += 1

def cleanUnicode(content):
    for i in range(len(content)):
        if content[i] >= 127 or content[i] < 32:
            content[i] = 32

def insertEmail(email, pid):
    email = email.lower()
    emails.add(email)
    print(email, len(emails), flush=True)

def getCompoundEmails(alltext, pid):
    '''Find compound emails in alltext like {name1 | name2}@cs.blah.edu'''

    alltext.replace('\n', ' ')
    alltext.replace('\r', ' ')
    alltext = replaceLoop(alltext, '  ', ' ', False, None)

    # print(alltext)
    for l in alltext.split('{'):
        if '}' in l:
            inbraces = l.split('}')[0]
            remain = l.split('}')[1]
            if remain and remain[0] == ' ':
                remain = remain[1:]
            if remain and remain[0] == '@':
                remain = remain.split('@')[1]
                remain = re.sub('[^0-9a-zA-Z@_\.\-]+', ' ', remain)
                domain = remain.split(' ')[0]
                print('GOT:', '{', inbraces, '} @', domain, flush=True) #'"', remain, '"',

                inbraces = inbraces.replace('|', ',')
                inbraces = inbraces.replace(', ', ',')
                inbraces = inbraces.replace(' ,', ',')
                inbraces = inbraces.replace(' ', ',')
                inbraces = inbraces.replace(',,', ',')
                # print('FIX:', '{', inbraces, '} @', domain, flush=True) #'"', remain, '"',
                for name in inbraces.split(','):
                    if name:
                        email = name + '@' + domain
                        email.replace(' ', '')
                        insertEmail(email, pid)

def getEmailsFromText(fname, pid=0):
    with open(fname, 'rb') as open_file:
        content2 = open_file.read()
        content = bytearray(content2)

    cleanUnicode(content)

    alltext = content.decode('utf-8')

    # Find all the lines with simple email address
    simpletext = re.sub('[^0-9a-zA-Z@_\.\-]+', ' ', alltext)

    for st in alltext.split(' '):
        if '@' in st and '.' in st:
            mobj = re.fullmatch(regex, st)
            if mobj:
                email = mobj.group(0)
                insertEmail(email, pid)

    getCompoundEmails(alltext, pid)

def getEmailsFromPdf(fname, pid):
    # print('file:', fname, flush=True)

    tempfname = 'temp' + str(pid) + '.txt'

    os.system('pdftotext -f 0 -l 1 -simple -nodiag -q "' + fname + '" ' + tempfname)

    getEmailsFromText(tempfname, pid)

def allFiles(dirs, allow_suffix = ''):
    '''Generates all files in the given directories and if allow_suffix is provided, filters it'''

    for dirPath in dirs:
        if os.path.isfile(dirPath) and (allow_suffix in dirPath or not allow_suffix):
            dirPath = removeNonAscii(dirPath)
            yield dirPath
        else:
            for root, dirs, filenames in os.walk(dirPath, topdown=True):
                dirs[:] = [d for d in dirs if d not in skipFolders]

                for f in filenames:
                    path = os.path.join(root, f)
                    path = removeNonAscii(path)
                    if os.path.isfile(path) and (allow_suffix in path or not allow_suffix):
                        yield path

def processFileList(file_chunk, func, args, pid):
    '''Helper function for processFilesParallel that takes a list of files and calls func on them serially'''

    for f in file_chunk:
        func(f, *args, pid)

    print('FINAL:', pid, len(emails), emails)
    with open('pdfemails' + str(pid) + '.txt', 'w') as fout:
        for e in emails:
            print(e, file = fout)

def processFilesParallel(dirs, allow_suffix, func, args, doParallel):
    '''Run func with args on all files in all dirs that contain allow_suffix in their name'''
    '''func must take filename as first arg.'''

    all_files = allFiles(dirs, allow_suffix)

    if doParallel:
        # Put generated files in list for hashing
        files = list(all_files)

        # Reorder the list of files arbitrarily to decorrelate the easy ones so thread workload is more uniform
        files = [y for x,y in sorted(zip([hashlib.md5(f.encode('utf-8')).hexdigest() for f in files], files))]

        # Parallel implementation
        core_count = multiprocessing.cpu_count()
        files_per_chunk = int((len(files) + core_count - 1) / core_count)
        file_chunks = [files[i * files_per_chunk:(i + 1) * files_per_chunk] for i in range(core_count)]

        processes = []
        for file_chunk in file_chunks:
            # file_chunk = file_chunk[0:10]
            p = multiprocessing.Process(target=processFileList, args=(file_chunk, func, args, len(processes)))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

    else:
        processFileList(all_files, func, args, 0)

def dohtml():
    files = allFiles({'.'}, '.htm')

    for f in files:
        getEmailsFromText(f)

    print(emails)

def dopdf():
    files = processFilesParallel({'pdf2'}, '', getEmailsFromPdf, (), True)

    print(emails)

def doUniqueTLDs():
    tryThese = ['edu', 'com', 'cn', 'tw', 'ca']
    with open('mpdfemails.txt') as f:
        for line in f:
            line = line.strip()
            tld = line.split('.')[-1]
            if tld not in TLDs:
                for tryTLD in tryThese:
                    if '.' + tryTLD in tld:
                        line = line.replace('.' + tld, '.' + tryTLD)
            tld = line.split('.')[-1]
            if tld not in TLDs:
                line = '.'.join(line.split('.')[:-1])
            tld = line.split('.')[-1]
            if tld not in TLDs:
                line = '.'.join(line.split('.')[:-1])
            tld = line.split('.')[-1]
            if tld not in TLDs:
                line = '.'.join(line.split('.')[:-1])
            tld = line.split('.')[-1]
            if tld not in TLDs:
                line = '.'.join(line.split('.')[:-1])
            print(line)

def makePersonNames():
    with open('ParticleMailingList.txt') as f:
        for line in f:
            line = line.strip()
            first = ''
            last = ''
            if '.' in line.split('@')[0] and len(line.split('@')[0].split('.')) >= 2:
                first = line.split('@')[0].split('.')[0]
                last = line.split('@')[0].split('.')[1]
                first = re.sub('[^a-zA-Z]+', '', first)
                last = re.sub('[^a-zA-Z]+', '', last)
            print(line.lower(), first.title(), last.title(), sep=',')

if __name__ == '__main__':
    # doUniqueTLDs()
    #  dopdf()
    makePersonNames()
