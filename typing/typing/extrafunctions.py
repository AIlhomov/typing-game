"""Extra functions for extra assignments in kmom10"""
import time
import random

def gross_net_wpm(words, misspelled_words, total_time_sec):
    """Gives the gross WPM and net WPM (DRY code)
    It also rounds up to nearest approximate digit."""
    total_min = total_time_sec / 60 #Minutes

    if total_min % 60 > 30: #Round up the total time if it's over 30 seconds
        int_con = int(total_min)
        decimal = total_min - int_con
        if decimal >= 0.5:
            int_con += 1
    
    gross_wpm = words / total_min #Number of written words / minutes
    net_wpm = gross_wpm - (misspelled_words / total_min)

    minutes = max(int(total_min), 0) #Also return minutes but only if its 1 or over.

    return gross_wpm, net_wpm, minutes

def animal_category(wpm):
    """Outputs which animal category you are depending on the net WPM you got"""
    wpm = max(wpm, 0) #If its something like -10 it should be 0 so the user can recieve a category
    wpm_ranges = { #Easier to update if needed (Makes a dict)
        (0, 10): 'Sengångare',
        (10, 20): 'Snigel',
        (20, 30): 'Sjöko',
        (30, 40): 'Människa',
        (40, 50): 'Gasell',
        (50, 60): 'Struts',
        (60, 70): 'Gepard',
        (70, 80): 'Svärdfisk',
        (80, 90): 'Sporrgås',
        (90, 100): 'Taggstjärtseglare',
        (100, 120): 'Kungsörn',
        (120, float('inf')): 'Pilgrimsfalk',
    }

    for (min_wpm, max_wpm), category in wpm_ranges.items():
        if min_wpm <= wpm < max_wpm:
            return category

    return None #Handle if its not in range
    
def sort_scores():
    """Sortes the score by the hard.txt first and so on.
    It also sortes by highest precentage."""
    # Initialize a dictionary to group scores by filename
    score_groups = {'hard.txt': [], 'medium.txt': [], 'easy.txt': []}

    with open('score.txt', 'r') as file:
        scores = [line.strip() for line in file.readlines()]

    for line in scores:
        parts = line.split('\t')
        filename = parts[2]
        precision = float(parts[1].strip('%'))

        if filename in score_groups: # If it equals to the file names in score_groups
            score_groups[filename].append((line, precision))

    #Sort the scores within each group by precision
    for filename, group in score_groups.items():
        sorted_group = sorted(group, key=lambda x: x[1], reverse=True) #Sorting groups by precision
        #Update the group with sorted lines, excluding the precision part
        score_groups[filename] = [line for line, _ in sorted_group]

    #Write the sorted scores back to the file
    with open('score.txt', 'w') as output_file:
        for filename in ['hard.txt', 'medium.txt', 'easy.txt']:
            for line in score_groups[filename]:
                output_file.write(line + '\n')
    
    with open('score.txt', 'r') as sorted_file:
        sorted_content = sorted_file.read()
        
    print(sorted_content) #Print contents of score.txt

def run_typing_test(test_duration):
    """This function runs a practice game where the user puts in a random char
    and the output would be the practice result."""
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,-<>/!#%&()=?+*_"

    user_input = ""
    errors = {}  #Dictionary to store incorrect characters and their counts

    start_time = time.time() #Start the timer
    end_time = start_time + test_duration


    while time.time() < end_time:
        #Randomly select a character from the characters string
        char_to_type = random.choice(characters)
        print(char_to_type)
        user_char = input()

        #Wrong letters:
        if user_char != char_to_type:
            if user_char in errors:
                errors[user_char] += 1
            else:
                errors[user_char] = 1
        #Append user input (it does not matter if its correct or not)
        user_input += user_char


    #Just some calculations:
    total_characters = len(user_input)
    correct_characters = total_characters - len(errors)
    correct_percentage = (correct_characters / total_characters) * 100

    #Result:
    print("Well done. Practice results:")
    print(errors) #Dictionary for amount of times chars was wrong
    print(f"Correct Percentage: {correct_percentage:.2f}%")
