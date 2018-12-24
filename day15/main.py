import operator
from collections import defaultdict
from dijkstra import dijkstra_multiple, dijkstra_p_queue

ELF_AP = 3
GOBLIN_AP = 3

ADJACENT_MODIFIERS = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

sort_coord_list = lambda list: sorted(list, key=lambda c: (c[1], c[0]))

get_next_player = lambda possible_players: sort_coord_list(possible_players)[0]

get_adjacent_coords = lambda origin: [tuple(map(operator.add, origin, mod)) for mod in ADJACENT_MODIFIERS]

get_empty_adjacent_coords = lambda origin, empty_nodes: [a for a in get_adjacent_coords(origin) if a in empty_nodes]

get_graph_edges = lambda nodes: {c: [(a, 1) for a in get_empty_adjacent_coords(c, nodes)] for c in nodes}

def setup_grid(grid_text):
    nodes = set()
    elves = defaultdict(int)
    goblins = defaultdict(int)

    for y, l in enumerate(grid_text):
        for x, c in enumerate(l):
            coord = (x, y)
            if c == '.':
                nodes.add(coord)
            elif c == 'E':
                elves[coord] = 200
            elif c == 'G':
                goblins[coord] = 200
    
    return nodes, elves, goblins

def attack(current_pos, is_elf, enemies, empty_space, players_in_round):
    enemy_coords = list(enemies.keys())
    enemies_nearby = [e for e in get_adjacent_coords(current_pos) if e in enemy_coords]
    if not enemies_nearby:
        return enemies, empty_space, False, players_in_round
    # Sort enemies by lowest hp then reading order
    sorted_enemies = sorted(enemies_nearby, key=lambda e: (enemies[e], e[1], e[0]))
    enemy_to_attack = sorted_enemies[0]

    if is_elf:
        enemies[enemy_to_attack] -= ELF_AP
    else:
        enemies[enemy_to_attack] -= GOBLIN_AP
    
    if enemies[enemy_to_attack] <= 0:
        if enemy_to_attack in players_in_round:
            players_in_round.remove(enemy_to_attack)
        empty_space.add(enemy_to_attack)
        del enemies[enemy_to_attack]

    return enemies, empty_space, True, players_in_round

def move(current_pos, friendlies, enemies, nodes, edges):
    # Get the coords I can move to
    adjacent_empty_coords = get_empty_adjacent_coords(current_pos, nodes)
    if not adjacent_empty_coords:
        return current_pos, friendlies, nodes
    # Get the coords I am aiming for
    enemy_coords = list(enemies.keys())
    open_coords_around_enemies = []
    for c in enemy_coords:
        open_coords = get_empty_adjacent_coords(c, nodes)
        open_coords_around_enemies += open_coords
    if not open_coords_around_enemies:
        return current_pos, friendlies, nodes
    # For each coord I can move to, get shortest distance to ones I am aiming for
    distances_from_adj_coord_to_enemy = defaultdict(int)
    for adj_coord in adjacent_empty_coords:
        # distances_to_enemy_adjacents = dijkstra_multiple(edges, nodes, adj_coord, open_coords_around_enemies)
        dij_p_q = dijkstra_p_queue(edges, nodes, adj_coord, (1, 1))
        distances_to_enemy_adjacents = {coord: distance for coord, distance in dij_p_q.items() if coord in open_coords_around_enemies}
        minimum_distance_to_enemy_adjacent = min(distances_to_enemy_adjacents.values())
        distances_from_adj_coord_to_enemy[adj_coord] = minimum_distance_to_enemy_adjacent

    # Sort coords I can move to by min distance, then reading order
    sorted_distance_results = sorted(distances_from_adj_coord_to_enemy.keys(), key=lambda c: (distances_from_adj_coord_to_enemy[c], c[1], c[0]))

    # Select first one and change friendlies dict and nodes
    coord_to_move_to = sorted_distance_results[0]
    if distances_from_adj_coord_to_enemy[coord_to_move_to] == float('inf'):
        return current_pos, friendlies, nodes
    
    nodes.add(current_pos)
    nodes.remove(coord_to_move_to)
    friendlies[coord_to_move_to] = friendlies[current_pos]
    del friendlies[current_pos]
    return coord_to_move_to, friendlies, nodes

def print_grid(elves, goblins, nodes, max_x, max_y):
    for y in range(0, max_y+1):
        to_print = ''
        for x in range(0, max_x+1):
            coord = (x, y)
            if coord in elves:
                to_print += 'E'
            elif coord in goblins:
                to_print += 'G'
            elif coord in nodes:
                to_print += '.'
            else:
                to_print += '#'
        print(to_print)

def main():
    grid_text = [l.rstrip() for l in open('input.txt', 'r').readlines()]
    nodes, elves, goblins = setup_grid(grid_text)
    rounds_elapsed = 0

    while goblins and elves:
        players_this_round = list(elves.keys()) + list(goblins.keys())
        while players_this_round:
            player_position = get_next_player(players_this_round)
            players_this_round.remove(player_position)
            graph_edges = get_graph_edges(nodes)
            
            is_elf = True if player_position in elves else False
            enemies = goblins if is_elf else elves
            friendlies = elves if is_elf else goblins
            
            enemies, nodes, did_attack, players_this_round = attack(player_position, is_elf, enemies, nodes, players_this_round)
            if not enemies:
                break
            if did_attack:
                continue
            
            updated_position, friendlies, nodes = move(player_position, friendlies, enemies, nodes, graph_edges)

            enemies, nodes, did_attack, players_this_round = attack(updated_position, is_elf, enemies, nodes, players_this_round)
            if not enemies:
                break
        
        rounds_elapsed += 1
        print('Finished round {0}'.format(rounds_elapsed))
        
        # print('\n')
    friendly_health = sum(elves.values()) if elves else sum(goblins.values())
    print('{0} win after {1} rounds with a total of {2} HP remaining'.format('Elves' if elves else 'Goblins', rounds_elapsed, friendly_health))
    print('Outcome: {0}'.format(
        friendly_health * (rounds_elapsed-1)
    ))

if __name__ == '__main__':
    main()