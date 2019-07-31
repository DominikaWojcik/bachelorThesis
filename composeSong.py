from mido import MidiFile
import numpy as np
from classes import Note
from classes import BunchOfNotes

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


def compose_song(songs, shifts, bunch_len):
    for song, shift in zip(songs, shifts):
        mid = MidiFile(song)
        temp, tempo = proccess_msg(mid)
        ticks_per_beat = mid.ticks_per_beat

        curr = None
        bun = []
        for note in temp:
            prev = curr
            curr = note
            if prev is None:
                continue

            p = Note(prev[0] - shift, ticks_to_ms(prev[1], ticks_per_beat, tempo))
            bun.append(p)
            if len(bun) <= bunch_len:
                continue
            bun.pop(0)
            c = Note(curr[0] - shift, ticks_to_ms(curr[1], ticks_per_beat, tempo))

            b = tuple(bun)
            if b not in dic:
                dic[b] = {}
                notes_amount[b] = 0
            notes_amount[b] += 1

            if c not in dic[b]:
                dic[b][c] = 1.0
            else:
                dic[b][c] += 1

    print(dic)
    print(notes_amount)

    for p in dic.keys():
        for c in dic[p].keys():
            dic[p][c] /= float(notes_amount[p])

    print(dic)

    n = list(dic.keys())[np.random.choice(len(list(dic.keys())))]
    notes = list(n)
    print(notes)

    for i in range(20):
        d = dic[tuple(notes[-bunch_len:])]
        n = np.random.choice([x for x in list(d.keys())], 1, list(d.values()))[0]
        notes.append(n)

    print(notes)
    return notes
