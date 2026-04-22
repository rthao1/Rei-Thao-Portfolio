import random
import heapq

class Network: # Network class used to represent the graph with nodes and edges
    def __init__(self, nodes):
        self.nodes = set(nodes)# Store node names as a set
        self.graph = {u: {} for u in nodes} #Graph adjacency list: graph[u][v] = weight

        # used sets to track failed nodes and the failed links
        self.failed_nodes = set()
        self.failed_links = set()
    
    def add_link(self, from_node, to_node, cost): #used to add links between nodes
        self.graph[from_node][to_node] = cost
        self.graph[to_node][from_node] = cost

    def fail_node(self, node):  # Used to mark a node as failed its removed from routing
        self.failed_nodes.add(node)
    
    def repair_node(self, u): # Used to repair a node and restore it to routing
        self.failed_nodes.discard(u)
    
    def fail_link(self, from_node, to_node):  # Used to make a link fail from both directions
        self.failed_links.add((from_node, to_node))
        self.failed_links.add((to_node, from_node))

    def repair_link(self, from_node, to_node): # Repairs a link in both directions
        self.failed_links.discard((from_node, to_node))
        self.failed_links.discard(( to_node, from_node))

    def neighbors(self, node):# Generator for all  neighbors of a node and Skips failed links and failed nodes
        for neighbor, weight in self.graph[node].items():
            if (node, neighbor) not in self.failed_links and neighbor not in self.failed_nodes:
                yield neighbor, weight
    
def print_graph(net): # Print the graph in an easy to read format
    print("\nNetwork graph:")
    for u, neighbors in net.graph.items():
        print(f"{u}: {neighbors}")

def create_custom_network(): # User enters nodes and edges manually
    print("\nEnter node names separated by spaces:")
    nodes = input("Nodes: ").split()
    net = Network(nodes)

    print("\nEnter links (u v w). Type 'done' to finish.")

    #loop to enter links until user types done
    while True:
        link_input = input("Link: ")
        if link_input.lower() == 'done':
            break

        u, v, w = link_input.split()
        net.add_link(u, v, int(w))
    
    start = input("\nEnter start node: ")
    goal = input("Enter goal node: ")

    return net, start, goal

    
def dijkstra(net, start, goal): # Dijkstra's shortest path algorithm accounts for failed nodes and failed links

    # If start or goal fails, no route is possible and return None to not waist time
    if start in net.failed_nodes or goal in net.failed_nodes:
        return None

    # Distance table
    dist = {node: float('inf') for node in net.nodes}
    dist[start] = 0

    # Priority queue of (distance, node)
    pq = [(0, start)]

    # Parent dictionary use for the path reconstruction
    parent = {start: None}

    while pq:
        d, u = heapq.heappop(pq)

        if u == goal: #Stops early if the goal is reached
            break

        for v, w in net.neighbors(u):  # Explore all  neighbors that weren't failed
            new_cost = d + w
            if new_cost < dist[v]:
                dist[v] = new_cost
                parent[v] = u
                heapq.heappush(pq, (new_cost, v))


    if dist[goal] == float('inf'): # If the goal is unreachable
        return None


    # Used to reconstruct the shortest path by following parents backward
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]

    return list(reversed(path)) 


def simulate_step(net, p_node_fail, p_link_fail):

   #Used to simulate random failures and repairs nodes that dont fail
    for node in list(net.nodes):
        random_value = random.random()
        #print ("Random node failed:", random_value) # for debugging
        if random_value< p_node_fail:
            net.fail_node(node)
        else:
            net.repair_node(node)

    # used to simulate random failures and repairs links that dont fail
    processed_links = set()
    for u in net.graph:
        for v in net.graph[u]:
            link = tuple(sorted([u, v]))
            if link not in processed_links: # Only process each link once (avoid duplicates from bidirectional links)
                processed_links.add(link)
                random_value = random.random()
                #print ("Random link failed:",random_value) # for debugging
                if random_value < p_link_fail:
                    net.fail_link(u, v)
                else:
                    net.repair_link(u, v)

def display_failures(net): # Print all failures in a easy to read format
    print("\nFailed Nodes:", list(net.failed_nodes))

    # Convert link failures into readable pairs
    failed_pairs = set()
    for u, v in net.failed_links:
        # Avoid duplicated reversed pairs
        if (v, u) not in failed_pairs:
            failed_pairs.add((u, v))

    print("Failed Links:", list(failed_pairs))

