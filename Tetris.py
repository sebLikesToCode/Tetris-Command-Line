import keyboard
import time
import random

gameEnd = False
wall = "██"
space = "  "
tetris_block = "██"

size_x = 10
size_y = 25
# The Background Well (10 wide, 20 tall)
well = [[0 for x in range(size_x)] for y in range(size_y)]

# Piece Tracking Coordinates
piece_x = 4  # Start near the middle
piece_y = 3  # Start at the very top

move_timer = 0.1
last_move_time = time.time()
score = 0
level = 0
total_lines = 0
kick_table = [
    (0, 0),   # Priority 1: Test normal rotation in place
    (-1, 0),  # Priority 2: Kick Left 1
    (1, 0),   # Priority 3: Kick Right 1
    (0, -1),  # Priority 4: Kick Up 1 (The Floor Kick!)
    (-1, -1), # Priority 5: Kick Left 1, Up 1
    (1, -1)   # Priority 6: Kick Right 1, Up 1
]

i_kick_table = [
    (0, 0),   # Priority 1: In place
    (-1, 0),  # Priority 2: Kick Left 1
    (1, 0),   # Priority 3: Kick Right 1
    (-2, 0),  # Priority 4: Kick Left 2 (CRITICAL FOR I PIECE)
    (2, 0),   # Priority 5: Kick Right 2 (CRITICAL FOR I PIECE)
    (0, -1),  # Priority 6: Kick Up 1
    (0, -2)   # Priority 7: Kick Up 2
]

t_piece = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0],
]

l_piece = [
    [2, 0, 0],
    [2, 2, 2],
    [0, 0, 0],
]

j_piece = [
    [0, 0, 3],
    [3, 3, 3],
    [0, 0, 0],
]

s_piece = [
    [0, 4, 4],
    [4, 4, 0],
    [0, 0, 0],
]

z_piece = [
    [5, 5, 0],
    [0, 5, 5],
    [0, 0, 0],
]

o_piece = [
    [6, 6],
    [6, 6],
]

