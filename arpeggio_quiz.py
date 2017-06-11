import random

ALL_PITCHES_DICT = {
    1: ["Gx", "A", "Bbb"],
    2: ["A#", "Bb", "Cbb"],
    3: ["Ax", "B", "Cb"],
    4: ["B#", "C", "Dbb"],
    5: ["C#", "Db"],
    6: ["Cx", "D", "Ebb"],
    7: ["D#", "Eb", "Fbb"],
    8: ["Dx", "E", "Fb"],
    9: ["E#", "F", "Gbb"],
    10: ["Ex", "F#", "Gb"],
    11: ["Fx", "G", "Abb"],
    12: ["G#", "Ab"]
}

VALID_PITCHES_LOWER = [pitch.lower() for pitch_list in ALL_PITCHES_DICT.values() for pitch in pitch_list] # Is a list of all values in ALL_PITCHES_DICT. Requires double list comprehension.

MUSICAL_ALPHABET = ["A", "B", "C", "D", "E", "F", "G"]
INTERVALS = {"m3": 3, "M3": 4, "b5": 6, "P5": 7, "#5": 8, "6": 9, "bb7": 9, "m7": 10, "M7": 11, }
QUALITIES = {  # Values are list of half step intervals above a root
    "major": ["M3", "P5"], 
    "minor": ["m3", "P5"], 
    "diminished": ["m3", "b5"],
    "major 7": ["M3", "P5", "M7"],
    "minor 7": ["m3", "P5", "m7"],
    "dominant 7": ["M3", "P5", "m7"],
    "half diminished": ["m3", "b5", "m7"],
    "diminished 7": ["m3", "b5", "bb7"]
}
VALID_QUALITIES = QUALITIES.keys() # ["major", "minor", etc.]
VALID_PRETTY_QUALITIES = ", ".join(["'{}'".format(quality) for quality in VALID_QUALITIES]) # "'major', 'minor', etc."
VALID_QUALITY_ALIASES_MAP = {
    "major": ["major", "maj"],
    "minor": ["minor", "min"],
    "diminished": ["diminished", "dim"],
    "major 7": ["major 7", "maj7", "maj 7", "M7"],
    "minor 7": ["minor 7", "min7", "min 7", "m7", "-7"],
    "dominant 7": ["dominant 7", "dominant", "dom 7", "dom7", "7", "dom"],
    "half diminished": ["half diminished", "half dim", "m7b5", "m7(b5)", "-7b5", "-7(b5)"]
}
ALL_VALID_QUALITY_ALIASES = [alias for quality_list in VALID_QUALITY_ALIASES_MAP.values() for alias in quality_list] # ["major", "maj", "diminished", "dim", etc.]
QUIT_STR = "(Type 'quit' at any time to stop.)"

def get_random_note():
    return Note(random.choice(ALL_PITCHES_DICT.keys()))

def get_random_quality():
    return random.choice(VALID_QUALITIES)

def get_random_arpeggio(quality=None):
    """
    Takes a list of possible arpeggio qualities (e.g., ["major", "minor"], and returns a random Arpeggio object with a quality from the possible list.
    If no quality is given, an Arpeggio object is returned with its quality randomly selected from `VALID_QUALITIES`.
    """
    if not quality:
        quality = [get_random_quality()]
    return Arpeggio(get_random_note(), random.choice(quality))

def is_valid_quality_alias(unchecked_alias, arpeggio):
    return unchecked_alias.lower() in VALID_QUALITY_ALIASES_MAP[arpeggio.quality]

def select_quiz(): # Helper function prompts user to select a quiz type and returns the corresponding quiz function.
    available_quizes = {"1": spelling_quiz, "2": identification_quiz}
    available_quizes_str = "('1' = spelling, '2' = identifying)"
    selection = ""
    while selection not in available_quizes:
        selection = raw_input("Would you like practice spelling or identifying arpeggios? {}: ".format(available_quizes_str))
        if selection.lower() == "quit":
            raise KeyboardInterrupt
    print
    return available_quizes[selection]

def get_selected_qualities_list():
    """
    Prompts the user with every available quality from `VALID_QUALITIES` (e.g., "1 = 'major', 2 = 'minor', etc.)
    Returns a list of selected qualities. ["major" "diminished"]
    """
    # Used in `spelling_quiz()` to practice spelling a specific quality arpeggio, like "minor".
    valid_spelling_quiz_qualities_dict = dict(enumerate(VALID_QUALITIES, 1)) # {1: 'major', 2: 'diminished', etc.}
    for number, quality in valid_spelling_quiz_qualities_dict.items():
        print("'{}' = {}".format(number, quality)) 
    try:
        selected_quality_indexes = raw_input("Enter the numbers (separated by a comma) for the qualities you'd like to practice, or type any other key for random: ")
        result = []
        for quality_index in selected_quality_indexes.split(","):
            result.append(valid_spelling_quiz_qualities_dict[int(quality_index)])
        return result
    except (ValueError, KeyError, TypeError):
        return None

def print_selected_qualities(selected_qualities_list):
    selected_string = "Selected qualities:"
    try:
        print("{} {}".format(selected_string, ", ".join(selected_qualities_list)))
    except TypeError:
        print("{} random".format(selected_string))
    print

