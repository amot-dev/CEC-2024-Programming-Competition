import tkinter as tk
import numpy as np
import resources


class Heatmap:
    def __init__(self, root):
        self.resources = resources.Resources()
        self.heatmap_window = tk.Toplevel(root)
        self.layer_toggle_labels = ["Oil", "Metals", "Helium", "Ships", "Coral Reef", "Endangered Species"]
        self.layer_toggle_vars = [tk.IntVar() for _ in self.layer_toggle_labels]  # Variables to hold toggle states

        # Create day label and arrow buttons
        self.decrement_button = tk.Button(self.heatmap_window, text="<", command=lambda: self.increment_day(-1))
        self.decrement_button.grid(row=0, column=0, pady=0)

        self.day_var = tk.IntVar(value=1)
        self.day_label = tk.Label(self.heatmap_window, textvariable=self.day_var)
        self.day_label.grid(row=0, column=1, pady=0)

        self.increment_button = tk.Button(self.heatmap_window, text=">", command=lambda: self.increment_day(1))
        self.increment_button.grid(row=0, column=2, pady=0)

        # Create layer toggles
        for i in range(len(self.layer_toggle_labels)):
            toggle = tk.Checkbutton(self.heatmap_window, text=self.layer_toggle_labels[i],
                                    variable=self.layer_toggle_vars[i], command=self.draw_grid)
            toggle.grid(row=i + 1, column=0, pady=0)  # Start from row 1 to leave space for day label and buttons

        # Create and draw canvas grid
        self.canvas = tk.Canvas(self.heatmap_window, width=500, height=500)
        self.canvas.grid(row=0, column=3, rowspan=100)
        self.cell_size = 5  # size of one cell in pixels
        self.draw_grid()

    def increment_day(self, count):
        day = self.day_var.get()
        if day == 1 and count == -1:
            day = 30
        elif day == 30 and count == 1:
            day = 1
        else:
            day += 1

        self.day_var.set(day)
        # Update grid
        self.resources.start_day(day)
        self.draw_grid()

    def draw_grid(self):
        resource = None


        # Find the maximum absolute value in the data from the checked boxes
        minvalue = 0.0
        maxvalue = 0.0
        obtain = True
        if self.layer_toggle_vars[0].get():
            maxvalue += np.nanmax(self.resources.oil)
        elif self.layer_toggle_vars[1].get():
            maxvalue += np.nanmax(self.resources.metals)
        elif self.layer_toggle_vars[2].get():
            maxvalue += np.nanmax(self.resources.helium)
        elif self.layer_toggle_vars[3].get():
            maxvalue += np.nanmax(self.resources.ships)
        elif self.layer_toggle_vars[4].get():
            maxvalue += np.nanmax(self.resources.coral_reef)
            obtain = False
        elif self.layer_toggle_vars[5].get():
            maxvalue += np.nanmax(self.resources.endangered_species)
            obtain = False

        self.canvas.delete("all")  # Clear the canvas
        for i in range(100):
            for j in range(100):
                rectangle_left_edge = j * self.cell_size
                rectangle_top_edge = i * self.cell_size
                rectangle_right_edge = rectangle_left_edge + self.cell_size
                rectangle_bottom_edge = rectangle_top_edge + self.cell_size
                if self.resources.world[i, j] == 1:
                    color = "#808080"
                else:
                    # Take the value of the selected radio box (unselected boxes will add 0)
                    value = 0
                    value += self.resources.oil[i, j] if self.layer_toggle_vars[0].get() and not np.isnan(self.resources.oil[i, j]) else 0
                    value += self.resources.metals[i, j] if self.layer_toggle_vars[1].get() and not np.isnan(self.resources.metals[i, j]) else 0
                    value += self.resources.helium[i, j] if self.layer_toggle_vars[2].get() and not np.isnan(self.resources.helium[i, j]) else 0
                    value += self.resources.ships[i, j] if self.layer_toggle_vars[3].get() and not np.isnan(self.resources.ships[i, j]) else 0
                    value += self.resources.coral_reef[i, j] if self.layer_toggle_vars[4].get() and not np.isnan(self.resources.coral_reef[i, j]) else 0
                    value += self.resources.endangered_species[i, j] if self.layer_toggle_vars[5].get() and not np.isnan(self.resources.endangered_species[i, j]) else 0

                    # Convert the total to a color for the heatmap
                    print(i, j, value, maxvalue, minvalue)
                    if maxvalue == 0:
                        color = "#000000"
                    else:
                        # Green for preserve resources and Red for obtain resources
                        component = int(255 * value / maxvalue)  # Scale the value to the range 0-255
                        color = "#00%02x00" % component if obtain else "#%02x0000" % component
                self.canvas.create_rectangle(rectangle_left_edge,
                                             rectangle_top_edge,
                                             rectangle_right_edge,
                                             rectangle_bottom_edge,
                                             fill=color, outline="")
