class Transposer:

    keymap = {"C":["B", "C#"], "C#":["C", "D"], "D":["C#", "D#"], "D#":["D", "E"], "E":["D#", "F"], "F":["E", "F#"], "F#":["F", "G"], "G":["F#", "G#"], "G#":["G", "A"], "A":["G#", "A#"], "A#":["A", "B"], "B":["A#", "C"]}

    notes = []
    flattened_notes = []

    # The input MUST be an array of arrays, with singular notes and chords denoted by ["X"] and ["X", "Y", "Z"] respectively.
    def __init__(self, notes):
        self.notes = notes
        self.flattened_notes = self.__flatten(self.notes)

    def __flatten(self, array_of_arrays):
        return [item for sublist in array_of_arrays for item in sublist]

    # Gets the next semitone up/down
    def __step(self, note, bool_step_up):
        neighbours = self.keymap[f"{note}"]

        if bool_step_up:
            return neighbours[1]
        else:
            return neighbours[0]

    # Counts the steps from note_1 to note_2. As the program does not account for octave difference, the direction of counting does not matter.
    def __count_steps(self, note_1, note_2):
        counter = 0
        
        while(note_1 != note_2):
            # Handle infinite while loop if it somehow happens...
            if counter > 12:
                print(f"Something went wrong and the __count_steps function failed!")
                return 0

            note_1 = self.__step(note_1, True)
            counter += 1

        return counter

    # Transposes the input by a certain number of semitones, n. Boolean "up" designates direction of transposition.
    def transpose_by(self, n_semitones, up=True):
        product = []

        for note_array in self.notes:
            new_note_array = []

            for note in note_array:
                new_note = note

                for i in range(n_semitones):
                    new_note = self.__step(new_note, up)

                new_note_array.append(new_note)

            product.append(new_note_array)

        return product

    # Transposes all notes so that the composition starts on the given note. 
    # Don't use this if the first element in the notes array is a chord!
    def start_on_note(self, note):
        n_steps = self.__count_steps(self.notes[0][0], note)

        # Here, up=True takes advantage of the fact that the __count_steps function
        # counts UP (so direction of transposition should be UP)
        return self.transpose_by(n_steps, up=True)

    # Finds all the possible starting note transpositions that avoid the notes provided 
    def avoid(self, notes_to_avoid):
        all_notes = list(self.keymap.keys())
        avoided_the_note = []

        for note in all_notes:
            transposition = self.start_on_note(note)
            reject = False

            for bad_note in notes_to_avoid:
                if bad_note in self.__flatten(transposition):
                    reject = True

            if reject:
                continue
            else:
                avoided_the_note.append(transposition)

        return avoided_the_note

t = Transposer([["A"], ["B"], ["C", "D"]])
print(t.avoid(["C", "C#"]))
