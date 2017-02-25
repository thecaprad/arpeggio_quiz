import random

ALL_PITCHES = {
    1: ["Gx", "A", "Bbb"],
    2: ["A#", "Bb"],
    3: ["Ax", "B", "Cb"],
    4: ["B#", "C", "Dbb"],
    5: ["C#", "Db"],
    6: ["Cx", "D", "Ebb"],
    7: ["D#", "Eb"],
    8: ["Dx", "E", "Fb"],
    9: ["E#", "F", "Gbb"],
    10: ["Ex", "F#", "Gb"],
    11: ["Fx", "G", "Abb"],
    12: ["G#", "Ab"]
}

MUSICAL_ALPHABET = ["A", "B", "C", "D", "E", "F", "G"]
INTERVALS = {"m3": 3, "M3": 4, "b5": 6, "P5": 7, "#5": 8}
QUALITIES = {"major": ["M3", "P5"], "minor": ["m3", "P5"], "diminished": ["m3", "b5"]} # Values are list of half step intervals above a root
VALID_QUALITIES = QUALITIES.keys() # "major", "minor", etc.

class QuitPrompt(Exception):
    pass

def get_random_note():
    return Note(random.choice(ALL_PITCHES.keys()))

def get_random_quality():
    return random.choice(VALID_QUALITIES)

def get_random_arpeggio():
    return Arpeggio(get_random_note(), get_random_quality())

def identification_quiz():
    """
    Prompt spells a randomly generated arpeggio and asks the user to define its quality.
    """
    solved = True # Forces first loop to generate a new arpeggio.
    while 1:
        if solved:
            arpeggio = get_random_arpeggio()
        solved = False
        answer = raw_input("Identify the quality of this arpeggio: '{}': ".format(arpeggio.get_notes_string())).lower()
        if answer == "quit":
            break
        if answer not in VALID_QUALITIES:
            print("Please enter a valid quality. (i.e., {})".format(", ".join(VALID_QUALITIES)))
        else:
            if answer == arpeggio.quality:
                print("Good on ya! The arpeggio is indeed {}.".format(arpeggio.get_name_string()))
                solved = True
            else:
                print("Nayeth. The arpeggio was in fact {}.".format(arpeggio.get_name_string()))
                solved = True
        print

class Note(object):
    def __init__(self, pitch_value, preferred_enharmonic_index=None):
        self.pitch_value = pitch_value
        self.enharmonics_list = ALL_PITCHES[self.pitch_value]
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
        root_primary_pitch_index = MUSICAL_ALPHABET.index(self.root.get_string()[0])
        for note in self.notes:
            if note.pitch_value == self.root.pitch_value: # Enharmonic for the root will not be reassigned.
                pass
            else:
                 primary_pitch = MUSICAL_ALPHABET[(((root_primary_pitch_index + int(QUALITIES[self.quality][i][1])) - 1) % 7)]
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
    identification_quiz()