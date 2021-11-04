import io
import sys
import math

import chess.pgn
from stockfish import Stockfish


def get_stats(game_description, engine_depth=10):
    """
    Takes a chess game in the PGN format and returns a dictionary
    containing the number of blunders, mistakes, and inaccuracies
    made by each player.

    Input:

    `game_description` – a string representing game in PGN
    
    `engine_depth` – an int that controls the engine's depth parameter

    Output:

    A dict of the form: {
        'white player name': {
            'inaccuracies': 4,
            'mistakes': 2,
            'blunders': 1,
        },
        'black player name': {
            'inaccuracies': 1,
            'mistakes': 2,
            'blunders': 0,
        },
    }
    """
    text_io = io.StringIO(game_description)
    game = chess.pgn.read_game(text_io)
    white_name, black_name = _get_players_names(game)
    moves = _get_moves(game)
    return _get_stats(white_name, black_name, moves, engine_depth)


def _get_players_names(game):
    return game.headers['White'], game.headers['Black']


def _get_moves(game):
    return [m.uci() for m in game.mainline_moves()]


def _get_stats(white_name, black_name, moves, engine_depth):
    engine = Stockfish(depth=engine_depth)
    stats = _init_stats()
    for i in range(1, len(moves) + 1):
        moves_history = moves[:i]
        _update_stats_on_move(stats, engine, moves_history)
    stats = _fix_names(stats, white_name, black_name)
    return stats


def _init_stats():
    return {
        'white': {
            'inaccuracies': 0,
            'mistakes': 0,
            'blunders': 0,
        },
        'black': {
            'inaccuracies': 0,
            'mistakes': 0,
            'blunders': 0,
        },
    }


def _update_stats_on_move(stats, engine, moves_history):
    engine.set_position(moves_history[:-1])
    prev_score = engine.get_evaluation()

    engine.set_position(moves_history)
    move_score = engine.get_evaluation()
    
    color = _whose_move(moves_history)

    move_type = _get_move_type(prev_score, move_score, color)
    if move_type is not None:
        stats[color][move_type] += 1
    

def _whose_move(moves_history):
    return 'white' if len(moves_history) % 2 == 1 else 'black'


def _get_move_type(prev_score, move_score, color):
    """
    Classify move as a blunder, mistake, or inaccuracy.
    There is no consensus on the classification, so do what lichess does:
    https://github.com/ornicar/lila/blob/master/modules/analyse/src/main/Advice.scala
    """
    if prev_score['type'] == 'mate':
        return None
    if move_score['type'] == 'mate':
        return 'blunders'
    
    prev_cp = prev_score['value']
    move_cp = move_score['value']

    prev_win_chances = _get_winning_chances(prev_cp)
    move_win_chances = _get_winning_chances(move_cp)

    delta = prev_win_chances - move_win_chances

    if color == 'black':
        delta *= -1
    
    if delta >= 0.3:
        return 'blunders'
    elif delta >= 0.2:
        return 'mistakes'
    elif delta >= 0.1:
        return 'inaccuracies'

    return None


def _get_winning_chances(cp):
    return 2 / (1 + math.exp(-0.004 * cp)) - 1


def _fix_names(stats, white_name, black_name):
    return {
        white_name: stats['white'],
        black_name: stats['black']
    }


if __name__ == '__main__':
    game_description = sys.stdin.read()
    stats = get_stats(game_description)
    print(stats)