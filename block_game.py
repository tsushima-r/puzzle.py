import tkinter as tk
import random

# カラーパレット（赤、青、緑、黄）
COLORS = ["red", "blue", "green", "yellow"]

class BlockGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Toonblast風パズル")

        self.score = 0
        self.score_label = tk.Label(root, text=f"スコア: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=10)

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.grid_size = 3  # 3×3の盤面
        self.buttons = []
        self.create_grid()

    def create_grid(self):
        self.buttons = []
        for row in range(self.grid_size):
            row_buttons = []
            for col in range(self.grid_size):
                color = random.choice(COLORS)
                btn = tk.Button(self.frame, bg=color, width=10, height=4,
                                command=lambda r=row, c=col: self.handle_click(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def handle_click(self, row, col):
        clicked_color = self.buttons[row][col]["bg"]
        match_coords = self.find_matches(row, col, clicked_color)

        if len(match_coords) >= 2:
            self.score += len(match_coords) * 10
            self.score_label.config(text=f"スコア: {self.score}")

            for r, c in match_coords:
                new_color = random.choice([c for c in COLORS if c != clicked_color])
                self.buttons[r][c].config(bg=new_color)

            self.root.after(100, self.check_no_moves)  # 少し待ってから確認
        else:
            self.check_no_moves()

    def find_matches(self, row, col, color):
        visited = set()
        stack = [(row, col)]
        matches = []

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            if self.buttons[r][c]["bg"] == color:
                matches.append((r, c))
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                        stack.append((nr, nc))
        return matches

    def has_possible_moves(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = self.buttons[row][col]["bg"]
                matches = self.find_matches(row, col, color)
                if len(matches) >= 2:
                    return True
        return False

    def check_no_moves(self):
        if not self.has_possible_moves():
            print("💡 消せるブロックがないため自動シャッフルします！")
            self.shuffle_board()

    def shuffle_board(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                new_color = random.choice(COLORS)
                self.buttons[row][col].config(bg=new_color)
        # 再確認（まれにまた消せない状態になる可能性があるため）
        self.root.after(100, self.check_no_moves)

if __name__ == "__main__":
    root = tk.Tk()
    game = BlockGame(root)
    root.mainloop()
