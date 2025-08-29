# Question 7 Detecting Cycles in dependency graphs
"""
You are given a set of service dependencies represented as pairs (service, depends_on). This means service cannot start until depends_on is available.

IN
deps = [
    ("service-A", "service-B"),
    ("service-B", "service-C"),
    ("service-C", "service-A"),  # forms a cycle
    ("service-D", "service-E"),
]
OUT
True   # because A -> B -> C -> A is a cycle

IN
deps = [
    ("service-A", "service-B"),
    ("service-B", "service-C"),
    ("service-C", "service-D"),
]
OUT:
False

If K;V and v is also a K then k;v if v is a K and repeat
"""

def cycle_check(dependency):
    if not dependency:
        return False
    
    dep_list = {}
    for k,v in dependency:
         print(f"K: {k}, V: {v}")
         dep_list[k] = v
    print(dep_list)
def has_cycle(deps):
    adj = {}
    for s,d in deps:
        if s not in adj: adj[s] = []
        if d not in adj: adj[d] = []
        adj[s].append(d)
    
    visiting = set()
    visited = set()
    
    def dfs(u):
        if u in visiting:
            return True
        if u in visited:
            return False
        
        visiting.add(u)
        for v in adj[u]:
            if dfs(v):
                return True
        visiting.remove(u)
        visiting.add(u)
        return False
    for node in adj:
        if dfs(node):
            return True
        return False
    


if __name__ == "__main__":
    deps_a = [
    ("service-A", "service-B"),
    ("service-B", "service-C"),
    ("service-C", "service-A"),  
    ("service-D", "service-E"),]
    deps_b = [
    ("service-A", "service-B"),
    ("service-B", "service-C"),
    ("service-C", "service-D"),]
    print(cycle_check(deps_a))
    print(cycle_check(deps_b))
    print(has_cycle(deps_a))
    print(has_cycle(deps_b))


