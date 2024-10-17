# keyword-buster.py
import argparse
import re

from tabulate import tabulate


def read_dictionary_words(filepath):
    """Read words from the specified file and return them as a list in uppercase."""
    with open(filepath, 'r') as file:
        words = [word.strip().upper() for word in file]
    return words


def find_matching_words(word_list, pattern):
    """Find and return words that match the given pattern."""
    regex_pattern = "^" + pattern.replace('?', '.') + "$"
    regex = re.compile(regex_pattern)
    return [word for word in word_list if regex.match(word)]


def main():
    parser = argparse.ArgumentParser(
        description="Align '?' characters in the provided words and print the longest word with additional details.")

    # Adding argument definitions
    parser.add_argument('words', metavar='WORD', type=str, nargs='+',
                        help='Words to be added to the list and evaluated')

    # Parsing the arguments
    args = parser.parse_args()

    # Reading words from the dictionary file
    dictionary_file = '/srv/dict/words_alpha.txt'
    word_list = read_dictionary_words(dictionary_file)

    # Adding words to a list and converting to uppercase
    words_list = [word.upper() for word in args.words]

    # Find the maximum index of '?'
    max_q_index = max(word.index('?') for word in words_list)

    # Prepend spaces to align all '?' characters on the same row
    aligned_words_list = []
    for word in words_list:
        current_q_index = word.index('?')
        prepend_spaces = max_q_index - current_q_index
        aligned_word = ' ' * prepend_spaces + word
        aligned_words_list.append(aligned_word)

    # Counting the number of words
    words_count = len(aligned_words_list)

    # Finding the longest word
    longest_word = max(aligned_words_list, key=len)

    # Creating an array with longest_word rows and words_count columns
    rows_count = len(longest_word)
    array = [['' for _ in range(words_count)] for _ in range(rows_count)]

    # Populating the array with characters from each word
    for col in range(words_count):
        for row in range(len(aligned_words_list[col])):
            array[row][col] = aligned_words_list[col][row]

    # # Printing the longest word and its length
    # print(f"The longest word is: {longest_word.strip()}")
    # print(f"Length of the longest word: {len(longest_word.strip())}")
    #
    # # Printing the total number of words
    # print(f"Total number of words: {words_count}")
    #
    # # Printing all the aligned words
    # print("\nAll provided words (aligned):")
    # for word in aligned_words_list:
    #     print(word)
    #
    # # Printing the array using tabulate
    # print("\nArray Representation:")
    table_fmt = 'grid'
    table_fmt = 'plain'
    print(tabulate(array, tablefmt=table_fmt))

    # Processing each command line argument
    for pattern in words_list:
        matching_words = find_matching_words(word_list, pattern)

        # Printing the results
        # print(f"\nPattern: {pattern}")
        print(f'{pattern}')
        # print("Matching words:")
        for word in matching_words:
            print(f'  {word}')


if __name__ == "__main__":
    main()
