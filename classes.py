class Note:
    def __init__(self, s, d):
        self.sound = s
        self.duration = d

    def __eq__(self, other):
        if self.sound == other.sound and self.duration == other.duration:
            return True
        return False

    def __str__(self):
        return str(self.sound) + ' ' + str(self.duration)

    def __repr__(self):
        return str(self.sound) + ' ' + str(self.duration)

    def __hash__(self):
        return hash(str(self))


class BunchOfNotes:
    def __init__(self):
        self.length = 0
        self.bunch = []

    def __init__(self, bunch, l):
        self.length = l
        self.bunch = bunch

    def add(self, note):
        self.length = self.length + 1
        self.bunch.append(note)
