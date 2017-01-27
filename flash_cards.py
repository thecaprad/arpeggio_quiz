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

class Note(object):
    def __init__(self, pitch_value):
        self.pitch_value = pitch_value
        self.enharmonics_list = ALL_PITCHES[self.pitch_value]
        self.preferred_enharmonic = self.get_biased_index() # Int representing an index for enharmonics_list.

    def get_string(self):
        return self.enharmonics_list[self.preferred_enharmonic]

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

def get_random_note():
    return Note(random.choice(ALL_PITCHES.keys()))

if __name__ == "__main__":
    n = get_random_note()
    print(n.preferred_enharmonic)
    a = Arpeggio(n, "diminished")
    print([note.enharmonics_list for note in a.notes])