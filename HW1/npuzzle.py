"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now). 
See Courseworks for detailed instructions.

@author: Naman Jain (nj2387)
"""

import time


def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped. 
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]
    
    new_state = []
    for row in range(len(state)): 
        new_row = []
        for column in range(len(state[row])): 
            if row == i1 and column == j1: 
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else: 
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)


def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions. 
    The result should be a list containing (Action, state) tuples. 
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))), 
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))] 
    """ 
  
    child_states = []

    # YOUR CODE HERE . Hint: Find the "hole" first, then generate each possible
    # successor state by calling the swap_cells method.
    # Exclude actions that are not applicable.
    i = -1
    j = -1
    for s in state:
        i = state.index(s)
        if 0 in s:
            j = s.index(0)
            break

    if (j + 1) < len(state):
        child_states.append(tuple(['Left', swap_cells(state, i, j, i, j + 1)]))
    if (j - 1) >= 0:
        child_states.append(tuple(['Right', swap_cells(state, i, j, i, j - 1)]))
    if (i + 1) < len(state):
        child_states.append(tuple(['Up', swap_cells(state, i, j, i + 1, j)]))
    if (i - 1) >= 0:
        child_states.append(tuple(['Down', swap_cells(state, i, j, i - 1, j)]))

    return child_states

            
def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise. 
    """    

    # YOUR CODE HERE
    n = len(state)
    goal_states = []
    for st in state:
        goal_states.extend([s for s in st])

    if len(goal_states) != (n * n):
        return False

    i = 0
    for gs in goal_states:
        if gs != i:
            return False
        i += 1

    return True

   
def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a queue in BFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    # YOUR CODE HERE
    fringe.append(state)
    parents[state] = (None, None)

    while True:

        if max_fringe < len(fringe):
            max_fringe = len(fringe)

        if not fringe:
            return None, states_expanded, max_fringe

        state_to_expand = fringe.pop(0)

        if goal_test(state_to_expand):
            return extract_solution(state_to_expand, parents), states_expanded, max_fringe

        if state_to_expand not in closed:
            states_expanded += 1
            new_states = get_successors(state_to_expand)
            closed.add(state_to_expand)
            for s in new_states:
                if s[1] not in closed:
                    fringe.append(s[1])
                    parents[s[1]] = (state_to_expand, s[0])


def extract_solution(final_state, parents):
    final_solution = []
    state = final_state
    while parents[state][0]:
        final_solution.insert(0, parents[state][1])
        state = parents[state][0]
    return final_solution

     
def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a stack in DFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    # YOUR CODE HERE
    fringe.append(state)
    parents[state] = (None, None)

    while True:

        if max_fringe < len(fringe):
            max_fringe = len(fringe)

        if not fringe:
            return None, states_expanded, max_fringe

        state_to_expand = fringe.pop()

        if goal_test(state_to_expand):
            return extract_solution(state_to_expand, parents), states_expanded, max_fringe

        if state_to_expand not in closed:
            states_expanded += 1
            new_states = get_successors(state_to_expand)
            closed.add(state_to_expand)
            for s in new_states:
                if s[1] not in closed:
                    fringe.append(s[1])
                    parents[s[1]] = (state_to_expand, s[0])


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """

    # YOUR CODE HERE
    i = 0
    misplaced_count = 0
    for st in state:
        for s in st:
            if i and s != i:
                misplaced_count += 1
            i += 1

    return misplaced_count


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the Manhattan distance between the current
    position and the goal position. Then return the sum of all distances.
    """

    i = 0
    tiles_position = {}
    tiles_expected_position = {}
    tile_value = 0
    for st in state:
        j = 0
        for s in st:
            tiles_position[s] = (i, j)
            tiles_expected_position[tile_value] = (i, j)
            tile_value += 1
            j += 1
        i += 1

    manhattan_distance = 0
    for k, v in tiles_position.items():
        if k:
            manhattan_distance += abs(v[0] - tiles_expected_position[k][0]) + abs(v[1] - tiles_expected_position[k][1])

    return manhattan_distance


def best_first(state, heuristic):
    """
    Best first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    # YOUR CODE HERE
    heappush(fringe, (heuristic(state), state))
    parents[state] = (None, None)

    while True:

        if max_fringe < len(fringe):
            max_fringe = len(fringe)

        if not fringe:
            return None, states_expanded, max_fringe

        state_to_expand = heappop(fringe)[1]

        if goal_test(state_to_expand):
            return extract_solution(state_to_expand, parents), states_expanded, max_fringe

        if state_to_expand not in closed:
            states_expanded += 1
            new_states = get_successors(state_to_expand)
            closed.add(state_to_expand)
            for s in new_states:
                if s[1] not in closed:
                    heappush(fringe, (heuristic(s[1]), s[1]))
                    parents[s[1]] = (state_to_expand, s[0])


def astar(state, heuristic):
    """
    A-star search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    costs = {}

    # YOUR CODE HERE
    costs[state] = 0
    heappush(fringe, (heuristic(state) + costs[state], state))
    parents[state] = (None, None)

    while True:

        if max_fringe < len(fringe):
            max_fringe = len(fringe)

        if not fringe:
            return None, states_expanded, max_fringe

        state_to_expand = heappop(fringe)[1]

        if goal_test(state_to_expand):
            return extract_solution(state_to_expand, parents), states_expanded, max_fringe

        if state_to_expand not in closed:
            states_expanded += 1
            new_states = get_successors(state_to_expand)
            closed.add(state_to_expand)
            for s in new_states:
                if s[1] not in closed:
                    costs[s[1]] = costs[state_to_expand] + 1
                    heappush(fringe, (heuristic(s[1]) + costs[s[1]], s[1]))
                    parents[s[1]] = (state_to_expand, s[0])


def print_result(solution, states_expanded, max_fringe):
    """
    Helper function to format test output. 
    """
    if solution is None: 
        print("No solution found.")
    else: 
        print("Solution has {} actions.".format(len(solution)))
    print("Total states expanded: {}.".format(states_expanded))
    print("Max fringe size: {}.".format(max_fringe))


if __name__ == "__main__":

    # Easy test case
    test_state = ((1, 4, 2),
                  (0, 5, 8),
                  (3, 6, 7))

    # More difficult test case
    # test_state = ((7, 2, 4),
    #               (5, 0, 6),
    #               (8, 3, 1))

    print(state_to_string(test_state))
    print()

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_fringe = bfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====DFS====")
    start = time.time()
    solution, states_expanded, max_fringe = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))
    
    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

