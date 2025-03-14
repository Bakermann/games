import time
import copy
import random
from rich.console import Console
from IPython.display import clear_output

global tab
global last_move


def initialize_grid(columns: int, rows: int = 7) -> list:
    """
    Initialize connect 4 grid.
    
    :param columns: number of columns
    :param rows: number of rows
    :return: game grid
    """
    global tab
    tab = [0] * columns
    for i in range(len(tab)):
        tab[i] = [' '] * rows
    return tab


def display(grid: list):
    """
    Display game grid
    
    :param grid: grid to display
    :return: 0
    """
    time.sleep(0.3)
    print("\n")
    clear_output(wait=True)
    for i in range(len(grid)):
        print(grid[i])


def make_move_player(player: int) -> tuple:
    """
    Ask the specified player for a move.

    :param player: 1 for Player 1 (X), 2 for Player 2 (O)
    :return: The move coordinates as a tuple (row, column)
    """
    global tab, last_move
    symbol = 'X' if player == 1 else 'O'
    while True:
        try:
            coup = int(input(f'Player {player} ({symbol}): Choose a column to play in 1-7\n'))
            if 1 <= coup <= 7 and tab[0][coup - 1] == ' ':
                coup -= 1  # Adjust for 0-based indexing
                break
            else:
                print("Invalid column. Try again.")
        except ValueError:
            print("Please enter a valid column number between 1 and 7.")

    # Place the player's symbol in the chosen column
    for i in range(len(tab) - 1, -1, -1):
        if tab[i][coup] == ' ':
            tab[i][coup] = symbol
            last_move = (i, coup)  # Save the last move
            return last_move


def make_move(move: tuple, j1: bool):
    """
    Make given move.
    
    :param move: row column coordinates 
    :param j1: whether to place a "O" or a "X"
    :return: 0
    """
    global tab, last_move
    for i in range(len(tab) - 1, -1, -1):
        if tab[i][move] == ' ':
            tab[i][move] = 'O' if j1 else 'X'
            move = [i, move]
            last_move = move
            break


def child_move(tab: list, move: tuple, j1: bool) -> tuple:
    """
    Make move on a simulation board.
    
    :param tab: grid to consider
    :param move: move column
    :param j1: whether to place a "O" or a "X"
    :return: grid and new move cordinates
    """
    for i in range(len(tab) - 1, -1, -1):
        if tab[i][move] == ' ':
            tab[i][move] = 'O' if j1 else 'X'
            move = [i, move]
            break
    return tab, move


# -1 nulle 0 en cours 1 victoire
def eval_position(tab: list, last_move: tuple) -> int:
    """
    Evaluate board postion.
    
    :param tab: grid to consider
    :param last_move: row columns coordinates of last move
    :return: -1 draw 0 going 1 victory
    """
    gc = dr = -1
    haut = bas = -1
    asc_gc = desc_dr = -1
    desc_gc = asc_dr = -1
    acc = 0
    for i in range(len(tab[0])):
        if tab[0][i] != ' ':
            acc += 1
    if acc == 7:
        return -1

    # ligne
    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        gc += 1
        y -= 1
        try:
            tab[x][y]
        except:
            break
    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        dr += 1
        y += 1
        try:
            tab[x][y]
        except:
            break
    ligne = dr + gc + 1

    # colonne
    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        haut += 1
        x -= 1
        try:
            tab[x][y]
        except:
            break
    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        bas += 1
        x += 1
        try:
            tab[x][y]
        except:
            break
    colonne = haut + bas + 1

    # diago \
    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        asc_gc += 1
        x -= 1
        y -= 1
        try:
            tab[x][y]
        except:
            break

    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        desc_dr += 1
        x += 1
        y += 1
        try:
            tab[x][y]
        except:
            break
    diago_desc = asc_gc + desc_dr + 1

    # diago /
    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        desc_gc += 1
        x += 1
        y -= 1
        try:
            tab[x][y]
        except:
            break

    x, y = last_move[0], last_move[1]
    while (tab[x][y] == tab[last_move[0]][last_move[1]]) & (x >= 0) & (y >= 0) & (
            tab[last_move[0]][last_move[1]] != ' '):
        asc_dr += 1
        x -= 1
        y += 1
        try:
            tab[x][y]
        except:
            break
    diago_asc = desc_gc + asc_dr + 1

    if (ligne >= 4) | (colonne >= 4) | (diago_desc >= 4) | (diago_asc >= 4):
        return 1
    return 0


