import tkinter as tk
import heatmap
import algorithm 

def main():
    root = tk.Tk()
    root.title("Preservation Path")
    root.configure(bg='#f0f0f0')  # Light grey background

    # Styling constants
    label_font = ("Arial", 14)
    button_font = ("Arial", 12, "bold")
    button_color = "#0078D7" 
    entry_font = ("Arial", 12)
    padding = {"padx": 10, "pady": 10}

    # Title Label
    title_label = tk.Label(root, text="Preservation Path", font=("Arial", 18, "bold"), bg='#f0f0f0')
    title_label.pack(**padding)

    # Map Button
    map_button = tk.Button(root, text="Map", font=button_font, bg=button_color, fg='white', command=lambda: heatmap.Heatmap(root))
    map_button.pack(**padding)

    # Algorithm Button
    algo = algorithm.Algorithm()
    algorithm_button = tk.Button(root, text="Algorithm", font=button_font, bg=button_color, fg='white', command=lambda: algo.run_algorithm(1))
    algorithm_button.pack(**padding)

    # Days Radio Buttons
    create_radio_group(root, "How many days to look ahead", range(4), label_font, padding)

    # Nodes Radio Buttons
    create_radio_group(root, "Number of nodes used for checking", range(1, 4), label_font, padding)

    # Scalers Entries
    scalers_frame = tk.Frame(root, bg='#f0f0f0')
    scalers_frame.pack(**padding)
    create_scaler_entry(scalers_frame, "Extraction Scaler:", entry_font, "1")
    create_scaler_entry(scalers_frame, "Preservation Scaler:", entry_font, "2")
    create_scaler_entry(scalers_frame, "Research Scaler:", entry_font, "0.2")

    root.mainloop()

def create_radio_group(root, label_text, range_values, label_font, padding):
    frame = tk.Frame(root, bg='#f0f0f0')
    frame.pack(**padding)

    label = tk.Label(frame, text=label_text, font=label_font, bg='#f0f0f0')
    label.pack(side='top')

    radio_var = tk.IntVar()
    for i in range_values:
        tk.Radiobutton(frame, text=str(i), variable=radio_var, value=i, bg='#f0f0f0').pack(side='left')

def create_scaler_entry(frame, label, font, default_value=""):
    entry_frame = tk.Frame(frame, bg='#f0f0f0')  # Assuming frame has a background color set to light grey
    entry_frame.pack(pady=5)
    tk.Label(entry_frame, text=label, bg='#f0f0f0', font=font).pack(side='left')
    entry = tk.Entry(entry_frame, font=font, validate="key", validatecommand=(entry_frame.register(lambda P: P.replace('.', '', 1).isdigit() or P == ""), '%P'))
    entry.pack(side='left', padx=5)
    entry.insert(0, default_value)  # Set default value
    return entry

if __name__ == "__main__":
    main()