def static_network():# Predefined static network 
    nodes = [f"N{i}" for i in range(1, 10)]
    net = Network(nodes)

    # Hardcoded links with weight 1
    links = [
        ("N1", "N2", 1), ("N1", "N4", 1),
        ("N2", "N3", 1), ("N2", "N5", 1),
        ("N3", "N6", 1),
        ("N4", "N5", 1), ("N4", "N7", 1),
        ("N5", "N6", 1), ("N5", "N8", 1),
        ("N6", "N9", 1),
        ("N7", "N8", 1),
        ("N8", "N9", 1)
    ]

    # used to load the links into the graph(link1 , link2, weight/cost)
    for u, v, w in links:
        net.add_link(u, v, w)

    start = "N1"
    goal = "N9"


    return net, start, goal

def manual_fail_repair(net, start, goal): # Manual failure/repair mode for user 
    print("\nManual Failure/Repair Mode")

    while True:
        print("select a option:")
        print("  1.fail node X")
        print("  2.repair node X")
        print("  3.fail link A B")
        print("  4.repair link A B")
        cmd = input("Enter a option type done when your finished: ").strip().lower()

        if cmd == "done":
            break

        # Fail node
        if cmd == '1':
          print("Enter node to fail:")
          node = input().strip()
          if node not in net.nodes:
              print("Invalid node.")
          else:
              net.fail_node(node)
              print(f"Node {node} FAILED.")

        # Repair node
        elif cmd == '2':
            print("Enter node to repair:")
            node = input().strip()
            if node not in net.nodes:
                print("Invalid node.")
            else:
                net.repair_node(node)
                print(f"Node {node} REPAIRED.")
        
        # Fail link
        elif cmd == '3':
            print("Enter link to fail (format: A B):")
            u, v = input().strip().split()
            if u not in net.nodes or v not in net.nodes:
                print("Invalid link nodes.")
            else:
                net.fail_link(u, v)
                print(f"Link {u}-{v} FAILED.")
        # Repair link
        elif cmd == '4':
            print("Enter link to repair (format: A B):")
            u, v = input().strip().split()
            if u not in net.nodes or v not in net.nodes:
                print("Invalid link nodes.")
            else:
                net.repair_link(u, v)
                print(f"Link {u}-{v} REPAIRED.")
        else:
            print("Invalid command format.")

        # Display all failures
        display_failures(net)

      
        path = dijkstra(net, start, goal)
        if path:
            print(f"Route from {start} to {goal}: {path}")
        else:
            print("No available path (network disconnected)")


if __name__ == "__main__":  # Main used as user interface
    print("Defining the network graph")
    print("1 = static  network")
    print("2 = Custom network")
    choice = input("Enter choice (1 or 2): ")

    # Load static or custom network based on user choice 1 = static , 2 = custom
    if choice == '1':

        # used to choose between manual fail/repair or random simulation R = random , F = manual fail/repair
        print("would you like manual fail/repair? or random simulation (F/R)")
        mode = input("Enter mode (F/R): ").strip().upper()
        if mode == 'R':
            net, start, goal = static_network()
            print("Using static network")
            print_graph(net)
            print("Start node:", start)
            print("Goal node:", goal)
            best_path = dijkstra(net, start, goal)
            print("Best path from", start, "to", goal, ":", best_path)
        else:
            net, start, goal = static_network()
            print("Using static network")
            print_graph(net)
            print("Start node:", start)
            print("Goal node:", goal)
            best_path = dijkstra(net, start, goal)
            print("Best path from", start, "to", goal, ":", best_path)
            manual_fail_repair(net, start, goal)

    elif choice == '2':
        # used to choose between manual fail/repair or random simulation R = random , F = manual fail/repair
        print("would you like manual fail/repair? or random simulation (F/R)")
        mode = input("Enter mode (F/R): ").strip().upper()
        if mode == 'R':
            print("Creating a custom network")
            net, start, goal = create_custom_network()
            print_graph(net)
            print("Start node:", start)
            print("Goal node:", goal)
            best_path = dijkstra(net, start, goal)
            print("Best path from", start, "to", goal, ":", best_path)
        else:
            print("Creating a custom network")
            net, start, goal = create_custom_network()
            print_graph(net)
            print("Start node:", start)
            print("Goal node:", goal)
            best_path = dijkstra(net, start, goal)
            print("Best path from", start, "to", goal, ":", best_path)
            manual_fail_repair(net, start, goal)
    else:
        print("Invalid choice. Exiting.")
        exit(1)

    # Random simulation mode
    for t in range(10):
        print(f"\n=== TIME STEP {t} ===")

        simulate_step(net, p_node_fail=0.05, p_link_fail=0.05)

        display_failures(net)

        path = dijkstra(net, start, goal)

        if path:
            print(f"Route from {start} to {goal}: {path}")
        else:
            print("No available path (network disconnected)")