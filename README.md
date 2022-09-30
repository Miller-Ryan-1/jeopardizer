## Jeopardizer

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Project Summary
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

#### Project Description
> - Many consider Jeopardy the apex of television gameshow competition.  Since the domination of Ken Jennings showed combining skill and preparation with strategy could lead to life changing outcomes, dozens of players have gone on huge winning streaks, often incrementally advancing certain strategems around preparation, board navigation/daily double targeting, and wagering.
> - Using the [J! Archive](https://j-archive.com/), itself rich with ready-made statistics, I collected every question over the past 20 seasons - 4,775 shows from September of 2001 to July of 2022.  This amounted to 285,181 questions/clues.  Each question had a number of characterisics, to include a computed difficulty level, discussed further in this readme.
> - An Exploratory Data Analysis was performed on the clues to discover how to focus one's preparation, as well as other game strategems.
> - A quizzlet application was created using TKinter to develop a simple GUI.

#### Goals
> - Identify key strategems around board navigation, betting, and common question types and categories.
> - Build a functional quizzlet app to help prospective players train.

#### Project Outputs
> - Exploratory Jupyter Notebook in which some analysis already performed, and which is also ready for further analysis using Python and Pandas [jeopardy_analysis.ipynb](https://github.com/Miller-Ryan-1/jeopardizer)
> - A quizzlet application. [quizzlet.py](https://github.com/Miller-Ryan-1/jeopardizer).  
> - Acqusition functions, which can be used to duplicate the process and collect clues from future shows. [acquire.py](https://github.com/Miller-Ryan-1/jeopardizer).

#### Other Files and Directories in Repo
> - Acquisition Jupyter Notebook, to assist in understanding the acquire.py code and process.
> - Data structure containing all the clues/questions pulled from acquisition ['master_question_list.csv'](https://github.com/Miller-Ryan-1/jeopardizer).
> - A helper notebook, 'quizzlet.ipynb', giving insight into how the Tkinter app was built using the data collected from J! Arcive.
> - An awesome Alex Trebek picture for the quizzlet

#### Data Dictionary / Clue Characteristics

At this time, there was no modeling performed, so there is no target variable.  However the following characteristics about questions were captured:

|Characteristic|Datatype|Definition|
|:-------|:--------|:----------|
| show_num | int64 | The show the clue is from, a 4-digit number of assigned by Jeopardy |
| show_yr | int64 | The year the clue was asked - gives temporal contextual reference |
| show_mo | object | The month the show was asked - gives seasonal contextual reference |
| round | object | Whether the clue is from the Jeopardy, Double Jeopardy or Final Jeopardy |
| category | object | The clue category | 
| value | object | The clue's value ($200, $400, $600, $800, $1000, $1200, $1600, $2000) |
| clue | object | The clue/question itself |
| is_DD | int | Whether or not the clue was a daily double (1 if so, 0 if not) | 
| answer | object | The correct answer to the clue/question | 
| is_stumper | int | Whether or not all three players passed on a question or got it wrong (1 if so, 0 if not) |
| level | int | The difficulty of the question, as determined below (1 - easiest, to 6 - most difficult) |


##### Clue Difficulty Level

While a clue's value typically indicates its difficulty (generally the higher value, the more difficult the question) a binning of difficulties was performed, mostly to make the quizzlet more structured.  The questions were stratified into 6 difficulty levels according to the following algorithm:
- Level 1: $200 and $400 questions 
- Level 2: $600, $800 and $1200 questions
- Level 3: $1000, $1600 and $2000 questions
- Level 4: Daily Doubles
- Level 5: Triple Stumpers
- Level 6: Final Jeopardy


<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Duplication Instructions
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

#### Libraries/Modules Needed
- Jupyter Notebook
- pandas
- numpy
- re (Regular Expressions)
- requests
- time
- bs4 (Beautiful Soup)
- seaborn
- matplotlib.pyplot
- tkinter
- PIL (Pillow)

#### Directions
1. Clone the repo:
  ``git clone git@github.com:Miller-Ryan-1/jeopardizer.git``
2. Use the jeopardy_analysis.ipynb Jupyter Notebook to see and perform analysis.
3. To run quizzlet, go to terminal and when in the directory type 'python quizzlet.py'.


<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Quizzlet Instructions
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

Instruction are straightforward and always displayed in the app during gameplay:
1. Hit START button to begin.
2. Select a category from one the four displayed.
3. After clicking on the selected category, the question will be displayed for 12 seconds, or until ANSWER is clicked.  After 12 seconds the answer disappears, and the ANSWER button changes to SEE ANSWER.
4. The answer will be displayed, along with details including the year and month of the show the question is from.
5. If you get it correct, click the ANSWERED CORRECTLY button.  Your difficulty level (shown in the upper right) will increase by one (if less than 6).
6. If you get it wrong, or the timer ran out before you answered, click the INCORRECT/OUT-OF-TIME button.  The difficulty level will decrease by one (if greater than 1).
7. Difficulty ranges from 1 to 6 (6 are all final jeopardies). Difficulty 5 level questions are all triple stumpers (no player got the answer on the show).
8. Running stats are kept, showing right total proportion or correct answers, current right answer streak, and difficulty level of questions you are at.
9. Quit anytime by closing the window.

<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

### Next Steps
<hr style="border-top: 10px groove blueviolet; margin-top: 1px; margin-bottom: 1px"></hr>

1. Add a PASS button to quizzlet, allowing folks to skip a question.
2. Standalone app (low priority, plus had issues trying this aleady with py2app).
3. Web app to run in browsers (would need to transfer logic to Flask html framework).
4. NLP Modeling project around question difficulty, to determine which question characteristics lead to triple stumpers or place them in daily doubles.
5. Continue to improve UI and design of quizzlet.
