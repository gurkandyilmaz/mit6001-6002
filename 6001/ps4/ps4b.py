# Problem Set 4B

import string
from pathlib import Path

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    inFile = open(file_name, 'r')
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open(STORY_FILENAME, "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###
CWD = Path().cwd()
WORDLIST_FILENAME = CWD / '6001/ps4/words.txt'
STORY_FILENAME = CWD / '6001/ps4/story.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        letters = string.ascii_lowercase
        shift_dic = {}
        for idx in range(len(letters)):
            shift_dic[letters[idx]] = letters[ (idx+shift)%26 ]
            shift_dic[letters[idx].upper()] = letters[ (idx+shift)%26 ].upper()
        return shift_dic

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_text = ""
        for word in self.get_message_text():    
            for character in word:
                if character in string.ascii_letters:
                    shifted_text += self.build_shift_dict(shift)[character]
                else:
                    shifted_text += character
        return shifted_text

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, self.shift)
        self.message_text_encrypted = Message.apply_shift(self, self.shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        decrypted_text = ""
        best_shift = 0
        for idx in range(len(string.ascii_lowercase), 0, -1):
            for word in self.apply_shift(idx).split():
                if word in self.get_valid_words():
                    best_shift = idx
                    if self.apply_shift(idx) not in decrypted_text:
                        decrypted_text += self.apply_shift(idx)
            else:
                continue
        return (best_shift, decrypted_text)

def test_PlainTextMessage():
    #messages_and_shifts format: {(text, shift_value):expected_value}
    messages_and_shifts = {("How are you? Z",0):"How are you? Z", ("How are you? Z",1):"Ipx bsf zpv? A", ("What is THIS?",3):"Zkdw lv WKLV?"}
    for (text, shift), expected in messages_and_shifts.items():
        plaint_text = PlaintextMessage(text,shift)
        actual = plaint_text.get_message_text_encrypted()
        assert actual == expected, f"Actual ({actual}) and Expected ({expected}) values are Different!!!"

def test_CiphertextMessage():
    #messages_and_shifts format: {(text, shift_value):expected_value}
    messages_and_shifts = {"jgnnq JGnNQ":(24,"hello HElLO"), "Ipx bsf zpv? A":(25,"How are you? Z"), "Zkdw lv WKLV?":(23,"What is THIS?")}
    for text, (shift,expected) in messages_and_shifts.items():
        cipher_text = CiphertextMessage(text)
        actual_shift, actual_text = cipher_text.decrypt_message()
        assert actual_text == expected, f"Actual ({actual_text}) and Expected ({expected}) values are Different !!"
        assert actual_shift == shift, f"Actula shift ({actual_shift} and Expected shift ({shift}) are Different !!)"
        print(f"Expected: {shift} {expected}")
        print(f"Actual: {actual_shift} {actual_text}")

if __name__ == '__main__':
    test_PlainTextMessage()
    test_CiphertextMessage()