i_piece = [
    [0, 0, 0, 0],
    [7, 7, 7, 7],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

pieces = [t_piece, i_piece, l_piece, j_piece, o_piece, s_piece, z_piece]
pieces_loop = [t_piece, i_piece, l_piece, j_piece, o_piece, s_piece, z_piece]

colors = {
    0: space,                                 # 0 is still empty space
    1: "\033[38;5;93m" + tetris_block + "\033[0m", # Purple (T)
    2: "\033[38;5;208m" + tetris_block + "\033[0m", # Orange/Red (L)
    3: "\033[38;5;21m" + tetris_block + "\033[0m", # Blue (J)
    4: "\033[92m" + tetris_block + "\033[0m", # Green (S)
    5: "\033[31m" + tetris_block + "\033[0m", # Red (Z)
    6: "\033[38;5;226m" + tetris_block + "\033[0m", # Yellow (O)
    7: "\033[96m" + tetris_block + "\033[0m", # Cyan (I)
    8: "\033[38;5;8m" + tetris_block + "\033[0m",



}


current_piece = random.choice(pieces_loop)
pieces_loop.remove(current_piece)
next_piece = random.choice(pieces_loop)
pieces_loop.remove(next_piece)

cells_hard_dropped = 0
cells_soft_dropped = 0


def print_board():
    print("\033[H", end="")  # move cursor to top-left

    temp_well = [row[:] for row in well]
    ghost_y = piece_y

    while not check_collision(piece_x, ghost_y + 1, current_piece):
        ghost_y += 1

    if ghost_y < size_y:
        for r in range(len(current_piece)):
            for c in range(len(current_piece)):
                if current_piece[r][c] != 0:
                    temp_well[ghost_y + r][piece_x + c] = 8


    for row_index in range(len(current_piece)):
        for column_index in range(len(current_piece)):
            if current_piece[row_index][column_index] != 0:
                global_x = piece_x + column_index
                global_y = piece_y + row_index

                temp_well[global_y][global_x] = current_piece[row_index][column_index]

    for y in range(5, size_y):
        print(wall, end="")
        for x in range(size_x):
            if temp_well[y][x] != 0:
                cell_id = temp_well[y][x]
                print(colors[cell_id], end="")  # Print a block!
            else:
                print(space, end="")  # Print empty space

        print(wall, end="")
        if y == 5:
            print(" SCORE: " + str(score), end="")

        elif y == 7:
            print(" LEVEL: " + str(level), end="")

        elif y == 9:
            print(" LINES: " + str(total_lines), end="")

        elif y == 11:
            print(" NEXT PIECE: ", end="")

        elif y >= 13 and y < 13 + len(next_piece):
            piece_row = y - 13
            print(space, end="")
            for cell in next_piece[piece_row]:
                if cell != 0:
                    print(colors[cell], end="")
                else:
                    print(space, end="")

        print("\033[K")



    print(wall * size_x + wall * 2)


def check_collision(future_x, future_y, piece):
    for row in range(len(piece)):
        for column in range(len(piece)):

            if piece[row][column] != 0:

                board_x = future_x + column
                board_y = future_y + row

                if board_y >= size_y:
                    return True

                if board_x < 0 or board_x >= size_x:
                    return True

                if well[board_y][board_x] != 0:
                    return True

    return False

def move_player(piece):
    global piece_x, last_move_time
    if time.time() - last_move_time >= move_timer:

        if keyboard.is_pressed("a"):
            if not check_collision(piece_x - 1, piece_y, piece):
                piece_x -= 1
                last_move_time = time.time()
        if keyboard.is_pressed("d"):
            if not check_collision(piece_x + 1, piece_y, piece):
                piece_x += 1
                last_move_time = time.time()


def pick_piece(next_pieces, current_pieces, all_pieces, remaining_pieces):
    current_pieces = next_pieces

    if len(remaining_pieces) == 0:
        remaining_pieces = all_pieces.copy()

    next_pieces = random.choice(remaining_pieces)
    remaining_pieces.remove(next_pieces)

    return next_pieces, current_pieces, remaining_pieces, all_pieces


def freeze_piece(piece):
    for row in range(len(piece)):
        for column in range(len(piece)):
            board_x = piece_x + column
            board_y = piece_y + row
            if piece[row][column] != 0:
                well[board_y][board_x] = piece[row][column]



def clear_lines():
    global total_lines, level, score
    lines_this_turn = 0
    for row in range(size_y - 1, -1, -1):
        if not 0 in well[row]:
            lines_this_turn += 1
            well.pop(row)
            well.insert(0, [0 for x in range(size_x)])

    if lines_this_turn == 1:
        score += (40 * level)
    elif lines_this_turn == 2:
        score += (100 * level)
    elif lines_this_turn == 3:
        score += (300 * level)
    elif lines_this_turn == 4:
        score += (1200 * level)

    total_lines += lines_this_turn
    level = total_lines // 10



def rotate_piece_cw(piece):
    rotated_piece = []
    for column in range(len(piece)):
        new_row = []
        for row in range(len(piece) - 1, -1, -1):
            new_row.append(piece[row][column])
        rotated_piece.append(new_row)
    return rotated_piece


def rotate_piece_ccw(piece):
    rotated_piece = []
    for column in range(len(piece) - 1, -1, -1):
        new_row = []
        for row in range(len(piece)):
            new_row.append(piece[row][column])
        rotated_piece.append(new_row)
    return rotated_piece



drop_time = 0.5 * (level ** 0.9)
last_drop = time.time()
spin_time = 0.2
last_spin = time.time()
while not gameEnd:
    if keyboard.is_pressed("s"):
        drop_time = 0.1
    else:
        drop_time = 0.3
    print_board()

    if time.time() - last_spin >= spin_time:
        if keyboard.is_pressed("left"):
            if len(current_piece) == 4:
                active_table = i_kick_table
            else:
                active_table = kick_table
            test_rotate = rotate_piece_ccw(current_piece)
            for kick_x, kick_y in active_table:
                test_x = piece_x + kick_x
                test_y = piece_y + kick_y
                if not check_collision(test_x, test_y, test_rotate):
                    current_piece = test_rotate
                    piece_x, piece_y = test_x, test_y
                    last_spin = time.time()
                    break
        if keyboard.is_pressed("right"):
            if len(current_piece) == 4:
                active_table = i_kick_table
            else:
                active_table = kick_table
            test_rotate = rotate_piece_cw(current_piece)
            for kick_x, kick_y in active_table:
                test_x = piece_x + kick_x
                test_y = piece_y + kick_y
                if not check_collision(test_x, test_y, test_rotate):
                    current_piece = test_rotate
                    piece_x, piece_y = test_x, test_y
                    last_spin = time.time()
                    break


    move_player(current_piece)
    # GRAVITY
    if time.time() - last_drop >= drop_time:
        # Look one step into the future
        if not check_collision(piece_x, piece_y + 1, current_piece):
            piece_y += 1  # Safe! Move down.
            if keyboard.is_pressed("s"):
                score += 1
        else:
            freeze_piece(current_piece) # CRASH! We hit the floor. (We will handle freezing here later)
            next_piece,current_piece,pieces_loop,pieces=pick_piece(next_piece,current_piece,pieces,pieces_loop)
            clear_lines()
            piece_x = 4
            piece_y = 3
            if check_collision(piece_x, piece_y + 1, current_piece):
                gameEnd = True
        last_drop = time.time()  # Reset the clock
    if keyboard.is_pressed("space"):
        while not check_collision(piece_x, piece_y + 1, current_piece):
            piece_y += 1
            cells_hard_dropped += 1
        score += cells_hard_dropped * 2
        cells_hard_dropped = 0
        freeze_piece(current_piece)
        clear_lines()

        # SPAWN NEXT PIECE IMMEDIATELY HERE
        next_piece, current_piece, pieces_loop, pieces = pick_piece(next_piece, current_piece, pieces, pieces_loop)
        piece_x = 4
        piece_y = 3
        print_board()
        last_drop = time.time()  # Reset gravity so the new piece doesn't fall instantly

        time.sleep(0.2)  # Prevent "double firing"

    # Keep the loop running fast enough to catch inputs later
    time.sleep(0.01)

print("Game Over")
time.sleep(1000)