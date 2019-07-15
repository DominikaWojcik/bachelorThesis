from mido import MidiFile
import numpy as np
from classes import Note

# więcej niż jedna nutka do tyłu

# mozna zmienic tonację utworów

# jednorodny zbiór plików

# rytm

# potem polifonizacja

dic = {}
notes_amount = {}
notes = {}


def ticks_to_ms(ticks, ticks_per_beat, tempo):
    ms = ((ticks / ticks_per_beat) * tempo) / 1000
    return int(ms - (ms % 250) + 250)


def proccess_msg(mid):
    temp_notes = []
    time = 0
    duration = 0
    for i, track in enumerate(mid.tracks):
        bunch = [0]

        for msg in track:
            if msg.type == "set_tempo":
                tempo = msg.tempo

            if msg.dict().get("type") == "note_off":
                time += msg.dict().get("time")
                duration += msg.dict().get("time")
                continue

            if msg.dict().get("note"):
                if duration + msg.dict().get("time") == 0:
                    bunch.append(msg.dict().get("note"))
                else:
                    duration += msg.dict().get("time")
                    # temp_notes.append(((bunch), duration, time))  #<-  coś takiego jeśli chcemy całe akordy
                    temp_notes.append((max(bunch), duration, time))
                    time += duration
                    duration = 0
                    bunch = [msg.dict().get("note")]
    return temp_notes, tempo


def compose_song(songs, shifts):
    for song, shift in zip(songs, shifts):
        mid = MidiFile(song)
        temp, tempo = proccess_msg(mid)
        ticks_per_beat = mid.ticks_per_beat

        curr = None
        for note in temp:
            prev = curr
            curr = note
            if prev is None:
                continue

            p = Note(prev[0] - shift, ticks_to_ms(prev[1], ticks_per_beat, tempo))
            c = Note(curr[0] - shift, ticks_to_ms(curr[1], ticks_per_beat, tempo))

            if p not in dic:
                dic[p] = {}
                notes_amount[p] = 0
            notes_amount[p] += 1

            if c not in dic[p]:
                dic[p][c] = 1
            else:
                dic[p][c] += 1

    for p in dic.keys():
        for c in dic[p].keys():
            dic[p][c] /= notes_amount[p]

    print(dic)

    degr = []
    durations = []
    sound = 64
    dur = 1000
    degr.append(sound)
    durations.append(dur)
    n = np.random.choice(list(dic.keys()))
    notes = [n]
    print(notes)
    for i in range(20):
        n = np.random.choice([x for x in list(dic[n].keys())], 1, list(dic[n].values()))[0]
        notes.append(n)

    print(notes)
    return notes

