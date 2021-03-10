from board_methods import load_map, display_board
from sys import argv
from random import randint, seed
import random


STARTING_FUNDS = 1500
BOARD_FILE_NAME = 'proj1_board1.csv'

PLAYER_SYMBOL = 'symbol'
PROPERTIES = 'properties'
MONEY = 'money'
PLAYER_NAME = 'player-name'
POSITION = 'Position'

ABBREVIATION = 'Abbrev'
PASS_GO_MONEY = 200
PLACE = 'Place'
THE_BANK = 'BANK'
OWNER = 'Owner'
PRICE = 'Price'
RENT = 'Rent'
BUILDING_RENT = 'BuildingRent'
BUILDING = 'Building'
BUILDING_COST = 'BuildingCost'
PROP_INFO = '\n\t{}\n\tPrice: {}\n\tOwner: {}\n\tBuilding: {}\n\tRent {}, {} (with building)\n'
PLAYER_INFO = '\nPlayer Name: {}\nPlayer Symbol: {}\nCurrent Money: {}\n\nProperties Owned:\n'

QUIT_STRING = 'quit'
# Global Variables
STARTING_FUND = 1500

def create_player(player_num, starting_money):
    name=input(player_num+", what is your name? ")
    symbol=input(player_num+", what symbol do you want your character to use? ")
    while len(symbol)!=1 or symbol.islower():
        symbol=input(player_num+", what symbol do you want your character to use? ")
    player={
        PLAYER_NAME:name,
        PLAYER_SYMBOL:symbol,
        MONEY:starting_money,
        POSITION:0,
        PROPERTIES:[]
    }
    return player


def eliminate_players(player_list):
    keep_players = []

def roll_dice():
    return random.randint(1,6)+random.randint(1,6)

def format_display(players, board):
    '''
    :param players:
    :param board:
    :return: a list of strings which will be displayed at each board position.
    '''
    player1_pos=players[0][POSITION]
    player2_pos=players[1][POSITION]
    str_list=[]
    if player1_pos==player2_pos:
        for index,building in enumerate(board):
            if index==player1_pos:
                str_list.append(building[ABBREVIATION].ljust(5)+"\n"+players[0][PLAYER_SYMBOL]+players[1][PLAYER_SYMBOL])
            else:
                str_list.append(building[ABBREVIATION].ljust(5)+"\n")
    else:
        for index,building in enumerate(board):
            if index==player1_pos:
                str_list.append(building[ABBREVIATION].ljust(5)+"\n"+players[0][PLAYER_SYMBOL])
            elif index==player2_pos:
                str_list.append(building[ABBREVIATION].ljust(5)+"\n"+players[1][PLAYER_SYMBOL])
            else:
                str_list.append(building[ABBREVIATION].ljust(5)+"\n")
    return str_list

def display_property(board):
    name=input("For which property do you want to get the information? ")
    for build in board:
        if build[ABBREVIATION]==name:
            if BUILDING in build:
                print(PROP_INFO.format(build[PLACE],build[PRICE],build[OWNER],"Yes",build[RENT],build[BUILDING_RENT]))
            else:
                print(PROP_INFO.format(build[PLACE],build[PRICE],build[OWNER],"No",build[RENT],build[BUILDING_RENT]))

def display_player(players,board):
    print("The players are:")
    for player in players:
        print("        {}".format(player[PLAYER_NAME]))
    name=input("Which player do you wish to know about? ")
    for player in players:
        if name==player[PLAYER_NAME]:
            print(PLAYER_INFO.format(player[PLAYER_NAME],player[PLAYER_SYMBOL],player[MONEY]))
            if len(player[PROPERTIES])==0:
                print("                No Properties Yet")
            else:
                for build_index in player[PROPERTIES]:
                    print("                {}  with a building: {}".format(board[build_index][PLACE],BUILDING in board[build_index]))

def build_buillding(player,board):
    build_lst=[]
    for build in player[PROPERTIES]:
        if not BUILDING in board[build]:
            print("{} {} {}".format(board[build][PLACE],board[build][ABBREVIATION],board[build][BUILDING_COST]))
            build_lst.append(board[build])
    choice=input("Which property do you want to build a building on? ")
    for build in build_lst:
        if build[ABBREVIATION]==choice:
            print("You have built the building for {}".format(build[PLACE]))
            build[BUILDING]=True
            player[MONEY]-=build[BUILDING_COST]
            return
    print("The property either has a building, isn't yours, or doesn't exist")


def take_turn(player, players, board):
    roll=roll_dice()
    player[POSITION]=(player[POSITION]+roll)%len(board)
    the_board=format_display(players,board)
    display_board(the_board)
    print(player[PLAYER_NAME],"you have rolled",roll)
    print(player[PLAYER_NAME],"you landed on",board[player[POSITION]][PLACE])
    

    if board[player[POSITION]][OWNER]!=THE_BANK and board[player[POSITION]][OWNER]!=player[PLAYER_NAME]:
        print("You landed on {}'s property, you must pay the rent.".format(board[player[POSITION]][OWNER]))
        cost=0
        if BUILDING in board[player[POSITION]]:
            cost=board[player[POSITION]][BUILDING_RENT]
        else:
            cost=board[player[POSITION]][RENT]
        print("You have paid {} to {}".format(cost,board[player[POSITION]][OWNER]))

    while True:
        print('''
    1) Buy Property
    2) Get Property Info
    3) Get Player Info
    4) Build a Building
    5) End Turn

    What do you want to do?''')
        choice=input("    ")
        if choice=='1':
            if board[player[POSITION]][PRICE]==-1:
                # Banks' property
                print("You cannot buy this property.  It cannot be bought or sold.")
            else:
                if board[player[POSITION]][OWNER]==THE_BANK:
                    if input("The property is unowned, do you want to buy it? ").lower()=='yes':
                        board[player[POSITION]][OWNER]=player[PLAYER_NAME]
                        player[PROPERTIES].append(player[POSITION])
                        player[MONEY]-=board[player[POSITION]][PRICE]
                        print("You have bought",board[player[POSITION]][PLACE])
                    else:
                        print("You have decided not to buy",board[player[POSITION]][PLACE])
                else:
                    print(board[player[POSITION]][OWNER],"is the owner of the property, you cannot buy it.")

        elif choice=='2': # Second choice
            display_property(board)
        elif choice=='3':
            display_player(players,board)
        elif choice=='4':
            build_buillding(player,board)
        elif choice=='5':
            return

def play_game(starting_money, pass_go_money, board_file = 'pyop2.csv'):
    players = [
        create_player('First player', starting_money),
        create_player('Second player', starting_money)]
    the_board = load_map(board_file)
    if not the_board:
        print("The board wasn't loaded.")
        return None
    for i in the_board:
        i[OWNER]=THE_BANK
        i[BUILDING_COST]=int(i[BUILDING_COST])
        i[BUILDING_RENT]=int(i[BUILDING_RENT])
        i[RENT]=int(i[RENT])
        i[PRICE]=int(i[PRICE])

        
    current_player=0
    while True:
        player=players[current_player%2]
        take_turn(player,players,the_board)
        if player[MONEY]<=0:
            print("The game has finally ended.  {} is the winner and now we can all go home.".format(players[(current_player+1)%2][PLAYER_NAME]))
            return
        else:
            current_player+=1


if __name__ == '__main__':
    if len(argv) >= 2:
        seed(argv[1])
    if len(argv) >= 3:
        play_game(STARTING_FUNDS, PASS_GO_MONEY, argv[2])
    else:
        play_game(STARTING_FUNDS, PASS_GO_MONEY, BOARD_FILE_NAME)
