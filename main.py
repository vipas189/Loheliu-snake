import threading
import keyboard
import random
import pyautogui
import sys


class snakeGame:

    def __init__(self, grid_size_y, grid_size_x):
        self.grid_size_y = grid_size_y
        self.grid_size_x = grid_size_x
        self.tiles = "\033[48;5;4m  "
        self.snakeHead = "\033[48;5;1m  "
        self.snack = "\033[48;5;214m  "
        self.tail = "\033[48;5;8m  "
        self.grid = []
        self.fps = 2
        self.frame = 0
        self.move = None
        self.tailLenght = 0
        self.speed = self.fps / (self.grid_size_y * self.grid_size_x) * 2
        self.tailPos = {"y": [], "x": []}
        self.snakePos = {
            "y": random.randint(0, self.grid_size_y - 1),
            "x": random.randint(0, self.grid_size_x - 1),
        }
        self.snackPos = {
            "y": random.randint(0, self.grid_size_y - 1),
            "x": random.randint(0, self.grid_size_x - 1),
        }

    def buttons(self):
        def move_up():
            while True:
                keyboard.wait("w")
                if self.move != "down":
                    self.move = "up"

        def move_down():
            while True:
                keyboard.wait("s")
                if self.move != "up":
                    self.move = "down"

        def move_left():
            while True:
                keyboard.wait("a")
                if self.move != "right":
                    self.move = "left"

        def move_right():
            while True:
                keyboard.wait("d")
                if self.move != "left":
                    self.move = "right"

        thread_up = threading.Thread(target=move_up)
        thread_down = threading.Thread(target=move_down)
        thread_left = threading.Thread(target=move_left)
        thread_right = threading.Thread(target=move_right)
        thread_up.start()
        thread_down.start()
        thread_left.start()
        thread_right.start()

    def grid_form(self):
        for i in range(self.grid_size_y):
            self.grid.append([])
            for _ in range(self.grid_size_x):
                self.grid[i].append(self.tiles)

    def grid_display(self):
        result = ""
        for x in range(self.grid_size_y):
            result += "".join(map(str, self.grid[x])) + "\n"
        sys.stdout.write("\033[?25l")
        sys.stdout.write("\033[H")
        sys.stdout.write(result)
        sys.stdout.flush()

    def difficulty(self):
        if self.snakePos == self.snackPos and round(self.fps, 2) < 9:
            self.fps += self.speed

    def tail_collision(self):
        if self.tailLenght > 0:
            return any(
                self.snakePos["y"] == self.tailPos["y"][i]
                and self.snakePos["x"] == self.tailPos["x"][i]
                for i in range(len(self.tailPos["y"]) - 1)
            )

    def snake_spawn(self):
        self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.snakeHead

    def snack_spawn(self):
        self.check_if_snack_pos_same_as_snake()
        self.grid[self.snackPos["y"]][self.snackPos["x"]] = self.snack

    def check_if_snack_pos_same_as_snake(self):
        if self.snackPos == self.snakePos:
            self.tailLenght += 1
        while True:
            if (
                any(
                    self.snackPos["y"] == self.tailPos["y"][i]
                    and self.snackPos["x"] == self.tailPos["x"][i]
                    for i in range(len(self.tailPos["y"]))
                )
                or self.snackPos == self.snakePos
            ):
                self.snackPos["y"] = random.randint(0, self.grid_size_y - 1)
                self.snackPos["x"] = random.randint(0, self.grid_size_x - 1)
            else:
                break

    def snake_tail(self):
        if self.tailLenght > 0:
            for x in range(len(self.tailPos["y"])):
                self.grid[self.tailPos["y"][x]][self.tailPos["x"][x]] = self.tail
                if x == len(self.tailPos["y"]) - 1:
                    self.grid[self.tailPos["y"][x]][self.tailPos["x"][x]] = self.tiles
                    if (
                        self.snakePos["y"] == self.tailPos["y"][x]
                        and self.snakePos["x"] == self.tailPos["x"][x]
                    ):
                        self.grid[self.tailPos["y"][x]][
                            self.tailPos["x"][x]
                        ] = self.snakeHead

    def snake_move(self):
        self.tailPos["y"].insert(0, self.snakePos["y"])
        self.tailPos["x"].insert(0, self.snakePos["x"])
        del self.tailPos["y"][self.tailLenght + 1 :]
        del self.tailPos["x"][self.tailLenght + 1 :]
        if self.move == "up":
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.tiles
            if self.snakePos["y"] == self.grid_size_y - self.grid_size_y:
                self.snakePos["y"] = self.grid_size_y - 1
            else:
                self.snakePos["y"] -= 1
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.snakeHead

        if self.move == "down":
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.tiles
            if self.snakePos["y"] == self.grid_size_y - 1:
                self.snakePos["y"] = self.grid_size_y - self.grid_size_y
            else:
                self.snakePos["y"] += 1
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.snakeHead

        if self.move == "left":
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.tiles
            if self.snakePos["x"] == self.grid_size_x - self.grid_size_x:
                self.snakePos["x"] = self.grid_size_x - 1
            else:
                self.snakePos["x"] -= 1
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.snakeHead

        if self.move == "right":
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.tiles
            if self.snakePos["x"] == self.grid_size_x - 1:
                self.snakePos["x"] = self.grid_size_x - self.grid_size_x
            else:
                self.snakePos["x"] += 1
            self.grid[self.snakePos["y"]][self.snakePos["x"]] = self.snakeHead

    def run(self):
        self.grid_form()
        self.buttons()
        self.snake_spawn()
        while True:
            self.snake_move()
            self.snake_tail()
            self.difficulty()
            self.snack_spawn()
            if self.tail_collision():
                print("Susipisai lochas!!!")
                break
            self.grid_display()
            pyautogui.sleep(1 / round(self.fps, 2))
            self.frame += 1


snake = snakeGame(10, 10)
snake.run()
