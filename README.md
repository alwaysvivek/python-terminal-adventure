# python-terminal-adventure

A text-based adventure game: **The Lost Scroll of Eldoria**

This is a **Codédex checkpoint project** that has been refactored into a testable Python package.

## Overview

Embark on an adventure through the Whispering Ruins to retrieve the ancient Lost Scroll of Eldoria. Navigate treacherous paths, avoid traps, battle guardians, and make choices that determine your fate!

## Project Structure

```
python-terminal-adventure/
├── codex_adventure/         # Game package
│   ├── __init__.py          # Package exports
│   └── game.py              # Game class with all logic
├── tests/                   # Unit tests
│   └── test_game.py         # pytest tests with deterministic RNG
├── terminal_game.py         # CLI entry point
├── README.md
└── LICENSE
```

## Running the Game

To play the interactive adventure game:

```bash
python3 terminal_game.py
```

## Running Tests

This project uses [pytest](https://pytest.org/) for testing. To run the tests:

```bash
# Install pytest if needed
pip install pytest

# Run all tests
pytest -q

# Run with verbose output
pytest -v
```

## Development

### Testable Design

The game logic has been refactored into the `codex_adventure.Game` class with:

- **Injectable RNG**: Pass a custom RNG with a `randint(a, b)` method for deterministic testing
- **Zero-sleep mode**: Set `sleep=0` to disable delays in tests
- **Modular methods**: Each game action is a separate method that can be unit tested

### Example Test Usage

```python
from codex_adventure import Game

class SeqRNG:
    """Returns values from a sequence for deterministic tests."""
    def __init__(self, values):
        self._values = values
        self._index = 0
    
    def randint(self, a, b):
        value = self._values[self._index % len(self._values)]
        self._index += 1
        return value

# Create game with deterministic RNG
rng = SeqRNG([40])  # Will return 40 for heal amount
game = Game(sleep=0, rng=rng)

# Test potion use
success, heal = game.use_potion()
assert success and heal == 40
```

## Next Steps

- Add CI workflow to run pytest on push
- Add more comprehensive test coverage
- Consider adding save/load game functionality

## License

See [LICENSE](LICENSE) for details.