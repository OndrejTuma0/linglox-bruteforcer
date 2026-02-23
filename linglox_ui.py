import requests
import keyboard
import threading
import time
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Linglox Bruteforcer")
root.geometry("300x250")

stop_typing_var = False
word_list = []
hotkeys_active = False
twowordsON = tk.BooleanVar()

def get_words(first_letter, last_letter, word_length):
    url = f"https://api.datamuse.com/words?sp={first_letter}{"?" * (word_length-2)}{last_letter}&max=1000"
    response = requests.get(url)
    if response.ok:
        status_label.config(text="Words fetched successfully.")
        data = response.json()
        return [word["word"] for word in data if " " not in word["word"]]
    else:
        status_label.config(text="Failed to fetch words.")

def check_words():
    global word_list
    firstletter = firstletter_typebox.get()
    lastletter = lastletter_typebox.get()

    try:
        wordlength = int(wordlength_typebox.get())
    except ValueError:
        status_label.config(text="Word length must be a number.")
        return

    if not len(firstletter) == 1 or not firstletter.isalpha():
        status_label.config(text="First letter must be a letter.")
        return
    if not len(lastletter) == 1 or not lastletter.isalpha():
        status_label.config(text="Last letter must be a letter.")
        return
    if wordlength < 2:
        status_label.config(text="Word length can't be smaller than 2.")
        return
    
    word_list = get_words(firstletter, lastletter, wordlength)

def show_words():
    if len(word_list) == 0:
        tk.messagebox.showinfo("Show words", "Word list is empty.")
    else:
        tk.messagebox.showinfo("Show words", f"{word_list}")

def type_words():
    global stop_typing_var
    for word in word_list:
        if stop_typing_var:
            break
        keyboard.write(word)
        keyboard.press_and_release("ctrl + a")
        keyboard.press_and_release("backspace")
        time.sleep(0.04)

def show_help():
    tk.messagebox.showinfo("How to use", "1. Fetch your words using the parameters and the 'Get Words' button.\n2. Go into Linglox, click on a textbox and press Q.\n3. The bruteforcer will try every word in the word list, if gets it correct, press E to stop.\n\nNote that this won't work on every single block/prompt. It just tries the most common words.")

def start_typing():
    global stop_typing_var
    stop_typing_var = False
    threading.Thread(target=type_words, daemon=True).start()

def stop_typing():
    global stop_typing_var
    stop_typing_var = True

def stop_program():
    os._exit(0)

def focusIn():
    global hotkeys_active
    keyboard.clear_all_hotkeys()
    hotkeys_active = False

def focusOut():
    global hotkeys_active
    if hotkeys_active:
        return
    keyboard.add_hotkey("f1", start_typing, suppress=True)
    keyboard.add_hotkey("f2", stop_typing, suppress=True)
    keyboard.add_hotkey("esc", stop_program, suppress=True)
    hotkeys_active = True

frameFirst = ttk.Frame(root)
frameFirst.pack(pady=5)

firstletter_typebox = ttk.Entry(frameFirst, width=5)
firstletter_typebox.pack(side="left", padx=5)

firstletter_label = ttk.Label(frameFirst, text="First letter")
firstletter_label.pack(side="left", padx=5)

frameLast = ttk.Frame(root)
frameLast.pack(pady=5)

lastletter_typebox = ttk.Entry(frameLast, width=5)
lastletter_typebox.pack(side="left", padx=5)

lastletter_label = ttk.Label(frameLast, text="Last letter")
lastletter_label.pack(side="left", padx=5)

frameLength = ttk.Frame(root)
frameLength.pack(pady=5)

wordlength_typebox = ttk.Entry(frameLength, width=5)
wordlength_typebox.pack(side="left", padx=5)

wordlength_label = ttk.Label(frameLength, text="Word length")
wordlength_label.pack(side="left", padx=5)

frameButtons = ttk.Frame(root)
frameButtons.pack(pady=5)

getWords_button = ttk.Button(frameButtons, text="Get Words", command=check_words)
getWords_button.pack(side="left", padx=5)

seeWords_button = ttk.Button(frameButtons, text="Show Words", command=show_words)
seeWords_button.pack(side="left", padx=5)

frameStatus = ttk.Frame(root)
frameStatus.pack(pady=5)

status_label = ttk.Label(frameStatus, text="Word list is empty.")
status_label.pack(padx=5)

frameHotkeys = ttk.Frame(root)
frameHotkeys.pack(side="bottom", pady=5)

hotkeyStart_label = ttk.Label(frameHotkeys, text="Start: F1")
hotkeyStart_label.pack(side="left", padx=5)

hotkeyStop_label = ttk.Label(frameHotkeys, text="Stop: F2")
hotkeyStop_label.pack(side="left", padx=5)

hotkeyExit_label = ttk.Label(frameHotkeys, text="Exit: Esc")
hotkeyExit_label.pack(side="left", padx=5)

frameHotkeysLabel = ttk.Frame(root)
frameHotkeysLabel.pack(side="bottom", pady=1)

hotkey_label = ttk.Label(frameHotkeysLabel, text="Hotkeys only work when focused out of bruteforcer.")
hotkey_label.pack(padx=5)

help_button = ttk.Button(root, text="?", width=2, command=show_help)
help_button.place(relx=1, y=10, x=-10, anchor="ne")

keyboard.add_hotkey("f1", start_typing, suppress=True)
keyboard.add_hotkey("f2", stop_typing, suppress=True)
keyboard.add_hotkey("esc", stop_program, suppress=True)

root.bind("<FocusIn>", lambda e: focusIn())
root.bind("<FocusOut>", lambda e: focusOut())

root.mainloop()