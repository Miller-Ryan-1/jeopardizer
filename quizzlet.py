'''
This is the logic and GUI buildout for the Jeopardizer App.
This app uses a database of over 250,000 jeopardy questions from seasons 18 (2001) through 38 (2022).
The database is contained in a .csv file called 'master_question_list.csv' and is loaded as a dataframe.
'''

# Some DS libraries
import pandas as pd
import numpy as np
import time

# Tkinter GUI and PIL for in-GUI images
from tkinter import *
from PIL import ImageTk, Image

# Stat Tracking Initializers
global level, num_correct, total_questions, streak, df
level = 1
num_correct = 0
total_questions = 0
streak = 0

# Load Dataframe and replace Null values with the word 'Null' (the actual answer)
df = pd.read_csv('master_question_list.csv', index_col = 0).drop(columns = 'index').fillna(f'Null')

# There are 2011 years listed as just '11', so they need to be converted to 2011
df['show_yr'] = np.where(df['show_yr'] == 11, 2011, df['show_yr'])

# Create the root frame
root = Tk()
root.title('Jeopardizer')
root.geometry('900x600')

# Display welcome text (static)
welcome_text = 'LET\'S PLAY JEOPARDY!'
welcome = Label(root, text = welcome_text, font = ('Impact', 24), width = 800, height = 2, bg = '#060CE9', fg = 'white')

# Display image (to be replaced by static instructions)
welcome_image = ImageTk.PhotoImage(Image.open('trebek.jpeg'))
trebek = Label(root, image = welcome_image)

# The pack actually displays them
welcome.pack()
trebek.pack()

# This ensures the mainloop displays at this point
root.update()

# Honor Trebek for a few seconds
time.sleep(3)

# Maybe I should change the label name...
trebek.destroy()

# Instructions to display
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
instructions = Label(root, anchor = W, text = instructions_text, width = 800, justify = LEFT, font=('Helvetica',11), bg = '#060CE9', fg = 'white')

# Creates the frame the app uses for events
active_frame = Frame(root)

instructions.pack()
active_frame.pack()

# Creates a start button.  When clicked goes to question screen.  The start frame is also passed so it can be destroyed.
start = Frame(active_frame)
start.pack()

# When clicked goes to clue screen.  The start frame is also passed so it can be destroyed.
start_button = Button(start, text = 'START', command = lambda: clueboard(start))
start_button.pack()


# -------------------------------------------------------------------------------
# CREATE CLUEBOARD
# -------------------------------------------------------------------------------

