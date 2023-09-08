# Start of UI file

# Importing required modules
import tkinter as tk

def create_window():
    # This function will create a new window
    window = tk.Tk()
    window.title("Prototype UI")

def create_buttons():
    # This function will create some buttons
    button1 = tk.Button(master=window, text="Button 1")
    button1.pack()

def finish_ui():
    # This function completes the UI
    create_buttons()
    
    # This line starts the Tkinter event loop
    window.mainloop()

# Running the UI
if __name__ == "__main__":
    create_window()
    finish_ui()
# End of UI file