class UrPiece:
    WhiteEnds = []
    BlackEnds = []
    WhiteStarts = []
    BlackStarts = []

    def __init__(self, color, symbol):
        self.color = color
        self.position = None
        self.complete = False
        self.symbol = symbol

    def find_moves_end(self, num_moves):
        position = self.position
        if not position:
            return None
        while num_moves > 0:
            if self.color == 'White':
                position = position.next_white
            else:
                position = position.next_black
            if position == None:
                return None
            num_moves -= 1
        return position

    def can_move(self, num_moves):
        if self.color == 'White':
            # Code for white
            end = None
            # position is none
            if self.position == None:
                # finished
                if self.complete:
                    return False
                # not finished
                else:
                    self.position = UrPiece.WhiteStarts[0]
                    end = self.find_moves_end(num_moves-1)
                    self.position = None
            else:
                end = self.find_moves_end(num_moves)
            # We now get the end, now we need to check rosette and exit
            # deal with start
            if self.position in UrPiece.WhiteStarts:
                end = self.find_moves_end(num_moves-1)
            # deal with exit
            if self.find_moves_end(num_moves-1) in UrPiece.WhiteEnds:
                return True
            # deal with normal condition
            # We have piece at end position
            if end == None:
                return False
            if end.piece:
                if end.piece.color == self.color:
                    return False
                else:
                    if end.rosette:
                        return False
                    else:
                        return True
            else:
                return True
        elif self.color == 'Black':
            # Code for white
            end = None
            # position is none
            if self.position == None:
                # finished
                if self.complete:
                    return False
                # not finished
                else:
                    self.position = UrPiece.BlackStarts[0]
                    end = self.find_moves_end(num_moves-1)
                    self.position = None
            else:
                end = self.find_moves_end(num_moves)
            # We now get the end, now we need to check rosette and exit
            # deal with start
            if self.position in UrPiece.BlackStarts:
                end = self.find_moves_end(num_moves-1)
            # deal with exit
            if self.find_moves_end(num_moves-1) in UrPiece.BlackEnds:
                return True
            # deal with normal condition
            # We have piece at end position
            if end == None:
                return False
            if end.piece:
                if end.piece.color == self.color:
                    return False
                else:
                    if end.rosette:
                        return False
                    else:
                        return True
            else:
                return True

    def move(self,num_moves):
        end=self.find_moves_end(num_moves)
        self.position.piece=None
        self.position=end
        if self.position:
            if self.position.piece:
                print(self.position.piece.symbol,"has been knocked off")
                self.position.piece.position=None
            self.position.piece=self
        else:
            print(self.symbol,"has finished the race!")
            self.complete=True

class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black, 'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
