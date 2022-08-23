import pandas as pd
import numpy as np
import re
import requests
import time
import sys
from bs4 import BeautifulSoup as bs

'''
For Jeopardizer v1.0 (7.2022):
These functions aquire data from all jeopardy games from a given game date on.
Data pulled includes:
- Show ID
- Year of Show
- Month of Show
- Round (Jeopardy, Double Jeopardy, Final Jeopardy)
- Category
- Clue Value
- Clue
- Answer
- Whether of not the Clue is a daily double
- Whether or not the Clue is a "triple stumper" (no one answeres correctly)
- The difficulty level (based on round, value, dd and triple stumper status)

The final function is the full acquisition function.

NEXT UPGRADES - 
1. Existing CSV checker/auto updater
2. Add Comments into category
3. Autotitle output files
4. Get show #6087 (IBM Watson challenge game 1, DJ and Final Round)
'''

def is_dd(url):
    '''
    This function examines a single show and determines which questions are a daily double
    '''
    # Creates a Beautiful Soup object from the show's page
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    
    # Indexer is used to match resulting dataframe with clues
    indexer = 1

    # Initialize a list for dataframe
    dd_list = []

    # Loop through the clue tags checking for daily doubles
    for thing in soup.find_all('td', class_ = 'clue'):
        # Initialize the object holding the row data
        row = {}
        row['q_index'] = indexer
        indexer += 1
        # Clues with daily doubles have a 'clue_value_daily_double' tag
        if thing.find('td', class_ = 'clue_value_daily_double'):
            row['is_DD'] = 1
        else:
            row['is_DD'] = 0
        dd_list.append(row)
    df_dd = pd.DataFrame(dd_list)
    
    # Returns a dataframe
    return df_dd


def answers(url):
    '''
    This function pulls all the answers to clues for a show as well as determines if they are a triple stumper
    '''
    # Creates a Beautiful Soup object from the show's page
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')

    # Indexer is used to match resulting dataframe with clues
    indexer = 1

    # Initialize a list for dataframe
    answers = []

    # Loop through the clue tags checking for daily doubles
    for clue in soup.find_all('td', class_ = 'clue'):
        # Initialize the object holding the row data
        answer = {}
        # Limit to index 61 (question 60) or an error ocurs
        if indexer < 61:
            answer['q_index'] = indexer
            # Answers have to be parsed from mouseover field.  For last record an error occurs, hence the try/except
            try:
                ans = clue.find('div', onmouseover = True).get('onmouseover')
            except:
                indexer +=1
                continue
            cls = bs(ans, 'html.parser')
            answer['answer'] = cls.find('em').text
            if 'Triple Stumper' in ans:
                answer['is_stumper'] = 1
            else:
                answer['is_stumper'] = 0
            answers.append(answer)
            indexer += 1
    df_ans = pd.DataFrame(answers)

    # Returns a dataframe
    return df_ans


def j_qs(url):
    '''
    Creates a dataframe of Jeopardy Clues and their associated data
    '''
    # Creates a Beautiful Soup object from the show's page
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')

    # Pulls in show and year information
    show_info = soup.find('div', attrs = {'id':'game_title'}).text
    show_num = re.findall(r'\d+', show_info)[0]
    show_yr = re.findall(r'\d+', show_info)[2]  
    show_mo = re.findall(r'[a-zA-Z]{2,}', show_info)[2]

    # Jeopardy clue value list
    j_value = ['200','400','600','800','1000'] 

    # Pull in the round categories
    j_category_list = soup.find('div', attrs = {'id':'jeopardy_round'}).find_all('td', attrs = {'class':'category_name'})
    j_categories = []
    for category in j_category_list:
        j_categories.append(category.get_text())

    # Initialize a list for dataframe
    questions = []

    # Clues are tagged by category (column) and value (row).  Look through them and add data
    for i in range(6):
        for j in range(5):
            question = {}
            # Question index mapped to row and column
            question['q_index'] = (i + 1) + (6* j)
            
            question['show_num'] = show_num
            question['show_yr'] = show_yr
            question['show_mo'] = show_mo
            question['round'] = 'Jeopardy'
            question['category'] = j_categories[i]
            question['value'] = j_value[j]
            
            #Try except due to error on last clue
            clue = f'clue_J_{i+1}_{j+1}'
            try:
                question['clue'] = soup.find('td', attrs = {'id':clue}).text
            except:
                continue
            
            questions.append(question)
    df_j_qs = pd.DataFrame(questions)

    # Returns a dataframe
    return df_j_qs


