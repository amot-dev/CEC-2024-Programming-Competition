import tkinter as tk
import heatmap
import algorithm
import numpy as np

root = tk.Tk()

map_button = tk.Button(root, text="Map", command=lambda: heatmap.view_map(root))
map_button.pack()

algorithm_button = tk.Button(root, text="Algorithm", command=algorithm.run_algorithm)
algorithm_button.pack()


class Resources:
    def __init__(self, oil, metals, helium, ships, coral_reef, endangered_species):
        self.oil = self.generate_table(oil)
        self.metals = self.generate_table(metals)
        self.helium = self.generate_table(helium)
        self.ships = self.generate_table(ships)
        self.coral_reef = self.generate_table(coral_reef)
        self.endangered_species = self.generate_table(endangered_species)

    def generate_table(self, file):
        # Load CSV file into a NumPy array, skipping the first line
        data = np.genfromtxt(file, delimiter=',', skip_header=1)
        x_coords = data[:, 1].astype(int)
        y_coords = data[:, 2].astype(int)
        values = data[:, 3]
        table_shape = (np.max(x_coords) + 1, np.max(y_coords) + 1)
        table = np.zeros(table_shape)
        table[x_coords, y_coords] = values
        return table







root.mainloop()