def run_quiz_prompt(quiz_function):
    # Runs interactive quiz prompt given either "identification_quiz" or "spelling_quiz".
    selected_quality = None # None will generate a random arpeggio.
    if quiz_function == spelling_quiz:
        selected_qualities = get_selected_qualities_list()
        print_selected_qualities(selected_qualities)
    while 1:
        arpeggio = get_random_arpeggio(selected_qualities)
        answer_string = "{} is spelled '{}.'".format(arpeggio.get_name_string(), arpeggio.get_notes_string())
        result = quiz_function(arpeggio)
        if result:
            print("Good on ya! " + answer_string)
        else:
            print("Nayeth. " + answer_string)
        print

def identification_quiz(arpeggio):
    answer = ""
    while answer not in ALL_VALID_QUALITY_ALIASES:
        answer = raw_input("Identify the quality of arpeggio '{}'. {}: ".format(arpeggio.get_notes_string(), QUIT_STR)).lower()
        if answer.lower() == "quit":
            raise KeyboardInterrupt
    return is_valid_quality_alias(answer, arpeggio)

def spelling_quiz(arpeggio):
    chord_intervals = ["R"] + QUALITIES[arpeggio.quality]
    print("Spell out each interval of {}. {}".format(arpeggio.get_name_string(), QUIT_STR))
    chord_interval_index = 0
    correct = True # Used to control loop.
    for note in arpeggio.notes:
        answer = ""
        while answer.lower() not in VALID_PITCHES_LOWER: # Catches typos, and allows user to resubmit.
            answer = raw_input("{}: ".format(chord_intervals[chord_interval_index]))
            if answer.lower() == "quit":
                raise KeyboardInterrupt
        chord_interval_index += 1
        if not answer.lower() == note.get_string().lower():
            correct = False
    return correct

class Note(object):
    def __init__(self, pitch_value, preferred_enharmonic_index=None):
        self.pitch_value = pitch_value
        self.enharmonics_list = ALL_PITCHES_DICT[self.pitch_value]
        if preferred_enharmonic_index == None:
            self.preferred_enharmonic_index = self.get_biased_index() # Int representing an index for enharmonics_list.
        else:
            self.preferred_enharmonic_index = preferred_enharmonic_index

    def get_string(self):
        return self.enharmonics_list[self.preferred_enharmonic_index]

    def get_biased_index(self):
        """
        Returns an index of enharmonics_list that represents a random enharmonic that is not
        double sharp 'x'
        or double flat 'bb'
        """
        double_sharp = "x"
        double_flat = "bb"
        possible_indexes = range(len(self.enharmonics_list))
        clean_indexes = []
        for index in possible_indexes:
            biased_enharmonic = self.enharmonics_list[index]
            if not biased_enharmonic.endswith(double_flat) and not biased_enharmonic.endswith(double_sharp):
                clean_indexes.append(index)
        return random.choice(clean_indexes)

class Arpeggio(object):
    def __init__(self, root, quality):
        self.root = root # Note object
        self.quality = quality # String found in VALID_QUALITIES
        self.notes = self.get_notes() # List of note objects
        self.assign_correct_preferred_enharmonics()

    def get_notes(self):
        """
        Returns list of note objects for the corresponding arpeggio based on the root and quality.
        """
        result = [self.root]
        for interval in QUALITIES[self.quality]:
            next_pitch_value = self.root.pitch_value + INTERVALS[interval]
            if next_pitch_value > 12: # Max pitch value is always 12.
                next_pitch_value = next_pitch_value % 12
            result.append(Note(next_pitch_value))
        return result
    
    def assign_correct_preferred_enharmonics(self):
        """
        Each note above the root in the arpeggio will have its preferred_enharmonic_index reassigned to match the correct spelling of
        the arpeggio relative to the root.
        """
        i = 0
        root_primary_pitch_index = MUSICAL_ALPHABET.index(self.root.get_string()[0]) # The primary pitch of "Bb" is "B", "F#" is "F", etc.
        """
        In `MUSICAL_ALPHABET`, "A"'s index is 0, "B"'s is 1, etc. 
        This index helps to calculate what the next interval's primary pitch should be. 
        """
        for note in self.notes:
            if note.pitch_value == self.root.pitch_value: # Enharmonic for the root will not be reassigned.
                pass
            else:
                try:
                    next_primary_pitch_index = int(QUALITIES[self.quality][i][1])
                except ValueError:
                    next_primary_pitch_index = int(QUALITIES[self.quality][i][2]) # This catches double flat ("bb7") spellings.
                primary_pitch = MUSICAL_ALPHABET[(((root_primary_pitch_index + next_primary_pitch_index) - 1) % 7)]
                for enharmonic in note.enharmonics_list:
                    if enharmonic.startswith(primary_pitch):
                        note.preferred_enharmonic_index = note.enharmonics_list.index(enharmonic)
                        break # There is only one correct enharmonic per note. No further looping required.
                i += 1

    def get_notes_string(self): # "D, F#, A"
        return ", ".join([note.get_string() for note in self.notes])

    def get_name_string(self): # "G major"
        return "{} {}".format(self.root.get_string(), self.quality)

if __name__ == "__main__":
    try:
        run_quiz_prompt(select_quiz())
    except (KeyboardInterrupt, EOFError):
        print
        pass