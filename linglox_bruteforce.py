import json
import keyboard
import threading
import time
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Linglox Bruteforcer")
root.geometry("300x300")

stop_typing_var = False
word_list = []
hotkeys_active = False

interval = 0.05

base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(base, "words_dictionary.json")) as f:
    words = json.load(f)

def get_words(first_letter, word_length, last_letter="", contains=""):
    status_label.config(text="Words fetched succesfully.")
    return [
        word for word in words
        if len(word) == word_length
        and word.lower().startswith(first_letter)
        and (not last_letter or word.lower().endswith(last_letter))
        and (not contains or contains in word.lower())
    ]

def check_words():
    global word_list
    firstletter = firstletter_typebox.get()
    lastletter = lastletter_typebox.get()
    contains = contains_typebox.get()

    try:
        wordlength = int(wordlength_typebox.get())
    except ValueError:
        status_label.config(text="Word length must be a number.")
        return

    if not firstletter.isalpha():
        status_label.config(text="First letter must be a letter.")
        return
    if wordlength < 2:
        status_label.config(text="Word length can't be smaller than 2.")
        return
    if lastletter and not lastletter.isalpha():
        status_label.config(text="Last letter must be a letter.")
        return
    if contains and not contains.isalpha():
        status_label.config(text="Contains must be a letter.")
        return
    
    kwargs = {}
    if lastletter:
        kwargs["last_letter"] = lastletter
    if contains:
        kwargs["contains"] = contains

    word_list = get_words(firstletter, wordlength, **kwargs)

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
        keyboard.write(f"{word}")
        time.sleep(0.01)
        keyboard.press_and_release("ctrl + a")
        keyboard.press_and_release("backspace")
        time.sleep(interval)

def show_help():
    tk.messagebox.showinfo("How to use", "1. Input the parameters and fetch your words using the 'Get Words' button.\n2. Go into Linglox, click on a textbox and press F1.\n3. The bruteforcer will try every word in the word list, if gets it correct, press F2 to stop.\n\nNote that this won't work on every single block/prompt. It just tries the most common words.\n\nSet the interval depending on the word length and your pc performance (If it's too low some words will not finish typing and it'll glitch out)")

def start_typing():
    global stop_typing_var
    stop_typing_var = False
    threading.Thread(target=type_words, daemon=True).start()

def stop_typing():
    global stop_typing_var
    stop_typing_var = True

def stop_program():
    os._exit(0)

def set_interval():
    global interval
    try:
        input = int(interval_typebox.get())
    except ValueError:
        status_label.config(text="Interval must be a number")
        return
    
    if input < 10:
        status_label.config(text="Interval must be atleast 10ms")
        return
    
    interval = input / 1000
    interval_label.config(text=f"Current interval: {interval*1000} ms")

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

############ UI ###########

frameFirst = ttk.Frame(root)
frameFirst.pack(pady=5)

firstletter_typebox = ttk.Entry(frameFirst, width=5)
firstletter_typebox.pack(side="left", padx=5)

firstletter_label = ttk.Label(frameFirst, text="Starts on")
firstletter_label.pack(side="left", padx=5)

frameLast = ttk.Frame(root)
frameLast.pack(pady=5)

lastletter_typebox = ttk.Entry(frameLast, width=5)
lastletter_typebox.pack(side="left", padx=5)

lastletter_label = ttk.Label(frameLast, text="Ends on (optional)")
lastletter_label.pack(side="left", padx=5)

frameContains = ttk.Frame(root)
frameContains.pack(pady=5)

contains_typebox = ttk.Entry(frameContains, width=5)
contains_typebox.pack(side="left", padx=5)

contains_label = ttk.Label(frameContains, text="Contains (optional)")
contains_label.pack(side="left", padx=5)

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

frameInterval = ttk.Frame(root)
frameInterval.pack(pady=10)

interval_typebox = ttk.Entry(frameInterval, width=5)
interval_typebox.pack(side="left", padx=5)
interval_typebox.insert(0, "50")

interval_label = ttk.Label(frameInterval, text="Interval (ms)")
interval_label.pack(side="left", padx=5)

interval_button = ttk.Button(frameInterval, text="Set", width=5, command=set_interval)
interval_button.pack(side="left", padx=5)

frameIntervalLabel = ttk.Frame(root)
frameIntervalLabel.pack(pady=5)

interval_label = ttk.Label(frameIntervalLabel, text=f"Current interval: {interval*1000} ms")
interval_label.pack(padx=5)

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