def dj_qs(url):
    '''
    Creates a dataframe of Double Jeopardy Clues and their associated data
    '''
    # Creates a Beautiful Soup object from the show's page
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')

    # Pulls in show and year information
    show_info = soup.find('div', attrs = {'id':'game_title'}).text
    show_num = re.findall(r'\d+', show_info)[0]
    show_yr = re.findall(r'\d+', show_info)[2]
    show_mo = re.findall(r'[a-zA-Z]{2,}', show_info)[2]

    # Double Jeopardy clue value list
    dj_value = ['400','800','1200','1600','2000']

    # Pulls in the round categories
    dj_category_list = soup.find('div', attrs = {'id':'double_jeopardy_round'}).find_all('td', attrs = {'class':'category_name'})
    dj_categories = []
    for category in dj_category_list:
        dj_categories.append(category.get_text())
    
    # Initialize a list for dataframe
    questions = []

    # Clues are tagged by category (column) and value (row).  Look through them and add data
    for i in range(6):
        for j in range(5):
            question = {}
            
            # Question index mapped to row and column
            question['q_index'] = 30 + (i + 1) + (6* j)

            question['show_num'] = show_num
            question['show_yr'] = show_yr
            question['show_mo'] = show_mo
            question['round'] = 'Double Jeopardy'
            question['category'] = dj_categories[i]
            question['value'] = dj_value[j]
            
            #Try except due to error on last clue
            clue = f'clue_DJ_{i+1}_{j+1}' 
            try:
                question['clue'] = soup.find('td', attrs = {'id':clue}).text
            except:
                continue 
            
            questions.append(question)
    df_dj_qs = pd.DataFrame(questions)

    # Returns a dataframe
    return df_dj_qs


def fj(url):
    '''
    Pulls the final jeopardy question
    '''
    # Creates a Beautiful Soup object from the show's page
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')

    # Pulls in show and year information
    show_info = soup.find('div', attrs = {'id':'game_title'}).text
    show_num = re.findall(r'\d+', show_info)[0]
    show_yr = re.findall(r'\d+', show_info)[2]
    show_mo = re.findall(r'[a-zA-Z]{2,}', show_info)[2]

    # Creates soup of final round html
    fj = soup.find('table', class_ = 'final_round')

    # Pull in final jeopardy clue data
    f_j = {}
    f_j['show_num'] = show_num
    f_j['show_yr'] = show_yr
    f_j['show_mo'] = show_mo
    f_j['round'] = 'Final Jeopardy'
    f_j['value'] = 'FJ'
    f_j['is_DD'] = 0
    f_j['category'] = fj.find('td', class_ = 'category_name').text
    f_j['clue'] = fj.find('td', attrs = {'id':'clue_FJ'}).text

    # Answer and triple stumper status pulled in as previous
    ans = fj.find('div', onmouseover = True).get('onmouseover')
    cls = bs(ans, 'html.parser')
    f_j['answer'] = cls.find('em').text
    if 'Triple Stumper' in ans:
        f_j['is_stumper'] = 1
    else:
        f_j['is_stumper'] = 0

    df_fj = pd.DataFrame([f_j])

    # Returns a dataframe
    return df_fj


def show_dataframe(df_dd, df_ans, df_j_qs, df_dj_qs, df_fj):
    '''
    Combines all of the dataframes from the show on the question index
    '''
    df_js = pd.concat([df_j_qs, df_dj_qs]).reset_index()
    df_game = df_js.merge(df_dd, on='q_index').merge(df_ans, on = 'q_index').drop(columns=['index','q_index'])
    df_game = pd.concat([df_game,df_fj]).reset_index().drop(columns=['index'])
    
    # Returns a dataframe
    return df_game


