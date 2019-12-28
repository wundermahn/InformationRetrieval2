"""
 SECTION: Libraries
 These libraries are needed for program execution
 NLTK: Tokenization of the data
 String: String manipulation functions
 CSV: Export to CSV for testing
 Operator: For sorting through dicts
 Re: For regular expressions used to remove tags
 Collections: Used for dict creation and custom data structure creation
 Struct: Used for packaging data as a binary file
 zlib: Used for compressing data
 ast: Used for conversion of data
 io: For reading and writing binary data
 Sys: For passing arguments to the program
"""
import nltk, string, csv, operator, re, collections, sys, struct, zlib, ast, io
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict, Counter

"""
    SECTION: Functions
    These functions areused throughout the program and are housed in this section
    as a header of sorts. They make the actual logic and flow of the program much cleaner.
"""

# Turns the text file into a usable input
def get_input(filepath):
    # Open the filepath in a read fashion
    f = open(filepath, 'r')
    # Read the file
    content = f.read()
    # Return the file as a list
    return content

# This function calculates the size of the vocabulary
def vocabulary_size(mydict):
    # Return the length of the dictionary passed in
    return len(mydict)

# This function sorts a dictionary object
def sort_dictionary(mydict):
    # This code was actually inspired by an article below:
    # Inspired by: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-1.php
    # Order the dictionary in a list
    # It sorts the items in a (list of) tuple format in reverse (descending) order on the 1 index (frequency) item
    ordered_dict = sorted(mydict.items(), key=operator.itemgetter(1), reverse=True)
    # Turn it back into a dictionary
    dict(ordered_dict)

    # Return it
    return ordered_dict

# This function searches a dictionary for a term
def search_dictionary(mydict, term):
    # Inspired by: https://stackoverflow.com/questions/44664247/python-dictionary-how-to-get-all-keys-with-specific-values
    # Create a list of dictionary keys that match the search term
    words = [k for k, v in mydict.items() if v == term]
    return words

# This function removes numbers or non alpha characters from an array
def remove_nums(arr): 
    # Create a reg exp pattern
    pattern = '[0-9]'
    # Set the array equal to itself with digits (0-9) removed
    arr = [re.sub(pattern, '', i) for i in arr] 
    # Remove the array
    return arr

# This function cleans the passed in paragraph and parses it
def get_words(para):
    # Create a list of stop words from NLTK
    stop_words = list(stopwords.words('english'))
    # Create an NLTK tokenizer to tokenize the paragraph
    words = RegexpTokenizer(r'\w+')
    # Convert everything to lowercase and tokenize
    lower = [word.lower() for word in words.tokenize(para)]
    # Remove any remaining punctuation
    nopunctuation = [nopunc.translate(str.maketrans('', '', string.punctuation)) for nopunc in lower]
    # Remove any integers
    no_integers = remove_nums(nopunctuation)
    # Remove any stopwords
    dirty_tokens = [data for data in no_integers if data not in stop_words]
    # Remove any blanks that have been created as a result of the cleaning
    tokens = [data for data in dirty_tokens if data.strip()]

    # Return the tokens / words
    return tokens    

# This function converts a dict object to binary
# The struct page was utilized heavily: https://docs.python.org/2/library/struct.html
def pack_dict(mydict):
    # Turn the dict into a string
    s = str(mydict)
    # Turn the string dict into a list of bytes
    s = bytes(s, 'utf-8')
    # Compress that using zlib
    s = zlib.compress(s)
    # Take the length of that object, which is needed to pack it
    length = len(s)
    # Use struct.pack() to pack it into a binary file
    bs = struct.pack('%ds' %length, s)
        
    # Return the length, which is needed to unpack, and the binary file
    return length, bs 

# This function saves a file to binary
# NOTE - It should be noted that the disk location is hardcoded to emphasis that it IS being written to disk
# The movement to an argument would be trivial
def save_binary(length, binary):
# The following Stack Overflow post helped to understand how to read and write binary data.
#https://stackoverflow.com/questions/17349484/python-mangles-struct-pack-strings-written-to-disk    
    # Create an io object to write the binary file
    binary_out = io.open("C:\\Users\\Kelly\\Desktop\\Testing\\test.bin", "wb+")
    # Create an io object to write the length in binary
    length_out = io.open("C:\\Users\\Kelly\\Desktop\\Testing\\length.bin", "wb+")
    # Write the binary file
    binary_out.write(binary)

    # Pack the length integer into binary data
    length = struct.pack('i', length)
    # Write the binary length
    length_out.write(length)

    # No return type

# Driver Program
def driver(file):
    # Load the data from the text file
    myfile = get_input(file)

    # Create a regular expression to tokenize paragraphs
    p = r'<P ID=\d+>(.*?)</P>'
    # Create the tokenizer
    paras = RegexpTokenizer(p)
    # Create a counter for the document frequency
    document_frequency = collections.Counter()
    # Create a counter for the collection frequency
    collection_frequency = collections.Counter()
    # Create a master list to hold the individual lists created for tuple of (docID, word)
    all_lists = []
    # Instance of the current word count in the paragraph
    currWordCount = 0
    # The current list for the tuple of (docID, word)
    currList = []
    # The number of paragraphs we will be reading
    num_paragraphs = len(paras.tokenize(myfile))

    # Start the paragraph ID at 0
    para_id = 0
    # Tokenize the file, and look at each paragraph
    # which is delimited by its HTML tags
    for para in paras.tokenize(myfile):
        # Update the paragraph ID
        para_id += 1
        # Create your tokens, via the get_words function
        tokens = get_words(para)
        # Update the collection frequency
        # which is just a total count of the words
        collection_frequency.update(tokens)
        # Update the document frequency of the words
        document_frequency.update(set(tokens))
        # Make sure the paragraphs have punctuation removed
        para = para.translate(str.maketrans('', '', string.punctuation))
        # Split them on spaces and convert everything to lowercase
        currPara = para.lower().split()
        # This mimics the logic in the get_words function
        for token in tokens:
            # Update the current word count for the current paragraph
            currWordCount = currPara.count(token)
            # Create the tuple
            currList = [token, tuple([para_id, currWordCount])]
            # Append it to the all_lists object
            all_lists.append(currList)

    # Create a blank dictionary (hash map)
    # This will be the postings list
    d = {}
    # Loop through the list of lists
    for key, new_value in all_lists:
        # Create a list of keys
        values = d.setdefault(key, [])
        # Append distinct values for the respective keys
        values.append(new_value)

    # Create the inverted index by combining the dictionary and postings list
    inverted_index = {word:(document_frequency[word], d[word]) for word in d}

    # Print out requested data
    print("Number of Paragraphs Processed: {}".format(num_paragraphs))
    print("Number of Unique Words (Vocabulary Size): {}".format(vocabulary_size(document_frequency)))
    print("Number of Total Words (Collection Size): {}".format(sum(collection_frequency.values())))

    # Create a binary file, and a binary representation of the bits as well
    length, binary = pack_dict(inverted_index)

    # Save that binary file to disk
    # In the function, it has been determined that:
    # C:\\Users\\Kelly\\Desktop\\Testing is the location. This could easily be changed
    # to be a function argument, but was intentionally left this way to verify it IS 
    # being written to disk.
    save_binary(length, binary)

# Main Program
def main():

    # Use argument as the filename or filepath
    driver(sys.argv[1])

# Call main
main()