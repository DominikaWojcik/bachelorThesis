from midiutil import MIDIFile


def mirror(arr):
    res = []
    res.append(arr[0])

    for i in range(1, len(arr)):
        diff = arr[i] - arr[i - 1]
        res.append(res[i - 1] - diff)
    return res


def does_it_sound_good(degrees1, degrees2, offset):
    i = 0
    while i + offset < len(degrees2):
        if not good_distance(degrees1[i], degrees2[i + offset]):
            return False
        i = i + 1
    return True


def good_distance(sound1, sound2):
    dist = (sound2 - sound1) % 12
    if dist in [0, 3, 4, 5, 7, 8, 9]:
        return True
    return False


def record_song(notes):
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 60  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    my_midi = MIDIFile(1)  # One track, defaults to format 1
    my_midi.addTempo(track, time, tempo)

    for n in notes:
        my_midi.addNote(track, channel, n.sound, time, n.duration / 1000, volume)
        time += n.duration / 1000

    with open("major-scale.mid", "wb") as output_file:
        my_midi.writeFile(output_file)
