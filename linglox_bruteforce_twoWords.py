import keyboard
import json
import threading
import time
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Linglox Bruteforcer (Two Words)")
root.geometry("350x350")

stop_typing_var = False
word_list_first = []
word_list_second = []
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
    global word_list_first
    global word_list_second
    firstletter_first = firstletter_firstword_typebox.get()
    lastletter_first = lastletter_firstword_typebox.get()
    firstletter_second = firstletter_secondword_typebox.get()
    lastletter_second = lastletter_secondword_typebox.get()
    contains_first = first_contains_typebox.get()
    contains_second = second_contains_typebox.get()

    try:
        wordlength_first = int(length_firstword_typebox.get())
        wordlength_second = int(length_secondword_typebox.get())
    except ValueError:
        status_label.config(text="Word length must be a number.")
        return

    if not firstletter_first.isalpha() or not firstletter_second.isalpha():
        status_label.config(text="First letter must be a letter.")
        return
    if wordlength_first < 2 or wordlength_second < 2:
        status_label.config(text="Word length can't be smaller than 2.")
        return
    if lastletter_first and not lastletter_first.isalpha() or lastletter_second and not lastletter_second.isalpha():
        status_label.config(text="Last letter must be a letter.")
        return
    if contains_first and not contains_first.isalpha() or contains_second and not contains_second.isalpha():
        status_label.config(text="Contains must be a letter.")
        return
    
    kwargs_first = {}
    if lastletter_first:
        kwargs_first["last_letter"] = lastletter_first
    if contains_first:
        kwargs_first["contains"] = contains_first

    kwargs_second = {}
    if lastletter_second:
        kwargs_second["last_letter"] = lastletter_second
    if contains_second:
        kwargs_second["contains"] = contains_second

    word_list_first = get_words(firstletter_first, wordlength_first, **kwargs_first)
    word_list_second = get_words(firstletter_second, wordlength_second, **kwargs_second)

def show_words():
    if len(word_list_first) == 0:
        tk.messagebox.showinfo("Show words", "Word list is empty.")
    else:
        tk.messagebox.showinfo("Show words", f"First word:\n{word_list_first} \n\n Second word:\n{word_list_second}")

def type_words():
    global stop_typing_var
    for firstWord in word_list_first:
        for secondWord in word_list_second:
            if stop_typing_var:
                break
            keyboard.write(f"{firstWord} {secondWord}")
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

###### UI #########

frameWords = ttk.Frame(root)
frameWords.pack(pady=5)

frameFirstWord = ttk.Frame(frameWords)
frameFirstWord.pack(side="left", pady=5)

firstword_label = ttk.Label(frameFirstWord, text="First word")
firstword_label.pack(padx=5)

frameFirstLetterFirstWord = ttk.Frame(frameFirstWord)
frameFirstLetterFirstWord.pack(pady=5)

firstletter_firstword_typebox = ttk.Entry(frameFirstLetterFirstWord, width=5)
firstletter_firstword_typebox.pack(side="left", padx=5)

firstletter_firstword_label = ttk.Label(frameFirstLetterFirstWord, text="Starts on")
firstletter_firstword_label.pack(side="left", padx=5)

frameLastLetterFirstWord = ttk.Frame(frameFirstWord)
frameLastLetterFirstWord.pack(pady=5)

lastletter_firstword_typebox = ttk.Entry(frameLastLetterFirstWord, width=5)
lastletter_firstword_typebox.pack(side="left", padx=5)

lastletter_firstword_label = ttk.Label(frameLastLetterFirstWord, text="Ends on (optional)")
lastletter_firstword_label.pack(side="left", padx=5)

firstword_frameContains = ttk.Frame(frameFirstWord)
firstword_frameContains.pack(pady=5)

first_contains_typebox = ttk.Entry(firstword_frameContains, width=5)
first_contains_typebox.pack(side="left", padx=5)

first_contains_label = ttk.Label(firstword_frameContains, text="Contains (optional)")
first_contains_label.pack(side="left", padx=5)

frameLengthFirstWord = ttk.Frame(frameFirstWord)
frameLengthFirstWord.pack(pady=5)

length_firstword_typebox = ttk.Entry(frameLengthFirstWord, width=5)
length_firstword_typebox.pack(side="left", padx=5)

length_firstword_label = ttk.Label(frameLengthFirstWord, text="Word length")
length_firstword_label.pack(side="left", padx=5)

##################

frameSecondWord = ttk.Frame(frameWords)
frameSecondWord.pack(side="left", pady=5)

secondword_label = ttk.Label(frameSecondWord, text="Second word")
secondword_label.pack(padx=5)

frameFirstLetterSecondWord = ttk.Frame(frameSecondWord)
frameFirstLetterSecondWord.pack(pady=5)

firstletter_secondword_typebox = ttk.Entry(frameFirstLetterSecondWord, width=5)
firstletter_secondword_typebox.pack(side="left", padx=5)

firstletter_secondword_label = ttk.Label(frameFirstLetterSecondWord, text="Starts on")
firstletter_secondword_label.pack(side="left", padx=5)

frameLastLetterSecondWord = ttk.Frame(frameSecondWord)
frameLastLetterSecondWord.pack(pady=5)

lastletter_secondword_typebox = ttk.Entry(frameLastLetterSecondWord, width=5)
lastletter_secondword_typebox.pack(side="left", padx=5)

lastletter_secondword_label = ttk.Label(frameLastLetterSecondWord, text="Ends on (optional)")
lastletter_secondword_label.pack(side="left", padx=5)

secondword_frameContains = ttk.Frame(frameSecondWord)
secondword_frameContains.pack(pady=5)

second_contains_typebox = ttk.Entry(secondword_frameContains, width=5)
second_contains_typebox.pack(side="left", padx=5)

second_contains_label = ttk.Label(secondword_frameContains, text="Contains (optional)")
second_contains_label.pack(side="left", padx=5)

frameLengthSecondWord = ttk.Frame(frameSecondWord)
frameLengthSecondWord.pack(pady=5)

length_secondword_typebox = ttk.Entry(frameLengthSecondWord, width=5)
length_secondword_typebox.pack(side="left", padx=5)

length_secondword_label = ttk.Label(frameLengthSecondWord, text="Word length")
length_secondword_label.pack(side="left", padx=5)

############################

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

help_button = ttk.Button(root, text="?", width=2, command=show_help)
help_button.place(relx=1, y=10, x=-10, anchor="ne")

keyboard.add_hotkey("f1", start_typing, suppress=True)
keyboard.add_hotkey("f2", stop_typing, suppress=True)
keyboard.add_hotkey("esc", stop_program, suppress=True)

root.bind("<FocusIn>", lambda e: focusIn())
root.bind("<FocusOut>", lambda e: focusOut())

root.mainloop()