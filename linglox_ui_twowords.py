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
root.geometry("350x300")

stop_typing_var = False
word_list_first = []
word_list_second = []
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
    global word_list_first
    global word_list_second
    firstletter_first = firstletter_firstword_typebox.get()
    lastletter_first = lastletter_firstword_typebox.get()
    firstletter_second = firstletter_secondword_typebox.get()
    lastletter_second = lastletter_secondword_typebox.get()

    try:
        wordlength_first = int(length_firstword_typebox.get())
        wordlength_second = int(length_secondword_typebox.get())
    except ValueError:
        status_label.config(text="Word length must be a number.")
        return

    if not len(firstletter_first) == 1 or not firstletter_first.isalpha() or not len(firstletter_second) == 1 or not firstletter_second.isalpha():
        status_label.config(text="First letter must be a letter.")
        return
    if not len(lastletter_first) == 1 or not lastletter_first.isalpha() or not len(lastletter_second) == 1 or not lastletter_second.isalpha():
        status_label.config(text="Last letter must be a letter.")
        return
    if wordlength_first < 2 or wordlength_second < 2:
        status_label.config(text="Word length can't be smaller than 2.")
        return

    word_list_first = get_words(firstletter_first, lastletter_first, wordlength_first)
    word_list_second = get_words(firstletter_second, lastletter_second, wordlength_second)

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
            keyboard.press_and_release("ctrl + a")
            keyboard.press_and_release("backspace")
            time.sleep(0.03)

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

firstletter_firstword_label = ttk.Label(frameFirstLetterFirstWord, text="First letter")
firstletter_firstword_label.pack(side="left", padx=5)

frameLastLetterFirstWord = ttk.Frame(frameFirstWord)
frameLastLetterFirstWord.pack(pady=5)

lastletter_firstword_typebox = ttk.Entry(frameLastLetterFirstWord, width=5)
lastletter_firstword_typebox.pack(side="left", padx=5)

lastletter_firstword_label = ttk.Label(frameLastLetterFirstWord, text="Last letter")
lastletter_firstword_label.pack(side="left", padx=5)

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

firstletter_secondword_label = ttk.Label(frameFirstLetterSecondWord, text="First letter")
firstletter_secondword_label.pack(side="left", padx=5)

frameLastLetterSecondWord = ttk.Frame(frameSecondWord)
frameLastLetterSecondWord.pack(pady=5)

lastletter_secondword_typebox = ttk.Entry(frameLastLetterSecondWord, width=5)
lastletter_secondword_typebox.pack(side="left", padx=5)

lastletter_secondword_label = ttk.Label(frameLastLetterSecondWord, text="Last letter")
lastletter_secondword_label.pack(side="left", padx=5)

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