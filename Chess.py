###LIBRARIES###
import logging
import math
import os
import sys
import time

import chess
import pygame
import pyperclip

# to see debug messages uncomment the next comment:
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

###INITIATION###
pygame.init()
pygame.font.init()
inBoard = chess.Board()

###VARIABLES###
width = 1250
height = 800
page = 0
previous_move_from = ""
previous_move_to = ""
locations = []
run = True
loop = False
show_moves = False
was_pressed = False
selected_sq = None
rect_surf_to = None
rect_surf_from = None
mouse_button_held = False
mouse_button_released = True
show_promotion_bar = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 55)
fontMedium = pygame.font.Font(None, 95)
fontBIG = pygame.font.Font(None, 100)

game_title = fontBIG.render("Chess Game", True, (0, 0, 0))
replay_instructions = font.render("Press any key to restart, or escape to close the program", True, (0, 0, 0), (255, 0, 255))
return_instructions = font.render("Press any key to return, or escape to close the program", True, (0, 0, 0), (255, 0, 255))
game_credits_text = fontMedium.render("Made by: WafflesOnTrees", True, (0, 0, 0))

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

def reset_variables():
    global previous_move_from, previous_move_to, locations, show_moves, was_pressed, selected_sq, rect_surf_to, rect_surf_from, mouse_button_held, mouse_button_released, show_promotion_bar, inBoard, loop

    inBoard = chess.Board()
    previous_move_from = ""
    previous_move_to = ""
    locations = []
    loop = False
    show_moves = False
    was_pressed = False
    selected_sq = None
    rect_surf_to = None
    rect_surf_from = None
    mouse_button_held = False
    mouse_button_released = True
    show_promotion_bar = False


def switch_page():
    global page
    mouse_left_click = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()

    next_page_pos1 = (1200, 25)
    next_pg_surf1 = pygame.Surface((50, 50), pygame.SRCALPHA)
    next_pg_rect1 = next_pg_surf1.get_rect(topleft=next_page_pos1)
    arrow_text1 = fontBIG.render(">", True, (0, 0, 0))
    next_page_pos2 = (1200, 725)
    next_pg_surf2 = pygame.Surface((50, 50), pygame.SRCALPHA)
    next_pg_rect2 = next_pg_surf2.get_rect(topleft=next_page_pos2)
    arrow_text2 = fontBIG.render("<", True, (0, 0, 0))

    next_pg_surf1.fill((0, 0, 0, 0))
    pygame.draw.rect(next_pg_surf1, (180, 180, 180), (0, 0, 50, 50), border_radius=10)
    pygame.draw.rect(next_pg_surf1, (0, 0, 0), (0, 0, 50, 50), 2, border_radius=10)
    next_pg_surf2.fill((0, 0, 0, 0))
    pygame.draw.rect(next_pg_surf2, (180, 180, 180), (0, 0, 50, 50), border_radius=10)
    pygame.draw.rect(next_pg_surf2, (0, 0, 0), (0, 0, 50, 50), 2, border_radius=10)

    if mouse_left_click and next_pg_rect1.collidepoint(mouse_pos):
        # I'd use an if statement (num < max) if I had more than two pages, but I don't...
        page = 1
    if mouse_left_click and next_pg_rect2.collidepoint(mouse_pos):
        # I'd use an if statement (num < max) if I had more than two pages, but I don't...
        page = 0

    next_pg_surf1.blit(arrow_text1, (5, -12))
    wn.blit(next_pg_surf1, next_page_pos1)
    next_pg_surf2.blit(arrow_text2, (5, -12))
    wn.blit(next_pg_surf2, next_page_pos2)


