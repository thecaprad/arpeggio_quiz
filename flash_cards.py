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
INTERVALS = {'m3': 3, 'M3': 4, 'b5': 6, 'P5': 7, '#5': 8, 'x5': 9}
QUALITIES = {'major': ['M3', 'P5'], 'minor': ['m3', 'P5'], 'diminished': ['m3', 'b5']} # Values are list of half step intervals above a root

class Note(object):
    def __init__(self, pitch_value, enharmonics_list):
        self.pitch_value = pitch_value
        self.enharmonics_list = enharmonics_list
        self.preferred_enharmonic = 0 # Int representing an index for enharmonics_list.

NOTES = [Note(pitch_value, enharmonics_list) for pitch_value, enharmonics_list in ALL_PITCHES.items()]