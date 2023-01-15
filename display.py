"""
Module: display.py
Displays output with given content to user.
Includes GUI (messagebox) and TUI (colored texts) versions.
"""

from tkinter import messagebox
import os

message_box_warning = messagebox.showwarning
message_box_error = messagebox.showerror
message_box_info = messagebox.showinfo


def terminal_error(message: str):
    """ Display error with red colored error prefix and given content. """
    print(f"[\033[7;31m ERROR \033[0;0m] \033[31m{message}\033[0;0m")

def terminal_warning(message: str):
    """ Display warning with orange colored warning prefix and given content. """
    print(f"[\033[7;33m WARNING \033[0;0m] \033[33m{message}\033[0;0m")

def terminal_info(message: str):
    """ Display info with blue colored info prefix and given content. """
    print(f"[\033[7;34m INFO \033[0;0m] \033[34m{message}\033[0;0m")

def terminal_success(message: str):
    """ Display success message with green colored success prefix and given content. """
    print(f"[\033[7;32m SUCCESS \033[0;0m] \033[32m{message}\033[0;0m")

def terminal_custom(title: str, message: str):
    """ Display styled message with custom title. """
    print(f"[\033[7;35m {title} \033[0;0m] \033[35m{message}\033[0;0m")

def cls():
    """ Clear terminal's screen. """
    os.system("cls")

