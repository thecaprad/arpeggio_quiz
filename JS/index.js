const allPitchesDict = {
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

// TODO: Can this be accomplished more simply with a zip of sorts?
const pitchIndex = {
    "Gx": 1,
    "A": 1,
    "Bbb": 1,
    "A#": 2, 
    "Bb": 2, 
    "Cbb": 2,
    "Ax": 3,
    "B": 3,
    "Cb": 3,
    "B#": 4,
    "C": 4,
    "Dbb": 4,
    "C#": 5,
    "Db": 5,
    "Cx": 6,
    "D": 6,
    "Ebb": 6,
    "D#": 7,
    "Eb": 7,
    "Fbb": 7,
    "Dx": 8,
    "E": 8,
    "Fb": 8,
    "E#": 9,
    "F": 9,
    "Gbb": 9,
    "Ex": 10,
    "F#": 10,
    "Gb": 10,
    "Fx": 11,
    "G": 11,
    "Abb": 11,
    "G#": 12,
    "Ab": 12
}

const musicalAlphabet = ["A", "B", "C", "D", "E", "F", "G"]

// Musical intervals mapped to the number of half-steps they represent.
// E.g., Major third interval = 4 half-steps.
const intervalValues = {
    "m3": 3, 
    "M3": 4,
    "P4": 5,
    "b5": 6, 
    "P5": 7, 
    "#5": 8, 
    "6": 9, 
    "bb7": 9, 
    "m7": 10, 
    "M7": 11,
}

class Note {
    // Takes a pitch value (as relates to allPitchesDict keys) and a 
    // primaryPitch string. A primaryPitch is a one-character string specifying the 
    // preferred starting note of an enharmonic.
    // E.g., the primaryPitch of "Bb" is "B." For "A#" it's "A."

    constructor(pitchValue, primaryPitch) {
        this.pitchValue = pitchValue;
        this.enharmonicList = allPitchesDict[pitchValue];
        this.preferredEnharmonic = this.enharmonicList.filter(function(enharmonic) {
            return enharmonic.startsWith(cleanRootString(primaryPitch));
        })[0];
    }
}

class Arpeggio {
    constructor(root, quality) {
        this.quality = quality;
        this.notes = this.buildArpeggio(root, quality);
        // this.buildArpeggio(root, quality);
    }

    buildArpeggio(root, quality) {
        const intervals = chordQualitySpellings[quality];
        let result = [root];
        intervals.forEach(function(interval) {
            // Determine next pitch value
            if (root.pitchValue + intervalValues[interval] > 12) {
                var nextPitchValue = (root.pitchValue + intervalValues[interval]) % 12;
            } else {
                var nextPitchValue = root.pitchValue + intervalValues[interval];
            }
            console.log(nextPitchValue);

            // Determine next primary note
            var rootIndex = musicalAlphabet.indexOf(root.preferredEnharmonic[0]);
            var intervalInt = parseInt(interval[1]);

            if (rootIndex + (intervalInt - 1) < 7) {
                var nextPrimaryPitch = musicalAlphabet[rootIndex + (intervalInt - 1)];
            } else {
                var dec = 6 - rootIndex;
                var remainingInt = intervalInt - dec;
                var nextPrimaryPitch = musicalAlphabet[remainingInt - 2];
            }
            console.log(nextPrimaryPitch);

            result.push(new Note(nextPitchValue, nextPrimaryPitch));
        })
        return result;
    }
}

// Instructions on how to spell common chord qualities.
// Given interval spellings are individually relative the root.
// E.g., major chords are spelled root + M3 + P5 (major third + perfect fifth).
const chordQualitySpellings = {
    "major": ["M3", "P5"], 
    "minor": ["m3", "P5"], 
    "diminished": ["m3", "b5"],
    "augmented": ["M3", "#5"],
    "major 7": ["M3", "P5", "M7"],
    "minor 7": ["m3", "P5", "m7"],
    "dominant 7": ["M3", "P5", "m7"],
    "half diminished": ["m3", "b5", "m7"],
    "diminished 7": ["m3", "b5", "bb7"]
}

function cleanRootString(root) {
    // "ABB" --> "Abb", "c#" --> "C#", "f" ->"F".
    // TODO: Consider making this return only the first character.
        // Are subsequent characters ever used?
    return root.charAt(0).toUpperCase() + root.slice(1).toLowerCase();
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('chordSubmit').addEventListener('click', function() {
        const root = cleanRootString(document.getElementById('root').value);
        const note = new Note(pitchIndex[root], root[0]);
        console.log(note);
    })
});
