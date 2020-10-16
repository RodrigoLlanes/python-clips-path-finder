
import time
import sys

from bot_interaction import *
from board_graphics import *
from editor_window import *
 
static_data = {
    'size': [11, 4],
    'max_depth': 41,
    'holes': [[5, 2], [3, 3], [8, 3], [4, 4], [5, 4], [6, 4]],
    'leaders': [[3, 1], [7, 1], [2, 2], [10, 2], [1, 3], [7, 3], [11, 3]]
}

dynamic_data = {
    'enemies': [[4, 2], [8, 2], [8, 4]],
    'boxes': [[3, 4], [4, 3], [11, 2]],
    'pos': [1, 1],
    'ammo': 3
}

def show_solution():
    runing = True
    def close():
        nonlocal runing
        runing = False

    path = get_path(static_data, dynamic_data)
    board = Board(static_data, dynamic_data, cell_size=50, close_callback=close)

    n = 0
    frame = 0
    while runing:
        frame += 1
        if n < len(path) - 1 and frame % 60 == 0:
            n += 1

        act = path[n]
        board.update(act)
    board.close()

def editor():
    runing = True
    selected_piece = None
    def get_selected_piece():
        nonlocal selected_piece
        return selected_piece
    def set_selected_piece(value):
        nonlocal selected_piece
        selected_piece = value


    def close():
        nonlocal runing
        runing = False

    board = Board(static_data, dynamic_data, cell_size=50, close_callback=close, get_selected_piece=get_selected_piece)

    def run(frame_rate=60):
        nonlocal board
        nonlocal runing
        path = get_path(static_data, dynamic_data)

        n = 0
        frame = 0
        while runing:
            frame += 1
            if n < len(path) - 1 and frame % frame_rate == 0:
                n += 1
            elif n == len(path) - 1 and frame % frame_rate == frame_rate - 1:
                break
            act = path[n]
            board.update(act)
        board.update(dynamic_data)

    editor = Editor(static_data, dynamic_data, board, run_callback=run, close_callback=close, set_selected_piece=set_selected_piece)


    n = 0
    frame = 0
    while runing:
        frame += 1
        board.update(dynamic_data)
        editor.update()
    editor.close()
    board.close()


if __name__ == '__main__':
    editor()