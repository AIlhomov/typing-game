"""Module to calculate the precision and results in a typing
game."""

import os
import time

import extrafunctions #My own module for extra assignments (4-6)

user_lines = None #Global variable
time_end_sec = None # Global variable

def read_lines(txt_file):
    """Opens the text file using "open" built-in function (DRY CODE)
    Also uses try, except."""
    try:
        with open(txt_file, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f'Error file: {txt_file} not found.')
        return None

def read_words_and_len(txt_file):
    """Returns the words in a list and returns the length of the txt file"""
    lines = read_lines(txt_file)
    list_words = []
    for line in lines:
        for word in line.split():
            word = word.rstrip('\n')
            list_words.append(word)
    length_word = len(list_words)
    return list_words, length_word

def lines_user_game(txt_file):
    """Runs the game. Reads the user lines and returns them. Also runs the timer"""
    global user_lines #MAKES IT ACCESSIABLE IN SHOW_RESULT LATER (looks nicer)
    global time_end_sec # Makes time accessiable 
    time_end_sec = 0
    lines = read_lines(txt_file) #read the lines from the txt
    user_lines = []
    
    
    start_time = time.time() #Start the timer
    print('Starting the typing game.\n\n')
    os.system('clear') #nice

    for line in lines:
        print(line.strip())
        user_input = input()
        user_lines.append(user_input)
        os.system('clear')
    time_end_sec = max(time.time() - start_time, 1) #time
    


    return user_lines

def save_score(username, word_precision, difficulty):
    """Saves the score in the score.txt file"""
    try:
        with open('score.txt', 'a') as file:
            file.write(f'{username}\t{word_precision}\t{difficulty}\n')
    except FileNotFoundError as filenot:
        print(f'Error: {filenot}')

def precision_word(txt_file, user_input):
    """Calculates if a word matches the original text
    loops through the index and line. It compares the word by index.
    Also gets the extra words if there exists to punish the user."""
    lines = read_lines(txt_file)
    #Counter for the correct words
    correct_word_count = 0
    wrong_word_count = 0
    extra_words = 0 #Punish the user if user_words exceeds original word by line
    #Enumerate gets the index and the lines by looping through it
    for index, line in enumerate(lines):
        list_original_text = line.split()
        #Gets the 'line word' for the index position.
        list_user_input = user_input[index].split()
        if len(list_user_input) > len(list_original_text) and list_user_input is not None: #Extra words in a line
            extra_words = len(list_user_input) - len(list_original_text)
        #Iterates through both lists
        for original_word, user_word in zip(list_original_text, list_user_input):
            original_word = original_word.rstrip('\n')
            if original_word == user_word:
                correct_word_count += 1
            else:
                wrong_word_count += 1
        #Calculate wrong words (Extra assignment for wpm) (Calculates the extra words that are wrong)
        for i in range(len(list_original_text)):
            try:
                _ = list_user_input[i]
            except IndexError:
                wrong_word_count += 1

    _, length_of_txt_file = read_words_and_len(txt_file)
    
    #Returns the word precision in percent
    return f'{(correct_word_count-extra_words) / length_of_txt_file * 100:.2f}%', wrong_word_count

def len_char(text_file):
    """Returns the char count in the given text file, (without spaces)"""
    #if its a regular text_file, original_input
    lines = read_lines(text_file)
    letters = []
    for line in lines:
        line = line.replace('\n', '')
        line = line.replace(' ', '') #without spaces
        letters += [char for char in line] #Loop through the line to count char in line
    return len(letters)
    


def precision_char(txt_file, user_input):
    """Works almost like word but not, it calculates the
    chars instead. It loops through the user and original.
    It also checks if there is an char thats outside an index."""
    lines = read_lines(txt_file) 
    char_right_count = 0
    wrong_char_list = []
    extra_chars_count = 0

    original_word = '_'
    index_in_word = 0 

    for index, word in enumerate(lines):
        #Removes newline at the end.
        lines[index] = word.rstrip('\n')

    for index, (line, user_input_line) in enumerate(zip(lines, user_input)):
        list_original_text = line.split(' ')
        list_user_input = user_input_line.split(' ')

        for original_word, user_word in zip(list_original_text, list_user_input):
            original_word = original_word.rstrip('\n')

            if len(user_word) > len(original_word):  # extra chars
                extra_chars_count += len(user_word) - len(original_word)
                
            if original_word and user_word:
                for index_in_word, (original, user) in enumerate(zip(original_word, user_word)):
                    if original == user:
                        char_right_count += 1
                    else:
                        wrong_char_list.append(original)
                # Handle remaining characters in original_word
                for remaining_original in original_word[index_in_word + 1:]:
                    wrong_char_list.append(remaining_original)
            else:  # User_input is None
                wrong_char_list.extend(original_word)
        # Check for extra user input words
        for index, original_wordd in enumerate(list_original_text):
            try:
                _ = list_user_input[index] # Force to an indexerror.
            except IndexError: # Everything thats missing after the user_input has been made.
                if len(list_user_input) - len(original_word) > 0:
                    extra_chars_count += len(list_user_input) - len(original_word)
                wrong_char_list.append(original_wordd)
    #Just some calculations..
    length_of_txt_file = len_char(txt_file) #Amount of chars in the original txt file
    result_procent = round((char_right_count - extra_chars_count) / length_of_txt_file * 100, 2) # %
    result_missed_chars = count_characters(wrong_char_list) #Wrong chars
    return result_procent, result_missed_chars #return a tuple
    
    
def count_characters(input_list):
    """takes a list of strings as an argument 
    and returns the character and the count values in its dictionary form."""
    char_count_dict = {}

    for element in input_list:
        #iterate through its characters
        for char in element:
            char_count_dict[char] = char_count_dict.get(char, 0) + 1
       
    
    sorted_char_count = dict(sorted(char_count_dict.items(), key=lambda item: item[1], reverse=True))
    
    #Formatted string:
    formatted_output = "Wrong spelled chars:\n"
    for char, count in sorted_char_count.items():
        formatted_output += f"  {char}: {count}\n"

    return formatted_output

def show_results(txt_file, user_txt):
    """Function to show the result, calls the function to show the result
    and also makes it look nicer."""
    word_result, wrong_word_count = precision_word(txt_file, user_txt)
    char_result, missed_chars_result = precision_char(txt_file, user_txt)
    print('\nGrundkrav:\n\n')
    print(f'Word precision: {word_result}\nCharacter precison: {char_result}%')
    print(missed_chars_result) #Missed chars in dict format
    
    #Extra assignments:
    print('Extra uppgifter:\n\n')
    non_empty_strings = [s for s in user_txt if s != ''] #Dont include '' as 1 word
    gross_wpm, net_wpm, minutes = extrafunctions.gross_net_wpm(len(non_empty_strings), wrong_word_count, time_end_sec)
    animal = extrafunctions.animal_category(net_wpm)
    print(f'It took {minutes} minutes and {time_end_sec} seconds\nGross WPM: {gross_wpm}\nNet WPM: {net_wpm}')
    print(f'You write as fast as a {animal} (translation required here..)')
