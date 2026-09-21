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
    int flow;                  // signed, because reverse flow can be negative
    unsigned int reverse;      // index of the corresponding reverse edge

    Edge(unsigned int from,
         unsigned int to,
         unsigned int capacity,
         int flow,
         unsigned int reverse)
        : from(from),
          to(to),
          capacity(capacity),
          flow(flow),
          reverse(reverse) {}

    // FIX: centralize the residual-capacity computation and do it in a
    // signed type (long long is plenty for realistic capacities). Every
    // place that needs "how much more can flow through this edge" should
    // go through this function instead of comparing/subtracting
    // `capacity` (unsigned) and `flow` (signed) directly, which silently
    // converts negative flow into a huge unsigned number and breaks both
    // comparisons and reasoning about reverse edges.
    long long residual_capacity() const {
        return static_cast<long long>(capacity) - static_cast<long long>(flow);
    }
};


class Graph {
public:

    unsigned int n;

    std::vector<std::vector<Edge>> adj;

    // parent[v] = {previous vertex, index of edge in adj[previous vertex]}
    std::vector<std::pair<unsigned int, unsigned int>> parent;


    Graph(unsigned int n)
        : n(n),
          adj(n),
          parent(n, {n, 0}) {}


    void add_edge(unsigned int from,
                  unsigned int to,
                  unsigned int capacity) {

        // Index where the forward edge will be stored
        unsigned int forward_index = adj[from].size();

        // Index where the reverse edge will be stored
        unsigned int reverse_index = adj[to].size();

        Edge forward(
            from,
            to,
            capacity,
            0,
            reverse_index
        );

        Edge reverse(
            to,
            from,
            0,
            0,
            forward_index
        );

        adj[from].push_back(forward);
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


        for (unsigned int i = 0; i < adj[u].size(); i++) {

            const Edge &edge = adj[u][i];

            if (!visited[edge.to] &&
                edge.residual_capacity() > 0) {

                visited[edge.to] = true;

                // Remember exactly which edge brought us here
                parent[edge.to] = {u, i};

                q.push(edge.to);


                if (edge.to == t) {
                    return true;
                }
            }
        }
    }

    return false;
}


unsigned int max_flow(Graph G,
                      unsigned int s,
                      unsigned int t) {

    unsigned int flow = 0;


    while (G.BFS(s, t)) {

        // -------------------------------------------------
        // 1. Find bottleneck of augmenting path
        // -------------------------------------------------

        long long path_flow = std::numeric_limits<long long>::max();

        unsigned int v = t;


        while (v != s) {

            unsigned int u = G.parent[v].first;
            unsigned int edge_index = G.parent[v].second;

            Edge &edge = G.adj[u][edge_index];

            long long residual_capacity = edge.residual_capacity();

            path_flow = std::min(path_flow, residual_capacity);

            v = u;
        }


        // -------------------------------------------------
        // 2. Send flow through the path
        // -------------------------------------------------

        v = t;


        while (v != s) {

            unsigned int u = G.parent[v].first;
            unsigned int edge_index = G.parent[v].second;

            Edge &edge = G.adj[u][edge_index];


            // Increase flow on current edge
            edge.flow += static_cast<int>(path_flow);


            // Find corresponding reverse edge
            Edge &reverse_edge =
                G.adj[edge.to][edge.reverse];


            // Decrease reverse flow
            reverse_edge.flow -= static_cast<int>(path_flow);


            // Move backwards through the path
            v = u;
        }


        flow += static_cast<unsigned int>(path_flow);
    }


    return flow;
}


int main() {

    Graph G(8);

    G.add_edge(0, 3, 1);
    G.add_edge(0, 1, 1);

    G.add_edge(3, 4, 1);
    G.add_edge(4, 7, 1);

    G.add_edge(3, 5, 1);
    G.add_edge(5, 6, 1);
    G.add_edge(6, 7, 1);

    G.add_edge(1, 2, 1);
    G.add_edge(2, 4, 1);


    std::cout << max_flow(G, 0, 7) << std::endl;

    return 0;
}