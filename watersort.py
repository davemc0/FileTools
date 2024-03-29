#!python

import copy
import random

n4 = 4
level31 = ['PpgB', 'BGPb', 'ogvB', 'boop', 'prrv', 'gGoB', 'bPrg', 'GrGv', 'Pvbp', '', '']
level37 = ['GBgv', 'ggPv', 'prvo', 'GPbb', 'brBG', 'roBr', 'vbPp', 'Goop', 'BPpg', '', '']
level50 = ['ogPv', 'pppr', 'gPgb', 'vobB', 'BPbv', 'pGbB', 'gPro', 'GvGr', 'GoBr', '', '']
level52 = ['gppr', 'Bvbb', 'vvPG', 'bGBr', 'gorB', 'gGPg', 'PPor', 'oboB', 'Gpvp', '', '']
level105= ['BGbb', 'Ppgv', 'oPrd', 'opro', 'GryB', 'yGdG', 'dPrl', 'lPpl', 'gvbB', 'dyvg', 'vylB', 'gbpo', '', '']
level874= ['grbB', 'bobr', 'rlpo', 'PBgp', 'lgbl', 'BGpl', 'oGBg', 'Popr', 'PGGP', '', '']

# g grey
# r red
# b light blue
# B dark blue
# o orange
# l light green
# p pink
# P purple
# G dark green

def getParams():
    global vials

    #print('How many vials? >', end='')
    #nVials = int(input())
    nVials = -1

    if nVials == -1:
        vials = level874
        return

    vials = ['' for v in range(nVials)]

    print('Enter colors of each vial as letters, starting from top-most non-empty.')
    for v in range(nVials):
        while True:
            print('Enter vial', v, '> ', end='')
            vials[v] = str(input())
            if len(vials[v]) > n4:
                print('Error. Length was', len(vials[v]))
            else:
                break
        print('vials[', v, '] = "', ' ' * (n4-len(vials[v])) + vials[v], '"', sep='')

def doMove(fromV, toV, lVials):
    '''Pour from vial fromV into vial toV'''

    didMove = False
    fromS = lVials[fromV]
    toS = lVials[toV]

    # print(fromS, toS)
    while len(fromS) > 0 and len(toS) < n4 and (len(toS)==0 or toS[0] == fromS[0]) and fromV != toV:
        toS = fromS[0] + toS
        fromS = fromS[1:]
        # print(fromS, toS)
        didMove = True

    lVials[fromV] = fromS
    lVials[toV] = toS

    return (didMove, lVials)

def isFinished(lVials):
    '''Return true if the board is solved, else false'''

    for vial in lVials:
        if len(vial) == 0:
            continue
        if len(vial) != n4:
            return False
        #print(vial, lVials)
        for c in vial[1:]:
            #print(c, vial[0])
            if c != vial[0]:
                #print('bbye')
                return False

    return True

def printGame(game):
    print('Solved it in', len(game), 'moves.')
    print('init:', vials)

    for fromV, toV, lVials in game:
        print(fromV, '->', toV, lVials)
    print()

def solveRandomly():
    global vials
    random.seed()
    bestGame = []

    while True:
        lVials = copy.deepcopy(vials)
        moves = 0
        tries = 0
        thisGame = []

        #print(lVials)
        while not isFinished(lVials) and tries < 5000 and moves < 60 and (moves < len(bestGame) or not bestGame):
            fromV = random.randrange(len(lVials))
            toV = random.randrange(len(lVials))
            # print(fromV, toV)
            (moved, lVials) = doMove(fromV, toV, lVials)
            if moved:
                moves += 1
                #print(fromV, '->', toV, lVials, tries, moves)
                thisGame.append((fromV, toV, copy.deepcopy(lVials)))
            tries += 1

        if isFinished(lVials):
            print(tries, len(thisGame))
            if len(thisGame) < len(bestGame) or not bestGame:
                bestGame = thisGame
                thisGame = []
                printGame(bestGame)
            #break
        else:
            #print("Couldn't solve it in", tries, 'tries and', moves, 'moves.')
            #print('.', end='')
            pass

def play():
    global vials

    while True:
        print('\n', vials, sep='')
        print('Pour from vial >', end='')
        fromV = int(input())
        print('Pour to vial >', end='')
        toV = int(input())
        (moved, vials) = doMove(fromV, toV, vials)
        print('Poured.' if moved else "Didn't pour.")
        if isFinished(vials):
            print(vials, 'You won!')
            break

def validate():
    global vials

    letterCnt = {}

    for vial in vials:
        for letter in vial:
            if letter not in letterCnt:
                letterCnt[letter] = 1
            else:
                letterCnt[letter] += 1

    if not all([letterCnt[letter] == 4 for letter in letterCnt]):
        print('Invalid vials:', letterCnt)
        exit()

def main():
    global vials
    getParams()
    validate()
    #play()
    solveRandomly()

if __name__ == '__main__':
    main()
