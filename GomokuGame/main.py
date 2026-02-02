#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五子棋游戏 - 支持人人对战和人机对战
作者: AI Assistant
日期: 2026-01-22
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
from typing import List, Tuple, Optional

# 游戏常量
BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2
PLAYER_NAMES = {BLACK: "黑棋", WHITE: "白棋"}
PLAYER_COLORS = {BLACK: "#000000", WHITE: "#FFFFFF"}

# AI评分常量
SCORE_FIVE = 100000
SCORE_FOUR = 10000
SCORE_OPEN_FOUR = 10000
SCORE_THREE = 1000
SCORE_OPEN_THREE = 5000
SCORE_TWO = 100
SCORE_OPEN_TWO = 500

class GomokuGame:
    """五子棋游戏逻辑类"""

    def __init__(self):
        self.board_size = BOARD_SIZE
        self.board: List[List[int]] = [[EMPTY for _ in range(self.board_size)]
                                        for _ in range(self.board_size)]
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.move_history: List[Tuple[int, int]] = []
        self.ai_mode = False

    def make_move(self, row: int, col: int) -> bool:
        """落子"""
        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = self.current_player
        self.move_history.append((row, col))

        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True

        # 检查是否平局
        if len(self.move_history) == self.board_size * self.board_size:
            self.game_over = True
            self.winner = None
            return True

        self.switch_player()
        return True

    def is_valid_move(self, row: int, col: int) -> bool:
        """检查落子是否有效"""
        return (0 <= row < self.board_size and
                0 <= col < self.board_size and
                self.board[row][col] == EMPTY and
                not self.game_over)

    def switch_player(self):
        """切换玩家"""
        self.current_player = WHITE if self.current_player == BLACK else BLACK

    def check_win(self, row: int, col: int) -> bool:
        """检查是否获胜"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        player = self.board[row][col]

        for dr, dc in directions:
            count = 1
            # 向前计数
            for i in range(1, 5):
                r, c = row + dr * i, col + dc * i
                if (0 <= r < self.board_size and
                    0 <= c < self.board_size and
                    self.board[r][c] == player):
                    count += 1
                else:
                    break
            # 向后计数
            for i in range(1, 5):
                r, c = row - dr * i, col - dc * i
                if (0 <= r < self.board_size and
                    0 <= c < self.board_size and
                    self.board[r][c] == player):
                    count += 1
                else:
                    break

            if count >= 5:
                return True
        return False

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """获取所有空位"""
        positions = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == EMPTY:
                    positions.append((row, col))
        return positions

    def get_adjacent_positions(self, distance: int = 2) -> List[Tuple[int, int]]:
        """获取已有棋子周围的空位（优化AI搜索范围）"""
        positions = set()
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != EMPTY:
                    for dr in range(-distance, distance + 1):
                        for dc in range(-distance, distance + 1):
                            r, c = row + dr, col + dc
                            if (0 <= r < self.board_size and
                                0 <= c < self.board_size and
                                self.board[r][c] == EMPTY):
                                positions.add((r, c))

        # 如果棋盘为空，返回中心位置
        if not positions:
            center = self.board_size // 2
            return [(center, center)]

        return list(positions)

    def ai_move(self) -> Optional[Tuple[int, int]]:
        """AI落子（使用改进的启发式算法）"""
        if not self.ai_mode or self.current_player != WHITE:
            return None

        best_move = self.find_best_move()
        if best_move:
            self.make_move(*best_move)
            return best_move
        return None

    def find_best_move(self) -> Optional[Tuple[int, int]]:
        """寻找最佳落子位置"""
        # 获取候选位置（只考虑已有棋子周围的位置）
        candidates = self.get_adjacent_positions(2)

        if not candidates:
            return None

        best_score = -float('inf')
        best_moves = []

        for row, col in candidates:
            # 评估攻击分数
            self.board[row][col] = WHITE
            attack_score = self.evaluate_position(row, col, WHITE)
            self.board[row][col] = EMPTY

            # 评估防守分数
            self.board[row][col] = BLACK
            defense_score = self.evaluate_position(row, col, BLACK)
            self.board[row][col] = EMPTY

            # 综合评分：攻击优先，但也要考虑防守
            total_score = attack_score * 1.2 + defense_score

            if total_score > best_score:
                best_score = total_score
                best_moves = [(row, col)]
            elif total_score == best_score:
                best_moves.append((row, col))

        # 如果有多个相同分数的位置，随机选择一个
        return random.choice(best_moves) if best_moves else None

    def evaluate_position(self, row: int, col: int, player: int) -> int:
        """评估某个位置的分数"""
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            line_score = self.evaluate_line(row, col, dr, dc, player)
            score += line_score

        return score

    def evaluate_line(self, row: int, col: int, dr: int, dc: int, player: int) -> int:
        """评估一条线上的分数"""
        count = 1
        open_ends = 0

        # 向前检查
        i = 1
        while i < 5:
            r, c = row + dr * i, col + dc * i
            if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                break
            if self.board[r][c] == player:
                count += 1
                i += 1
            elif self.board[r][c] == EMPTY:
                open_ends += 1
                break
            else:
                break

        # 向后检查
        i = 1
        while i < 5:
            r, c = row - dr * i, col - dc * i
            if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                break
            if self.board[r][c] == player:
                count += 1
                i += 1
            elif self.board[r][c] == EMPTY:
                open_ends += 1
                break
            else:
                break

        # 根据连子数和开放端数量评分
        return self.get_score(count, open_ends)

    def get_score(self, count: int, open_ends: int) -> int:
        """根据连子数和开放端数量返回分数"""
        if count >= 5:
            return SCORE_FIVE
        elif count == 4:
            if open_ends == 2:
                return SCORE_OPEN_FOUR
            elif open_ends == 1:
                return SCORE_FOUR
        elif count == 3:
            if open_ends == 2:
                return SCORE_OPEN_THREE
            elif open_ends == 1:
                return SCORE_THREE
        elif count == 2:
            if open_ends == 2:
                return SCORE_OPEN_TWO
            elif open_ends == 1:
                return SCORE_TWO
        return 0

    def undo_move(self) -> bool:
        """悔棋"""
        if not self.move_history or self.game_over:
            return False

        # 在AI模式下，需要撤销两步（玩家和AI的）
        steps = 2 if self.ai_mode else 1

        for _ in range(min(steps, len(self.move_history))):
            row, col = self.move_history.pop()
            self.board[row][col] = EMPTY
            self.switch_player()

        return True

    def reset(self):
        """重置游戏"""
        self.board = [[EMPTY for _ in range(self.board_size)]
                      for _ in range(self.board_size)]
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.move_history = []


class GomokuGUI:
    """五子棋图形界面类"""

    def __init__(self, root):
        self.root = root
        self.root.title("五子棋游戏 - Gomoku - via GitHub Copilot + Claude Sonet 4.5")
        self.root.resizable(False, False)

        self.game = GomokuGame()
        self.cell_size = 35
        self.margin = 40
        self.board_size = self.margin * 2 + self.cell_size * (self.game.board_size - 1)

        # 最后落子位置（用于高亮显示）
        self.last_move = None

        self.setup_ui()
        self.draw_board()

    def setup_ui(self):
        """设置界面"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#F5DEB3')
        main_frame.pack(padx=10, pady=10)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="五子棋(via GitHub Copilot + Claude Sonet 4.5)",
            font=('Arial', 24, 'bold'),
            bg='#F5DEB3',
            fg='#8B4513'
        )
        title_label.pack(pady=5)

        # 画布框架
        canvas_frame = tk.Frame(main_frame, bg='#8B4513', bd=2, relief=tk.RAISED)
        canvas_frame.pack(padx=5, pady=5)

        # 画布
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.board_size,
            height=self.board_size,
            bg='#DEB887',
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # 信息框架
        info_frame = tk.Frame(main_frame, bg='#F5DEB3')
        info_frame.pack(pady=5)

        self.info_label = tk.Label(
            info_frame,
            text="当前玩家: 黑棋",
            font=('Arial', 14, 'bold'),
            bg='#F5DEB3',
            fg='#000000'
        )
        self.info_label.pack()

        self.mode_label = tk.Label(
            info_frame,
            text="模式: 人人对战",
            font=('Arial', 12),
            bg='#F5DEB3',
            fg='#555555'
        )
        self.mode_label.pack()

        # 按钮框架
        button_frame = tk.Frame(main_frame, bg='#F5DEB3')
        button_frame.pack(pady=10)

        # 按钮样式
        btn_style = {
            'font': ('Arial', 11),
            'width': 12,
            'height': 1,
            'bd': 2,
            'relief': tk.RAISED
        }

        self.new_game_button = tk.Button(
            button_frame,
            text="新游戏",
            command=self.new_game,
            bg='#90EE90',
            **btn_style
        )
        self.new_game_button.grid(row=0, column=0, padx=5)

        self.mode_button = tk.Button(
            button_frame,
            text="人机对战",
            command=self.toggle_mode,
            bg='#87CEEB',
            **btn_style
        )
        self.mode_button.grid(row=0, column=1, padx=5)

        self.undo_button = tk.Button(
            button_frame,
            text="悔棋",
            command=self.undo_move,
            bg='#FFB6C1',
            **btn_style
        )
        self.undo_button.grid(row=0, column=2, padx=5)

        # 提示光标位置
        self.hover_position = None

    def draw_board(self):
        """绘制棋盘"""
        self.canvas.delete("all")

        # 绘制网格线
        for i in range(self.game.board_size):
            # 横线
            x1 = self.margin
            y1 = self.margin + i * self.cell_size
            x2 = self.margin + (self.game.board_size - 1) * self.cell_size
            y2 = y1
            width = 2 if i in [0, self.game.board_size - 1] else 1
            self.canvas.create_line(x1, y1, x2, y2, fill='#654321', width=width)

            # 竖线
            x1 = self.margin + i * self.cell_size
            y1 = self.margin
            x2 = x1
            y2 = self.margin + (self.game.board_size - 1) * self.cell_size
            width = 2 if i in [0, self.game.board_size - 1] else 1
            self.canvas.create_line(x1, y1, x2, y2, fill='#654321', width=width)

        # 绘制天元和星位
        star_positions = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for row, col in star_positions:
            x = self.margin + col * self.cell_size
            y = self.margin + row * self.cell_size
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='#654321', outline='#654321')

        # 绘制棋子
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.game.board[row][col] != EMPTY:
                    self.draw_piece(row, col, self.game.board[row][col])

        # 高亮最后落子位置
        if self.last_move:
            row, col = self.last_move
            x = self.margin + col * self.cell_size
            y = self.margin + row * self.cell_size
            self.canvas.create_rectangle(
                x-3, y-3, x+3, y+3,
                outline='red',
                width=2
            )

    def draw_piece(self, row: int, col: int, player: int):
        """绘制棋子"""
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        radius = self.cell_size // 2 - 2

        color = PLAYER_COLORS[player]

        # 绘制阴影效果
        self.canvas.create_oval(
            x - radius + 2, y - radius + 2,
            x + radius + 2, y + radius + 2,
            fill='#808080',
            outline=''
        )

        # 绘制棋子
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline='#000000' if player == WHITE else '#333333',
            width=2
        )

        # 白棋添加高光效果
        if player == WHITE:
            self.canvas.create_oval(
                x - radius // 3, y - radius // 3,
                x - radius // 3 + 8, y - radius // 3 + 8,
                fill='#FFFFFF',
                outline=''
            )

    def on_mouse_move(self, event):
        """鼠标移动事件"""
        if self.game.game_over:
            return

        col = round((event.x - self.margin) / self.cell_size)
        row = round((event.y - self.margin) / self.cell_size)

        if (0 <= row < self.game.board_size and
            0 <= col < self.game.board_size and
            self.game.board[row][col] == EMPTY):
            if self.hover_position != (row, col):
                self.hover_position = (row, col)
                # 可以在这里添加预览效果

    def on_click(self, event):
        """鼠标点击事件"""
        if self.game.game_over:
            return

        # 如果是AI回合，不响应点击
        if self.game.ai_mode and self.game.current_player == WHITE:
            return

        col = round((event.x - self.margin) / self.cell_size)
        row = round((event.y - self.margin) / self.cell_size)

        if self.game.make_move(row, col):
            self.last_move = (row, col)
            self.draw_board()
            self.update_info()

            if self.game.game_over:
                self.show_game_over()
            elif self.game.ai_mode and self.game.current_player == WHITE:
                # AI延迟落子，增加真实感
                self.root.after(500, self.ai_turn)

    def ai_turn(self):
        """AI回合"""
        move = self.game.ai_move()
        if move:
            self.last_move = move
            self.draw_board()
            self.update_info()

            if self.game.game_over:
                self.show_game_over()

    def update_info(self):
        """更新信息显示"""
        if not self.game.game_over:
            player_name = PLAYER_NAMES[self.game.current_player]
            player_color = PLAYER_COLORS[self.game.current_player]
            self.info_label.config(
                text=f"当前玩家: {player_name}",
                fg=player_color if player_color != "#FFFFFF" else "#000000"
            )

        mode_text = "人机对战" if self.game.ai_mode else "人人对战"
        self.mode_label.config(text=f"模式: {mode_text}")

    def show_game_over(self):
        """显示游戏结束信息"""
        if self.game.winner:
            winner_name = PLAYER_NAMES[self.game.winner]
            message = f"🎉 {winner_name} 获胜！"
            self.info_label.config(text=message, fg='#FF0000')
            messagebox.showinfo("游戏结束", message)
        else:
            message = "平局！"
            self.info_label.config(text=message, fg='#0000FF')
            messagebox.showinfo("游戏结束", message)

    def new_game(self):
        """开始新游戏"""
        self.game.reset()
        self.last_move = None
        self.draw_board()
        self.update_info()

    def toggle_mode(self):
        """切换游戏模式"""
        self.game.ai_mode = not self.game.ai_mode
        self.game.reset()
        self.last_move = None
        self.draw_board()
        self.update_info()

        if self.game.ai_mode:
            self.mode_button.config(text="人人对战")
        else:
            self.mode_button.config(text="人机对战")

    def undo_move(self):
        """悔棋"""
        if self.game.undo_move():
            self.last_move = self.game.move_history[-1] if self.game.move_history else None
            self.draw_board()
            self.update_info()
        else:
            messagebox.showwarning("提示", "无法悔棋")


def main():
    """主函数"""
    root = tk.Tk()

    # 设置窗口图标（如果需要的话）
    # root.iconbitmap('icon.ico')

    gui = GomokuGUI(root)

    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()