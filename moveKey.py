import music21


def get_key(filenames):
    tonics = []
    modes = []

    for filename in filenames:
        score = music21.converter.parse(filename)
        key = score.analyze('key')
        tonics.append(str(key.tonic))
        modes.append(str(key.mode))

    return tonics, modes


def get_shift(filenames, keys_tonic):
    res = []
    sounds = {'c': 0, 'c#': 1, 'd': 2, 'd#': 3, 'e': 4, 'f': 5, 'f#': 6, 'g': 7, 'g#': 8, 'a': 9, 'a#': 10, 'h': 11, 'b':10}

    for filename, key_tonic in zip(filenames, keys_tonic):
        print(keys_tonic)
        key = key_tonic.lower().replace('-', '')
        res.append(sounds[key])

    return res