def available_moves(grid: list) -> list:
    """
    Return available moves based on grid.

    :param grid: current board
    :return: list containing 1 at free index
    """
    l = [1] * len(grid[0])
    for j in range(len(l)):
        if grid[0][j] != ' ':
            l[j] = 0
    return l


def JMCTS_0(j1: bool = True):
    """
    Random move selector computer.

    :param j1: whether to put "O" or "X"
    :return:
    """
    global tab
    dispo = [ind for ind, ele in enumerate(available_moves(tab)) if ele == 1]
    coup = random.choice(dispo)
    make_move(coup, j1)


def JMCTS(n: int = 1_000, ia1: bool = True) -> list:
    """
    Simulate n games with MCTS algorithm.

    :param n: number of simulation
    :param ia1: whether to put "O" or "X"
    :return: list containing a score for each possible move
    """
    global tab
    dispo = [ind for ind, ele in enumerate(available_moves(tab)) if ele == 1]
    fils = [0] * len(dispo)
    for i in range(len(fils)):
        fils[i] = copy.deepcopy(tab)
        fils[i] = child_move(fils[i], dispo[i], True)  # chaque coup potentiel
    resultat = [0] * len(fils)

    # jouer n parties aléatoires par fils et stock le résultat
    for i in range(len(fils)):

        # simulation de n parties
        for j in range(n):
            tab_fils, last_move = fils[i]
            j1 = True
            while eval_position(tab_fils, last_move) == 0:
                j1 = not j1
                dispo2 = [ind for ind, ele in enumerate(available_moves(tab_fils)) if ele == 1]
                coup = random.choice(dispo2)
                tab_fils, last_move = child_move(tab_fils, coup, j1)
            if j1:
                resultat[i] += 1 if eval_position(tab_fils, last_move) == 1 else 0
            else:
                resultat[i] += -1 if eval_position(tab_fils, last_move) == 1 else 0

    # coup aléatoire parmi les meilleurs fils
    dispo3 = [ind for ind, ele in enumerate(resultat) if ele == max(resultat)]
    coup = random.choice(dispo3)
    make_move(dispo[coup], ia1)
    return resultat


def try_win() -> int:
    """
    Find one move win if possible.
    
    :return: winning move column. else -1 
    """
    global tab
    dispo = [ind for ind, ele in enumerate(available_moves(tab)) if ele == 1]
    fils = [0] * len(dispo)
    for i in range(len(fils)):
        fils[i] = copy.deepcopy(tab)
        fils[i] = child_move(fils[i], dispo[i], True)
        tab_fils, last_move = fils[i]
        if eval_position(tab_fils, last_move) == 1:
            return i
    return -1


def avoid_loss():
    """
    Find opponent one move win if exists.
    
    :return: losing move column. else -1 
    """
    global tab
    dispo = [ind for ind, ele in enumerate(available_moves(tab)) if ele == 1]
    fils = [0] * len(dispo)
    for i in range(len(fils)):
        fils[i] = copy.deepcopy(tab)
        fils[i] = child_move(fils[i], dispo[i], False)
        tab_fils, last_move = fils[i]
        if eval_position(tab_fils, last_move) == 1:
            return i
    return -1


def JMCTS2(n: int = 1_000, ia1: bool = True):
    """
    Simulate n games with improved MCTS algorithm.

    :param n: number of simulation
    :param ia1: whether to put "O" or "X"
    :return: 
    """
    w = try_win()
    l = avoid_loss()
    if w != -1:
        make_move(w, ia1)
    elif l != -1:
        make_move(l, ia1)
    else:
        JMCTS(n, ia1)


