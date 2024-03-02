import numpy as np


class Resources:
    def __init__(self, day=1):
        self.world = None
        self.oil = None
        self.metals = None
        self.helium = None
        self.ships = None
        self.coral_reef = None
        self.endangered_species = None
        self.start_day(day)

    def start_day(self, day):
        self.world = self.generate_table(f"data/world_array_data_day_{day}.csv")
        self.oil = self.generate_table(f"data/oil_data_day_{day}.csv")
        self.metals = self.generate_table(f"data/metal_data_day_{day}.csv")
        self.helium = self.generate_table(f"data/helium_data_day_{day}.csv")
        self.ships = self.generate_table(f"data/ship_data_day_{day}.csv")
        self.coral_reef = self.generate_table(f"data/coral_data_day_{day}.csv")
        self.endangered_species = self.generate_table(f"data/species_data_day_{day}.csv")

    def generate_table(self, file):
        # Load CSV file into a NumPy array, skipping the first line
        data = np.genfromtxt(file, delimiter=',', skip_header=1)
        x_coords = data[:, 1].astype(int)
        y_coords = data[:, 2].astype(int)
        value = data[:, 3]
        table_shape = (np.max(x_coords) + 1, np.max(y_coords) + 1)
        table = np.zeros(table_shape)
        table[x_coords, y_coords] = abs(value)
        return table
