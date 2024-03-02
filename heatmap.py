import tkinter as tk

# placeholder
heatmap = [["#FFF000" for _ in range(10)] for _ in range(10)]


def view_map(root):
    map_window = tk.Toplevel(root)
    for i in range(10):
        for j in range(10):
            label = tk.Label(map_window, bg=heatmap[i][j], width=2, height=1)
            label.grid(row=i, column=j)
