import tkinter as tk

root = tk.Tk()
container = tk.Frame(root, bg = "yellow")
container.pack(expand = True, fill = "both")
drawArea = tk.Canvas(container, bg = "red")
drawArea.update()
drawArea.configure(width = container.winfo_width(), height = container.winfo_height())
drawArea.pack()

root.mainloop()