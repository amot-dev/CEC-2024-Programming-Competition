import numpy as np


class Resources:
    def __init__(self, day=1):
        self.world = None
        self.obtainable_scale = 1
        self.preservation_scale = 2
        self.information_scale = 0.2

        self.oil = None
        self.metals = None
        self.helium = None
        self.ships = None
        self.coral_reef = None
        self.endangered_species = None
        self.algal = None
        self.start_day(day)

    def start_day(self, day):
        self.world = self.generate_table(f"data/world_array_data_day_{day}.csv")
        self.oil = self.generate_table(f"data/oil_data_day_{day}.csv")
        self.metals = self.generate_table(f"data/metal_data_day_{day}.csv")
        self.helium = self.generate_table(f"data/helium_data_day_{day}.csv")
        self.ships = self.generate_table(f"data/ship_data_day_{day}.csv")
        self.coral_reef = self.generate_table(f"data/coral_data_day_{day}.csv")
        self.endangered_species = self.generate_table(f"data/species_data_day_{day}.csv")
        self.algal = self.generate_table(f"data/algal_data_day_{day}.csv")

    def calculate_value(self, x, y):
        # Sum values based on weights
        value = 0
        value += self.obtainable_scale * self.oil[x, y]
        value += self.obtainable_scale * self.metals[x, y]
        value += self.obtainable_scale * self.helium[x, y]
        value += self.obtainable_scale * self.ships[x, y]
        value -= self.preservation_scale * self.coral_reef[x, y]
        value += self.preservation_scale * self.endangered_species[x, y]
        value += self.information_scale * self.algal[x, y]
        return value

    def generate_table(self, file):
        # Load CSV file into a NumPy array, skipping the first line
        data = np.genfromtxt(file, delimiter=',', skip_header=1)
        x_coords = data[:, 1].astype(int)
        y_coords = data[:, 2].astype(int)
        values = data[:, 3]

        # absolute values to ensure all values are positive
        abs_values = np.abs(values)
        # Find the maximum value for normalization
        max_value = np.max(abs_values)
        # Avoid division by zero by checking if max_value is not 0
        normalized_values = abs_values / max_value if max_value > 0 else abs_values

        # Determine the shape of the table based on the max coordinates
        table_shape = (np.max(x_coords) + 1, np.max(y_coords) + 1)
        # Initialize the table with zeros
        table = np.zeros(table_shape)

        table[x_coords, y_coords] = normalized_values

        return table