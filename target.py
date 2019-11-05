import point

"""Method that gets a the centroid for a given list of targets"""
def get_fov_center_point(targets):
    return point.Point(sum([t.right_ascension for t in targets]) / len(targets), sum([t.declination - 90 for t in targets]) / len(targets))

"""Method that returns a tuple containing the most targets within the FOV of the given
radius of the input target that also includes the input target"""
def get_most_targets_fov(radius, target):
    targets = max(target.points_in_fov[radius], key=lambda x: len(x))
    targets.append(target)
    return (get_fov_center_point(targets), targets)

"""Method that creates a list of FOVNodes from the given radius and the targets"""
def get_nodes(radius, targets):
    nodes = []
    while targets:
        temp_nodes = []
        for i in targets:
            temp_nodes.append(get_most_targets_fov(radius, i))
        max_node = max(temp_nodes, key=lambda x: len(x[1]))
        nodes.append(point.FOVNode(max_node[0], max_node[1]))
        for i in nodes[-1:].targets:
            targets.remove(i)
    for i in nodes:
        for j in nodes:
            if i.center != j.center:
                j.adjacency_list.append((i, j.euclidean_distance(i)))
    return nodes

"""Method that returns an ordered list that gives the optimal observation path,
currently based on the FOVNode, which gives the greatest targets for the its distance"""
def get_optimal_path(nodes):
    nodes = sorted(nodes, key=lambda x: len(x.targets))
    ordered_nexts = []
    for i in nodes:
        list_pull_from = [j for j in i.adjacency_list if j[0] not in ordered_nexts]
        ordered_nexts.append(max(list_pull_from, key=lambda x: len(x[0].targets) / x[1])[0])
    return ordered_nexts