def add_level(df_game):
    '''
    Assigns a clue difficulty level (1-6) based on the following:
    1 ('Easiest') - Jeopardy Round $200 & $400 questions | Double Jeopardy Round $400 questions
    2 - Jeopardy Round $600 & $800 questions | Double Jeopardy Round $800 & $1200 questions
    3 - Jeopardy Round $1000 questions| Double Jeopardy Round $1600 & $1800 questions
    4 - Daily Double questions
    5 - Triple Stumper questions
    6 ('Hardest') - Final Jeopardy questions
    '''
    df_game['level'] =  np.where(df_game['is_DD'] == 1, 4, \
                        np.where(df_game['is_stumper'] == 1, 5, \
                        np.where(df_game['round'] == 'Final Jeopardy', 6, \
                        np.where((df_game['value'] == '200') | (df_game['value'] == '400'), 1, \
                        np.where((df_game['value'] == '600') | (df_game['value'] == '800') | (df_game['value'] == '1200'), 2, \
                        np.where((df_game['value'] == '1000') | (df_game['value'] == '1600') | (df_game['value'] == '2000'), 3, '')))))) 
    
    # Returns a dataframe
    return df_game       


def acquire_show(url):
    '''
    Utilizes all funtions above to create a consolidated show gameframe
    '''
    df_j_qs = j_qs(url)
    df_dj_qs = dj_qs(url)
    df_dd = is_dd(url)
    df_ans = answers(url)
    df_fj = fj(url)
    df_game = show_dataframe(df_dd, df_ans, df_j_qs, df_dj_qs, df_fj)
    df_game = add_level(df_game)

    #!# When used to pull singles games:
    df_game.to_csv('jeopardy_games.csv')
    # Returns a dataframe
    return df_game


def acquire_shows(start_page):
    '''
    Acquires all shows from the start page on
    Note: start page is the end of a show url of the form: 'showgame.php?game_id=7409'
    '''
    # Create filename realted to a slice/regex of start page
    # Check to see if csv exist
    output = pd.DataFrame()
    base_url = 'https://j-archive.com/'
    url = base_url + start_page

    # Creates a Beautiful Soup object from the show's first page
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')

    # Checks to ensure the first game is not the most recent show, which does not have a 'next_game' tag (4 vs. 5)
    first_game = soup.find('table', attrs = {'id':'contestants_table'})
    checker = len(first_game.select('a'))

    # Creates a show scrape counter
    counter = 1

    # The checker loops through all shows until the most recent show, which only has 4 tags (vs 5 for not most recent shows)
    while checker == 5:
        # Creates status indicator
        show_id = re.findall(r'game_id=\d+',url)[0]
        print(f'Scraping page {counter}: {show_id}')
        # Pulls in show and appends it to the current clue dataframe
        try:
            df_game = acquire_show(url)
        except:
            print(f'Failed timeout on show_id {show_id}, file saved from previous show.')
            break

        output = pd.concat([output,df_game])
        print(f'Clue Bank Size = {output.shape[0]}')
        
        # Creates a Beautiful Soup object from the newest page
        # IN future, create nested try/excepts to create a break for the requests
        try:
            r = requests.get(url)
            soup = bs(r.content, 'html.parser')
        except:
            print(f'Scrape halted after show_id {show_id}, file saved.')
            break
        
        # Finds the next page for the next loop, try/except due to error at the end
        next_list = soup.find('table', attrs = {'id':'contestants_table'})
        try:
            next_url = next_list.find_all('a')[4]["href"]
        except:
            break
        url = base_url + next_url
        checker = len(next_list.select('a'))
        counter += 1
        time.sleep(.5)

    output.to_csv('jeopardy_games.csv')
    # Great job, function!
    print('Done Scraping!')
    
    # Returns a dataframe
    return output  

'''
You can run the acquire_shows function from the command line like a pro!
While in the directory in the terminal, type >> python acquire.py acquire_shows {short url}
{short url} = the specific game url component such as 'showgame.php?game_id=7409'
'''
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])

def merge_dataframes(dataframe_list):
    path = 'cached_games/'
    new_list = [f'{path}{n}.csv' for n in dataframe_list]

    master_list = pd.DataFrame()
    counter = 0

    for df_name in new_list:
        df = pd.read_csv(df_name, converters={'answer' : str})
        df = df.drop(columns = 'Unnamed: 0')
        master_list = pd.concat([master_list,df])
        counter += 1
    
    master_list = master_list.reset_index()
    print(f'Successfully combined {counter} files into master list.')

    master_list.to_csv('master_question_list.csv')

    return master_list