import itertools
import string
import collections
import time
import copy
leaves = open("leaves.txt").read().split()
leavesDict = {leaves[i]:float(leaves[i+1]) for i in range(0, len(leaves), 2)}
leavesDict[''] = 0
diphths = [["".join(i) for i in itertools.permutations(list(string.ascii_uppercase), 2)] + \
                                        [j*2 for j in string.ascii_uppercase]][0]
subdicts = {diphth: set(open("resources/" + diphth + ".txt").read().split()) \
                         for diphth in diphths}

regBoard=[[" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O "],
                      ['01', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS'],
                      ['02', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'DWS', ' '],
                      ['03', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
                      ['04', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
                      ['05', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
                      ['06', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'B', ' ', ' ', ' ', 'TLS', ' '],
                      ['07', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', 'A', ' ', ' ', 'DLS', ' ', ' '],
                      ['08', 'TWS', ' ', ' ', 'DLS', ' ', ' ', 'B', 'A', 'G', 'S', ' ', 'DLS', ' ', ' ', 'TWS'],
                      ['09', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', 'E', ' ', ' ', 'DLS', ' ', ' '],
                      ['10', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' '],
                      ['11', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
                      ['12', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
                      ['13', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
                      ['14', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'DWS', ' '],
                      ['15', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS']]

extraList=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
         "TWS", "DWS", "TLS", "DLS", \
         "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", \
         "*", " "]
class Move():
    def __init__(self, word, board, row, column, direction, prevBoard, \
                 doNotScoreWord = False, revWordWhenScoring = True):
        self.word = word
        self.board = board
        self.row = row
        self.col = column
        self.direction = direction
        self.prevBoard = prevBoard
        self.dnsw = doNotScoreWord
        self.rwws = revWordWhenScoring
        
    def comp(self, other):
        return self.score+self.valuation>other.score+other.valuation

    def getScore(self):
        self.score = self.prevBoard.getScore(self)
        return self.score
    def getEvaluation(self, rack):
        nR = rack[:]
        for letter in self.word:
            try:
                nR.remove(letter)
            except:
                pass #through-words & to-words, ??
        self.valuation = leavesDict[''.join(i for i in sorted(nR))]
        return self.valuation
class Board():
    def __init__(self, board=None):
        if board is None:
            self.board = regBoard
        else:
            self.board = board
        self.subdicts = subdicts
        self.extraList = extraList

    def checkWord(self, word):
        if len(word) > 1:
            try:
                if word.upper() in self.subdicts[word[:2]]:
                    return True
                return False
            except:
                return False
        return False

    def getWords(self, board):
        words = []
        uai = [] #used across indexes
        udi = [] #used down indexes
        #Iterate through; find a letter -> follow right/down
        c = 0
        for (rIndex, row) in enumerate(board):
            for (cIndex, col) in enumerate(row):
                if col not in self.extraList:
                    nR, nC = rIndex, cIndex
                    word=collections.OrderedDict()
                    while uai.count((nR, nC))<1 and \
                          nR < len(board) and nC < len(board[nR]) and \
                          board[nR][nC] not in self.extraList:
                        letter = board[nR][nC]
                        if word.get(letter):
                            letter += str(c) #differentiate
                            c += 1
                        word[letter] = (nR, nC)
                        uai.append((nR, nC))
                        nC += 1
                    if len(word)>1:
                        words.append(word)
##                    else:
##                        for index in word.values():
##                            uai.remove(index)
                    
                    nC = cIndex #reset horizontal index
                    word=collections.OrderedDict()
                    while udi.count((nR, nC))<1 and \
                          nR < len(board) and nC < len(board[nR]) and \
                          board[nR][nC] not in self.extraList:
                        letter = board[nR][nC]
                        if word.get(letter):
                            letter += str(c) #differentiate
                            c += 1
                        word[letter] = (nR, nC)
                        udi.append((nR, nC))
                        nR += 1
                    if len(word)>1:
                        words.append(word)
##                    else:
##                        for index in word.values():
##                            udi.remove(index)

        return words

    
    def expandFrom(self, point, places, extendedFrom, ):
        assert point not in extendedFrom
        
        usedPlaces = [point]
        
        rT, cT = point
        cT += 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            cT += 1
            
        cT = point[1]
        cT -= 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            cT -= 1

        cT = point[1]
        rT += 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            rT += 1

        rT = point[0]
        rT -= 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            rT -= 1
        return usedPlaces
    
    def removeDuplicates(self, oldList):
        newList = []
        for item in oldList:
          if item not in newList:
            newList.append(item)
        oldList = newList
        return newList
    
    def checkBoard(self, board):
        if board[0] != [" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O "]:
            return False
        if [i[0] for i in board] != [' ', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']:
            return False
        if board[8][8] == "*":
            return False
        
        words = self.getWords(board)
        correctWords = [word for word in words if self.checkWord(''.join(letter[0] for letter in word.keys()))]
        if len(correctWords) < len(words):
            return False
        word=correctWords
        
        places = [value for word in words for value in word.values()]
        top = places[0]
        extendedFrom = []
        usedPlaces = self.expandFrom(top, places, extendedFrom)
        l = [coord for place in places for coord in place]
        #Extend to the edge of the board
        for j in range(min(l), max(l)+1):
            np = usedPlaces[:]
            for i in np:
                try:
                    usedPlaces.extend(self.expandFrom(i, places, extendedFrom))
                    usedPlaces = self.removeDuplicates(usedPlaces)
                    extendedFrom.append(i)
                  #  if sorted(usedPlaces) == sorted(places):
                        #return True
                except AssertionError:
                    pass
                
        #if any place wasn't used return false
        for place in places:
            if place not in usedPlaces:
                return False
        return True
    
    def getPlaces(self, board):
        words = [word for word in self.getWords(board) if self.checkWord(''.join(letter[0] for letter in word.keys()))]
        places = [value for word in words for value in word.values()]
        return places

    def getScore(self, move):
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
                   "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
                   "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
                   "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
                   "x": 8, "z": 10}
        oldWords = self.getWords(self.board)
        allWords = self.getWords(move.board.board)
        newWords = []
        for word in allWords:
            if word not in oldWords:
                newWords.append(word)
                
        wordScore = 0
        wordMult = 1
        scored = []
        if not move.dnsw:
            if move.rwws:
                sw = reversed(move.word)
                im = 1
            else:
                sw = move.word
                im = -1
            for (index, letter) in enumerate(sw):
                row = move.row
                col = move.col
                
                if move.direction == 'D':
                    row -= index*im
                else:
                    col -= index*im
                    
                lettMult = 1
                oldLetter = self.board[row][col]
                if oldLetter in ['TLS', 'DLS']:
                    lettMult *= ['D', 'T'].index(oldLetter[0])+2
                elif oldLetter in ['TWS', 'DWS']:
                    wordMult *= ['D', 'T'].index(oldLetter[0])+2
                elif oldLetter == '*':
                    wordMult *= 2
                wordScore += self.scores[letter.lower()] * lettMult

                scored.append((row, col))
            wordScore *= wordMult

        for word in newWords:
            if ''.join(letter[0] for letter in word.keys()) != move.word: #fix for same auxillary words
                #print(word, move.word)
                auxWordScore = 0
                auxWordMult = 1
                for (letter, place) in word.items():
                    lettMult = 1
                    letter = letter[0]
                    row, col = place
                    oldLetter = self.board[row][col]
                    if oldLetter in ['TLS', 'DLS']:
                        lettMult *= ['D', 'T'].index(oldLetter[0])+2
                    elif oldLetter in ['TWS', 'DWS']:
                        auxWordMult *= ['D', 'T'].index(oldLetter[0])+2
                    auxWordScore += self.scores[letter.lower()] * lettMult
                auxWordScore *= auxWordMult
                wordScore += auxWordScore
        if len(move.word) == 7:
            wordScore += 50 #Bingo!
        return wordScore
                    
        
class CPU():
    def __init__(self, rack):
        self.board = Board()
        self.rack = rack
        self.checkWord = self.board.checkWord
        self.extraList = self.board.extraList
        
    def gacc(self, iterable, maxDepth):
        allWords = []
        for depth in range(2, maxDepth + 1): 
            for word in itertools.permutations(iterable, depth):
                allWords.append("".join(word))
                
        if len(allWords)>0:
            allWords.pop(0)
        correctWords = []
        for word in allWords:
            if self.checkWord(word):
                correctWords.append(word)

        return correctWords
    
    def displayBoard(self, board):
        
        count = 0
        text = "-"*64
        text += "\n"
        text += "|"
        for i in range(16):
            line = board[i]
            for j in line:
                if j == " ":
                    if i == 0:
                        j = "  "
                    else:
                        j = "   "
                if (j[0] in string.ascii_uppercase  or j == "*") and len(j) < 3:
                    j = " " + j[0] + " "
                text += j
                text += "|"
                count += 1
                if count == 16 and i != 15:
                    text += "\n"
                    text += "-" * 64
                    text += "\n"
                    text += "|"
                    count = 0
        text += "\n"
        text += "-" * 64
        text += "\n"
        print(text)

    def takeTurn(self):
        prevBoard = self.rNab()
        words = self.board.removeDuplicates(self.gacc(self.rack, len(self.rack)))
        
        places = self.board.getPlaces(self.board.board)
        plays = []
        neighbors = []

        if places == []:
            for i in range(1, 15):
                places.append((i, 8))
                places.append((8, i))
        across, down = [], []
        for place in places:
            r, c = place
            neighbors.append((r+1,c))
            neighbors.append((r-1,c))
            neighbors.append((r,c+1))
            neighbors.append((r,c-1))
        neighbors = self.board.removeDuplicates(neighbors)
        for word in words:
            for neighbor in neighbors:
                rIndex, cIndex = neighbor
                for direc in ['A', 'D']:
                    newBoard = self.rNab()
                    if self.playWord(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard)
                        #play.getScore()
                        #play.getEvaluation(self.rack)
                        plays.append(play)
                        continue
                        
                    newBoard = self.rNab()
                    if self.playWordOpp(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, revWordWhenScoring=False)
                        #play.getScore()
                        #play.getEvaluation(self.rack)
                        plays.append(play)
                #print(word, neighbor, "done", len(plays))

        for (d, row) in enumerate(self.board.board[1:]):
            for play in self.complete(self.slotify(row[1:]), 'A', d+1):
                #play.getScore()
                #play.getEvaluation(self.rack)
                plays.append(play)
        columns = [[row[i] for row in self.board.board[1:]] for i in range(len(self.board.board))]
        for (d, col) in enumerate(columns):
            for play in self.complete(self.slotify(col), 'D', d):
                #play.getScore()
                #play.getEvaluation(self.rack)
                plays.append(play)               
        return plays

    def proxyBoard(self):
        return Board(copy.deepcopy(self.board.board))

    def playWord(self, word, row, col, direc, board):
        for letter in reversed(word):
            if row>15 or col>15:
                return False
            if board.board[row][col] in string.ascii_uppercase:
                return False
            board.board[row][col] = letter
            if direc=='A':
                col -= 1
            else:
                row -= 1
        if board.checkBoard(board.board):
            return True
        return False

    def playWordOpp(self, word, row, col, direc, board, skip=False):
        i = 0
        #for letter in word:
        while i < len(word)-1:
            if row>15 or col>15:
                return False
            if board.board[row][col] in string.ascii_uppercase:
                if skip:
                    i -= 1
                else:
                    return False
            else:
                board.board[row][col] = word[i]
            if direc=='A':
                col += 1
            else:
                row += 1
            i += 1
        if board.checkBoard(board.board):
            return True
        return False
    
    def rNab(self):
        #nbo = []
       # for row in self.board.board:
        #  nbo.append([col for col in row])
        return Board([[col[:] for col in row] for row in self.board.board])

    def gac(self, iterable, maxDepth):
        allWords = []
        for depth in range(1, maxDepth + 1): 
            for word in itertools.permutations(iterable, depth):
                allWords.append("".join(word))
        return allWords
    
    def place(self, slot, pos, word, direc, depth):
        slot, reps = slot
        currPos = pos
        newSlot = list(slot)

        index = 0
        w=False
        while index < len(word)-1:
            newPos = currPos + index
            if newSlot[newPos] != '.':
                currPos += 1
                index -= 1
            else:
                newSlot[newPos] = word[index]
                if not w:
                    wordPos = currPos+index
                    w=True
            index += 1
        if w:
            wordPos += 1
        else:
            return False
        #print(wordPos == slot.index(slot.strip('.')[0]))
        newSlot = ''.join(letter for letter in newSlot)
        if not all(self.checkWord(i) for i in newSlot.strip('.').split('.') if i != ''):
            return False
        
        newBoardSlot = []
        for (index, newLetter) in enumerate(newSlot):
            if newLetter == '.':
                newBoardSlot.append(reps[index])
            else:
                newBoardSlot.append(newLetter)
        newBoard = self.rNab()
        oldBoard = self.rNab()
        row, col = depth, depth
        if direc == 'A':
            newBoardSlot.insert(0, str(depth).zfill(2))
            newBoard.board[depth] = newBoardSlot[:]
            col = wordPos
        else:
            for (index, row) in enumerate(newBoard.board[1:]):
                row[depth] = newBoardSlot[index]

            row = wordPos
        move = Move(word, newBoard, row, col, direc, oldBoard, doNotScoreWord=True)
        if move.board.checkBoard(move.board.board):
            return move
        return False
        
    def complete(self, slot, direc, depth):
        if depth==0:
            return []
        words = self.board.removeDuplicates(self.gac(self.rack, 7))
        newSlots = []
        slotForLen = slot[0]
        if slotForLen != '...............':
            edgeFinder = [i[0] for i in enumerate(slotForLen) if i[1] !='.']
            for word in words:
                for pos in range(edgeFinder[0], edgeFinder[-1]+len(word)+1):
                    if pos-len(word) in range(len(slotForLen)):
                        if slotForLen[pos-len(word)] == '.':
                        #    if direc == 'A':
                           #     r, c = depth, slotForLen.index(slotForLen.strip('.')[0])
                       #     else:
                               # r, c = slotForLen.index(slotForLen.strip('.')[0]), depth
                         #    newb=self.rNab()
                          #  if self.playWordOpp(word, r, c, direc, newb,     skip=True):
                                #self.displayBoard(newBoard.board)
                               #newSlots.append(Move(word, newb, r, c, direc, self.rNab(), doNotScoreWord=True))
                            newSlots.append(self.place(slot, pos-len(word), word, direc, depth))
                           # if newSlot:
                            #newSlots.append(newSlot)
        return newSlots

    def slotify(self, slot):
        slotForReps = slot
        slot = ''.join(i for i in slot)
        slot = slot.replace(' ', '.')
        for i in self.extraList:
            slot = slot.replace(i, '.')
        #print(slot)
        return slot, slotForReps

    #Theoretical optimization functions
    def asw(self, word):
        if word[:2] in vsd:
            return True
        return False
    
    def aew(self, word):
        if word[-2:] in ved:
            return True
        return False
    
c = CPU([i for i in 'AWS'])
c.displayBoard(c.board.board)
q=0
for i in range(10):
    h = time.time()
    d=c.takeTurn()
    e=time.time()-h
    print(e)
    q+=e
print(q/10)
for i in d:
    pass
    if i:
        pass
        #c.displayBoard(i.board.board)
##for i in c.takeTurn():
##    c.displayBoard(i.board.board)
##    #print(i.score, i.valuation)
##    #print(i.row, i.col)
##    #print(i.board.board[i.row])
##    #print(i.board.board[i.row][i.col])
##    #print(i.dnsw, i.rwws)
'''            try: newSlot[newPos]
            except:
                print(pos)
                print(word)
                print(slot)
                print(currPos, index)
                print(pos+len(word), len(slot))
                print(newSlot, len(newSlot))'''