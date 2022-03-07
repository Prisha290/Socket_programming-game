import os


# generate a map

class Maze(object):
    def __init__(self):
        self.map_data = [
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

        self.x_move = -1
        self.y_move = -1
        self.x = 0
        self.y = 1
        self.end_x = 7
        self.end_y = 9

    # Print the directions
    def print_instruction(self):
        print('%50s' % '\033[0;36;40mw\033[0m')
        print('Please Input Your Direction:',
              "\033[0;36;40ma <--|--> d   p1: 'st1' p2: 'st2'\033[0m")
        print('%50s' % '\033[0;36;40ms\033[0m')

    # draw map
    def print_map(self):
        # Clear Console
        os.system('cls' if os.name == 'nt' else 'clear')

        for nums in self.map_data:
            for num in nums:
                if num == 1:
                    print(" •", end=" ")
                elif num == 0:
                    print("  ", end=" ")
                else:
                    print(" 🏃", end="")
            print("")

    def startup(self):
        while True:
            self.print_map()
            self.print_instruction()
            order = input()

            # Left
            if order == "a":
                self.y_move = self.y - 1
                # if reach a wall then game over
                if self.map_data[self.x][self.y_move] == 1:
                    print("Cannot go there")
                    continue

                else:
                    self.map_data[self.x][self.y], self.map_data[self.x][self.y_move] \
                        = self.map_data[self.x][self.y_move], self.map_data[self.x][self.y]
                    self.y = self.y_move
                    self.print_map()

            # Down
            elif order == "s":
                self.x_move = self.x + 1
                if self.map_data[self.x_move][self.y] == 1:
                    print("Cannot go there")
                    continue
                else:
                    self.map_data[self.x][self.y], self.map_data[self.x_move][self.y] \
                        = self.map_data[self.x_move][self.y], self.map_data[self.x][self.y]
                    self.x = self.x_move
                    self.print_map()

            # Right
            elif order == "d":
                self.y_move = self.y + 1
                if self.map_data[self.x][self.y_move] == 1:
                    print("Cannot go there")
                    continue
                else:
                    self.map_data[self.x][self.y], self.map_data[self.x][self.y_move] \
                        = self.map_data[self.x][self.y_move], self.map_data[self.x][self.y]
                    self.y = self.y_move
                    self.print_map()


            # Up
            elif order == "w":
                self.x_move = self.x - 1
                if self.map_data[self.x_move][self.y] == 1:
                    print("Cannot go there")
                    continue
                else:
                    self.map_data[self.x][self.y], self.map_data[self.x_move][self.y] \
                        = self.map_data[self.x_move][self.y], self.map_data[self.x][self.y]
                    self.x = self.x_move
                    self.print_map()

            # invalid input
            else:
                print("Please enter a valid letter (w,a,s,d)！")
                continue

            # Check if the player has reached the finish line
            if self.map_data[self.x][self.y] == self.map_data[self.end_x][self.end_y]:
                print("You finished!")
                break

# if __name__ == '__main__':
#     maze = Maze()
#     maze.startup()
