import tkinter as tk
import heatmap
import algorithm

root = tk.Tk()

map_button = tk.Button(root, text="Map", command=lambda: heatmap.view_heatmap(root))
map_button.pack()

algorithm_button = tk.Button(root, text="Algorithm", command=algorithm.run_algorithm)
algorithm_button.pack()

root.mainloop()
