"""Main function.
This is a game, called typing game. It has 3 different text files.
And also you can train with 1 char each."""

import functions
import extrafunctions

menu_text = """
This is a typing test.
Test your limits.
Choose difficulty down below.
1. Easy
2. Medium
3. Hard
4. Leaderboard
5. Train
q. Quit"""

def main():
    """Main function where the typing game happens"""
    stop = False
    
    while not stop:
        user_text = ''

        print(chr(27) + "[2J" + chr(27) + "[;H")
        print(menu_text)
        choice = input()

        if choice == '1':
            filename = 'easy.txt'
            user_text = functions.lines_user_game(filename)
        elif choice == '2':
            filename = 'medium.txt'
            user_text = functions.lines_user_game(filename)
        elif choice == '3':
            filename = 'hard.txt'
            user_text = functions.lines_user_game(filename)
        elif choice == '4':
            print('Leaderboard:\n')   
            extrafunctions.sort_scores()
        elif choice == '5':
            time_train = int(input('How long do you want the training to last for (seconds)? '))
            extrafunctions.run_typing_test(time_train)

        elif choice == 'q':
            print('Goodbye.')
            break
        else:
            print('That is not a valid choice. You can only choose from the menu')

        if user_text: #RESULT:
            functions.show_results(filename, user_text)
            name = input('Who is playing? ')
            percent, _ = functions.precision_word(filename, user_text)
            functions.save_score(name, percent, filename)
    
        if not stop:
            input('\nPress enter to continue...')
    
if __name__ == "__main__":
    main()
