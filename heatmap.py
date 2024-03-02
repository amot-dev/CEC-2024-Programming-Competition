import tkinter as tk


def view_heatmap(root):
    heatmap_window = tk.Toplevel(root)
    layer_toggle_labels = ["Oil", "Metals", "Helium", "Ships", "Coral Reef", "Endangered Species"]

    # Create layer toggles
    for i in range(len(layer_toggle_labels)):
        toggle = tk.Checkbutton(heatmap_window, text=layer_toggle_labels[i], height=1)
        toggle.grid(row=i, column=0, pady=0)

    # Create canvas grid
    canvas = tk.Canvas(heatmap_window, width=500, height=500)
    canvas.grid(row=0, column=1, rowspan=100)
    cell_size = 5  # size of one cell in pixels

    # Create cells in grid
    for i in range(100):
        for j in range(100):
            rectangle_left_edge = j * cell_size
            rectangle_top_edge = i * cell_size
            rectangle_right_edge = rectangle_left_edge + cell_size
            rectangle_bottom_edge = rectangle_top_edge + cell_size
            color = "#808080"
            canvas.create_rectangle(rectangle_left_edge,
                                    rectangle_top_edge,
                                    rectangle_right_edge,
                                    rectangle_bottom_edge,
                                    fill=color, outline="")
