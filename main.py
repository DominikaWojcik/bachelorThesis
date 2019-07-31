#!/usr/bin/env python

import os
import composeSong
import recordSong
import moveKey

path = '/home/dominikas14/PycharmProjects/pracaInz/muzyka_powazna'
songs = []
for r, d, f in os.walk(path):
    for file in f:
        if '.mid' in file:
            songs.append(os.path.join(r, file))

print(songs)

songs = ['/home/dominikas14/PycharmProjects/pracaInz/muzyka_powazna/bwv1041a.mid']
# songs = ['river_flow.mid']
keys, modes = moveKey.get_key(songs)
print('done')
shifts = moveKey.get_shift(songs, keys)
print('here')
notes = composeSong.compose_song(songs, shifts, 10)
print('almost')
recordSong.record_song(notes)
