import pandas as pd
import numpy as np
from typing import List
from collections import Counter
import random


class GameOfLife:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.initial_df = self.get_initial_df(self.rows, self.columns)
        self.previous_generation_df = pd.DataFrame()
        self.next_generation_df = pd.DataFrame()

    @staticmethod
    def get_initial_df(rows, columns) -> pd.DataFrame:
        return pd.DataFrame(np.zeros((rows, columns)))
        #return pd.DataFrame(np.random.randint(0, 2, size=(rows, columns)))

    @staticmethod
    def get_all_cells_data(df: pd.DataFrame) -> List:
        cells: List = []
        for label, content in df.items():
            for c in range(len(content)):
                cells.append({"x_position": c, "y_position": label, "value": content[c]})
        return cells

    def get_cell_neighbors_positions(self, cell):
        x = cell['x_position']
        y = cell['y_position']
        dimension_x, dimension_y = self.initial_df.shape
        neighbors = [(x2, y2) for x2 in range(x - 1, x + 2)
                     for y2 in range(y - 1, y + 2)
                     if (-1 < x < dimension_x and
                         -1 < y < dimension_y and
                         (x != x2 or y != y2) and
                         (0 <= x2 < dimension_x) and
                         (0 <= y2 < dimension_y))]
        return neighbors

    def get_cell_neighbors_positions_and_values(self, cell, df) -> List:
        neighbors_positions = self.get_cell_neighbors_positions(cell)
        neighbors_cells: List = []
        for position in neighbors_positions:
            neighbors_cells.append(
                {
                    "y_position": position[0],
                    "x_position": position[1],
                    "value": df.iloc[position[0]][position[1]]
                }
            )
        return neighbors_cells

    @staticmethod
    def get_next_generation_for_cell(cell_examination, neighbors):
        neighbors_values = Counter([x['value'] for x in neighbors])
        if cell_examination['value']:
            if neighbors_values[1] < 2:
                cell_examination['value'] = 0
                return cell_examination
        else:
            if neighbors_values[1] > 2:
                cell_examination['value'] = 1
                return cell_examination
        return cell_examination


if __name__ == "__main__":
    size = [int(x) for x in input('Game frame size (rows , columns). Format example: 5, 6 \n').split(",")]
    game = GameOfLife(rows=size[0], columns=size[1])
    number_of_life_cells = int(input('Enter number of random life cells INTEGER  \n'))
    all_cells = game.get_all_cells_data(game.initial_df)
    for cell_position in random.sample(all_cells, number_of_life_cells):
        game.initial_df.iloc[cell_position['x_position']][cell_position['y_position']] = 1
    print(game.initial_df)
    game.next_generation_df = game.initial_df
    generation = 0
    while not game.previous_generation_df.equals(game.next_generation_df):
        for cell in all_cells:
            neighbors_cells = game.get_cell_neighbors_positions_and_values(cell, game.initial_df)
            cell_new_generation = game.get_next_generation_for_cell(cell_examination=cell, neighbors=neighbors_cells)
            game.next_generation_df.iloc[cell_new_generation['x_position']][cell_new_generation['y_position']] = \
                cell_new_generation['value']
        print(f"GENERATION N {generation} \n {game.next_generation_df} \n")
        game.previous_generation_df = game.next_generation_df
        input()
    print("GAME OVER")