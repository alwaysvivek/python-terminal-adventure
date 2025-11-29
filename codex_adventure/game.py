"""
codex_adventure.game

This module contains the Game class that encapsulates the game state and logic
for the Lost Scroll of Eldoria adventure game.

This is a Codédex checkpoint project refactored into a testable package.
"""

import random
import time
from typing import Any, Callable, Optional, Protocol, Tuple


class RNGProtocol(Protocol):
    """Protocol for random number generators used by the Game class."""
    def randint(self, a: int, b: int) -> int:
        """Return a random integer N such that a <= N <= b."""
        ...


class DefaultRNG:
    """Default RNG that wraps Python's random module."""
    def randint(self, a: int, b: int) -> int:
        return random.randint(a, b)


class Game:
    """
    Encapsulates the game state and logic for the Lost Scroll of Eldoria.

    Attributes:
        player_hp (int): The player's current health points.
        player_name (str): The player's name.
        has_key (bool): Whether the player has the rusty key.
        has_potion (bool): Whether the player has a healing potion.
        game_over (bool): Whether the game has ended.
        guardian_hp (int): The guardian's health points.

    Args:
        sleep (float): Duration in seconds to sleep for dramatic pauses.
                       Set to 0 for testing.
        rng: An object with a randint(a, b) method for random number generation.
             Defaults to DefaultRNG which wraps Python's random module.
    """

    def __init__(self, sleep: float = 1.0, rng: Optional[RNGProtocol] = None):
        """Initialize the game with optional sleep duration and RNG."""
        self._sleep_duration = sleep
        self._rng = rng if rng is not None else DefaultRNG()
        self.reset()

    def reset(self) -> None:
        """Reset the game state to initial values."""
        self.player_hp: int = 100
        self.player_name: str = ""
        self.has_key: bool = False
        self.has_potion: bool = True  # Player starts with one healing potion
        self.game_over: bool = False
        self.guardian_hp: int = 50

    def _sleep(self, duration: Optional[float] = None) -> None:
        """Sleep for the specified duration or the default duration."""
        time.sleep(duration if duration is not None else self._sleep_duration)

    def _randint(self, a: int, b: int) -> int:
        """Return a random integer N such that a <= N <= b."""
        return self._rng.randint(a, b)

    def use_potion(self) -> Tuple[bool, int]:
        """
        Use a healing potion if available.

        Returns:
            Tuple of (success: bool, heal_amount: int).
            If no potion available, returns (False, 0).
        """
        if not self.has_potion:
            return (False, 0)

        heal_amount = self._randint(20, 40)
        self.player_hp += heal_amount
        if self.player_hp > 100:
            self.player_hp = 100  # Cap health at 100
        self.has_potion = False
        return (True, heal_amount)

    def enter_eastern_path(self) -> Tuple[str, int]:
        """
        Enter the eastern path and handle trap/key events.

        Returns:
            Tuple of (event: str, damage_or_zero: int).
            event is one of: "trap", "safe", "safe_key_found"
        """
        event_chance = self._randint(1, 100)

        if event_chance > 40:  # 60% chance of a trap
            damage = self._randint(15, 30)
            self.player_hp -= damage
            return ("trap", damage)
        else:
            # Safe navigation - chance to find a key
            if not self.has_key:
                if self._randint(1, 3) == 1:
                    self.has_key = True
                    return ("safe_key_found", 0)
            return ("safe", 0)

    def investigate_cave(self) -> str:
        """
        Investigate the cave and attempt to open the chest.

        Returns:
            One of: "no_key", "chest_empty", "chest_potion"
        """
        if not self.has_key:
            return "no_key"

        if not self.has_potion:
            self.has_potion = True
            return "chest_potion"
        else:
            return "chest_empty"

    def enter_western_path(self) -> Tuple[str, bool]:
        """
        Enter the western path.

        Returns:
            Tuple of (path_taken: str, key_found: bool).
            path_taken is always "western".
        """
        # Check for key while crossing stream
        key_found = False
        if self._randint(1, 4) == 1 and not self.has_key:
            self.has_key = True
            key_found = True
        return ("western", key_found)

    def drink_from_stream(self) -> int:
        """
        Drink from the stream to restore health.

        Returns:
            The amount of health restored.
        """
        healing = self._randint(5, 15)
        self.player_hp += healing
        return healing

    def battle_guardian_once(self) -> Tuple[str, int, int]:
        """
        Attack the guardian once in battle.

        Returns:
            Tuple of (result: str, player_attack: int, guardian_attack: int).
            result is one of: "guardian_defeated", "guardian_retaliates"
        """
        player_attack = self._randint(10, 25)
        self.guardian_hp -= player_attack

        if self.guardian_hp <= 0:
            return ("guardian_defeated", player_attack, 0)

        guardian_attack = self._randint(10, 20)
        self.player_hp -= guardian_attack
        return ("guardian_retaliates", player_attack, guardian_attack)

    def attempt_sneak(self) -> Tuple[bool, int]:
        """
        Attempt to sneak past the guardian.

        Returns:
            Tuple of (success: bool, damage_if_failed: int).
        """
        sneak_chance = self._randint(1, 100)
        if sneak_chance > 70:  # 30% chance to sneak
            return (True, 0)
        else:
            damage = self._randint(20, 35)
            self.player_hp -= damage
            return (False, damage)

    def run_cli(self) -> None:
        """
        Run the interactive command-line interface for the game.

        This method handles all user input and game flow.
        """
        print("Welcome, brave adventurer, to the Lost Scroll of Eldoria!")
        print("Your quest is to retrieve the ancient scroll hidden deep within the Whispering Ruins.")
        self.player_name = input("First, tell us your name: ")
        print(f"\nGreetings, {self.player_name}. May your courage guide you!\n")
        self._sleep()

        while not self.game_over and self.player_hp > 0:
            print("-" * 50)
            print(f"Current Health: {self.player_hp} HP")
            if self.has_potion:
                print("You have a healing potion.")
            else:
                print("You have no healing potions left.")
            print("-" * 50)
            self._sleep()

            print("\nYou stand at the entrance of the Whispering Ruins. Two paths diverge.")
            print("1. Enter the overgrown Eastern Path (might be dangerous but shorter).")
            print("2. Take the winding Western Path (longer but potentially safer).")

            choice1 = input("What do you do? (1 or 2): ")

            if choice1 == '1':
                print("\nYou venture into the Eastern Path. Thorns scratch at your armor, and strange whispers echo.")
                self._sleep(2 * self._sleep_duration)

                event, damage = self.enter_eastern_path()

                if event == "trap":
                    print("Suddenly, a tripwire snags your leg! It's a hidden trap!")
                    print(f"You take {damage} damage. Current HP: {self.player_hp}.")
                    if self.player_hp <= 0:
                        break
                    self._sleep()
                    print("You managed to disarm the trap, but it cost you.")
                elif event == "safe_key_found":
                    print("You carefully navigate the path, avoiding any traps. Good job!")
                    print("You notice a glinting object hidden in the foliage. It's a rusty key!")
                    self._sleep()
                else:
                    print("You carefully navigate the path, avoiding any traps. Good job!")

                print("\nFurther down the path, you see a flickering light from a small cave.")
                print("1. Investigate the cave.")
                print("2. Continue on the main path.")

                choice2 = input("What do you do? (1 or 2): ")

                if choice2 == '1':
                    print("\nYou cautiously approach the cave. Inside, you find a chest!")
                    self._sleep()

                    result = self.investigate_cave()
                    if result == "no_key":
                        print("The chest is locked. You need a key.")
                    elif result == "chest_potion":
                        print("You use the rusty key and open the chest!")
                        print("Inside, you find a shimmering healing potion!")
                    else:  # chest_empty
                        print("You use the rusty key and open the chest!")
                        print("The chest is empty except for some ancient dust.")
                else:
                    print("You decide to stick to the main path, wary of hidden dangers.")

            elif choice1 == '2':
                print("\nYou choose the winding Western Path. It's quieter here, but the journey feels longer.")
                self._sleep(2 * self._sleep_duration)
                print("After a while, you come across a peaceful stream.")
                print("1. Drink from the stream (might restore some health).")
                print("2. Cross the stream and continue.")

                choice2_western = input("What do you do? (1 or 2): ")

                if choice2_western == '1':
                    print("\nYou cup your hands and drink the cool, refreshing water.")
                    healing = self.drink_from_stream()
                    print(f"You restore {healing} HP. Current HP: {self.player_hp}.")
                else:
                    print("You quickly cross the stream, eager to continue your journey.")

                _, key_found = self.enter_western_path()
                if key_found:
                    print("While crossing, your foot nudges a loose stone, revealing a hidden compartment. You find a shiny silver key!")
                    self._sleep()

            else:
                print("Invalid choice. You stand confused for a moment, losing precious time.")
                self._sleep()
                continue

            # Mid-point check and challenge
            print("\nRegardless of your path, you now stand before the Guardian's Chamber.")
            print("A gargoyle-like creature awakens, blocking your way to the inner sanctum!")
            print(f"Guardian HP: {self.guardian_hp}")

            while self.player_hp > 0 and not self.game_over:
                print(f"\nYour HP: {self.player_hp} | Guardian HP: {self.guardian_hp} (approx.)")
                print("1. Attack the Guardian.")
                print("2. Try to sneak past.")
                if self.has_potion:
                    print("3. Use a healing potion.")

                battle_choice = input("What do you do? (1, 2, or 3 if available): ")

                if battle_choice == '1':
                    result, player_atk, guardian_atk = self.battle_guardian_once()
                    print(f"You strike the Guardian for {player_atk} damage!")

                    if result == "guardian_defeated":
                        print("The Guardian crumbles to dust! You defeated it!")
                        self.game_over = True
                        break
                    else:
                        print("The Guardian growls, still standing!")
                        print(f"The Guardian retaliates, hitting you for {guardian_atk} damage!")
                        self._sleep()

                elif battle_choice == '2':
                    print("You attempt to sneak past the enraged Guardian...")
                    self._sleep()
                    success, damage = self.attempt_sneak()

                    if success:
                        print("You successfully slip past the Guardian!")
                        self.game_over = True
                        break
                    else:
                        print("The Guardian spots you and unleashes a furious roar!")
                        print(f"You take {damage} damage. Current HP: {self.player_hp}!")
                        self._sleep()

                elif battle_choice == '3' and self.has_potion:
                    print("You quickly drink your healing potion!")
                    success, heal_amount = self.use_potion()
                    print(f"You recover {heal_amount} HP. Current HP: {self.player_hp}.")
                    self._sleep()

                elif battle_choice == '3' and not self.has_potion:
                    print("You try to use a potion, but you don't have any left!")

                else:
                    print("Invalid battle choice. You hesitate, losing your advantage!")
                    guardian_attack = self._randint(5, 15)
                    self.player_hp -= guardian_attack
                    print(f"The Guardian takes advantage, hitting you for {guardian_attack} damage!")
                    self._sleep()

                if self.player_hp <= 0:
                    print("\nYour vision blurs, and you collapse. The quest ends here.")
                    self.game_over = True
                    break

            if self.game_over and self.player_hp > 0:
                print("\nWith the Guardian defeated (or bypassed), you enter the inner sanctum.")
                print("There, resting on a pedestal, is the glowing Lost Scroll of Eldoria!")
                print(f"Congratulations, {self.player_name}! You have completed your adventure and claimed the scroll!")

            elif self.player_hp <= 0:
                print("\nGAME OVER.")
                print("Your adventure in the Whispering Ruins has come to an end.")

        print("\nThanks for playing!")
