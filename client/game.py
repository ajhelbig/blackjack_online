from raylib import *

class Game:

    def __init__(self):
        self.game_id = ""
        self.player_id = ""
        self.players = list()
        self.player_hands = list()
        self.dealer_hands = list()

        InitWindow(800, 450, b"Blackjack Client")
        SetTargetFPS(60)

    def play(self):
        while not WindowShouldClose():
            BeginDrawing()
            ClearBackground(WHITE)
            DrawText(b"Hello world", 190, 200, 20, VIOLET)
            EndDrawing()
        CloseWindow()