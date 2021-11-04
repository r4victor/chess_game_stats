# chess_game_stats

## Overview

`chess_game_stats` is a Python library/CLI tool that takes a description of a chess game in the PGN format and returns the number of blunders, mistakes, and inaccuracies made by each player in the game.

## Requirements

1. Python >= 3.6
2. [stockfish](https://stockfishchess.org/)
3. Python packages: `python-chess`, `stockfish`.

## Usage

To use `chess_game_stats` as a library, pass the PGN description to the `get_stats()` function.

```python
stats = get_stats(game_in_pgn)
```

Returned `stats` is a dict in the following format:

```
{
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
```

To use `chess_game_stats` as a CLI tool, pass the PGN description to the stdin:

```
cat game.pgn | python chess_game_stats.py
```
