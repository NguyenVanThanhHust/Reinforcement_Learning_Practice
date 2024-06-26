import numpy as np
import pandas as pd

class Env:
    def __init__(self) -> None:
        self.coordinates = {
            "A": ((6, 1),),  # agent start position
            "W": ((3, range(3)), (range(5, 8), 3)),  # wall
            "T": ((range(3), 8), (3, range(8, 12))),  # trap
            "P": ((6, 10), (0, 11)),  # portal
            "LP": ((2, 1),),  # late portal
            "G": ((2, 9),),  # goal
        }   
        self.generate_grid()
        self.generate_reward_map()

    def generate_grid(self) -> pd.DataFrame:
        grid = np.zeros((8, 12), dtype=np.object_)
        for key, values in self.coordinates.items():
            for value in values:
                grid[value] = key
        self.grid = pd.DataFrame(grid)
    
    def activate_late_portal(self):
        late_portal_coordinate = self.coordinates.get("LP")[0]
        self.grid.loc[late_portal_coordinate] = "P"

    def generate_reward_map(self):
        reward_map = np.zeros((8, 12), dtype=np.float32)
        reward_map = self.coordinates["G"][0] = 1
        self.reward_map = reward_map

    def get_reward(self, coordinates: tuple = None, reverse: bool = True) -> int:
        """
        Queries the reward map and returns the reward associated to the coordinates
        @reverse: - if the coordinates are derived from the agent state, set reverse to True
                    They have to be reversed before querying the dataframe as
                    agent(state) = (x,y) = pd.Dataframe.loc(y,x) with (x,y) = (col, row)
                  - if the coordinates come from env.coordinates, then set reverse to False
                    as they are already in the (row, col) format
        """
        if reverse:
            return self.reward_map.loc[coordinates[::-1]]
        else:
            return self.reward_map.loc[coordinates]
        
        