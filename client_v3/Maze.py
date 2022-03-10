# Maze generator -- Randomized Prim Algorithm
import json
import os


class Maze:
    def __init__(self, game_difficulty):
        with open('levels.json', 'r') as json_file:
            data = json_file.read()
        obj = json.loads(data)
        self.maze = obj[game_difficulty]

        # Player position
        self.player_posX = 0
        self.player_posY = 1

        # Finish position
        self.finish_posX = len(self.maze) - 1
        self.finish_posY = len(self.maze[0]) - 2

        # Maze Emoji's
        self.MAZE_WALL = "\U0001F7E8"
        self.FINISH = "\U0001F3C1"
        self.PLAYER = "\U0001F3C3"

    def print_maze(self):
        # Clear terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[0])):
                if self.maze[i][j] == 'c':
                    print("  ", end=" ")
                elif self.maze[i][j] == 'f':
                    print(self.FINISH, end=" ")
                elif self.maze[i][j] == 's':
                    print(self.PLAYER, end=" ")
                else:
                    print(self.MAZE_WALL, end=" ")

            print('\n')

    def print(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[0])):
                print(self.maze[i][j], end=" ")

            print('\n')

    def start_game(self):
        self.print_maze()
        x_move = -1
        y_move = -1
        # Player Movement
        while True:
            print('%49s' % '\033[0;35;40mw\033[0m')
            print('Please Input Your Direction:',
                  "\033[0;35;40ma <--|--> d \033[0m")
            print('%49s' % '\033[0;35;40ms\033[0m')
            order = input("->  ")

            # Left
            if order == "a":
                y_move = self.player_posY - 1
                # if reach a wall then game over
                if self.maze[self.player_posX][y_move] == "w":
                    print("Cannot go there")
                    self.print_maze()
                    continue

                else:
                    self.maze[self.player_posX][self.player_posY], self.maze[self.player_posX][y_move] = \
                        self.maze[self.player_posX][y_move], self.maze[self.player_posX][self.player_posY]
                    self.player_posY = y_move
                    self.print_maze()

            # Down
            elif order == "s":
                x_move = self.player_posX + 1
                if self.maze[x_move][self.player_posY] == "w":
                    print("Cannot go there")
                    self.print_maze()
                    continue
                else:
                    self.maze[self.player_posX][self.player_posY], self.maze[x_move][self.player_posY] = \
                    self.maze[x_move][
                        self.player_posY], \
                    self.maze[
                        self.player_posX][
                        self.player_posY]
                    self.player_posX = x_move
                    self.print_maze()

            # Right
            elif order == "d":
                y_move = self.player_posY + 1
                if self.maze[self.player_posX][y_move] == "w":
                    print("Cannot go there")
                    self.print_maze()
                    continue
                else:
                    self.maze[self.player_posX][self.player_posY], self.maze[self.player_posX][y_move] = \
                        self.maze[self.player_posX][y_move], self.maze[self.player_posX][self.player_posY]
                    self.player_posY = y_move
                    self.print_maze()

            # Up
            elif order == "w":
                x_move = self.player_posX - 1
                if self.maze[x_move][self.player_posY] == "w":
                    print("Cannot go there")
                    self.print_maze()
                    continue
                else:
                    self.maze[self.player_posX][self.player_posY], self.maze[x_move][self.player_posY] = \
                    self.maze[x_move][
                        self.player_posY], \
                    self.maze[
                        self.player_posX][
                        self.player_posY]
                    self.player_posX = x_move
                    self.print_maze()

            # Invalid Input
            else:
                print("[Please Enter A Valid Letter (w,a,s,d)! ]")
                self.print_maze()
                continue

            # Check if the player has reached the finish line
            if self.maze[self.player_posX][self.player_posY] == self.maze[self.finish_posX][self.finish_posY]:
                print("You finished! 🤩")
                break

# if __name__ == '__main__':
#     smaze = Maze("medium")  # hard mode doesnt work
#     smaze.start_game()
#     # print("Finish: ", smaze.finish_posX, smaze.finish_posY)
