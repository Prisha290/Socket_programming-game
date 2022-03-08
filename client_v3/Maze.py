# Maze generator -- Randomized Prim Algorithm


import os
import random


class Maze:

  def __init__(self, game_difficulty):
    self.difficulty = {
      1: (10, 10),
      2: (20, 10),
      3: (40, 20),
      4: (80, 40)
    }
    self.width = self.difficulty[game_difficulty][0]
    self.height = self.difficulty[game_difficulty][1]
    self.maze = []
    self.start = (0, 0)
    self.end = (0, 0)
    self.wall = 'w'
    self.cell = 'c'
    self.unvisited = 'u'
    self.visited = []
    self.path = []
    # Player position
    self.player_posX = -1
    self.player_posY = -1
    # Finish position
    self.finish_posX = -1
    self.finish_posY = -1
    # Maze Emoji's
    self.MAZE_WALL = "\U0001F7E8"
    self.FINISH = "\U0001F3C1"
    self.PLAYER = "\U0001F3C3"
    self.generate_maze()

  def print_maze(self):
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, self.height):
      for j in range(0, self.width):
        if self.maze[i][j] == 'u':
          print(" u", end=" ")
        elif self.maze[i][j] == 'c':
          print("  ", end=" ")
        elif self.maze[i][j] == 'f':
          print(self.FINISH, end=" ")
        elif self.maze[i][j] == 's':
          print(self.PLAYER, end=" ")
        else:
          print(self.MAZE_WALL, end=" ")

      print('\n')

  # Find number of surrounding cells
  def surrounding_cells(self, rand_wall):
    s_cells = 0
    if self.maze[rand_wall[0] - 1][rand_wall[1]] == 'c':
      s_cells += 1
    if self.maze[rand_wall[0] + 1][rand_wall[1]] == 'c':
      s_cells += 1
    if self.maze[rand_wall[0]][rand_wall[1] - 1] == 'c':
      s_cells += 1
    if self.maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
      s_cells += 1

    return s_cells

  def generate_maze(self):
    # Denote all cells as unvisited
    for i in range(0, self.height):
      line = []
      for j in range(0, self.width):
        line.append(self.unvisited)
      self.maze.append(line)

    # Randomize starting point and set it a cell
    starting_height = int(random.random() * self.height)
    starting_width = int(random.random() * self.width)
    if starting_height == 0:
      starting_height += 1
    if starting_height == self.height - 1:
      starting_height -= 1
    if starting_width == 0:
      starting_width += 1
    if starting_width == self.width - 1:
      starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    self.maze[starting_height][starting_width] = self.cell
    walls = [[starting_height - 1, starting_width], [starting_height, starting_width - 1],
             [starting_height, starting_width + 1], [starting_height + 1, starting_width]]

    # Denote walls in maze
    self.maze[starting_height - 1][starting_width] = 'w'
    self.maze[starting_height][starting_width - 1] = 'w'
    self.maze[starting_height][starting_width + 1] = 'w'
    self.maze[starting_height + 1][starting_width] = 'w'

    while walls:
      # Pick a random wall
      rand_wall = walls[int(random.random() * len(walls)) - 1]

      # Check if it is a left wall
      if rand_wall[1] != 0:
        if self.maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and self.maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
          # Find the number of surrounding cells
          s_cells = self.surrounding_cells(rand_wall)

          if s_cells < 2:
            # Denote the new path
            self.maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            # Upper cell
            if rand_wall[0] != 0:
              if self.maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                self.maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
              if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] - 1, rand_wall[1]])

            # Bottom cell
            if rand_wall[0] != self.height - 1:
              if self.maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                self.maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
              if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] + 1, rand_wall[1]])

            # Leftmost cell
            if rand_wall[1] != 0:
              if self.maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                self.maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
              if [rand_wall[0], rand_wall[1] - 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] - 1])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Check if it is an upper wall
      if rand_wall[0] != 0:
        if self.maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and self.maze[rand_wall[0] + 1][rand_wall[1]] == 'c':

          s_cells = self.surrounding_cells(rand_wall)
          if s_cells < 2:
            # Denote the new path
            self.maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            # Upper cell
            if rand_wall[0] != 0:
              if self.maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                self.maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
              if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] - 1, rand_wall[1]])

            # Leftmost cell
            if rand_wall[1] != 0:
              if self.maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                self.maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
              if [rand_wall[0], rand_wall[1] - 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] - 1])

            # Rightmost cell
            if rand_wall[1] != self.width - 1:
              if self.maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                self.maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
              if [rand_wall[0], rand_wall[1] + 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] + 1])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Check the bottom wall
      if rand_wall[0] != self.height - 1:
        if self.maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and self.maze[rand_wall[0] - 1][rand_wall[1]] == 'c':

          s_cells = self.surrounding_cells(rand_wall)
          if s_cells < 2:
            # Denote the new path
            self.maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            if rand_wall[0] != self.height - 1:
              if self.maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                self.maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
              if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] + 1, rand_wall[1]])
            if rand_wall[1] != 0:
              if self.maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                self.maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
              if [rand_wall[0], rand_wall[1] - 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] - 1])
            if rand_wall[1] != self.width - 1:
              if self.maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                self.maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
              if [rand_wall[0], rand_wall[1] + 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] + 1])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Check the right wall
      if rand_wall[1] != self.width - 1:
        if self.maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and self.maze[rand_wall[0]][rand_wall[1] - 1] == 'c':

          s_cells = self.surrounding_cells(rand_wall)
          if s_cells < 2:
            # Denote the new path
            self.maze[rand_wall[0]][rand_wall[1]] = 'c'

            # Mark the new walls
            if rand_wall[1] != self.width - 1:
              if self.maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                self.maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
              if [rand_wall[0], rand_wall[1] + 1] not in walls:
                walls.append([rand_wall[0], rand_wall[1] + 1])
            if rand_wall[0] != self.height - 1:
              if self.maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                self.maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
              if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] + 1, rand_wall[1]])
            if rand_wall[0] != 0:
              if self.maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                self.maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
              if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                walls.append([rand_wall[0] - 1, rand_wall[1]])

          # Delete wall
          for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
              walls.remove(wall)

          continue

      # Delete the wall from the list anyway
      for wall in walls:
        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
          walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, self.height):
      for j in range(0, self.width):
        if self.maze[i][j] == 'u':
          self.maze[i][j] = 'w'

    # Set starting position of the player
    for i in range(0, self.width):
      if self.maze[1][i] == 'c':
        self.maze[0][i] = 's'
        self.player_posX = 0
        self.player_posY = i
        break

    # Set finish position of the player
    for i in range(self.width - 1, 0, -1):
      if self.maze[self.height - 2][i] == 'c':
        self.maze[self.height - 1][i] = 'f'
        self.finish_posX = self.height - 1
        self.finish_posY = i
        break

  def start_game(self):
    self.print_maze()
    x_move = -1
    y_move = -1
    # Player Movement
    while True:
      print('%50s' % '\033[0;36;40mw\033[0m')
      print('Please Input Your Direction:',
            "\033[0;36;40ma <--|--> d \033[0m")
      print('%50s' % '\033[0;36;40ms\033[0m')
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
          self.maze[self.player_posX][self.player_posY], self.maze[x_move][self.player_posY] = self.maze[x_move][
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
          self.maze[self.player_posX][self.player_posY], self.maze[x_move][self.player_posY] = self.maze[x_move][
                                                                                                 self.player_posY], \
                                                                                               self.maze[
                                                                                                 self.player_posX][
                                                                                                 self.player_posY]
          self.player_posX = x_move
          self.print_maze()

      # Invalid Input
      else:
        print("Please enter a valid letter (w,a,s,d)!")
        continue

      # Check if the player has reached the finish line
      if self.maze[self.player_posX][self.player_posY] == self.maze[self.finish_posX][self.finish_posY]:
        print("You finished")
        break


# if __name__ == '__main__':
#     smaze = Maze(2)
#     smaze.generate_maze()
#     smaze.start_game()
