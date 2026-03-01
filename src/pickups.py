
class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=20, symbol="?"):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Trap:
    """En fälla på spelplanen. Kostar poäng om man kliver på den."""
    def __init__(self):
        self.name = "trap"
        self.symbol = "X"

    def __str__(self):
        return self.symbol


pickups = [Item("carrot"), Item("apple"), Item("strawberry"), Item("cherry"),
           Item("watermelon"), Item("radish"), Item("cucumber"), Item("meatball")]


def randomize(grid):
    """Placerar alla items på slumpmässiga lediga positioner."""
    for item in pickups:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen


def place_spade(grid):
    """Placerar en spade på en slumpmässig ledig ruta."""
    spade = Item("spade", value=0, symbol="S")
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, spade)
            break


def place_traps(grid, count=3):
    """Placerar fällor på kartan."""
    for _ in range(count):
        while True:
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, Trap())
                break


def place_exit(grid):
    """Placerar exit (E) på en slumpmässig ledig ruta."""
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, "E")
            break


# extra frukter som kan spawna via bördig jord
_extra_fruits = ["banana", "pear", "plum", "grape", "lemon", "lime", "peach"]

def spawn_random_fruit(grid):
    """Skapar en ny frukt på en slumpmässig ledig ruta."""
    import random
    name = random.choice(_extra_fruits)
    fruit = Item(name)
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, fruit)
            print(f"A wild {name} has appeared on the map!")
            return fruit

