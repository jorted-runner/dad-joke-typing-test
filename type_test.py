from tkinter import *
from tkinter import messagebox
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_url = os.environ.get("API_URL")
api_key = os.environ.get("API_KEY")
paragraph = ''
time_of_test = 0
total_time = 0
timer = None
FONT_NAME = "Courier"

def get_joke():
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    response.raise_for_status()
    return response.json()[0]['joke']

def count_down(time_of_test):
    global timer, total_time
    canvas.itemconfig(timer_text, text=(f"{time_of_test} seconds"))
    timer = window.after(1000, count_down, time_of_test + 1)
    total_time = time_of_test

def start_timer(event=None):
    global paragraph
    paragraph = get_joke()
    example_text.config(text=paragraph)
    text.delete(0, END)
    text.focus_set()
    count_down(time_of_test)

def stop_timer(event=None):
    global timer
    window.after_cancel(timer)
    user_text = text.get()
    accuracy, num_words = check_accuracy(user_text, paragraph)
    wpm = calc_wpm(num_words, total_time)
    messagebox.showinfo(title="Results", message=f"Test Results\n\nTotal Time: {total_time} seconds\nWPM: {wpm:.2f}\nAccuracy: {accuracy:.2f}%")

def check_accuracy(user_input, expected_text):
    user_input = user_input.strip()
    expected_words = expected_text.split()
    user_words = user_input.split()
    num_correct = 0
    for i in range(min(len(expected_words), len(user_words))):
        if expected_words[i] == user_words[i]:
            num_correct += 1
    accuracy = (num_correct / len(expected_words)) * 100  
    return accuracy, len(user_words)

def calc_wpm(num_words, time):
    return ((num_words / time) * 60)

window = Tk()
window.geometry("500x500")
window.config(background="light gray")
window.title("Type Speed Test")

logo_label = Label(font=(FONT_NAME, 35, 'bold'), background="light gray")
logo_label.config(text="Typing Speed Test")
logo_label.grid(column=0, row=0, columnspan=3)

canvas = Canvas(width=300, height=50, highlightthickness=0, background="light gray")
timer_text = canvas.create_text(150, 25, text="Timer", fill="black", font=(FONT_NAME, 20, "bold"))
canvas.grid(column=0, row=1, columnspan=3)

example_text = Label(font=(FONT_NAME, 15), text="This is where the example text will appear when you start the test.", wraplength=450, padx=20, pady=20, background="light gray", highlightthickness=2, highlightbackground="black")
example_text.grid(column=1, columnspan=3, row=2)

text = Entry(width=75)
text.grid_configure(padx=(20), pady=(20))
text.grid(column=1, columnspan=3, row=4)

instructions = Label(font=(FONT_NAME, 15), text="Press 'Tab' to start test.\nPress 'Enter' to end test", wraplength=500, padx=20, pady=20, background="light gray")
instructions.grid(column=0, columnspan=3, row=5)

window.bind('<Tab>', start_timer)
window.bind('<Return>', stop_timer)

window.mainloop()