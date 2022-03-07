# Capacitated Vehicle Routing Problem with Pickup Delivery
## Question
You have been asked to write a control program for a mail train system.
The system takes as inputs:

- A graph containing a set of nodes, N, and edges, E : N → N. Each edge has a (positive) journey time e_t – this is the number of time steps that it takes a train to travel along an edge (in either direction).
- Each node contains a set of packages. Each package has an integer weight, W_p and a destination node D_p.
- You have a set of trains Q, each of which has an integer capacity, C_q. Each train is located at a starting node.
- Trains start off empty.


Your program should output a list of moves. Each move has:

- A time (t) at which the move happens.
- A node (n) at which the move happens.
- A train, (q) making the move.
- A set of packages (O) to move onto the train at this node.
- A set of packages (P) to move off the train at this node.
- An edge (e) for the train to move down. Each move, the train t must be at node n. It offloads the packages O onto the node, picks up the packages P and then travels down edge e, arriving at t + e_t
- O and P may be empty.
- You cannot overload the train (the sum of the weights of all packages in P must be smaller
than or equal to C_q)
- E may be the special value ‘null’, meaning that the train stays at n.
- O must be a subset of the letters currently located at n.
- Once a train has started down an edge, E: n1 → n2 it cannot be called back. It will arrive at n2 in e_t time units.
- A train can only be in one place at once. A train may only traverse an edge if it is at one node or the other of that edge.
- No train may ever be overloaded.
- Any number of trains can be at the same node at the same time.
- A train can carry any number of letters, so long as the total weight of the letters is <= the capacity of the train.
- Any number of trains may traverse the same edge at the same time (this is somewhat unrealistic, but makes the problem easier to solve)


At the end of your sequence of moves, all letters must have been moved off a train to their
destination nodes.

It would obviously be nice to generate a minimal (or at least relatively short) sequence of moves, but
correctness is more important than optimality.

Optimality, is measured by the maximum time of any move (ie. we are interested in schedules which
minimise the time it takes to deliver the letters rather than that minimise the number of moves).

We don't care where the trains end up at the end of the sequence of moves.

### Example
```
// example input
3 // number of stations
A // station name
B // station name
C // station name

2 // number of routes
E1,A,B,3 // route from A to B that takes 3 units of time
E2,B,C,1 // route from B to C that takes 1 unit of time

1 // number of deliveries to be performed
P1,A,C,5 // package P1 with weight 5 located currently at station A that must be delivered to station C

1 // number of trains
Q1,B,6 // train T1 with capacity 6 located at station B

// example output
@0, n = B, q = Q1, load= { }, drop= { }, moving B->A:E1 arr 3
@3, n = A, q = Q1, load= { D1 }, drop= { }, moving B->C:E2 arr 4
```

## Solution
### Assumption
Since no constrain was given for the input, we assume the following to be true:
- 1 <= N
- 1 <= E
- 1 <= P
- 1 <= Q
- There is always a possible path for each package pickup and delivery
- Any package weight does not exceed the max capacity of any vehicle

### Algorithm
Since the question does not necessarily ask for optimal solution (min time), we make the problem/solution simpler by only using a train to deliver 1 package at a time.

First we calculate the shortest distance between each node, hence this become All Pair Shortest Problem. We can use the Floyd Warshal algorithm, to do this, and it has O(N^3) time complexity and n^2 space complexity, where N is the number of nodes.

Then, we loop through each package and assign the closest train to pickup and deliver. We also keep track the location of the train after moving.

The method above may not give the most optimal solution (min travel time) as it is actually possible to pickup multiple packages at once before delivering and this may have faster solution.

### Afterthought
For a better algorithm, we should use algorithm used to solve TSP (Traveling Salesman Problem), or VRP (Vehicle Routing Problem) such as flow formulations, or meta heuristic algorithms eg. Genetic Algorithm, Tabu search, etc.

Note that this problem is variant of VRP with additional properties such as:
- Capacity constrains
- Pickup and delivery
- Open Vehicle Routing (not required to return to depot)
- Multiple trips (Vechicles can do more than one route)
- Multi Depot (vehicles can start from multiple points)

### Testcases
`input1.txt`
```
3
A
B
C
2
E1,A,B,3
E2,B,C,1
1
P1,A,C,5
1
Q1,B,6
```
Command
```
cat input1.txt | python main.py
```
Output
```
Train Q1
@0, n=B, q=Q1, load={}, drop={}, moving B->A:E1
@3, n=A, q=Q1, load={P1}, drop={}, moving A->B:E1
@6, n=B, q=Q1, load={}, drop={}, moving B->C:E2
@7, n=C, q=Q1, load={}, drop={P1}
```
`input2.txt`
```
4
A
B
C
D
3
E1,A,B,3
E2,B,C,1
E3,C,D,2
3
P1,A,C,5
P2,B,D,5
P3,A,D,8
2
Q1,B,10
Q2,C,6 
```
Command
```
cat input2.txt | python main.py
```
Output
```
Train Q1
@0, n=B, q=Q1, load={}, drop={}, moving B->A:E1
@3, n=A, q=Q1, load={P1}, drop={}, moving A->B:E1
@6, n=B, q=Q1, load={}, drop={}, moving B->C:E2
@7, n=C, q=Q1, load={}, drop={P1}
@7, n=C, q=Q1, load={}, drop={}, moving C->B:E2
@8, n=B, q=Q1, load={}, drop={}, moving B->A:E1
@11, n=A, q=Q1, load={P3}, drop={}, moving A->B:E1
@14, n=B, q=Q1, load={}, drop={}, moving B->C:E2
@15, n=C, q=Q1, load={}, drop={}, moving C->D:E3
@17, n=D, q=Q1, load={}, drop={P3}

Train Q2
@0, n=C, q=Q2, load={}, drop={}, moving C->B:E2
@1, n=B, q=Q2, load={P2}, drop={}, moving B->C:E2
@2, n=C, q=Q2, load={}, drop={}, moving C->D:E3
@4, n=D, q=Q2, load={}, drop={P2}
```







