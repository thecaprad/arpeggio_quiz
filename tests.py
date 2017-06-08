import unittest, random

from arpeggio_quiz import Note, Arpeggio

class AssignEnharmonicTests(unittest.TestCase):
    def test_A_M3(self):
        a = Arpeggio(Note(1, 1), "major") # Root: "A", chord: major.
        note = a.notes[1]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "C#")

    def test_A_P5(self):
        a = Arpeggio(Note(1, 1), "major") # Root: "A", chord: major.
        note = a.notes[2]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "E")

    def test_C_flat_M3(self):
        a = Arpeggio(Note(3, 2), "major") # Root: "Cb", chord: major.
        note = a.notes[1]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "Eb")

    def test_C_flat_P5(self):
        a = Arpeggio(Note(3, 2), "major") # Root: "Cb", chord: major.
        note = a.notes[2]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "Gb")

    def test_F_sharp_M3(self):
        a = Arpeggio(Note(10, 1), "major") # Root: "F#", chord: major.
        note = a.notes[1]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "A#")

    def test_F_sharp_P5(self):
        a = Arpeggio(Note(10, 1), "major") # Root: "F#", chord: major.
        note = a.notes[2]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "C#")

    def test_A_m3(self):
        a = Arpeggio(Note(1, 1), "minor") # Root: "A", chord: minor.
        note = a.notes[1]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "C")

    def test_C_flat_m3(self):
        a = Arpeggio(Note(3, 2), "minor") # Root: "Cb", chord: minor.
        note = a.notes[1]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "Ebb")

    def test_B_m3(self):
        a = Arpeggio(Note(3, 1), "diminished") # Root: "B", chord: diminished.
        note = a.notes[1]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "D")

    def test_B_b5(self):
        a = Arpeggio(Note(3, 1), "diminished") # Root: "B", chord: diminished.
        note = a.notes[2]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "F")

    def test_Fb_m3(self):
        a = Arpeggio(Note(8, 2), "diminished") # Root: "Fb", chord: diminished.
        note = a.notes[1]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "Abb")

    def test_Fb_b5(self):
        a = Arpeggio(Note(8, 2), "diminished") # Root: "Fb", chord: diminished.
        note = a.notes[2]
        self.assertEqual(note.enharmonics_list[note.preferred_enharmonic_index], "Cbb")

if __name__ == "__main__":
    unittest.main()