def p1_v_p2(i: int = 6, j: int = 7):
    """
    Launch P1 v P2 game.
    
    :param i: number of columns
    :param j: number of rows
    :return: 
    """
    global tab
    initialize_grid(i, j)
    while True:
        make_move_player(1)
        display(tab)
        if eval_position(tab, last_move) == 1:
            print('PLAYER 1 ONE')
            break
        make_move_player(2)
        display(tab)
        if eval_position(tab, last_move) == 1:
            print('PLAYER 2 WINS')
            break


def p1_v_rdm(i: int = 6, j: int = 7):
    """
    Launch P1 v random game.

    :param i: number of columns
    :param j: number of rows
    :return: 
    """
    global tab, last_move
    initialize_grid(i, j)
    display(tab)
    r = random.choice([0, 1])
    while True:
        if r == 0:
            make_move_player(1)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('PLAYER WINS')
                break
            JMCTS_0()
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('IA WINS')
                break
        else:
            JMCTS_0()
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('IA WINS')
                break
            make_move_player(1)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('PLAYER WINS')
                break


def p1_vs_pmcts(lvl: int = 1_000, i: int = 6, j: int = 7):
    """
    Launch P1 v MCTS game.
        
    :param lvl: number of simulation for MCTS
    :param i: number of columns
    :param j: number of rows
    :return: 
    """
    global tab, last_move
    initialize_grid(i, j)
    display(tab)
    r = random.choice([0, 1])
    while True:
        if r == 0:
            make_move_player(1)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('PLAYER WINS')
                break
            JMCTS(lvl)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('IA WINS')
                break
        else:
            JMCTS(lvl)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('IA WINS')
                break
            make_move_player(1)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('PLAYER WINS')
                break


# j1 v JMCTS2
def p1_vs_pmcts2(lvl: int = 1_000, i: int = 6, j: int = 7):
    """
    Launch P1 v MCTS2 game.

    :param lvl: number of simulation for MCTS
    :param i: number of columns
    :param j: number of rows
    :return: 
    """
    global tab, last_move
    initialize_grid(i, j)
    display(tab)
    r = random.choice([0, 1])
    while True:
        if r == 0:
            make_move_player(1)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('PLAYER WINS')
                break
            JMCTS2(lvl)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('IA WINS')
                break
        else:
            JMCTS2(lvl)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('IA WINS')
                break
            make_move_player(1)
            display(tab)
            if eval_position(tab, last_move) == 1:
                print('PLAYER WINS')
                break


def ia_vs_ia2(i=6, j=7):
    """
    Launch MCTS v MCTS2 game.

    :param i: number of columns
    :param j: number of rows
    :return: 
    """
    global tab, last_move
    initialize_grid(i, j)
    display(tab)

    while True:
        JMCTS(ia1=True)
        display(tab)
        if eval_position(tab, last_move) == 1:
            print('IA WINS')
            break
        time.sleep(1)
        JMCTS2(ia1=False)
        display(tab)
        if eval_position(tab, last_move) == 1:
            print('IA2 WINS')
            break
        time.sleep(1)


def connect4():
    """Launcg connect4 game."""

    text = 'Choose game mode \n'
    text += '    1 For P1 vs P2\n'
    text += '    2 For P vs Random (easy)\n'
    text += '    3 For P vs JMCTS (medium)\n'
    text += '    4 For P vs JMCTS2 (hard)\n'
    text += '    5 For JMCTS vs JMCTS2 \n\n'
    c = Console(width=30)
    c.rule('Puissance 4', style='black')
    choix = 0
    while choix not in ['1', '2', '3', '4', '5']:
        choix = str(input(text))
    else:
        if choix == '1':
            p1_v_p2()
        elif choix == '2':
            p1_v_rdm()
        elif choix == '3':
            p1_vs_pmcts()
        elif choix == '4':
            p1_vs_pmcts2()
        else:
            ia_vs_ia2()
    return 0


if __name__ == "__main__":
    connect4()
