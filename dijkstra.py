import heapq

def find_shortest_paths(origin, get_neighbors):
    """Shorted path to every point in the territory"""
    dists = {}
    preds = {}
    todo = [(0, origin, None)]
    while todo:
        d, cur, prev = heapq.heappop(todo)
        dists[cur] = d
        preds[cur] = prev
        for x in get_neighbors(cur, preds):
            if x not in dists:
                heapq.heappush(todo, (d + 1, x, cur))
        # if len(preds) == 500:
        #     return preds
    return preds, dists

def path_to(target, preds):
    path = [target]
    while preds[target] is not None:
        target = preds[target]
        path.append(target)
    return list(reversed(path))
        
        
def steps_to(target, preds):
    path = path_to(target, preds)
    steps = []
    for i in range(len(path) - 1):
        from_x, from_y = path[i]
        to_x, to_y = path[i + 1]
        step = to_x - from_x, to_y - from_y
        steps.append(step)
    return steps
    
    
    
