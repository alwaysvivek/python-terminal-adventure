import random
import time # Used to simulate a pause for better readability

# --- Game Variables ---
player_hp = 100
player_name = ""
has_key = False
has_potion = True # Player starts with one healing potion
game_over = False

# --- Game Start ---
print("Welcome, brave adventurer, to the Lost Scroll of Eldoria!")
print("Your quest is to retrieve the ancient scroll hidden deep within the Whispering Ruins.")
player_name = input("First, tell us your name: ")
print(f"\nGreetings, {player_name}. May your courage guide you!\n")
time.sleep(1)

# --- Game Loop ---
while not game_over and player_hp > 0:
    print(f"--------------------------------------------------")
    print(f"Current Health: {player_hp} HP")
    if has_potion:
        print("You have a healing potion.")
    else:
        print("You have no healing potions left.")
    print(f"--------------------------------------------------")
    time.sleep(1)

    print("\nYou stand at the entrance of the Whispering Ruins. Two paths diverge.")
    print("1. Enter the overgrown Eastern Path (might be dangerous but shorter).")
    print("2. Take the winding Western Path (longer but potentially safer).")
    
    choice1 = input("What do you do? (1 or 2): ")

    if choice1 == '1':
        print("\nYou venture into the Eastern Path. Thorns scratch at your armor, and strange whispers echo.")
        time.sleep(2)
        event_chance = random.randint(1, 100)
        
        if event_chance > 40: # 60% chance of a trap
            print("Suddenly, a tripwire snags your leg! It's a hidden trap!")
            damage = random.randint(15, 30)
            player_hp -= damage
            print(f"You take {damage} damage. Current HP: {player_hp}.")
            if player_hp <= 0:
                break # Exit the loop if dead
            time.sleep(1)
            print("You managed to disarm the trap, but it cost you.")
            
        else:
            print("You carefully navigate the path, avoiding any traps. Good job!")
            if not has_key: # Chance to find a key if you don't have one
                if random.randint(1, 3) == 1:
                    print("You notice a glinting object hidden in the foliage. It's a rusty key!")
                    has_key = True
                    time.sleep(1)
            
        print("\nFurther down the path, you see a flickering light from a small cave.")
        print("1. Investigate the cave.")
        print("2. Continue on the main path.")
        
        choice2 = input("What do you do? (1 or 2): ")
        
        if choice2 == '1':
            print("\nYou cautiously approach the cave. Inside, you find a chest!")
            time.sleep(1)
            if has_key:
                print("You use the rusty key and open the chest!")
                if not has_potion: # Only give potion if they don't have one
                    print("Inside, you find a shimmering healing potion!")
                    has_potion = True
                else:
                    print("The chest is empty except for some ancient dust.")
            else:
                print("The chest is locked. You need a key.")
        else:
            print("You decide to stick to the main path, wary of hidden dangers.")

    elif choice1 == '2':
        print("\nYou choose the winding Western Path. It's quieter here, but the journey feels longer.")
        time.sleep(2)
        print("After a while, you come across a peaceful stream.")
        print("1. Drink from the stream (might restore some health).")
        print("2. Cross the stream and continue.")
        
        choice2_western = input("What do you do? (1 or 2): ")
        
        if choice2_western == '1':
            print("\nYou cup your hands and drink the cool, refreshing water.")
            healing = random.randint(5, 15)
            player_hp += healing
            print(f"You restore {healing} HP. Current HP: {player_hp}.")
        else:
            print("You quickly cross the stream, eager to continue your journey.")
            
        if random.randint(1, 4) == 1 and not has_key: # Small chance to find a key
             print("While crossing, your foot nudges a loose stone, revealing a hidden compartment. You find a shiny silver key!")
             has_key = True
             time.sleep(1)

    else:
        print("Invalid choice. You stand confused for a moment, losing precious time.")
        time.sleep(1)
        continue # Skip to the next loop iteration

    # --- Mid-point check and challenge ---
    print("\nRegardless of your path, you now stand before the Guardian's Chamber.")
    print("A gargoyle-like creature awakens, blocking your way to the inner sanctum!")
    print(f"Guardian HP: {50}") # Simple static HP for the guardian for this demo

    while player_hp > 0 and not game_over:
        print(f"\nYour HP: {player_hp} | Guardian HP: {50} (approx.)")
        print("1. Attack the Guardian.")
        print("2. Try to sneak past.")
        if has_potion:
            print("3. Use a healing potion.")

        battle_choice = input("What do you do? (1, 2, or 3 if available): ")

        if battle_choice == '1':
            player_attack = random.randint(10, 25)
            guardian_hp = 50 - player_attack # Simulate guardian taking damage for one round
            print(f"You strike the Guardian for {player_attack} damage!")
            if guardian_hp <= 0:
                print("The Guardian crumbles to dust! You defeated it!")
                game_over = True # Win condition
                break
            else:
                print("The Guardian growls, still standing!")
            
            guardian_attack = random.randint(10, 20)
            player_hp -= guardian_attack
            print(f"The Guardian retaliates, hitting you for {guardian_attack} damage!")
            time.sleep(1)

        elif battle_choice == '2':
            print("You attempt to sneak past the enraged Guardian...")
            time.sleep(1)
            sneak_chance = random.randint(1, 100)
            if sneak_chance > 70: # 30% chance to sneak
                print("You successfully slip past the Guardian!")
                game_over = True # Win condition by sneaking
                break
            else:
                print("The Guardian spots you and unleashes a furious roar!")
                damage = random.randint(20, 35)
                player_hp -= damage
                print(f"You take {damage} damage. Current HP: {player_hp}!")
                time.sleep(1)
                
        elif battle_choice == '3' and has_potion:
            print("You quickly drink your healing potion!")
            heal_amount = random.randint(20, 40)
            player_hp += heal_amount
            if player_hp > 100: player_hp = 100 # Cap health at 100
            has_potion = False
            print(f"You recover {heal_amount} HP. Current HP: {player_hp}.")
            time.sleep(1)
        elif battle_choice == '3' and not has_potion:
            print("You try to use a potion, but you don't have any left!")
        else:
            print("Invalid battle choice. You hesitate, losing your advantage!")
            guardian_attack = random.randint(5, 15)
            player_hp -= guardian_attack
            print(f"The Guardian takes advantage, hitting you for {guardian_attack} damage!")
            time.sleep(1)
        
        if player_hp <= 0:
            print("\nYour vision blurs, and you collapse. The quest ends here.")
            game_over = True
            break # Exit inner battle loop

    if game_over and player_hp > 0: # Check if game_over was set to True by winning
        print("\nWith the Guardian defeated (or bypassed), you enter the inner sanctum.")
        print("There, resting on a pedestal, is the glowing Lost Scroll of Eldoria!")
        print(f"Congratulations, {player_name}! You have completed your adventure and claimed the scroll!")
        
    elif player_hp <= 0: # This case is handled by the break, but good to have a final check
        print("\nGAME OVER.")
        print("Your adventure in the Whispering Ruins has come to an end.")

# End of game
print("\nThanks for playing!")
