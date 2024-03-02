import tkinter as tk
import heatmap
import algorithm

root = tk.Tk()

map_button = tk.Button(root, text="Map", command=lambda: heatmap.Heatmap(root))
map_button.pack()

algorithm_button = tk.Button(root, text="Algorithm", command=algorithm.run_algorithm)
algorithm_button.pack()

root.mainloop()
