import pandas as pd
import numpy as np
from typing import List
from collections import Counter
from tabulate import tabulate

from app.console import Console


class GameOfLife:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.initial_df = self.get_initial_df(self.rows, self.columns)
        self.previous_generation_df = pd.DataFrame()
        self.next_generation_df = pd.DataFrame()
        self.this_generation_df = pd.DataFrame()

    @staticmethod
    def get_initial_df(rows, columns) -> pd.DataFrame:
        return pd.DataFrame(np.zeros((rows, columns)))
        # return pd.DataFrame(np.random.randint(0, 2, size=(rows, columns)))

    @staticmethod
    def get_all_cells_data(df: pd.DataFrame) -> List:
        cells: List = []
        for label, content in df.items():
            for c in range(len(content)):
                cells.append({"x_position": c, "y_position": label, "value": content[c]})
        return cells

    def get_cell_neighbors_positions(self, cell_positions):
        x = cell_positions['x_position']
        y = cell_positions['y_position']
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
    # set initial data
    console = Console()

    # create a lifeless world
    game = GameOfLife(rows=console.init_frame_size[0], columns=console.init_frame_size[1])

    # add living organisms
    for cell_position in console.init_life_cells:
        game.initial_df.iloc[cell_position[0]][cell_position[1]] = 1
    print(f"INITIAL FRAME \n5,6{tabulate(game.initial_df, tablefmt='pipe', headers='keys')}")

    # set this and next generation
    game.this_generation_df = game.initial_df.copy()
    game.next_generation_df = game.initial_df.copy()
    generation = 0

    # time starting
    while not game.previous_generation_df.equals(game.next_generation_df):
        all_cells = game.get_all_cells_data(game.this_generation_df)
        for cell in all_cells:
            # get neighbors of selected cell
            neighbors_cells = game.get_cell_neighbors_positions_and_values(cell, game.this_generation_df)

            # find out what will happen to this place in the next generation
            cell_new_generation = game.get_next_generation_for_cell(cell_examination=cell, neighbors=neighbors_cells)

            # apply a new place to future generations
            game.next_generation_df.iloc[cell_new_generation['x_position']][cell_new_generation['y_position']] = \
                cell_new_generation['value']
        print(f"GENERATION N {generation} \n {tabulate(game.next_generation_df, tablefmt='pipe', headers='keys')} \n")

        # set previous and this generation frame for next period of time
        game.previous_generation_df = game.this_generation_df.copy()
        game.this_generation_df = game.next_generation_df.copy()
        generation += 1
        input()
    if set(game.next_generation_df.values.ravel()) == {1}:
        print("The whole world came to life !")
    elif set(game.next_generation_df.values.ravel()) == {0}:
        print("The whole world has died :(")
    else:
        print("Nothing else changes. The world will remain as it is")
    print("GAME OVER")
