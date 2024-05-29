import re


def extract_yt_term(command):
    '''Using re extracts search terms from user's command & return it 
    if not found returns None'''
    
    # Define an regular expression pattern to capture the song name 
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command parameter
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None 
    return match.group(1) if match else None


def remove_words(input_string, words_to_remove):
    '''Function to remove unwanted words from query'''

    # Split the input string into single-single words - list
    words = input_string.lower().split()

    # Remove unwanted words
    filtered_words = [word for word in words if word not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string
