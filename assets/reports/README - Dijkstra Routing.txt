README

Project Topic 4: Dynamic routing mechanism design in faulty network
Group: Tristan Ramirez, Minh Huy Tran, Rei Thao

Overview: 
This program simulates network routing on a graph while allowing nodes and links to fail and be repaired.
The program uses Dijkstra’s algorithm to find the shortest path even when we have fail nodes and links.

Network Types:
   1. static built-in network
   2. custom user-defined network. You will need to enter:
      - Node names
      - Links (u v w format)
      - Start and goal nodes	

Failure Modes:
   1. Manual failure/repair mode
   2. Random failure simulation mode

How to Run Program:
   1. Download "DRTN.py" file
   2. Open terminal or command prompt and navigate to the file's directory. Command: "cd [FILE PATH]"
   3. Run file. Command: "python3 DRTN.py"

When the program runs, you will see a menu. This loads a predefined 9-node grid network from N1 to N9.
Example:
   Nodes: A B C D
   Link: A B 3
   Link: B C 2
   Link: C D 4
   done
   Start: A
   Goal: D

After choosing the network, you must choose between manual fail/repair or random simulation (F/R).
Under random simulation nodes and links may fail with 5% probability per timestep. 
The simulation runs for 10 timesteps automatically.

F - Manual Mode Scenario:
   1. fail node X
   2. repair node X
   3. fail link A B
   4. repair link A B
Enter option and type "done" when finished:
Example:
   1 
   Enter node to fail: 
   N5
   3
   Enter link to fail (format: A B):
   N2 N5

   done

R - Random Failure Simulation Scenario:
Example:
   === TIME STEP 0 ===
   Failed Nodes: []
   Failed Links: []
   Route from N1 to N9: ['N1', 'N2', 'N3', 'N6', 'N9']

Simulation Output:
   - All failed nodes
   - All failed links
   - Best available path from start → goal

Example:
   Failed Nodes: ['N3']
   Failed Links: [('N5', 'N6')]
   No available path (network disconnected)