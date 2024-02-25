import random
import heapq


def create_empty_maze(): # Creating the  6 x 6 maze 
    maze = []
    for i in range(6):
        row = []
        for j in range(6):
            node_Number = str(i * 6 + j)
            row.append(node_Number)
        maze.append(row) 
    return maze

def select_start_and_goal(): # Creates random start and goal nodes to the given criteria 
    start_node = random.randint(0, 11)
    goal_node = random.randint(24, 35)
    return start_node, goal_node

def select_barrier_nodes(start_node, goal_node): # Creates randomly selected barrier nodes, not start or goal nodes
    all_nodes = []
    for node in range(36):
        if node != start_node and node != goal_node:
            all_nodes.append(node)
    
    barrier_nodes = random.sample(all_nodes, 4)
    return barrier_nodes

def calculate_manhattan_distance(node, goal_node):
    node_row, node_col = divmod(node, 6)
    goal_row, goal_col = divmod(goal_node, 6)
    return abs(node_row - goal_row) + abs(node_col - goal_col)


def perform_dfs(maze, start_node, goal_node, barrier_nodes):
    visited = []
    stack = []
    path = []

    row_length = len(maze[0])
    col_length = len(maze[0])
    grid_size = len(maze) * row_length

    stack.append(start_node)
    visited.append(start_node)
    while stack:
        current_node = stack.pop()
        path.append(current_node)

        if current_node == goal_node:
            print("DFS Results:")
            print("Goal reached !!!!")
            break
        
        row, col = divmod(current_node, row_length)

        neighbors = [
            (row - 1, col),  # Up
            (row + 1, col),  # Down
            (row, col - 1),  # Left
            (row, col + 1),  # Right
            (row - 1, col - 1),  # Up-Left
            (row - 1, col + 1),  # Up-Right
            (row + 1, col - 1),  # Down-Left
            (row + 1, col + 1)   # Down-Right
        ]

        neighbors.sort()

        for neighbor_x, neighbor_y in neighbors:
            if 0 <= neighbor_x < row_length and 0 <= neighbor_y < row_length \
             and maze[neighbor_x][neighbor_y] != '#':
                neighbor_node = neighbor_x * row_length + neighbor_y

                if neighbor_node not in visited:
                    stack.append(neighbor_node)
                    visited.append(neighbor_node)

    print("Time: ", len(visited)-1, "minutes")
    return list(path), list(visited)


def a_star(maze, start_node, goal_node, barrier_nodes):
    visited = []
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_node, []))  # Cost, node, path

    row_length = len(maze[0])

    while priority_queue:
        cost, current_node, path = heapq.heappop(priority_queue)

        if current_node not in visited:
            visited.append(current_node)

            if current_node == goal_node:
                return visited, cost, path + [goal_node]

            row, col = divmod(current_node, row_length)

            neighbors = [
                (row - 1, col),  # Up
                (row + 1, col),  # Down
                (row, col - 1),  # Left
                (row, col + 1),  # Right
                (row - 1, col - 1),  # Up-Left
                (row - 1, col + 1),  # Up-Right
                (row + 1, col - 1),  # Down-Left
                (row + 1, col + 1)   # Down-Right
            ]

            valid_neighbors = []
            for r, c in neighbors:
                neighbor = r * row_length + c
                if 0 <= r < len(maze) and 0 <= c < row_length and neighbor not in visited and neighbor not in barrier_nodes:
                    valid_neighbors.append(neighbor)

            for neighbor in valid_neighbors:
                heapq.heappush(priority_queue, (cost + 1 + calculate_manhattan_distance(neighbor, goal_node), neighbor, path + [current_node]))
    return visited
    


def setup_maze(): # Creates the maze using the above functions 
    maze = create_empty_maze()
    start_node, goal_node = select_start_and_goal()
    barrier_nodes = select_barrier_nodes(start_node, goal_node)
    
    maze[start_node // 6][start_node % 6] = 'S'  
    maze[goal_node // 6][goal_node % 6] = 'G'    
    
    for node in barrier_nodes:
        maze[node // 6][node % 6] = '#'
    
    visited, path = perform_dfs(maze,start_node, goal_node, barrier_nodes)

    print("Visited nodes: ", path)
    print("Final path: ", visited)

    visited_astar, cost_astar, final_path_astar = a_star(maze, start_node, goal_node, barrier_nodes)


    print("\nA* Results:")
    print("Visited Nodes:", visited_astar)
    print("Cost to Find Goal (A*):", len(visited_astar) - 1)
    print("Final Path (A*):", final_path_astar)
    print("Time:", len(visited_astar)-1, "minutes")

    Max_length = len(str(len(maze) * len(maze[0])))

    for row in maze: # makes the row into a single string seperated by spaces 
        adjusted_row = [f"{node_Number: <{Max_length}}" for node_Number in row] # Makes the maze more organized when printing
        print(' '.join(adjusted_row))

setup_maze()









