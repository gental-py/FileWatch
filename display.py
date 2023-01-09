from tkinter import messagebox

error = messagebox.showerror
warning = messagebox.showwarning
info = messagebox.showinfo


class StyleShell:
    """ Display message with different styles. """

    def error(message: str):
        print(f"[\033[7;31m ERROR \033[0;0m] \033[31m{message}\033[0;0m")

    def warning(message: str):
        print(f"[\033[7;33m WARNING \033[0;0m] \033[33m{message}\033[0;0m")

    def info(message: str):
        print(f"[\033[7;34m INFO \033[0;0m] \033[34m{message}\033[0;0m")

    def success(message: str):
        print(f"[\033[7;32m SUCCESS \033[0;0m] \033[32m{message}\033[0;0m")
    

