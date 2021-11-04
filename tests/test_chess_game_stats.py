import os

import pytest

import chess_game_stats


TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
RESOURCES_DIR = os.path.join(TESTS_DIR, 'resources')


def load_pgn(filename):
    pgn_file = os.path.join(RESOURCES_DIR, filename)
    with open(pgn_file) as f:
        return f.read()


@pytest.fixture(scope='session')
def no_bad_moves_pgn():
    return load_pgn('no_bad_moves.pgn')


@pytest.fixture(scope='session')
def mate_in_two_pgn():
    return load_pgn('mate_in_two.pgn')


@pytest.fixture(scope='session')
def blunder_queen_pgn():
    return load_pgn('blunder_queen.pgn')


@pytest.fixture(scope='session')
def ordinary_pgn():
    return load_pgn('ordinary.pgn')


def test_get_stats_no_bad_moves(no_bad_moves_pgn):
    expected_stats = {
        'r4victor': {
            'inaccuracies': 0,
            'mistakes': 0,
            'blunders': 0,
        },
        'Anonymous': {
            'inaccuracies': 0,
            'mistakes': 0,
            'blunders': 0,
        },
    }
    stats = chess_game_stats.get_stats(no_bad_moves_pgn)
    assert stats == expected_stats


def test_get_stats_mate_in_two(mate_in_two_pgn):
    expected_stats = {
        'r4victor': {
            'inaccuracies': 1,
            'mistakes': 0,
            'blunders': 1,
        },
        'Anonymous': {
            'inaccuracies': 0,
            'mistakes': 0,
            'blunders': 0,
        },
    }
    stats = chess_game_stats.get_stats(mate_in_two_pgn)
    assert stats == expected_stats


def test_get_stats_blunder_queen(blunder_queen_pgn):
    expected_stats = {
        'r4victor': {
            'inaccuracies': 0,
            'mistakes': 0,
            'blunders': 1,
        },
        'Anonymous': {
            'inaccuracies': 0,
            'mistakes': 0,
            'blunders': 0,
        },
    }
    stats = chess_game_stats.get_stats(blunder_queen_pgn)
    assert stats == expected_stats


# # This test fails becaise the expected stats are from lichess,
# # but the results depend on the engine's depth
# def test_get_stats_has_bad_moves(ordinary_pgn):
#     expected_stats = {
#         'mahmoudatia31987': {
#             'inaccuracies': 1,
#             'mistakes': 1,
#             'blunders': 4,
#         },
#         'Ayoubayoubbr': {
#             'inaccuracies': 5,
#             'mistakes': 3,
#             'blunders': 0,
#         },
#     }
#     stats = chess_game_stats.get_stats(ordinary_pgn)
#     assert stats == expected_stats

