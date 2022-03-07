# recursive function for reconstructing shortest path
def _print_path(path, v, u, route):
    if path[v][u] == v:
        return
    _print_path(path, v, path[v][u], route)
    route.append(path[v][u])

def get_shortest_route(path, v, u, route=None):
    if not route:
        route = [v]
    _print_path(path, v, u, route)
    route.append(u)
    return route

def solution(N, E, P, Q):
    # Build adjancency matrix, path variable is needed for path reconstruction
    adj_m = [[float('inf') for x in range(len(N))] for _ in range(len(N))]
    path = [[-1 for x in range(len(N))] for _ in range(len(N))]
    edge_names = {}
    for i in range(len(N)):
        adj_m[i][i] = 0
        path[i][i] = 0 
    for e in E:
        adj_m[e['src']][e['dest']] = e['dist']
        adj_m[e['dest']][e['src']] = e['dist']
        path[e['src']][e['dest']] = e['src']
        path[e['dest']][e['src']] = e['dest']
        edge_names[(e['src'], e['dest'])] = e['name']
        edge_names[(e['dest'], e['src'])] = e['name']
    

    n = len(N)
    dist_m = adj_m.copy()

    # Built distance matrix by solving all pair shortest path problem using Floyd Warshal Algorithm
    for k in range(n):
        for v in range(n):
            for u in range(n):
                # If vertex `k` is on the shortest path from `v` to `u`,
                # then update the value of cost[v][u] and path[v][u]
                if dist_m[v][k] != float('inf') and dist_m[k][u] != float('inf') \
                        and (dist_m[v][k] + dist_m[k][u] < dist_m[v][u]):
                    dist_m[v][u] = dist_m[v][k] + dist_m[k][u]
                    path[v][u] = path[k][u]

    # time complexity = O(N^3) where N is number of nodes
    # space complexity = O(N^2)

    

    # Assign packages to closest trains (This might not give an optimal solution with min travel time)
    # to make this simpler, a train will just deliver 1 package at a time.
    assignments = [[] for t in Q]
    total_time = 0
    for package in P:
        min_dist = float('inf')
        closest_train = 0
        for i, train in enumerate(Q):
            train_loc = train['start'] if len(assignments[i]) == 0 else assignments[i][-1]['src']
            curr_dist = dist_m[package['src']][train_loc]
            if min_dist > curr_dist and package['weight'] <= train['capacity']:
                min_dist = curr_dist
                closest_train = i
        assignments[closest_train].append(package)

    # Print moves
    for j, train in enumerate(Q):
        total_time = 0
        train_loc = train['start']
        print(f"Train {train['name']}")
        for package in assignments[j]:
            route = get_shortest_route(path, train_loc, package['src'])
            route = get_shortest_route(path, package['src'], package['dest'], route=route)
            
            for i in range(len(route)-1):
                loading = package['name'] if route[i] == package['src'] else ''
                dropping = package['name'] if route[i] == package['dest'] else ''
                print(f"@{total_time}, n={N[route[i]]}, q={train['name']}, load={{{loading}}}, drop={{{dropping}}}, moving {N[route[i]]}->{N[route[i+1]]}:{edge_names[(route[i], route[i+1])]}")
                total_time += dist_m[route[i]][route[i+1]]
            train_loc = package['dest']
            
            print(f"@{total_time}, n={N[route[-1]]}, q={train['name']}, load={{}}, drop={{{package['name']}}}")
        print()
    
    # An idea for optimal solution with bruteforce method is to generate all possible mapping of packages to trains.
    # Then find the package assigments with minimal time taking into account whether to pickup multiple package at once when fasterd
    
    # For more optimal solution, we should use algorithm suited for TSP (Traveling Salesman problem) or specifically CVRP (Capacitated Vehicle Routing Problem) 
    # E.g https://developers.google.com/optimization/routing/cvrp



if __name__ == '__main__':
    # Parsing user inputs
    n_stations = int(input())
    N = []
    for i in range(n_stations):
        N.append(input())

    n_routes = int(input())
    E = []
    for _ in range(n_routes):
        data = input().rstrip().split(',')
        E.append({
            'name':data[0],
            'src':N.index(data[1]), 
            'dest':N.index(data[2]), 
            'dist':int(data[3])
        })

    n_del = int(input())
    P = []
    for _ in range(n_del):
        data = input().rstrip().split(',')
        P.append({
            'name':data[0],
            'src':N.index(data[1]), 
            'dest':N.index(data[2]), 
            'weight':int(data[3])
        })

    n_trains = int(input())
    Q  = []
    for _ in range(n_trains):
        data = input().rstrip().split(',')
        Q.append({
            'name':data[0],
            'start':N.index(data[1]), 
            'capacity':int(data[2])
        })
    
    solution(N, E, P, Q)


