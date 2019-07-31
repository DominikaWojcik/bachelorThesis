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
    def __init__(self, bunch, length):
        self.length = length
        self.bunch = bunch

    def __eq__(self, other):
        if self.bunch == other.bunch and self.length == other.length:
            return True
        return False

    def __str__(self):
        return str(self.bunch)

    def __repr__(self):
        return str(self.bunch)

    def __hash__(self):
        return hash(str(self))