import tkinter as tk
import random
app =App()
# Размеры поля
GRID_SIZE = 10
CELL_SIZE = 40

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Морской бой")
        self.turn = "player"
        self.player_score = 0
        self.enemy_score = 0
        self.difficulty = "easy"  # Уровень сложности (easy, medium, hard)

        # Игровые поля
        self.player_canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="white")
        self.player_canvas.grid(row=1, column=0, padx=10, pady=10)
        self.draw_grid(self.player_canvas)

        self.enemy_canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="white")
        self.enemy_canvas.grid(row=1, column=1, padx=10, pady=10)
        self.draw_grid(self.enemy_canvas)

        # Кнопки
        self.place_ships_button = tk.Button(root, text="Авторасстановка", command=self.auto_place_ships)
        self.place_ships_button.grid(row=0, column=0, pady=10)

        self.start_button = tk.Button(root, text="Начать игру", command=self.start_game)
        self.start_button.grid(row=0, column=1, pady=10)

        self.restart_button = tk.Button(root, text="Рестарт", command=self.restart_game)
        self.restart_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Уровни сложности
        self.level_buttons = tk.Frame(root)
        self.level_buttons.grid(row=4, column=0, columnspan=2, pady=10)
        tk.Label(self.level_buttons, text="Уровень сложности:").grid(row=0, column=0, padx=5)
        tk.Button(self.level_buttons, text="Легкий", command=lambda: self.set_difficulty("easy")).grid(row=0, column=1, padx=5)
        tk.Button(self.level_buttons, text="Средний", command=lambda: self.set_difficulty("medium")).grid(row=0, column=2, padx=5)
        tk.Button(self.level_buttons, text="Сложный", command=lambda: self.set_difficulty("hard")).grid(row=0, column=3, padx=5)

        # Счет
        self.score_label = tk.Label(root, text="Счет: Игрок 0 - 0 Компьютер")
        self.score_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Игровые данные
        self.player_ships = []
        self.enemy_ships = []
        self.player_moves = set()
        self.enemy_moves = set()

    def draw_grid(self, canvas):
        """Рисует клеточный фон на холсте."""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x1, y1 = i * CELL_SIZE, j * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                canvas.create_rectangle(x1, y1, x2, y2, outline="lightblue")

    def auto_place_ships(self):
        """Автоматически размещает корабли на поле игрока."""
        self.player_canvas.delete("all")
        self.draw_grid(self.player_canvas)
        self.player_ships = self.place_ships_randomly()
        self.show_ships(self.player_canvas, self.player_ships)

    def start_game(self):
        """Начало игры с авторасстановкой кораблей противника."""
        self.enemy_ships = self.place_ships_randomly()
        self.enemy_canvas.delete("all")
        self.draw_grid(self.enemy_canvas)
        self.enemy_canvas.bind("<Button-1>", self.player_turn)

    def restart_game(self):
        """Рестарт игры."""
        self.player_score = 0
        self.enemy_score = 0
        self.update_score()
        self.player_moves.clear()
        self.enemy_moves.clear()
        self.auto_place_ships()
        self.start_game()

    def set_difficulty(self, difficulty):
        """Устанавливает уровень сложности."""
        self.difficulty = difficulty
        print(f"Уровень сложности: {self.difficulty}")

    def place_ships_randomly(self):
        """Рандомно расставляет корабли с учетом ограничений."""
        ships = []
        ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Размеры кораблей

        for size in ship_sizes:
            while True:
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)
                orientation = random.choice(["horizontal", "vertical"])
                if self.can_place_ship(x, y, size, orientation, ships):
                    ships.append((x, y, size, orientation))
                    break
        return ships

    def can_place_ship(self, x, y, size, orientation, ships):
        """Проверяет возможность размещения корабля."""
        coordinates = []
        for i in range(size):
            nx, ny = (x + i, y) if orientation == "horizontal" else (x, y + i)
            if nx >= GRID_SIZE or ny >= GRID_SIZE:
                return False
            coordinates.append((nx, ny))

        for nx, ny in coordinates:
            # Проверка соседних клеток на наличие других кораблей
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (nx + dx, ny + dy) in [coord for ship in ships for coord in self.get_ship_coordinates(ship)]:
                        return False
        return True

    def get_ship_coordinates(self, ship):
        """Возвращает все координаты клеток корабля."""
        x, y, size, orientation = ship
        return [(x + i, y) if orientation == "horizontal" else (x, y + i) for i in range(size)]

    def show_ships(self, canvas, ships):
        """Отображает корабли на холсте."""
        for ship in ships:
            x, y, size, orientation = ship
            for i in range(size):
                nx, ny = (x + i, y) if orientation == "horizontal" else (x, y + i)
                canvas.create_rectangle(nx * CELL_SIZE, ny * CELL_SIZE,
                                         (nx + 1) * CELL_SIZE, (ny + 1) * CELL_SIZE, fill="blue")

    def player_turn(self, event):
        """Ход игрока."""
        if self.turn != "player":
            return

        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        if (x, y) in self.player_moves:
            return
        self.player_moves.add((x, y))

        hit = any((x, y) in self.get_ship_coordinates(ship) for ship in self.enemy_ships)
        color = "red" if hit else "white"
        self.enemy_canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                           (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=color)

        if hit:
            self.player_score += 1
            self.update_score()

        self.turn = "enemy"
        self.enemy_turn()

    def enemy_turn(self):
        """Ход компьютера."""
        if self.turn != "enemy":
            return

        while True:
            if self.difficulty == "easy":
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            elif self.difficulty == "medium":
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)  # Улучшить стратегию
            else:  # Hard
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)  # Улучшить стратегию

            if (x, y) not in self.enemy_moves:
                self.enemy_moves.add((x, y))
                break

        hit = any((x, y) in self.get_ship_coordinates(ship) for ship in self.player_ships)
        color = "red" if hit else "white"
        self.player_canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                            (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=color)

        if hit:
            self.enemy_score += 1
            self.update_score()

        self.turn = "player"

    def update_score(self):
        """Обновляет счет на экране."""
        self.score_label.config(text=f"Счет: Игрок {self.player_score} - {self.enemy_score} Компьютер")

# Запуск игры
root = tk.Tk()
game = BattleshipGame(root)
root.mainloop()
