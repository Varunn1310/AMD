#include <iostream>
#include <bits/stdc++.h>

using namespace std;

class Graph{
    int V;
    vector<list<int>> adj;
 public:

    Graph(int V);
    void add_Edge(int n, int w);
    void BFS(int s);
    bool is_Reachable(int s, int d);
};

Graph::Graph(int V){
    this->V=V;
    adj.resize(V);
}

void Graph::add_Edge(int n, int w){
    adj[n].push_back(w);
}

void Graph::BFS(int s){
    vector<bool> visited;
    visited.resize(V, false);
    list<int> queue;
    visited[s]=true;
    queue.push_back(s);
    
    while(!queue.empty()){
        s = queue.front();
        cout<<"->"<<s;
        queue.pop_front();
        list<int>::iterator i;
        for(i=adj[s].begin();i != adj[s].end(); ++i){
            if(!visited[*i]){
                visited[*i]=true;
                queue.push_back(*i);
            }
        }
    }

}

bool Graph::is_Reachable(int s, int d){
    if(s==d)
        return true;
    vector<bool> visited;
    visited.resize(V, false);
    list<int> queue;
    visited[s]=true;
    queue.push_back(s);

    while(!queue.empty()){
        queue.pop_front();
        list<int>::iterator i;
        for(i=adj[s].begin();i != adj[s].end(); ++i){
            if(*i == d){
                return true;
            }
            if(!visited[*i]){
                visited[*i]=true;
                queue.push_back(*i);
            }
        }
    }
    return false;
}

int main(){
    Graph g(4);
    g.add_Edge(0, 1);
    g.add_Edge(0, 2);
    g.add_Edge(1, 2);
    g.add_Edge(2, 0);
    g.add_Edge(2, 3);
    g.add_Edge(3, 3);

    int source = 0, destination = 1;
    if(g.is_Reachable(source, destination))
        cout<< "\n There is a path from " << source << " to " << destination;
    else
        cout<< "\n There is no path from " << source << " to " << destination;
    return 0;
}