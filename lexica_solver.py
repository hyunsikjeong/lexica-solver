import copy
import urllib.request
import os.path
import json
import time

### INPUT ###

infile = open("input.txt", "r")
whole = infile.read()
infile.close()

board = whole[10:16] + "\n" + whole[19:25] + "\n" + whole[28:34] + "\n" + whole[37:43] + "\n" + whole[46:52] + "\n" + whole[55:61]

vertical = [[whole[1], whole[64]], [whole[2], whole[65]], [whole[3], whole[66]], [whole[4], whole[67]], [whole[5], whole[68]], [whole[6], whole[69]]]
horizontal = [[whole[9], whole[16]], [whole[18], whole[25]], [whole[27], whole[34]], [whole[36], whole[43]], [whole[45], whole[52]], [whole[54], whole[61]]]

# start_time = time.time()

### INPUT ###

### CODE ###

checked_yes = set()
checked_no = set()

checked_yes.add("cote")
checked_yes.add("fewer")
checked_yes.add("banyan")
checked_yes.add("agar")

def word_checker(word):
    if len(word) <= 2:
        return True
    if word in checked_yes:
        return True
    elif word in checked_no:
        return False

    if word[-2:] == "er":
        if word_checker(word[:-1]) or word_checker(word[:-2]):
            checked_yes.add(word)
            return True
        if len(word)>=5 and word[-3] == word[-4] and word_checker(word[:-3]):
            checked_yes.add(word)
            return True
        if len(word)>=4 and word[-3] == 'i' and word_checker(word[:-3] + 'y'):
            checked_yes.add(word)
            return True
        
    if word[-3:] == "est":
        if word_checker(word[:-2]) or word_checker(word[:-3]):
            checked_yes.add(word)
            return True
        if len(word)>=6 and word[-4] == word[-5] and word_checker(word[:-4]):
            checked_yes.add(word)
            return True
        if len(word)>=5 and word[-4] == 'i' and word_checker(word[:-4] + 'y'):
            checked_yes.add(word)
            return True

    url = "http://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=" + word
    res = urllib.request.urlopen(url)
    res = json.loads(res.read())
    
    if res["count"] > 0:
        checked_yes.add(word)
        return True
    else:
        checked_no.add(word)
        return False

def transpose(board):
    temp = board.split('\n')
    for i in range(6):
        temp[i] = list(temp[i])

    ret = [ [], [], [], [], [], [] ]
    for i in range(6):
        for j in range(6):
            ret[i].append( temp[j][i] )
        ret[i] = "".join(ret[i])
    return "\n".join(ret)

class gameboard:
    def __init__(self, board, vertical, horizontal):
        self.board = copy.deepcopy(board)
        self.vertical = copy.deepcopy(vertical)
        self.horizontal = copy.deepcopy(horizontal)
        self.debug = False

    def set_debug(self, value):
        if value is True or value is False:
            self.debug = value

    def horizontal_checker(self, line):
        temp = self.board[line*7:line*7+6].split("*")
        for i in range(len(temp)):
            if not word_checker(temp[i]):
                return False
        return True

    def checker(self):
        if self.board.find("_") != -1:
            return False

        temp = self.board.replace("\n", "*").split("*")
        for i in range(len(temp)):
           if not word_checker(temp[i]):
                return False

        temp = transpose(self.board).replace("\n", "*").split("*")
        for i in range(len(temp)):
            if not word_checker(temp[i]):
                return False

        return True

    #every horizontal line,
    #1. fill the horizontal letters
    #2. fill the vertical letters
    #3. check the horizontal line.
    #4. pass, then next line
    #5. If the final line, run it in the checker

    def solve_1(self, line, idx):
        if self.debug:
            print("Solving: state 1, line " + str(line) + " idx " + str(idx) + "\n")
            print(self.board)

        if line == 6:
            return self.checker()
            
        if idx == 6:
            for i in range(len(self.horizontal[line])):
                if self.horizontal[line][i] != '#':
                    return False
            return self.solve_2(line, 0)
        
        if self.board[line*7+idx] == '_':
            if self.solve_1(line,idx+1):
                return True
            for i in range(len(self.horizontal[line])):
                if self.horizontal[line][i] == '#':
                    continue
                t = self.horizontal[line][i]
                self.horizontal[line][i] = '#'
                self.board = self.board[:line*7+idx] + t + self.board[line*7+idx+1:]
                if self.solve_1(line,idx+1):
                    return True
                self.board = self.board[:line*7+idx] + '_' + self.board[line*7+idx+1:]
                self.horizontal[line][i] = t
            return False
        else:
            return self.solve_1(line, idx+1)

    def solve_2(self, line, idx):
        if self.debug:
            print("Solving: state 2, line " + str(line) + " idx " + str(idx) + "\n")
            print(self.board)
            
        if idx == 6:
            for i in range(6):
                if self.board[line*7+i] == '_':
                    return False
            if self.horizontal_checker(line):
                return self.solve_1(line+1, 0)
            return False
            
        if self.board[line*7+idx] == '_':
            for i in range(len(self.vertical[idx])):
                if self.vertical[idx][i] == '#':
                    continue
                t = self.vertical[idx][i]
                self.vertical[idx][i] = '#'
                self.board = self.board[:line*7+idx] + t + self.board[line*7+idx+1:]
                if self.solve_2(line, idx+1):
                    return True
                self.board = self.board[:line*7+idx] + '_' + self.board[line*7+idx+1:]
                self.vertical[idx][i] = t
            return False
        else:
            return self.solve_2(line, idx+1)

    def solve(self):
        return self.solve_1(0, 0)

    def print(self):
        print(self.board)

    def get_board(self):
        return self.board

        

gb = gameboard(board, vertical, horizontal)
#gb.set_debug(True)
print(gb.solve())
gb.print()

with open("output.txt","w") as f:
    f.write( gb.get_board() )

"""
if gb.solve():
    infile = open("boards/" + str(num) + "_in.txt", "w")
    infile.write(whole)
    infile.close()
    outfile = open("boards/" + str(num) + "_out.txt", "w")
    outfile.write(gb.get_board())
    outfile.close()
"""

#print(time.time()-start_time)
