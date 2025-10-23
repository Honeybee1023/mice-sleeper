#!/usr/bin/env python3
"""
6.101 Lab:
Mice-sleeper
"""

# import typing  # optional import
# import pprint  # optional import
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game, all_keys=False):
    """
    Prints a human-readable version of a game (provided as a dictionary)

    By default uses only "board", "dimensions", "state", "visible" keys (used
    by doctests). Setting all_keys=True shows all game keys.
    """
    if all_keys:
        keys = sorted(game)
    else:
        keys = ("board", "dimensions", "state", "visible")
        # Use only default game keys. If you modify this you will need
        # to update the docstrings in other functions!

    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(nrows, ncolumns, num_mice):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       num_mice (int): The number of mice to be added to the board

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, 3))
    board:
        [0, 0, 0, 0]
        [0, 0, 0, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    return new_game_nd((nrows, ncolumns), num_mice)


def place_mice_2d(game, num_mice, disallowed):
    """
    Add mice to the given game, subject to limitations on where they may be
    placed.  The first num_mice valid locations from an appropriate
    random_coordinates generator should be used.

    Parameters:
       game (dict): game state
       num_mice (int): the number of mice to be added
       disallowed (set): a set of (r, c) locations where mice cannot be placed

    This function works by mutating the given game, and it always returns None

    >>> g = new_game_2d(2, 2, 2)
    >>> place_mice_2d(g, 2, set())
    >>> dump(g)
    board:
        [2, 'm']
        [2, 'm']
    dimensions: (2, 2)
    state: ongoing
    visible:
        [False, False]
        [False, False]

    >>> g = new_game_2d(2, 2, 2)
    >>> place_mice_2d(g, 2, {(0, 1), (1, 0)})
    >>> dump(g)
    board:
        ['m', 2]
        [2, 'm']
    dimensions: (2, 2)
    state: ongoing
    visible:
        [False, False]
        [False, False]
    """
    place_mice_nd(game, num_mice, disallowed)
    return None


def reveal_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mice (including diagonally), then recursively reveal its eight
    neighbors.  Return an integer indicating how many new squares were revealed
    in total, including neighbors, and neighbors of neighbors, and so on.

    If this is the first reveal performed in a game, then before performing
    the reveal operation, we add the appropriate number of mice to the game
    (the number given at initialization time).  No mice should be placed in
    the location to be revealed, nor in any of its neighbors.

    The state of the game should be changed to 'lost' when at least one mouse
    is visible on the board, 'won' when all safe squares (squares that do not
    contain a mouse) and no mice are visible, and 'ongoing' otherwise.

    If the game is not ongoing, or if the given square has already been
    revealed, reveal_2d should not reveal any squares.

    Parameters:
       game (dict): Game state
       row (int): Where to start revealing cells (row)
       col (int): Where to start revealing cells (col)

    Returns:
       int: the number of new squares revealed

    >>> game = new_game_2d(2, 4, 3)
    >>> reveal_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        [3, 'm', 2, 0]
        ['m', 'm', 2, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, True, True]
        [False, False, True, True]
    >>> reveal_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        [3, 'm', 2, 0]
        ['m', 'm', 2, 0]
    dimensions: (2, 4)
    state: won
    visible:
        [True, False, True, True]
        [False, False, True, True]
    """
    return reveal_nd(game, (row, col))


def render_2d(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    'm' (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mice).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored and
    all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = new_game_2d(2, 4, 3)
    >>> reveal_2d(game, 0, 0)
    4
    >>> render_2d(game, False)
    [[' ', '1', '_', '_'], [' ', '1', '_', '_']]
    >>> render_2d(game, True)
    [[' ', '1', 'm', 'm'], [' ', '1', '3', 'm']]
    >>> reveal_2d(game, 0, 3)
    1
    >>> render_2d(game, False)
    [[' ', '1', '_', 'm'], [' ', '1', '_', '_']]
    """
    raise NotImplementedError


# N-D IMPLEMENTATION



def new_game_nd(dimensions, num_mice):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       dimensions (sequence): Dimensions of the board
       num_mice (int): The number of mice to be added to the board

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), 3)
    >>> dump(g)
    board:
        [[0, 0], [0, 0], [0, 0], [0, 0]]
        [[0, 0], [0, 0], [0, 0], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    game = {"dimensions": dimensions, "state": "ongoing"}

    if len(dimensions)==1:
        game["board"] = [0]
        game["visible"] = [False]
        for _ in range(dimensions[0]-1):
            game["board"].append(0)
            game["visible"].append(False)

    else:
        game["board"] = [[]]
        game["visible"] = [[]]
        for _ in range(dimensions[0]-1):
            game["board"].append([])
            game["visible"].append([])

        # game["board"] = [[]] * dimensions[0]
        # game["visible"] = [[]] * dimensions[0]
        one_less_dimension = new_game_nd(dimensions[1:], num_mice)


        def deep_copy(input):
            if isinstance(input, list):
                return [deep_copy(x) for x in input]
            else: return input

        for ind in range(dimensions[0]):
            # use a recursive copy so each top-level slice has independent inner lists
            game["board"][ind] = deep_copy(one_less_dimension["board"])
            game["visible"][ind] = deep_copy(one_less_dimension["visible"])

    game["coord_to_val"]={}
    for coord in all_coords(game["dimensions"]):
        game["coord_to_val"][coord] = get_value_nd(game, coord, initial=True)

    game["revealed_coords"] = set()

    game["num_mice"] = num_mice

    return game

def set_value_nd(game, coord, value, type = "board"):
    """
    Mutates game board
    """
    def value_to_set(curr_list, coord, value):
        if len(coord) < 1:
            return value
        if len(coord) == 1:
            curr_list[coord[0]] = value
            return curr_list
        else:
            curr_list[coord[0]] = value_to_set(curr_list[coord[0]], coord[1:], value)
            return curr_list

    game[type][coord[0]] = value_to_set(game[type][coord[0]], coord[1:], value)

    if type == "board": game["coord_to_val"][coord] = value

    return None

def get_value_nd(game, coord, initial = False):
    """
    return value of board at that coord
    """
    if initial:
        def get_val(curr_list, coord):
            if len(coord) <= 0:
                return []
            if len(coord) == 1:
                return curr_list[coord[0]]
            else:
                return get_val(curr_list[coord[0]], coord[1:])

        return get_val(game["board"][coord[0]], coord[1:])

    else: return game["coord_to_val"][coord]


def get_neighbors_nd(game, coord, iteration=0):
    """
    Return set of coords that are neighbors of coord (including itself)
    """
    if len(coord) == 1:
        val = coord[0]
        if val == 0 and val == game["dimensions"][iteration]-1:
            return {(val,)}
        elif val == 0:
            return {(coord[0]+1, ), (coord[0],)}
        elif val == game["dimensions"][iteration]-1:
            return {(coord[0],), (coord[0]-1,)}
        else: return {(coord[0]+1, ), (coord[0],), (coord[0]-1,)}
    else:
        neighbors = set()
        first = coord[0]
        rest = coord[1:]
        rest_neighbors = get_neighbors_nd(game, rest, iteration+1)
        for neighbor_coord in rest_neighbors:
            if first == 0 and first == game["dimensions"][iteration]-1:
                neighbors.add((first,) + neighbor_coord)
            elif first == 0:
                neighbors.add((first,) + neighbor_coord)
                neighbors.add((first+1,) + neighbor_coord)
            elif first == game["dimensions"][iteration]-1:
                neighbors.add((first,) + neighbor_coord)
                neighbors.add((first-1,) + neighbor_coord)
            else:
                neighbors.add((first,) + neighbor_coord)
                neighbors.add((first+1,) + neighbor_coord)
                neighbors.add((first-1,) + neighbor_coord)
        return neighbors

def all_coords(dimension):
    """
    Return a set of all the coordinates in an n-dimensional game board
    """
    if len(dimension)==1:
        return set((x,) for x in range(dimension[0]))
    else:
        output = set()
        rest_coords = all_coords(dimension[1:])
        for first in range(dimension[0]):
            for coord in rest_coords:
                output.add((first,)+coord)
        return output
    
def place_mice_nd(game, num_mice, disallowed):
    """
    Add mice to the given game, subject to limitations on where they may be
    placed.  The first num_mice valid locations from an appropriate
    random_coordinates generator should be used.

    Parameters:
       game (dict): game state
       num_mice (int): the number of mice to be added
       disallowed (set): a set of tuples, each representing a location where
                         mice cannot be placed

    This function works by mutating the given game, and it always returns None

    >>> g = new_game_nd((2, 2, 2), 2)
    >>> place_mice_nd(g, 2, set())
    >>> dump(g)
    board:
        [[2, 2], [2, 2]]
        [['m', 'm'], [2, 2]]
    dimensions: (2, 2, 2)
    state: ongoing
    visible:
        [[False, False], [False, False]]
        [[False, False], [False, False]]


    >>> g = new_game_nd((2, 2, 2), 2)
    >>> place_mice_nd(g, 2, {(1, 0, 0), (0, 1, 1)})
    >>> dump(g)
    board:
        [[2, 2], [2, 2]]
        [[2, 'm'], ['m', 2]]
    dimensions: (2, 2, 2)
    state: ongoing
    visible:
        [[False, False], [False, False]]
        [[False, False], [False, False]]
    """
    #place the mice first
    generator = random_coordinates(game["dimensions"])
        #You must give generator a name, otherwise you call function anew each time
    # for _ in range(3):
    #     print(next(generator))
    remaining_mice = num_mice
    mice_spots = set()
    while remaining_mice>0:
        coord = next(generator)
        if coord not in disallowed:
            set_value_nd(game, coord, 'm')
            mice_spots.add(coord)
            remaining_mice -= 1
            disallowed.add(coord)

    #update neighbors
    empty_spots = all_coords(game["dimensions"]) - mice_spots
    for spot in empty_spots:
        curr_mouse_count = 0
        neighbors = get_neighbors_nd(game, spot) - {spot}
        for neighbor in neighbors:
            if get_value_nd(game, neighbor)=='m':
                curr_mouse_count+=1
        set_value_nd(game, spot, curr_mouse_count)

    return None

def game_won_nd(game):
    """
    Return True if game is won, False otherwise
    """
    if game["state"] == "lost":
        return False
    elif game["state"] == "won":
        return True
    else: #still labelled ongoing
        total_coords = 1
        for val in game["dimensions"]:
            total_coords *= val
        return total_coords == len(game["revealed_coords"]) + game["num_mice"]


def reveal_nd(game, coordinates):
    """
    Recursively reveal square at coords and neighboring squares.

    Update the visible to reveal square at the given coordinates; then
    recursively reveal its neighbors, as long as coords does not contain and is
    not adjacent to a mouse.  Return a number indicating how many squares were
    revealed.  No action should be taken (and 0 should be returned) if the
    incoming state of the game is not 'ongoing', or if the given square has
    already been revealed.

    If this is the first reveal performed in a game, then before performing
    the reveal operation, we add the appropriate number of mice to the game
    (the number given at initialization time).  No mice should be placed in
    the location to be revealed, nor in any of its neighbors.


    The updated state is 'lost' when at least one mouse is visible on the
    board, 'won' when all safe squares (squares that do not contain a mouse)
    and no mice are visible, and 'ongoing' otherwise.

    Parameters:
       coordinates (tuple): Where to start revealing squares

    Returns:
       int: number of squares revealed

    >>> g = new_game_nd((2, 4, 2), 3)
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [['m', 3], ['m', 3], [1, 1], [0, 0]]
        [['m', 3], [3, 3], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> reveal_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [['m', 3], ['m', 3], [1, 1], [0, 0]]
        [['m', 3], [3, 3], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, True], [False, False], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> reveal_nd(g, (0, 0, 0))
    1
    >>> dump(g)
    board:
        [['m', 3], ['m', 3], [1, 1], [0, 0]]
        [['m', 3], [3, 3], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: lost
    visible:
        [[True, True], [False, False], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    """
    first_reveal = (len(game["revealed_coords"])==0)
    #check incoming game state
    #if not ongoing, return 0
    if game["state"] != "ongoing":
        return 0
    #if already revealed, return 0
    if coordinates in game["revealed_coords"]:
        return 0
    #else
    #check if first reveal
    #if first reveal, then 
    if first_reveal:
        # first call place mice with disallowed coords being neighbors of coord plus coord itself
        disallowed = get_neighbors_nd(game, coordinates)
        place_mice_nd(game, game["num_mice"] , disallowed)
    #now do reveal
    #add this coord to revealed
    game["revealed_coords"].add(coordinates)
    num_revealed = 1
    #var = value at this coord
    val = get_value_nd(game, coordinates)
    #reveal this coord in visible
    set_value_nd(game, coordinates, True, type="visible")
    #if mouse, we lost
    if val == 'm':
        game["state"] = "lost"
    #if number, just reveal this square
    #if 0, call reveal on all neighbors that are not revealed yet
    elif val == 0:
        neighbors = get_neighbors_nd(game, coordinates) - {coordinates} - game["revealed_coords"]
        for neighbor in neighbors:
            num_revealed += reveal_nd(game, neighbor)
    #check if won using helper function and update
    if game["state"] != "lost":
        if game_won_nd(game):
            game["state"] = "won"
    
    return num_revealed


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), 'm'
    (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring mice).
    The game['visible'] array indicates which squares should be visible.  If
    all_visible is True (the default is False), the game['visible'] array is
    ignored and all cells are shown.

    Parameters:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = new_game_nd((2, 4, 2), 3)
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]
    >>> render_nd(g, True)
    [[['m', '3'], ['m', '3'], ['1', '1'], [' ', ' ']],
     [['m', '3'], ['3', '3'], ['1', '1'], [' ', ' ']]]
    """
    raise NotImplementedError


def random_coordinates(dimensions):
    """
    Given a tuple representing the dimensions of a game board, return an
    infinite generator that yields pseudo-random coordinates within the board.
    For a given tuple of dimensions and seed, the output sequence will always
    be the same.
    """

    def prng(state):
        # see https://en.wikipedia.org/wiki/Lehmer_random_number_generator
        while True:
            yield (state := state * 48271 % 0x7FFFFFFF) / 0x7FFFFFFF

    prng_gen = prng(
        seed
        if (seed := getattr(random_coordinates, "seed", None)) is not None
        else (sum(dimensions) + 61016101)
    )
    while True:
        yield tuple(int(dim * val) for val, dim in zip(prng_gen, dimensions))


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so,
    # comment out the above line, and uncomment the below line of code.  This
    # may be useful as you write/debug individual doctests or functions.  Also,
    # the verbose flag can be set to True to see all test results, including
    # those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )

    # test for set_value_nd: 
    # expected: {'board': [[[2, 2], ['m', 2]], [['m', 'm'], [2, 2]]]}
    # test_game = {"board": [ [[2, 2], [2, 2]], [['m', 'm'], [2, 2]] ]}
    # set_value_nd(test_game, (0, 1, 0), 'm')
    # print(test_game)

    # g = new_game_nd((2,2), 2)
    # g["board"][0][0] = "hi"
    # dump(g)

    # g = new_game_nd((2,2,2), 2)
    # g["board"][0][0][0] = "hi"
    # dump(g)
    # set_value_nd(g, (0, 0, 0), 'm')
    # dump(g)

    # test for get_value_nd: 
    # expected: 1
    # test_game = {"board": [ [[2, 2], [1, 2]], [['m', 'm'], [2, 2]] ]}
    # print(get_value_nd(test_game, (0, 1, 0)))

    # test for get_neighbors_nd:
    # should have 12
    # test_game = {"dimension": (3, 2, 4)}
    # print(len(get_neighbors_nd(test_game, (0, 1, 2))))
    # print(get_neighbors_nd(test_game, (0, 1, 2)))

    #test for all_coords
    # expected:{(1, 0, 1), (0, 0, 0), (1, 0, 0), (0, 0, 2), (1, 0, 2), (0, 0, 1)}
    # print(all_coords((2,1,3)))

    #test for place_mice
    # g = new_game_nd((2,2,2), 2)
    # place_mice_nd(g, 2, set())
    # dump(g)

    #test for reveal_nd
    # g = new_game_nd((2, 4, 2), 3)
    # print(reveal_nd(g, (0, 3, 0)))
    # dump(g)
    # print(reveal_nd(g, (0, 0, 1)))
    # dump(g)
    # print(reveal_nd(g, (0, 0, 0)))
    # dump(g)

    # game = new_game_2d(2, 4, 3)
    # print(reveal_2d(game, 0, 3))
    # dump(game)
    # print(reveal_2d(game, 0, 0))
    # dump(game)

    game = new_game_nd((4,), 1)
    print(reveal_nd(game, (0,)))
    dump(game)


    
