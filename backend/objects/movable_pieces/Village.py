from backend.objects.movable_pieces.Settlement import Settlement

class Village(Settlement):
    def __init__(self, player):
        super().__init__(player)
        self.victory_points = 1