def game_over():
    ###VARIABLES###
    global font, fontBIG, replay_instructions, run, loop
    ###GAME OVER?###
    outcome = inBoard.outcome(claim_draw=True)  # claim_draw checks for three-fold-repetition and 50 move rule (draw's)
    if outcome is not None:
        loop = True
        if outcome.termination.value == 1:  # checkmate
            if outcome.winner:
                logging.debug("white won")
                text = fontBIG.render("White won by checkmate", True, (0, 0, 0))
            else:
                logging.debug("black won")
                text = fontBIG.render("Black won by checkmate", True, (0, 0, 0))
        elif outcome.termination.value == 2:  # stalemate
            logging.debug("stalemate")
            text = fontBIG.render("Stalemate", True, (0, 0, 0))
        elif outcome.termination.value == 3:  # stalemate (INSUFFICIENT_MATERIAL)
            logging.debug("stalemate (INSUFFICIENT_MATERIAL)")
            text = fontBIG.render("Stalemate by insufficient material", True, (0, 0, 0))
        elif outcome.termination.value == 4:  # stalemate (SEVENTYFIVE_MOVES)
            logging.debug("stalemate (SEVENTYFIVE_MOVES) (literally how bro??!)")
            text = fontBIG.render("Stalemate by seventy five move rule", True, (0, 0, 0))
        elif outcome.termination.value == 5:  # stalemate (FIVEFOLD_REPETITION)
            logging.debug("# stalemate (FIVEFOLD_REPETITION) (literally how bro??!)")
            text = fontBIG.render("Stalemate by fivefold repetition", True, (0, 0, 0))
        elif outcome.termination.value == 6:  # stalemate (FIFTY_MOVES)
            logging.debug("stalemate (FIFTY_MOVES)")
            text = fontBIG.render("Stalemate by fifty move rule", True, (0, 0, 0))
        elif outcome.termination.value == 7:  # stalemate (THREEFOLD_REPETITION)
            logging.debug("stalemate (THREEFOLD_REPETITION)")
            text = fontBIG.render("Stalemate by threefold repetition", True, (0, 0, 0))
        elif outcome.termination.value == 8:  # variant win
            logging.debug("this is only for standard chess, how did you get a variant win?")
            if outcome.winner:
                logging.debug("white won (variant)")
                text = fontBIG.render("white won", True, (0, 0, 0))
            else:
                logging.debug("black won (variant)")
                text = fontBIG.render("black won", True, (0, 0, 0))
        elif outcome.termination.value == 9:  # variant loss
            logging.debug("this is only for standard chess, how did you get a variant loss?")
            if outcome.winner:
                logging.debug("white lost (variant)")
                text = fontBIG.render("white won", True, (0, 0, 0))
            else:
                logging.debug("black lost (variant)")
                text = fontBIG.render("black won", True, (0, 0, 0))
        elif outcome.termination.value == 10:  # variant draw
            text = fontBIG.render("draw (variant)", True, (0, 0, 0))
        else:
            logging.debug("how the fork did you get here? (game_over function)")
            text = fontBIG.render("idk mann'", True, (0, 0, 0))

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        pygame.quit()
                        sys.exit()
                    else:
                        loop = False
                        reset_variables()
            wn.fill((85, 116, 116))
            text_x = math.sin(time.perf_counter()) * -30
            text_location = text.get_rect(center=(width / 2, text_x + 200))
            text_bg = text.get_size()
            # outcome rect & outline
            pygame.draw.rect(wn, (255, 255, 255),
                             (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                             border_radius=25)
            pygame.draw.rect(wn, (0, 0, 0),
                             (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                             4, border_radius=25)

            # replay instructions
            replay_instructions_location = replay_instructions.get_rect(center=(width/2, height-200))
            wn.blit(replay_instructions, replay_instructions_location)

            wn.blit(text, text_location)
            pygame.display.flip()


def draw():
    ###VARIABLES
    global locations, previous_move_to, previous_move_from, rect_surf_from, rect_surf_to

    ###BOARD###
    for col in range(8):
        for row in range(8):
            if (row + col) % 2 == 0:
                pygame.draw.rect(wn, (180, 180, 180), (col * 100, row * 100, 100, 100))
            else:
                pygame.draw.rect(wn, (124, 124, 124), (col * 100, row * 100, 100, 100))

    ###MOVE GHOST SQUARE###
    if previous_move_from != "" and previous_move_to != "":
        rect_surf_from, rect_surf_to = pygame.Surface((100, 100), pygame.SRCALPHA), pygame.Surface((100, 100),
                                                                                                   pygame.SRCALPHA)
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


def movement():
    global chess_dict, locations, inBoard, previous_move_from, previous_move_to, show_promotion_bar, promotion_move, mouse_button_released, mouse_button_held
    mouse_left_click = pygame.mouse.get_pressed()[0]
    mouse_position = pygame.mouse.get_pos()
    legal_moves = list(inBoard.legal_moves)

    ###MOVING PIECES###
    if mouse_left_click and mouse_button_released and not show_promotion_bar:
        logging.debug("Mouse left click detected")
        mouse_button_released = False
        for square_index, value in chess_dict.items():
            rect = pygame.Rect(value[0], value[1], 100, 100)
            if rect.collidepoint(mouse_position):
                logging.debug(f"Mouse collided with rect {rect}")
                if len(locations) == 0:
                    square_name = chess.square_name(square_index)
                    logging.debug(f"No locations, adding square {square_name}")
                    locations.append(square_name)
                    break
                elif len(locations) == 1:
                    from_square = locations[0]
                    to_square = chess.square_name(square_index)
                    logging.debug(f"1 location, to_square {to_square}")
                    if from_square != to_square:
                        logging.debug("From square different than to square")
                        move = chess.Move.from_uci(f"{from_square}{to_square}")
                        # check for promotions
                        if chess.Move.from_uci(f"{from_square}{to_square}q") in legal_moves:
                            promotion_move = move
                            show_promotion_bar = True
                            locations.append(to_square)
                            logging.debug(f"Promotion move detected: {move}")
                        elif move in legal_moves:
                            logging.debug(f"Legal move {move}")
                            print(move)
                            locations.append(to_square)
                            previous_move_from = chess.parse_square(from_square)
                            previous_move_to = chess.parse_square(to_square)
                            inBoard.push(move)
                            locations = []
                        elif inBoard.piece_at(chess.parse_square(to_square)) is not None:
                            logging.debug("There is a piece already")
                            locations[0] = to_square
                        else:
                            logging.debug("Not a piece but also not legal")
                            locations = []
                    else:
                        logging.debug("Same square")
                        locations = []
                    break
                else:
                    logging.debug(f"promoting (probably (hopefully!))")

    if not mouse_left_click:
        mouse_button_released = True

    ###CIRCLE MOVE HINT###
    if len(locations) == 1:
        from_square = chess.parse_square(locations[0])
        for move in legal_moves:
            if move.from_square == from_square:
                to_square = chess_dict[move.to_square]
                circle_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(circle_surf, (0, 0, 0, 35.7), (50, 50), 20)
                wn.blit(circle_surf, to_square)

    ###PROMOTION###
    if show_promotion_bar and len(locations) == 2:
        to_square = locations[1]
        logging.debug(f"Showing promotion bar at {to_square}")
        promotion_rects = []
        if inBoard.turn:  # True = white, False = black
            promotion_rects.append(
                wn.blit(piece_images_white[chess.QUEEN], (chess_dict[chess.parse_square(to_square)][0], 0)))
            promotion_rects.append(
                wn.blit(piece_images_white[chess.ROOK], (chess_dict[chess.parse_square(to_square)][0], 100)))
            promotion_rects.append(
                wn.blit(piece_images_white[chess.BISHOP], (chess_dict[chess.parse_square(to_square)][0], 200)))
            promotion_rects.append(
                wn.blit(piece_images_white[chess.KNIGHT], (chess_dict[chess.parse_square(to_square)][0], 300)))
        else:
            promotion_rects.append(
                wn.blit(piece_images_black[chess.QUEEN], (chess_dict[chess.parse_square(to_square)][0], 400)))
            promotion_rects.append(
                wn.blit(piece_images_black[chess.ROOK], (chess_dict[chess.parse_square(to_square)][0], 500)))
            promotion_rects.append(
                wn.blit(piece_images_black[chess.BISHOP], (chess_dict[chess.parse_square(to_square)][0], 600)))
            promotion_rects.append(
                wn.blit(piece_images_black[chess.KNIGHT], (chess_dict[chess.parse_square(to_square)][0], 700)))

        if mouse_left_click and mouse_button_released:
            logging.debug(f"Mouse click detected for promotion at {mouse_position}")
            for i, rect in enumerate(promotion_rects):
                if rect.collidepoint(mouse_position):
                    promotion_piece = ['q', 'r', 'b', 'n'][i]
                    move_with_promotion = chess.Move.from_uci(f"{promotion_move.uci()}{promotion_piece}")
                    inBoard.push(move_with_promotion)
                    logging.debug(f"Promotion to {promotion_piece}")
                    previous_move_from = promotion_move.from_square
                    previous_move_to = promotion_move.to_square
                    show_promotion_bar = False
                    locations = []
                    mouse_button_released = False
                    break


def paste_pos():
    global inBoard, previous_move_from, previous_move_to
    color = (109, 131, 137)
    left_click = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    button_text = "PASTE BOARD FEN"

    paste_pos = (800, 0)
    paste_surf = pygame.Surface((400, 150), pygame.SRCALPHA)
    paste_rect = paste_surf.get_rect(topleft=paste_pos)

    if paste_rect.collidepoint(mouse_pos):
        color = (67, 101, 90)
        if left_click:
            try:
                inBoard = chess.Board(pyperclip.paste())
                button_text = "DONE"
                previous_move_from, previous_move_to = "", ""
            except ValueError:
                button_text = "INVALID"

    paste_surf.fill((255, 0, 255, 0))
    pygame.draw.rect(paste_surf, color, (0, 0, 400, 150), border_radius=25)
    pygame.draw.rect(paste_surf, (0, 0, 0), (0, 0, 400, 150), 8, border_radius=25)

    button_prompt = font.render(button_text, True, (255, 255, 255))
    text_rect = button_prompt.get_rect(center=(paste_surf.get_width() // 2, paste_surf.get_height() // 2))

    paste_surf.blit(button_prompt, text_rect.topleft)
    wn.blit(paste_surf, paste_pos)


def copy_pos():
    color = (109, 131, 137)
    left_click = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    button_text = "COPY BOARD FEN"

    paste_pos = (800, 162.5)
    paste_surf = pygame.Surface((400, 150), pygame.SRCALPHA)
    paste_rect = paste_surf.get_rect(topleft=paste_pos)

    if paste_rect.collidepoint(mouse_pos):
        color = (67, 101, 90)
        if left_click:
            pyperclip.copy(inBoard.fen())
            button_text = "COPIED"

    paste_surf.fill((255, 0, 255, 0))
    pygame.draw.rect(paste_surf, color, (0, 0, 400, 150), border_radius=25)
    pygame.draw.rect(paste_surf, (0, 0, 0), (0, 0, 400, 150), 8, border_radius=25)

    button_prompt = font.render(button_text, True, (255, 255, 255))
    text_rect = button_prompt.get_rect(center=(paste_surf.get_width() // 2, paste_surf.get_height() // 2))
    paste_surf.blit(button_prompt, text_rect.topleft)
    wn.blit(paste_surf, paste_pos)


def reset_board():
    global inBoard, previous_move_from, previous_move_to

    color = (109, 131, 137)
    left_click = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    button_text = "RESET BOARD"

    reset_pos = (800, 325)
    reset_surf = pygame.Surface((400, 150), pygame.SRCALPHA)
    reset_rect = reset_surf.get_rect(topleft=reset_pos)

    if reset_rect.collidepoint(mouse_pos):
        color = (67, 101, 90)
        if left_click:
            inBoard = chess.Board()
            button_text = "DONE"
            previous_move_from, previous_move_to = "", ""

    reset_surf.fill((255, 0, 255, 0))
    pygame.draw.rect(reset_surf, color, (0, 0, 400, 150), border_radius=25)
    pygame.draw.rect(reset_surf, (0, 0, 0), (0, 0, 400, 150), 8, border_radius=25)

    button_prompt = font.render(button_text, True, (255, 255, 255))
    text_rect = button_prompt.get_rect(center=(reset_surf.get_width() // 2, reset_surf.get_height() // 2))

    reset_surf.blit(button_prompt, text_rect.topleft)
    wn.blit(reset_surf, reset_pos)


def resign_white():
    global run

    color = (109, 131, 137)
    left_click = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    button_text = "WHITE RESIGN"

    resign_pos = (800, 487.5)
    resign_surf = pygame.Surface((400, 150), pygame.SRCALPHA)
    resign_rect = resign_surf.get_rect(topleft=resign_pos)

    if resign_rect.collidepoint(mouse_pos):
        color = (67, 101, 90)
        if left_click:
            button_text = "done"
            loop = True
            while loop:
                text = fontBIG.render("Black wins!", True, (0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            pygame.quit()
                            sys.exit()
                        else:
                            reset_variables()
                            loop = False
                            run = True
                wn.fill((85, 116, 116))
                text_x = math.sin(time.perf_counter()) * -30
                text_location = text.get_rect(center=(width / 2, text_x + 200))
                text_bg = text.get_size()
                # outcome rect & outline
                pygame.draw.rect(wn, (255, 255, 255),
                                 (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                                 border_radius=25)
                pygame.draw.rect(wn, (0, 0, 0),
                                 (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                                 4, border_radius=25)

                # replay instructions
                replay_instructions_location = replay_instructions.get_rect(center=(width / 2, height - 200))
                wn.blit(replay_instructions, replay_instructions_location)

                wn.blit(text, text_location)
                pygame.display.flip()

    resign_surf.fill((255, 0, 255, 0))
    pygame.draw.rect(resign_surf, color, (0, 0, 400, 150), border_radius=25)
    pygame.draw.rect(resign_surf, (0, 0, 0), (0, 0, 400, 150), 8, border_radius=25)
    button_prompt = font.render(button_text, True, (255, 255, 255))
    text_rect = button_prompt.get_rect(center=(resign_surf.get_width() // 2, resign_surf.get_height() // 2))

    resign_surf.blit(button_prompt, text_rect.topleft)
    wn.blit(resign_surf, resign_pos)


def resign_black():
    global run

    color = (109, 131, 137)
    left_click = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    button_text = "BLACK RESIGN"

    resign_pos = (800, 650)
    resign_surf = pygame.Surface((400, 150), pygame.SRCALPHA)
    resign_rect = resign_surf.get_rect(topleft=resign_pos)

    if resign_rect.collidepoint(mouse_pos):
        color = (67, 101, 90)
        if left_click:
            button_text = "done"
            loop = True
            while loop:
                text = fontBIG.render("White wins!", True, (0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            pygame.quit()
                            sys.exit()
                        else:
                            reset_variables()
                            loop = False
                            run = True
                wn.fill((85, 116, 116))
                text_x = math.sin(time.perf_counter()) * -30
                text_location = text.get_rect(center=(width / 2, text_x + 200))
                text_bg = text.get_size()
                # outcome rect & outline
                pygame.draw.rect(wn, (255, 255, 255),
                                 (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                                 border_radius=25)
                pygame.draw.rect(wn, (0, 0, 0),
                                 (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                                 4, border_radius=25)

                # replay instructions
                replay_instructions_location = replay_instructions.get_rect(center=(width / 2, height - 200))
                wn.blit(replay_instructions, replay_instructions_location)

                wn.blit(text, text_location)
                pygame.display.flip()


    resign_surf.fill((255, 0, 255, 0))
    pygame.draw.rect(resign_surf, color, (0, 0, 400, 150), border_radius=25)
    pygame.draw.rect(resign_surf, (0, 0, 0), (0, 0, 400, 150), 8, border_radius=25)

    button_prompt = font.render(button_text, True, (255, 255, 255))
    text_rect = button_prompt.get_rect(center=(resign_surf.get_width() // 2, resign_surf.get_height() // 2))

    resign_surf.blit(button_prompt, text_rect.topleft)
    wn.blit(resign_surf, resign_pos)


def game_credits():
    global game_title, return_instructions, game_credits_text, run

    color = (109, 131, 137)
    left_click = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    button_text = "Credits"
    font = pygame.font.Font(None, 36)  # Adjust the font initialization if needed
    width, height = 1200, 800  # Adjust the screen size if needed

    credit_pos = (800, 0)
    credit_surf = pygame.Surface((400, 150), pygame.SRCALPHA)
    credit_rect = credit_surf.get_rect(topleft=credit_pos)

    if credit_rect.collidepoint(mouse_pos):
        color = (67, 101, 90)
        if left_click:
            loop = True
            while loop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            pygame.quit()
                            sys.exit()
                        else:
                            reset_variables()  # Ensure this function is defined
                            loop = False
                            run = True

                wn.fill((85, 116, 116))
                text_x = math.sin(time.perf_counter()) * -30

                text_location = game_title.get_rect(center=(width / 2, text_x + 200))
                credit_location = game_credits_text.get_rect(center=(width / 2, text_x + 400))
                credit_bg = game_credits_text.get_size()
                text_bg = game_title.get_size()

                pygame.draw.rect(wn, (255, 255, 255),
                                 (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                                 border_radius=25)
                pygame.draw.rect(wn, (0, 0, 0),
                                 (text_location[0] - 25, text_location[1] - 25, text_bg[0] + 50, text_bg[1] + 50),
                                 4, border_radius=25)

                pygame.draw.rect(wn, (255, 255, 255),
                                 (credit_location[0] - 25, credit_location[1] - 25, credit_bg[0] + 50,
                                  credit_bg[1] + 50),
                                 border_radius=25)
                pygame.draw.rect(wn, (0, 0, 0),
                                 (credit_location[0] - 25, credit_location[1] - 25, credit_bg[0] + 50,
                                  credit_bg[1] + 50),
                                 4, border_radius=25)

                replay_instructions_location = return_instructions.get_rect(center=(width / 2, height - 100))
                wn.blit(return_instructions, replay_instructions_location)

                wn.blit(game_title, text_location)
                wn.blit(game_credits_text, credit_location)
                pygame.display.flip()

    credit_surf.fill((255, 0, 255, 0))
    pygame.draw.rect(credit_surf, color, (0, 0, 400, 150), border_radius=25)
    pygame.draw.rect(credit_surf, (0, 0, 0), (0, 0, 400, 150), 8, border_radius=25)

    button_prompt = fontBIG.render(button_text, True, (255, 255, 255))
    text_rect = button_prompt.get_rect(center=(credit_surf.get_width() // 2, credit_surf.get_height() // 2))

    credit_surf.blit(button_prompt, text_rect.topleft)
    wn.blit(credit_surf, credit_pos)


while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button_released = True
    wn.fill((85, 116, 116))
    game_over()
    draw()
    movement()
    if page == 0:
        paste_pos()
        copy_pos()
        reset_board()
        resign_white()
        resign_black()
    elif page == 1:
        game_credits()
    switch_page()

    pygame.display.flip()

print(inBoard.fen())
pygame.quit()
sys.exit()
