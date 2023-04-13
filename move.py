
class Move:
    def __init__(self, initial, final):
        #initial and final are squares
        self.initial = initial
        self.final = final
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    def to_text(self):
        ini = self.initial
        fin = self.final
        return f'({ini.row}, {ini.col}) -> ({fin.row}, {fin.col})'
    def to_num(self):
        ini = self.initial
        fin = self.final
        return ini.row, ini.col, fin.row, fin.col