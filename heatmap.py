import tkinter as tk
import numpy as np
import resources


class Heatmap:
    def __init__(self, root):
        self.resources = resources.Resources()
        self.heatmap_window = tk.Toplevel(root)
        self.layer_toggle_labels = ["Oil", "Metals", "Helium", "Ships", "Coral Reef", "Endangered Species"]
        self.layer_toggle_vars = tk.IntVar()  # Variables to hold toggle states

        # Styling constants
        button_font = ("Arial", 10, "bold")
        radio_font = ("Arial", 10)
        button_color = "#0078D7"  # blue
        radio_color = "#f0f0f0"  # Light grey
        text_color = "#000000"  # black

        # Create day label and arrow buttons
        self.decrement_button = tk.Button(self.heatmap_window, text="<", font=button_font, bg=button_color, fg=text_color, command=lambda: self.increment_day(-1))
        self.decrement_button.grid(row=0, column=0, pady=5, padx=5)

        self.daytext_label = tk.Label(self.heatmap_window, text="Day: ", font=button_font)
        self.daytext_label.grid(row=0, column=1, pady=5)

        self.day_var = tk.IntVar(value=1)
        self.day_label = tk.Label(self.heatmap_window, textvariable=self.day_var, font=button_font)
        self.day_label.grid(row=0, column=2, pady=5)

        self.increment_button = tk.Button(self.heatmap_window, text=">", font=button_font, bg=button_color, fg=text_color, command=lambda: self.increment_day(1))
        self.increment_button.grid(row=0, column=3, pady=5, padx=5)

        # Create layer toggles
        for i, label in enumerate(self.layer_toggle_labels):
            toggle = tk.Radiobutton(self.heatmap_window, text=label, font=radio_font, bg=radio_color,
                                    variable=self.layer_toggle_vars, value=i, indicatoron=False,
                                    command=self.draw_grid, selectcolor=button_color, fg=text_color)
            toggle.grid(row=i + 1, column=1, pady=2, sticky='ew')


        # Create and draw canvas grid
        self.canvas = tk.Canvas(self.heatmap_window, width=500, height=500)
        self.canvas.grid(row=0, column=5, rowspan=100)
        self.cell_size = 5  # size of one cell in pixels
        self.draw_grid()


    def increment_day(self, count):
        day = self.day_var.get()
        if day == 1 and count == -1:
            day = 30
        elif day == 30 and count == 1:
            day = 1
        else:
            day += count
        print(day)
        self.day_var.set(day)
        # Update grid
        self.resources.start_day(day)
        self.draw_grid()


    def draw_grid(self):
        resource = None

        # Find the maximum absolute value in the data from the checked boxes
        maxvalue = 0.0
        obtain = True
        if self.layer_toggle_vars.get() == 0:
            maxvalue += np.nanmax(self.resources.oil)
        elif self.layer_toggle_vars.get() == 1:
            maxvalue += np.nanmax(self.resources.metals)
        elif self.layer_toggle_vars.get() == 2:
            maxvalue += np.nanmax(self.resources.helium)
        elif self.layer_toggle_vars.get() == 3:
            maxvalue += np.nanmax(self.resources.ships)
        elif self.layer_toggle_vars.get() == 4:
            maxvalue += np.nanmax(self.resources.coral_reef)
            obtain = False
        elif self.layer_toggle_vars.get() == 5:
            maxvalue += np.nanmax(self.resources.endangered_species)
            obtain = False

        # Clear the canvas and redraw
        self.canvas.delete("all")
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
                    value += self.resources.oil[i, j] if self.layer_toggle_vars.get() == 0 and not np.isnan(
                        self.resources.oil[i, j]) else 0
                    value += self.resources.metals[i, j] if self.layer_toggle_vars.get() == 1 and not np.isnan(
                        self.resources.metals[i, j]) else 0
                    value += self.resources.helium[i, j] if self.layer_toggle_vars.get() == 2 and not np.isnan(
                        self.resources.helium[i, j]) else 0
                    value += self.resources.ships[i, j] if self.layer_toggle_vars.get() == 3 and not np.isnan(
                        self.resources.ships[i, j]) else 0
                    value += self.resources.coral_reef[i, j] if self.layer_toggle_vars.get() == 4 and not np.isnan(
                        self.resources.coral_reef[i, j]) else 0
                    value += self.resources.endangered_species[i, j] if self.layer_toggle_vars.get() == 5 and not np.isnan(
                        self.resources.endangered_species[i, j]) else 0

                    # Convert the total to a color for the heatmap
                    # print(i, j, value, maxvalue, minvalue)
                    if maxvalue == 0:
                        color = "#000000"
                    else:
                        # Green for preserve resources and Red for obtain resources
                        component = int(255 * value / maxvalue)  # Scale the value to the range 0-255
                        color = "#%02x0000" % component if obtain else "#00%02x00" % component
                self.canvas.create_rectangle(rectangle_left_edge,
                                             rectangle_top_edge,
                                             rectangle_right_edge,
                                             rectangle_bottom_edge,
                                             fill=color, outline="")
