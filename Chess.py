###LIBRARIES###
import pygame
import os
import chess

###INITIATION###
pygame.init()
pygame.font.init()
inBoard = chess.Board()

###VARIABLES###
width = 1200
height = 800
previous_move_from = ""
previous_move_to = ""
locations = []
run = True
show_moves = False
was_pressed = False
selected_sq = None
mouse_button_down = False
clock = pygame.time.Clock()
font = pygame.font.Font(os.path.join("Fonts", "ColorBasic.otf"), 21)

###DICTIONARIES###
chess_dict = {
    0: (0, 700),
    1: (100, 700),
    2: (200, 700),
    3: (300, 700),
    4: (400, 700),
    5: (500, 700),
    6: (600, 700),
    7: (700, 700),
    8: (0, 600),
    9: (100, 600),
    10: (200, 600),
    11: (300, 600),
    12: (400, 600),
    13: (500, 600),
    14: (600, 600),
    15: (700, 600),
    16: (0, 500),
    17: (100, 500),
    18: (200, 500),
    19: (300, 500),
    20: (400, 500),
    21: (500, 500),
    22: (600, 500),
    23: (700, 500),
    24: (0, 400),
    25: (100, 400),
    26: (200, 400),
    27: (300, 400),
    28: (400, 400),
    29: (500, 400),
    30: (600, 400),
    31: (700, 400),
    32: (0, 300),
    33: (100, 300),
    34: (200, 300),
    35: (300, 300),
    36: (400, 300),
    37: (500, 300),
    38: (600, 300),
    39: (700, 300),
    40: (0, 200),
    41: (100, 200),
    42: (200, 200),
    43: (300, 200),
    44: (400, 200),
    45: (500, 200),
    46: (600, 200),
    47: (700, 200),
    48: (0, 100),
    49: (100, 100),
    50: (200, 100),
    51: (300, 100),
    52: (400, 100),
    53: (500, 100),
    54: (600, 100),
    55: (700, 100),
    56: (0, 0),
    57: (100, 0),
    58: (200, 0),
    59: (300, 0),
    60: (400, 0),
    61: (500, 0),
    62: (600, 0),
    63: (700, 0)
}
piece_images_white = {
    chess.PAWN: pygame.transform.scale(pygame.image.load(os.path.join("Images", "white_pieces", "WP.png")), (90, 90)),
    chess.KNIGHT: pygame.transform.scale(pygame.image.load(os.path.join("Images", "white_pieces", "WN.png")), (90, 90)),
    chess.BISHOP: pygame.transform.scale(pygame.image.load(os.path.join("Images", "white_pieces", "WB.png")), (90, 90)),
    chess.ROOK: pygame.transform.scale(pygame.image.load(os.path.join("Images", "white_pieces", "WR.png")), (90, 90)),
    chess.QUEEN: pygame.transform.scale(pygame.image.load(os.path.join("Images", "white_pieces", "WQ.png")), (90, 90)),
    chess.KING: pygame.transform.scale(pygame.image.load(os.path.join("Images", "white_pieces", "WK.png")), (90, 90))
}
piece_images_black = {
    chess.PAWN: pygame.transform.scale(pygame.image.load(os.path.join("Images", "black_pieces", "BP.png")), (90, 90)),
    chess.KNIGHT: pygame.transform.scale(pygame.image.load(os.path.join("Images", "black_pieces", "BN.png")), (90, 90)),
    chess.BISHOP: pygame.transform.scale(pygame.image.load(os.path.join("Images", "black_pieces", "BB.png")), (90, 90)),
    chess.ROOK: pygame.transform.scale(pygame.image.load(os.path.join("Images", "black_pieces", "BR.png")), (90, 90)),
    chess.QUEEN: pygame.transform.scale(pygame.image.load(os.path.join("Images", "black_pieces", "BQ.png")), (90, 90)),
    chess.KING: pygame.transform.scale(pygame.image.load(os.path.join("Images", "black_pieces", "BK.png")), (90, 90))
}

###WINDOW###
wn = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

def draw():
    ###VARIABLES
    global locations, previous_move_to, previous_move_from

    ###BOARD###
    for col in range(8):
        for row in range(8):
            if (row + col) % 2 == 0:
                pygame.draw.rect(wn, (180, 180, 180), (col * 100, row * 100, 100, 100))
            else:
                pygame.draw.rect(wn, (124, 124, 124), (col * 100, row * 100, 100, 100))

    ###MOVE GHOST SQUARE###
    if previous_move_from != "" and previous_move_to != "":
        rect_surf_from, rect_surf_to = pygame.Surface((100, 100), pygame.SRCALPHA), pygame.Surface((100, 100),                                                                                    pygame.SRCALPHA)
        rect_surf_from.fill((51, 51, 255, 127.5))
        rect_surf_to.fill((51, 51, 255, 127.5))
        wn.blit(rect_surf_from, chess_dict[previous_move_from])
        wn.blit(rect_surf_to, chess_dict[previous_move_to])

    ###MOVE SQUARE###
    if len(locations) == 1:
        for move in inBoard.legal_moves:
            if move.from_square == chess.parse_square(locations[0]):
                rect_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(rect_surf, (51, 51, 255, 128), (0, 0, 100, 100))
                wn.blit(rect_surf, chess_dict[move.from_square])

    ###PIECES###
    for square in chess.SQUARES:
        piece = inBoard.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                piece_image = piece_images_white.get(piece.piece_type)
            else:
                piece_image = piece_images_black.get(piece.piece_type)
            if piece_image:
                wn.blit(piece_image, (chess_dict[square][0] + 5, chess_dict[square][1] + 5))


def movement(): # add promotions
    ###VARIABLES###
    global chess_dict, locations, inBoard, mouse_button_down, previous_move_from, previous_move_to
    mouse_left_click = pygame.mouse.get_pressed()[0]
    mouse_position = pygame.mouse.get_pos()
    legal_moves = list(inBoard.legal_moves)

    ###MOVING PIECES###
    if mouse_left_click and not mouse_button_down:
        mouse_button_down = True
        for square_index, value in chess_dict.items():
            rect = pygame.Rect(value[0], value[1], 100, 100)
            if rect.collidepoint(mouse_position):
                if len(locations) == 0:
                    locations.append(chess.square_name(square_index))
                    break
                elif len(locations) == 1:
                    from_square = locations[0]
                    to_square = chess.square_name(square_index)

                    if from_square != to_square:
                        move = chess.Move.from_uci(f"{from_square}{to_square}")
                        if move in legal_moves:
                            print(move)
                            locations.append(to_square)
                            previous_move_from = chess.parse_square(from_square)
                            previous_move_to = chess.parse_square(to_square)
                            inBoard.push(move)
                            locations = []
                        elif inBoard.piece_at(chess.parse_square(to_square)) is not None:
                            locations[0] = to_square
                        else:
                            locations = []
                    else:
                        locations = []
                    break

    ###CIRCLE MOVE HINT###
    if len(locations) == 1:
        from_square = chess.parse_square(locations[0])
        for move in legal_moves:
            if move.from_square == from_square:
                to_square = chess_dict[move.to_square]
                circle_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(circle_surf, (0, 0, 0, 35.7), (50, 50), 20)
                wn.blit(circle_surf, to_square)


while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_down = False
    wn.fill((0, 0, 0))
    draw()
    movement()
    pygame.display.flip()
    for move in inBoard.legal_moves:
        if move.to_square == chess.parse_square("h1"):
            print(move)

print(inBoard.fen())
pygame.quit()
