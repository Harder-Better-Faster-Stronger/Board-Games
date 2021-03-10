from random import choice
from sys import argv

from board_square import BoardSquare, UrPiece

WHITE='White'
BLACK='Black'

class RoyalGameOfUr:
    STARTING_PIECES = 7

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'], rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]

                for i in self.board:
                    for j in i:
                        if j.entrance==BLACK:
                            UrPiece.BlackStarts.append(j)
                        if j.entrance==WHITE:
                            UrPiece.WhiteStarts.append(j)
                        if j.exit==BLACK:
                            UrPiece.BlackEnds.append(j)
                        if j.exit==WHITE:
                            UrPiece.WhiteEnds.append(j)

        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def take_turn(self,player=WHITE,ros=False):
        self.display_board()
        roll=self.roll_d4_dice()
        print("You rolled {}".format(roll))
        if ros:
            print("You have landed on a rosette, go again.")
        if player==WHITE:
            num=1
            for piece in self.WhitePieces:
                if piece.complete:
                    pass
                if piece.can_move(roll):
                    string= "currently off the board" if piece.position==None else piece.position.position
                    print(num,piece.symbol,string)
                    num+=1
            for piece in self.WhitePieces:
                if piece.complete:
                    print(piece.symbol,"has completed the race.")
            if num==1 or roll==0:
                print("No more move")
                return
            choice=input("Which move do you wish to make? ")
            while not choice.isnumeric() or int(choice)<=0 or int(choice)>=num:
                choice=input("Sorry, that wasn't a valid selection, which move do you wish to make? ")
            current_pos=None
            choice=int(choice)
            for piece in self.WhitePieces:
                if piece.complete:
                    pass
                if piece.can_move(roll):
                    choice-=1
                    if choice==0:
                        if piece.position==None:
                            piece.position=UrPiece.WhiteStarts[0]
                            piece.move(roll-1)
                        else:
                            piece.move(roll)
                        current_pos=piece.position
            if current_pos and current_pos.rosette:
                self.take_turn(ros=True)

        elif player==BLACK:
            num=1
            for piece in self.BlackPieces:
                if piece.complete:
                    pass
                if piece.can_move(roll):
                    string= "currently off the board" if piece.position==None else piece.position.position
                    print(num,piece.symbol,string)
                    num+=1
            for piece in self.BlackPieces:
                if piece.complete:
                    print(piece.symbol,"has completed the race.")
            if num==1 or roll==0:
                print("No more move")
                return
            choice=input("Which move do you wish to make?")
            while not choice.isnumeric() or int(choice)<=0 or int(choice)>=num:
                choice=input("Sorry, that wasn't a valid selection, which move do you wish to make? ")
            current_pos=None
            choice=int(choice)
            for piece in self.BlackPieces:
                if piece.complete:
                    pass
                if piece.can_move(roll):
                    choice-=1
                    if choice==0:
                        if piece.position==None:
                            piece.position=UrPiece.BlackStarts[0]
                            piece.move(roll-1)
                        else:
                            piece.move(roll)
                        current_pos=piece.position
            if current_pos and current_pos.rosette:
                self.take_turn(player=BLACK,ros=True)

    def check_winner(self,player=WHITE):
        if player==WHITE:
            for p in self.WhitePieces:
                if not p.complete:
                    return False
            return True
        if player==BLACK:
            for p in self.BlackPieces:
                if not p.complete:
                    return False
            return True

    def play_game(self):
        """
            Your job is to recode this function to play the game.
        """
        if not self.board:
            print("You must load the board.")
        # init urpiece
        self.WhitePieces=[UrPiece(WHITE,'W{}'.format(i)) for i in range(1,self.STARTING_PIECES+1)]
        self.BlackPieces=[UrPiece(BLACK,'B{}'.format(i)) for i in range(1,self.STARTING_PIECES+1)]
        # input name
        name1=input("What is your name? ")
        print(name1,"you will play as white.")
        name2=input("What is your name? ")
        print(name2,"you will play as black.")
        running=True
        while running:
            self.take_turn()
            if self.check_winner():
                print(name1,"win the game.")
                return
            self.take_turn(player=BLACK)
            if self.check_winner(player=BLACK):
                print(name2,"win the game.")
                return 

if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()
