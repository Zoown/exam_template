from .grid import Grid
from .player import Player
from . import pickups



# Spelaren börjar nära mitten av spelplanen
player = Player(18, 6)
score = 0
inventory = []

g = Grid()
g.set_player(player)
g.make_walls()
pickups.randomize(g)
pickups.place_spade(g)
pickups.place_traps(g, 3)
pickups.place_exit(g)

# håll koll på hur många saker som ska samlas
total_items = len(pickups.pickups)
items_collected = 0
game_won = False
move_counter = 0


def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.  Items: {items_collected}/{total_items}")
    print(game_grid)


def has_spade():
    """Kollar om spelaren har en spade i inventory."""
    for item in inventory:
        if item.name == "spade":
            return True
    return False


def remove_spade():
    """Tar bort spaden från inventory (den förbrukas)."""
    for i in range(len(inventory)):
        if inventory[i].name == "spade":
            inventory.pop(i)
            return


def handle_move(dx, dy, jumping=False):
    """Flytta spelaren och hantera vad som händer på den nya rutan.
    Om jumping=True försöker vi hoppa 2 steg, men vid vägg tar vi bara 1."""
    global score, items_collected, game_won, move_counter

    # bestäm hur långt vi ska gå
    if jumping:
        # försök 2 steg, men om ruta 2 är blockerad => ta bara 1 steg
        step1_ok = player.can_move(dx, dy, g)
        if step1_ok:
            # kolla om steg 2 också går
            step2_x = player.pos_x + dx * 2
            step2_y = player.pos_y + dy * 2
            if (0 <= step2_x < g.width and 0 <= step2_y < g.height
                    and g.get(step2_x, step2_y) != g.wall):
                # hoppa 2 steg, landa direkt utan att interagera med mellanrutan
                actual_dx = dx * 2
                actual_dy = dy * 2
            else:
                # vägg i vägen vid steg 2, ta bara 1 steg
                actual_dx = dx
                actual_dy = dy
        else:
            # kan inte ens ta steg 1
            actual_dx = dx
            actual_dy = dy
    else:
        actual_dx = dx
        actual_dy = dy

    new_x = player.pos_x + actual_dx
    new_y = player.pos_y + actual_dy

    # kan vi gå dit?
    if not player.can_move(actual_dx, actual_dy, g):
        # kolla om vi har spade och försöker gå in i en vägg
        target_x = player.pos_x + dx
        target_y = player.pos_y + dy
        if 0 <= target_x < g.width and 0 <= target_y < g.height:
            if g.get(target_x, target_y) == g.wall and has_spade():
                g.clear(target_x, target_y)
                remove_spade()
                print("You used the spade to break through the wall!")
        return

    player.move(actual_dx, actual_dy)
    score -= 1  # the floor is lava - tappar 1 poäng per steg
    move_counter += 1

    # bördig jord - var 25:e drag spawnar en ny frukt
    if move_counter % 25 == 0:
        new_fruit = pickups.spawn_random_fruit(g)

    # kolla vad som finns på nya rutan
    thing = g.get(player.pos_x, player.pos_y)

    if isinstance(thing, pickups.Item):
        score += thing.value
        inventory.append(thing)
        g.clear(player.pos_x, player.pos_y)
        # räkna bara vanliga items, inte spaden
        if thing.name != "spade":
            items_collected += 1
        print(f"You found a {thing.name}! +{thing.value} points.")

    elif isinstance(thing, pickups.Trap):
        score -= 10
        print("You fell into a trap! -10 points.")
        # fällan ligger kvar, man kan trampa i den igen

    elif thing == "E":
        if items_collected >= total_items:
            game_won = True
            print("You made it to the exit! YOU WIN!")
        else:
            remaining = total_items - items_collected
            print(f"This is the exit, but you still need {remaining} more item(s).")


# --- Spelets huvudloop ---
command = ""
while command not in ["q", "x"] and not game_won:
    print_status(g)

    raw = input("WASD=move, J+WASD=jump, I=inventory, Q=quit: ").casefold()
    # kolla om det är ett jump-kommando (t.ex. "jw", "jd")
    jump = False
    if len(raw) >= 2 and raw[0] == "j":
        jump = True
        command = raw[1]
    else:
        command = raw[:1]

    if command == "w":
        handle_move(0, -1, jump)
    elif command == "a":
        handle_move(-1, 0, jump)
    elif command == "s":
        handle_move(0, 1, jump)
    elif command == "d":
        handle_move(1, 0, jump)
    elif command == "i":
        # skriv ut spelarens inventory
        if len(inventory) == 0:
            print("Inventory is empty.")
        else:
            print("-- Inventory --")
            for item in inventory:
                print(f"  - {item.name}")

# Spelet är slut
if game_won:
    print(f"\nFinal score: {score} points. Well done!")
else:
    print("Thank you for playing!")
