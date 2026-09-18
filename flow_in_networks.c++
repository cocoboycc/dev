#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
#include <limits>

class Edge {
public:

    unsigned int from;
    unsigned int to;
    unsigned int capacity;
    unsigned int flow;

    Edge(unsigned int from, unsigned int to,
         unsigned int capacity, unsigned int flow)
        : from(from), to(to), capacity(capacity), flow(flow) {}
};

class Graph {
public:

    unsigned int n;
    std::vector<Edge> edges;
    std::vector<std::vector<Edge>> adj;

    // parent[v] = edge that was used to reach v
    std::vector<Edge> parent;

    Graph(unsigned int n)
        : n(n), adj(n), parent(n, Edge(0, 0, 0, 0)) {}

    void add_edge(unsigned int from, unsigned int to,
                  unsigned int capacity) {

        Edge edge(from, to, capacity, 0);

        edges.push_back(edge);
        adj[from].push_back(edge);

        // Reverse edge
        Edge reverse(to, from, 0, 0);
        adj[to].push_back(reverse);
    }

    bool BFS(unsigned int s, unsigned int t);
};


bool Graph::BFS(unsigned int s, unsigned int t) {

    std::vector<bool> visited(n, false);
    std::queue<unsigned int> q;

    q.push(s);
    visited[s] = true;

    while (!q.empty()) {

        unsigned int u = q.front();
        q.pop();

        for (auto edge : adj[u]) {

            // Only use edges with remaining capacity
            if (!visited[edge.to] &&
                edge.capacity > edge.flow) {

                visited[edge.to] = true;

                // Remember how we reached this vertex
                parent[edge.to] = edge;

                q.push(edge.to);

                if (edge.to == t) {
                    return true;
                }
            }
        }
    }

    return false;
}


unsigned int max_flow(Graph G, unsigned int s, unsigned int t) {

    unsigned int flow = 0;

    while (G.BFS(s, t)) {

        // Find bottleneck of path
        unsigned int path_flow =
            std::numeric_limits<unsigned int>::max();

        unsigned int v = t;

        while (v != s) {

            Edge edge = G.parent[v];

            path_flow = std::min(
                path_flow,
                edge.capacity - edge.flow
            );

            v = edge.from;
        }


        // Update flow along path
        v = t;

        while (v != s) {

            Edge edge = G.parent[v];

            // edit edge flow
            for (auto &e : G.adj[edge.from]) {

                if (e.to == edge.to) {
                    e.flow += path_flow;
                    break;
                }
            }

            // edit reverse edge flow
            for (auto &e : G.adj[edge.to]) {

                if (e.to == edge.from) {
                    e.flow -= path_flow;
                    break;
                }
            }

            v = edge.from;
        }

        flow += path_flow;
    }

    return flow;
}

int main() {
    unsigned int n; 
    std::cin>>n; 
    Graph G(n); 

    G.add_edge(0, 1, 10);
    G.add_edge(0, 2, 5);
    G.add_edge(1, 2, 15);
    G.add_edge(1, 3, 10);
    G.add_edge(2, 3, 10);
    std::cout << max_flow(G, 0, 3) << std::endl;

    return 0; 
}