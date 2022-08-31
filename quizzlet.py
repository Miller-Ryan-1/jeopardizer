'''
Jeopardy Quiz App
To Dos:
1. Fix all sizes and layouts
2. Figure out timer for answer function
3. Figure out how to get this standalone so someone without Python or dependencies can use it
4. Pop Trebek in there for a few seconds and then replace that frame with the instruction
5. Else?...
'''

import pandas as pd
import numpy as np
import re

from tkinter import *
from PIL import ImageTk, Image

# Initializers
global level, num_correct, total_questions, streak, df
level = 1
num_correct = 0
total_questions = 0
streak = 0

# Load Dataframe
df = pd.read_csv('master_question_list.csv', index_col = 0).drop(columns = 'index').fillna(f'Null')

# Below is the first page
root = Tk()
root.title('Jeopardizer')

welcome_text = 'LET\'S PLAY JEOPARDY!'
welcome = Label(root, text = welcome_text, width = 100, height = 2, bg = 'blue', fg = 'white')

instructions_text = '''
                    Instructions:\n
                    1. Click START below.\n
                    2. Select a category from the four displayed.\n
                    3. After clicking on the selected category, the question will be displayed for 10 seconds, or until ANSWER is clicked.\n
                    4. The answer will be displayed, along with details including the year and month of the show the question is from.\n
                    5. If you get it correct, click the CORRECT button.  Your difficultly level (shown in the upper right) will increase by one.\n
                    6. If you get it wrong, or the timer ran out before you answered, click the MISSED/SKIPPED button.  The difficulty level will decrease by one (if greater than 1).\n
                    7. Difficulty ranges from 1 to 6 (all final jeopardies). Difficulty 5 level questions are all triple stumpers (no player got the answer on the show).\n
                    8. Quit anytime by closing the window.
                    '''
instructions = Label(root, text = instructions_text, width = 100, justify = 'left', wraplength = 600)

active_frame = Frame(root)

welcome.pack()
instructions.pack()
active_frame.pack()

# ToDo: Disable the button but keep the root going in the background (since it has instructions)
frame1 = Frame(active_frame)
frame1.pack()

start_button = Button(frame1, text = 'START', command = lambda: clueboard(frame1))

start_button.pack()


# -------------------------------------------------------------------------------
# CREATE CLUEBOARD
# -------------------------------------------------------------------------------

def clueboard(frame1):
    frame1.destroy() ###

    clues = Frame(active_frame)
    clues.pack()
    # clues = Toplevel()
    # clues.title('Clues')

    record = Label(clues, text = f'Correct: {num_correct}/{total_questions}')
    streak_counter = Label(clues, text = f'Steak: {streak}')
    curr_level = Label(clues, text = f'Level: {level}')

    button_text = df[df.level == level].sample(4)

    button1 = Button(clues, text = button_text.iloc[0][4], command = lambda: question(button_text,0, clues))
    button2 = Button(clues, text = button_text.iloc[1][4], command = lambda: question(button_text,1, clues))
    button3 = Button(clues, text = button_text.iloc[2][4], command = lambda: question(button_text,2, clues))
    button4 = Button(clues, text = button_text.iloc[3][4], command = lambda: question(button_text,3, clues))

    record.grid(row = 0, column = 0)
    streak_counter.grid(row = 1, column = 0)
    curr_level.grid(row = 0, column = 1, rowspan = 2)
    button1.grid(row=2, column = 0)
    button2.grid(row=2, column = 1)
    button3.grid(row=3, column = 0)
    button4.grid(row=3, column = 1)


# -------------------------------------------------------------------------------
# QUESTION
# -------------------------------------------------------------------------------

def question(button_text, q_index, clues):

    clues.destroy() ###

    question = Frame(active_frame)
    question.pack()
    # question = Toplevel()
    # question.title('Question')

    record = Label(question, text = f'Correct: {num_correct}/{total_questions}')
    streak_counter = Label(question, text = f'Steak: {streak}')
    curr_level = Label(question, text = f'Level: {level}')

    category = Label(question, text = f'Category: {button_text.iloc[q_index][4]}')
    q_round = Label(question, text = f'Round: {button_text.iloc[q_index][3]}')
    q_value = Label(question, text = f'Value: ${button_text.iloc[q_index][5]}')
    show_yr = Label(question, text = f'Show Year: {button_text.iloc[q_index][1]}')
    show_mo = Label(question, text = f'Show Month: {button_text.iloc[q_index][2]}')

    q = Label(question, text = button_text.iloc[q_index][6])

    answer_now = Button(question, text = 'Answered', command = lambda: answer(button_text.iloc[q_index],question))
    
    record.grid(row = 0, column = 0)
    streak_counter.grid(row = 1, column = 0)
    curr_level.grid(row = 0, column = 1, rowspan = 2)

    category.grid(row = 2, column = 0, columnspan = 2)
    q_round.grid(row = 3, column = 0)
    q_value.grid(row = 3, column = 1)
    show_yr.grid(row = 4, column = 0)
    show_mo.grid(row = 4, column = 1)

    q.grid(row = 5, column = 0, columnspan = 2)

    answer_now.grid(row = 6, column = 0, columnspan = 2)


# -------------------------------------------------------------------------------
# ANSWER
# -------------------------------------------------------------------------------

def answer(entry, question):
    question.destroy()

    answer = Frame(active_frame)
    answer.pack()
    # answer = Toplevel()
    # answer.title('Answer')

    # question.destroy()

    q = Label(answer, text = entry[6])

    corr_answer = Label(answer, text = entry[8])

    corr_button = Button(answer, text = 'Answered Correctly', command = lambda : correct_answer(answer))
    incorr_button = Button(answer, text = 'Incorrect/Out-of-Time', command = lambda : incorrect_answer(answer))

    q.grid(row = 0, column = 0, columnspan = 2)
    corr_answer.grid(row = 1, column = 0, columnspan = 2)

    corr_button.grid(row = 2, column = 0)
    incorr_button.grid(row = 2, column = 1)


def correct_answer(answer):

    #answer.destroy()

    global level, num_correct, total_questions, streak
    total_questions += 1
    num_correct += 1
    streak += 1

    if level < 6:
        level += 1
    
    clueboard(answer)


def incorrect_answer(answer):

    #answer.destroy()

    global level, num_correct, total_questions, streak
    total_questions += 1
    
    if level > 1:
        level -= 1
    
    streak = 0

    clueboard(answer)







mainloop()