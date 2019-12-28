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
 Time: Used to time how long it takes the code to reference the dictionary
"""
import nltk, string, csv, operator, re, collections, sys, struct, zlib, ast, io, time
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict, Counter

"""
    SECTION: Functions
    These functions areused throughout the program and are housed in this section
    as a header of sorts. They make the actual logic and flow of the program much cleaner.
"""

# This function searches a dictionary for a term
def search_dictionary(mydict, term):
    # Inspired by: https://stackoverflow.com/questions/44664247/python-dictionary-how-to-get-all-keys-with-specific-values
    # Create a list of dictionary values that match the search term
    words = [v for k, v in mydict.items() if k == term]
    # Return that list
    return words

# This function searches a dictionary for a term
# but returns only its document frequency
def search_dictionary_frequency(mydict, term):
    # Inspired by: https://stackoverflow.com/questions/44664247/python-dictionary-how-to-get-all-keys-with-specific-values
    # Create a list of frequencies that match the search term
    words = [v[0] for k, v in mydict.items() if k == term]
    # Return that list
    return words

# This function searches a dictionary for a term
# but returns only its postings list
def search_dictionary_postings(mydict, term):
    # Inspired by: https://stackoverflow.com/questions/44664247/python-dictionary-how-to-get-all-keys-with-specific-values
    # Create a list of postings that match the search term
    words = [v[1] for k, v in mydict.items() if k == term]
    # Return that list
    return words  

# This function unpacks a binary object into a dictionary
# The struct page was utilized heavily: https://docs.python.org/2/library/struct.html
def unpack_dict(length, binary):
    # Unpack the binary file passed in using its length
    s2 = struct.unpack('%ds' %length,binary)[0]
    # Decompress it using zlib
    s2 = zlib.decompress(s2)
    # Convert from bytes to string
    s2 = s2.decode("utf-8")
    # Convert from string to dictionary
    dic2 = ast.literal_eval(s2)

    # Return the dictionary
    return dic2 

# This function saves a file to binary
# NOTE - It should be noted that the disk location is hardcoded to emphasis that it IS being read from disk
# The movement to an argument would be trivial
def load_binary():
# The following Stack Overflow post helped to understand how to read and write binary data.
#https://stackoverflow.com/questions/17349484/python-mangles-struct-pack-strings-written-to-disk    
    # Create an io object to read the binary file
    binary_file = io.open("C:\\Users\\Kelly\\Desktop\\Testing\\test.bin", "rb")
    # Create an io object to write the length in binary
    length_file = io.open("C:\\Users\\Kelly\\Desktop\\Testing\\length.bin", "rb")
    
    # Read in the binary file
    binary = binary_file.read()
    # Read in the length
    length = length_file.read()
    # Unpack the length binary data back into an int
    length = struct.unpack('i', length)

    # Return the length and the binary
    return length, binary

# This function compares two postings lists (passed in as indices)
# for similarities
def compare_postings(posting1, posting2):
    # Create a list for all of the documents in the first index
    posting1_docs = []
    # Create a list for all of the documents in the second index
    posting2_docs = []
    # Create a list that will house what is in both docs
    in_both_docs = []

    # Loop through the first index
    for item in posting1:
        # Extract all of the docIDs
        posting1_docs = [num[0] for num in item]
       
    # Loop through the second index
    for item in posting2:
        # Extract all of the docIDs
        posting2_docs = [num[0] for num in item]
    
    # Determine which IDs are in both
    in_both_docs = [docid for docid in posting1_docs if docid in posting2_docs]

    # Return it
    return in_both_docs
# Main Program
def main():

    time_start = time.time()
    # Load the file(s) from disk
    length, binary = load_binary()
    # Create the index by unpacking the data
    index = unpack_dict(length, binary)

    # Initialize a timer to time how long it takes to load the file
    time_finish = time.time()
    elapsed = time_finish - time_start
    print("Time to finish loading: {}".format(elapsed))

    """
        SECTION: TESTING
        This section performs the three test cases as supplied by the program requirements
        1.  Print out the document frequency and postings list for terms: “Harare", "plutonium", “Bolsonaro”, “feisty". 
        
        2. Give document frequency, but do not print postings for the words: "Hopkins", “Harvard”, “Stanford”, "Brown", and
        “college” (these postings lists are longer).

        3. Print out the docids for documents that have both "Elon" and "Musk" in the text. You can do this by finding the
        postings lists for each term, and then intersecting the two lists. For this test you do not need to use or supply frequency
        information. Please print the docids in increasing order.

    """

    # Initialize a timer to time how long it takes to perform this retrieval
    time_start_1 = time.time()
    # Alert user to activity
    print(" PRINTING OUT DOCUMENT FREQUENCY AND POSTINGS LISTS FOR TERMS: ")
    print(" Harare, plutonium, Bolsonaro")
    print(" In the form: word: document_frequency, (document_id, frequency_in_doc)")
    print()
    # Perform lookups
    harare = search_dictionary(index, 'harare')
    plutonium = search_dictionary(index, 'plutonium')
    bolsonaro = search_dictionary(index, 'bolsonaro')
    # Print results
    print("HARARE: ", harare)
    print("PLUTONIUM: ", plutonium)
    print("BOLSONARO: ", bolsonaro)
    # End timer and determine runtime
    time_finish_1 = time.time()
    elapsed_1 = time_finish_1 - time_start_1
    # Alert to runtime
    print("Time to finish Test 1: {}".format(elapsed_1))

    print(" ------------------------------------------------------------------------ ")
    
    # Initialize a timer to time how long it takes to perform this retrieval
    time_start_2 = time.time()
    # Alert user to activity
    print(" PRINTING OUT DOCUMENT FREQUENCY FOR TERMS: ")
    print(" Hopkins, Harvard, Stanford, Brown, and college ")
    print(" In the form: word: document_frequency")
    print()
    # Perform lookups    
    hopkins = search_dictionary_frequency(index, 'hopkins')
    harvard= search_dictionary_frequency(index, 'harvard')
    stanford = search_dictionary_frequency(index, 'stanford')
    brown = search_dictionary_frequency(index, 'brown')
    college = search_dictionary_frequency(index, 'college')
    # Print results
    print("HOPKINS: ", hopkins)
    print("HARVARD: ", harvard)
    print("STANFORD: ", stanford)
    print("BROWN: ", brown)
    print("COLLEGE: ", college)
    # End timer and determine runtime
    time_finish_2 = time.time()
    elapsed_2 = time_finish_2 - time_start_2
    # Alert to runtime
    print("Time to finish Test 2: {}".format(elapsed_2))

    print(" ------------------------------------------------------------------------ ")

    # Initialize a timer to time how long it takes to perform this retrieval
    time_start_3 = time.time()
    # Alert user to activity
    print(" PRINTING OUT DOCUMENT IDs FOR: ")
    print(" Docs with both ELON and MUSK ")
    print(" In the form: [ID]")
    print()
    # Perform lookups
    elon = search_dictionary_postings(index, 'elon')
    musk = search_dictionary_postings(index, 'musk')
    in_both = compare_postings(elon, musk)
    # Print results
    print("Doc IDs which both ELON and MUSK are in: {}".format(in_both))
    # End timer and determine runtime
    time_finish_3 = time.time()
    elapsed_3 = time_finish_3 - time_start_3
    # Alert to runtime
    print("Time to finish Test 3: {}".format(elapsed_3))

    print(" ------------------------------------------------------------------------ ")
    
    # Alert to total program runtime
    print("Total time to finish: {}".format(time_finish_3 - time_start))
# Call main
main()