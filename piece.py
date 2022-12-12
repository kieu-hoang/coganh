import os
class Piece:
    def __init__(self, color, texture=None, texture_rect=None):
        self.color = color
        self.value = 1 if color == 'blue' else -1
        self.moves = []
        self.texture = texture
        self.texture_rect = texture_rect
        self.set_texture()
    def set_texture(self):
        self.texture = os.path.join(f'{self.color}_btn.png')   
    def add_move(self, move):
        self.moves.append(move)
    def clear_moves(self):
        self.moves = []
    def change_color(self):
        if self.color == 'blue':
            self.color = 'red'
        else:
            self.color = 'blue'   
        self.set_texture()
        self.update_value()
    def update_value(self):
        if self.color == 'blue':
            self.value = 1
        else:
            self.value = -1 