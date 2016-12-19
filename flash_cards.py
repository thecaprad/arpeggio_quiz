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

class Note(object):
    def __init__(self, pitch_value, enharmonics_list):
        self.pitch_value = pitch_value
        self.enharmonics_list = enharmonics_list
        self.preferred_enharmonic = 0 # Int representing an index for enharmonics_list.

NOTES = [Note(pitch_value, enharmonics_list) for pitch_value, enharmonics_list in ALL_PITCHES.items()]