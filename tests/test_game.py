"""
tests/test_game.py

Unit tests for the codex_adventure.Game class.
Uses a SeqRNG (sequence-returning RNG) for deterministic testing.
"""

import pytest
from codex_adventure import Game


class SeqRNG:
    """
    A sequence-returning RNG for deterministic testing.
    
    Returns values from the provided sequence in order, cycling if necessary.
    """
    
    def __init__(self, values: list[int]):
        """Initialize with a list of values to return."""
        self._values = values
        self._index = 0
    
    def randint(self, a: int, b: int) -> int:
        """Return the next value from the sequence."""
        value = self._values[self._index % len(self._values)]
        self._index += 1
        return value


class TestUsePotion:
    """Tests for the use_potion method."""
    
    def test_use_potion_heals_and_caps(self):
        """Test that potion heals player and caps HP at 100."""
        # SeqRNG will return 40 for heal amount
        rng = SeqRNG([40])
        game = Game(sleep=0, rng=rng)
        
        # Set HP to 80 - healing 40 should cap at 100
        game.player_hp = 80
        game.has_potion = True
        
        success, heal_amount = game.use_potion()
        
        assert success is True
        assert heal_amount == 40
        assert game.player_hp == 100  # Capped at 100, not 120
        assert game.has_potion is False
    
    def test_use_potion_no_potion(self):
        """Test that using potion fails when player has none."""
        rng = SeqRNG([40])
        game = Game(sleep=0, rng=rng)
        game.has_potion = False
        
        success, heal_amount = game.use_potion()
        
        assert success is False
        assert heal_amount == 0


class TestEasternPath:
    """Tests for the eastern path events."""
    
    def test_trap_damage_bounds(self):
        """Test that trap damage is within expected bounds."""
        # First value > 40 triggers trap, second value is damage
        rng = SeqRNG([50, 20])  # 50 > 40 triggers trap, damage = 20
        game = Game(sleep=0, rng=rng)
        
        event, damage = game.enter_eastern_path()
        
        assert event == "trap"
        assert 15 <= damage <= 30
        assert game.player_hp == 80  # 100 - 20
    
    def test_find_key_on_east_path(self):
        """Test finding key on eastern path when avoiding trap."""
        # First value <= 40 avoids trap, second value == 1 finds key
        rng = SeqRNG([40, 1])  # 40 <= 40 avoids trap, 1 finds key
        game = Game(sleep=0, rng=rng)
        game.has_key = False
        
        event, damage = game.enter_eastern_path()
        
        assert event == "safe_key_found"
        assert damage == 0
        assert game.has_key is True
    
    def test_safe_no_key(self):
        """Test safe passage without finding key."""
        # First value <= 40 avoids trap, second value != 1 no key
        rng = SeqRNG([40, 2])  # 40 <= 40 avoids trap, 2 != 1 no key
        game = Game(sleep=0, rng=rng)
        game.has_key = False
        
        event, damage = game.enter_eastern_path()
        
        assert event == "safe"
        assert damage == 0
        assert game.has_key is False


class TestWesternPath:
    """Tests for the western path events."""
    
    def test_drink_stream_heals(self):
        """Test that drinking from stream restores health."""
        rng = SeqRNG([10])  # Will heal 10 HP
        game = Game(sleep=0, rng=rng)
        game.player_hp = 90
        
        healing = game.drink_from_stream()
        
        assert healing == 10
        assert game.player_hp == 100


class TestGuardianBattle:
    """Tests for guardian battle mechanics."""
    
    def test_battle_guardian_down_by_attack(self):
        """Test defeating the guardian with a powerful attack."""
        # Attack deals 25 damage, enough to defeat guardian at 25 HP
        rng = SeqRNG([25])
        game = Game(sleep=0, rng=rng)
        game.guardian_hp = 25
        
        result, player_atk, guardian_atk = game.battle_guardian_once()
        
        assert result == "guardian_defeated"
        assert player_atk == 25
        assert guardian_atk == 0
        assert game.guardian_hp == 0
    
    def test_battle_guardian_retaliates(self):
        """Test guardian retaliation when not defeated."""
        # Player attacks for 10, guardian retaliates for 15
        rng = SeqRNG([10, 15])
        game = Game(sleep=0, rng=rng)
        game.guardian_hp = 50
        
        result, player_atk, guardian_atk = game.battle_guardian_once()
        
        assert result == "guardian_retaliates"
        assert player_atk == 10
        assert guardian_atk == 15
        assert game.guardian_hp == 40
        assert game.player_hp == 85


class TestSneak:
    """Tests for sneak mechanics."""
    
    def test_attempt_sneak_success_and_fail(self):
        """Test sneak attempt success and failure."""
        # Test successful sneak (value > 70)
        rng_success = SeqRNG([71])
        game_success = Game(sleep=0, rng=rng_success)
        
        success, damage = game_success.attempt_sneak()
        
        assert success is True
        assert damage == 0
        
        # Test failed sneak (value <= 70)
        rng_fail = SeqRNG([70, 25])  # 70 <= 70 fails, 25 damage
        game_fail = Game(sleep=0, rng=rng_fail)
        
        success, damage = game_fail.attempt_sneak()
        
        assert success is False
        assert damage == 25
        assert game_fail.player_hp == 75  # 100 - 25


class TestInvestigateCave:
    """Tests for cave investigation."""
    
    def test_investigate_cave_no_key(self):
        """Test investigating cave without a key."""
        game = Game(sleep=0)
        game.has_key = False
        
        result = game.investigate_cave()
        
        assert result == "no_key"
    
    def test_investigate_cave_get_potion(self):
        """Test getting potion from chest."""
        game = Game(sleep=0)
        game.has_key = True
        game.has_potion = False
        
        result = game.investigate_cave()
        
        assert result == "chest_potion"
        assert game.has_potion is True
    
    def test_investigate_cave_empty(self):
        """Test finding empty chest when already have potion."""
        game = Game(sleep=0)
        game.has_key = True
        game.has_potion = True
        
        result = game.investigate_cave()
        
        assert result == "chest_empty"


class TestReset:
    """Tests for game reset functionality."""
    
    def test_reset_restores_initial_state(self):
        """Test that reset restores all initial values."""
        game = Game(sleep=0)
        
        # Modify state
        game.player_hp = 50
        game.player_name = "Test"
        game.has_key = True
        game.has_potion = False
        game.game_over = True
        game.guardian_hp = 10
        
        game.reset()
        
        assert game.player_hp == 100
        assert game.player_name == ""
        assert game.has_key is False
        assert game.has_potion is True
        assert game.game_over is False
        assert game.guardian_hp == 50
