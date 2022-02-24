import os

# generate a map
map_data = [
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
# Current player's position
x = 0
y = 1
end_x = 7
end_y = 9

# Global variables to store the current position for p1 and p2
player1_pos = [0, 1]
player2_pos = [0, 16]

x_move = -1
y_move = -1


# To start the game with p1
def init_player1():
    global x
    global y
    global end_x
    global end_y

    x = 0
    y = 1
    end_x = 7
    end_y = 9


# To start the game with p2
def init_player2():
    global x
    global y
    global end_x
    global end_y

    x = 0
    y = 16
    end_x = 7
    end_y = 24


# To store the current position for p1 before switching the player
def store_p1_pos(a, b):
    global player1_pos
    player1_pos = [a, b]


# To store the current position for p2 before switching the player
def store_p2_pos(a, b):
    global player2_pos
    player2_pos = [a, b]


# Switch to player1
def switch_to_player1():
    global x
    global y
    global end_x
    global end_y
    global player1_pos

    x = player1_pos[0]
    y = player1_pos[1]
    end_x = 7
    end_y = 9


# Switch to player1
def switch_to_player2():
    global x
    global y
    global end_x
    global end_y
    global player2_pos

    x = player2_pos[0]
    y = player2_pos[1]
    end_x = 7
    end_y = 24


# Print the directions
def print_instruction():
    print('%50s' % '\033[0;36;40mw\033[0m')
    print('Please Input Your Direction:',
          "\033[0;36;40ma <--|--> d   p1: 'st1' p2: 'st2'\033[0m")
    print('%50s' % '\033[0;36;40ms\033[0m')


# Convert one map to two
def convert(array):
    arr_len = len(array[0])
    for i in range(len(array)):
        for j in range(5):
            array[i].append(0)

    for col in range(len(array)):
        row = array[col]
        original = row[0:arr_len:1]
        row.extend(original)


# draw map
def print_map():
    # Clear Console
    os.system('cls' if os.name == 'nt' else 'clear')

    for nums in map_data:
        for num in nums:
            if num == 1:
                print(" •", end=" ")
            elif num == 0:
                print("  ", end=" ")
            else:
                print(" 🏃", end="")
        print("")


convert(map_data)
print_map()

init_player = input("Enter 1 for Player1, 2 for Player2: ")
if init_player == '1':
    init_player1()
else:
    init_player2()

print_map()

while True:
    print_instruction()
    order = input()

    # Left
    if order == "a":
        y_move = y - 1
        # if reach a wall then game over
        if map_data[x][y_move] == 1:
            print("Cannot go there")
            continue

        else:
            map_data[x][y], map_data[x][y_move] = map_data[x][y_move], map_data[x][y]
            y = y_move
            print_map()

    # Down
    elif order == "s":
        x_move = x + 1
        if map_data[x_move][y] == 1:
            print("Cannot go there")
            continue
        else:
            map_data[x][y], map_data[x_move][y] = map_data[x_move][y], map_data[x][y]
            x = x_move
            print_map()

    # Right
    elif order == "d":
        y_move = y + 1
        if map_data[x][y_move] == 1:
            print("Cannot go there")
            continue
        else:
            map_data[x][y], map_data[x][y_move] = map_data[x][y_move], map_data[x][y]
            y = y_move
            print_map()


    # Up
    elif order == "w":
        x_move = x - 1
        if map_data[x_move][y] == 1:
            print("Cannot go there")
            continue
        else:
            map_data[x][y], map_data[x_move][y] = map_data[x_move][y], map_data[x][y]
            x = x_move
            print_map()

    # Switch to player1
    elif order == 'st1':
        store_p2_pos(x, y)
        switch_to_player1()
        print_map()

    # Switch to player1
    elif order == "st2":
        store_p1_pos(x, y)
        switch_to_player2()
        print_map()

    # invalid input
    else:
        print("Please enter a valid letter (w,a,s,d)！")
        continue

    # Check if the player has reached the finish line
    if map_data[x][y] == map_data[end_x][end_y]:
        print("You win")
        break