def clueboard(start):
    '''
    Loads 4 random questions from the database based on current difficulty level (1-6).
    Displays each question's category on a button.
    User selects the category of their choosing by clicking its button.
    '''
    # Get rid of start button
    start.destroy()

    # Create new frame to replace start button
    clues = Frame(active_frame)
    clues.pack()

    # Current Player Stats
    record = Label(clues, font = ('Helvetica',18), text = f'Correct: {num_correct}/{total_questions}')
    streak_counter = Label(clues, font = ('Helvetica',18), text = f'Steak: {streak}')
    curr_level = Label(clues, font = ('Helvetica',18), text = f'Level: {level}')

    # This object holds the four questions
    button_text = df[df.level == level].sample(4)

    # Create a button for each question, displaying the category.  Passes the question object and question number.
    # Also passes the clue frame so it can be destroyed.
    button1 = Button(clues, text = button_text.iloc[0][4], font = ('Times New Roman',14), height = 6, width = 30, wraplength = 120, command = lambda: question(button_text,0, clues))
    button2 = Button(clues, text = button_text.iloc[1][4], font = ('Times New Roman',14), height = 6, width = 30, wraplength = 120, command = lambda: question(button_text,1, clues))
    button3 = Button(clues, text = button_text.iloc[2][4], font = ('Times New Roman',14), height = 6, width = 30, wraplength = 120, command = lambda: question(button_text,2, clues))
    button4 = Button(clues, text = button_text.iloc[3][4], font = ('Times New Roman',14), height = 6, width = 30, wraplength = 120, command = lambda: question(button_text,3, clues))

    # Place the lables and buttons via a grid system
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
    '''
    Based on the selected category, displays the question as well as information about the
    question and show it came from. 
    Includes a countdown timer giving players 10 seconds to read and answer before question disappears.
    Players can answer at any time by pressing 'Answered' button.
    '''

    # Get rid of clues
    clues.destroy()

    # Replace clues with quesiton frame
    question = Frame(active_frame)
    question.pack()

    # Current stats
    record = Label(question, font = ('Helvetica',18), text = f'Correct: {num_correct}/{total_questions}')
    streak_counter = Label(question, font = ('Helvetica',18), text = f'Steak: {streak}')
    curr_level = Label(question, font = ('Helvetica',18), text = f'Level: {level}')

    # Question Information - note it pulls from question object passed
    category = Label(question, text = f'Category: {button_text.iloc[q_index][4]}')
    q_round = Label(question, text = f'Round: {button_text.iloc[q_index][3]}')
    q_value = Label(question, text = f'Value: ${button_text.iloc[q_index][5]}')
    show_yr = Label(question, text = f'Show Year: {button_text.iloc[q_index][1]}')
    show_mo = Label(question, text = f'Show Month: {button_text.iloc[q_index][2]}')

    # Question Itself
    q = Label(question, font = ('Helvetica',18), wraplength = 600, text = button_text.iloc[q_index][6])

    # This button moves to the answer screen, also passing the question and counter frames for destruction
    answer_now = Button(question, padx = 20, pady = 20, text = 'Answered', command = lambda: answer(button_text.iloc[q_index],question, counter))
    
    # Places the widgets
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

    # Creates a frame to hold a countdown timer
    counter = Frame(active_frame)
    counter.pack()

    # Initiailize the timer (uses 12 second, can be changed) and the label that holds it
    timer = 12
    countdown = Label(counter, font = ('Helvetica',24), text = timer)
    countdown.pack()

    # Ensures the app runs to this point, otherwise it is blocked by the countdown loop
    active_frame.update()

    # Countdown loop
    while timer > 0:
        timer -= 1
        # 1 second countdown, naturally
        time.sleep(1)
        # Update the label with the new time
        countdown.config(text = timer)
        countdown.update()

        # Once the timer is up, hide the question and change the button name
        if timer == 1:
            q.config(text = 'Out of Time')
            answer_now.config(text = 'See Answer')
            countdown.destroy()

# -------------------------------------------------------------------------------
# ANSWER
# -------------------------------------------------------------------------------

def answer(entry, question, counter):
    '''
    Reveals the answer.  Player then, on honor, answers whether they got it right or not, 
    and within the allotted time.
    '''

    # Clean up
    question.destroy()
    counter.destroy()

    # Answer frame creation
    answer = Frame(active_frame)
    answer.pack()

    # Reminder of the question
    q = Label(answer, text = entry[6])

    # Gives answer
    corr_answer = Label(answer, font = ('Helvetica',24), text = f'What is {entry[8]}?')

    # Creates buttons for either correct or incorrect/missed
    corr_button = Button(answer, padx = 20, pady = 20, text = 'Answered Correctly', command = lambda : correct_answer(answer))
    incorr_button = Button(answer, padx = 20, pady = 20, text = 'Incorrect/Out-of-Time', command = lambda : incorrect_answer(answer))

    # Place everything
    q.grid(row = 0, column = 0, columnspan = 2)
    corr_answer.grid(row = 1, column = 0, columnspan = 2, rowspan = 2)

    corr_button.grid(row = 3, column = 0)
    incorr_button.grid(row = 3, column = 1)


def correct_answer(answer):
    '''
    This updates the stats on a correct answer and returns to the clueboard for the next question
    '''
    # Needs to refer to the global stat-keeping variables, adding +1 to all
    global level, num_correct, total_questions, streak
    total_questions += 1
    num_correct += 1
    streak += 1

    # Levels are capped at 6
    if level < 6:
        level += 1
    
    clueboard(answer)


def incorrect_answer(answer):
    '''
    This updates the stats on an incorrect/missed answer and returns to the clueboard for the next question
    '''
    # Needs to refer to the global stat-keeping variables
    global level, total_questions, streak
    total_questions += 1
    
    # Level floor is 1
    if level > 1:
        level -= 1
    
    # Reset streak, darn!
    streak = 0

    clueboard(answer)

mainloop()