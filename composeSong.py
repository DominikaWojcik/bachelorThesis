from mido import MidiFile
import numpy as np

# więcej niż jedna nutka do tyłu

# mozna zmienic tonację utworów

# jednorodny zbiór plików

# rytm

# potem polifonizacja


dic = {}
sound_amount = {}
mid = MidiFile('river_flow.mid')
ticks_per_beat = mid.ticks_per_beat
tempo = 60


def get_duration(msg, track):
    duration = 0
    found = False
    for m in track:
        if found is False and m == msg:
            duration = 0
            found = True

        elif found and m.dict().get("type") == "note_off" and \
                        m.dict().get("channel") == msg.dict().get("channel") and \
                        m.dict().get("note") == msg.dict().get("note") or \
                        \
                        m.dict().get("channel") == msg.dict().get("channel") and \
                        m.dict().get("note") == msg.dict().get("note") and \
                        m.dict().get("velocity") == 0:

            return round(float(m.dict().get("time") + duration) / 250) * 250
        elif found:
            duration += m.dict().get("time")


def ticks_to_ms(ticks):
    ms = ((ticks / ticks_per_beat) * tempo) / 1000
    return int(ms - (ms % 250) + 250)


def add_to_chain(prev, curr, duration, shift):
    for p in prev:
        p -= shift
        for c in curr:
            c -= shift
            if p not in dic:
                dic[p] = {}
                sound_amount[p] = 0
            sound_amount[p] += 1

            if (c, ticks_to_ms(duration)) not in dic[p]:
                dic[p][(c, ticks_to_ms(duration))] = 1
            else:
                dic[p][(c, ticks_to_ms(duration))] += 1


def compose_song(songs, shifts):
    print(shifts)
    for song, shift in zip(songs, shifts):
        mid = MidiFile(song)
        for i, track in enumerate(mid.tracks):
            print('Track {}: {}'.format(i, track.name))

            curr = []
            prev = []

            for msg in track:
                if msg.type == "set_tempo":
                    tempo = msg.tempo
                if msg.dict().get("type") == "note_off":
                    print(msg)
                    continue

                if msg.dict().get("note"):

                    if msg.dict().get("time") == 0:
                        curr.append(msg.dict().get("note"))
                    else:
                        add_to_chain(prev, curr, msg.dict().get("time"), shift)
                        prev = curr
                        curr = []

                    print(msg)

    for p in dic.keys():
        for c in dic[p].keys():
            dic[p][c] /= sound_amount[p]

    print(dic)

    degr = []
    durations = []
    sound = 64
    dur = 1000
    degr.append(sound)
    durations.append(dur)
    for i in range(20):
        sound = np.random.choice([x[0] for x in list(dic[sound].keys())], 1, list(dic[sound].values()))[0]
        degr.append(sound)

        dur = np.random.choice([x[1] for x in list(dic[sound].keys())], 1, list(dic[sound].values()))[0]
        durations.append(dur)

    return degr, durations
