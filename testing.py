import random
import point
import target as tg

"Checks if path generated is valid"
def check_if_path_correct(ordered_nexts, targets, radius):
    last = float("inf")
    for i in ordered_nexts:
        temp = [j for j in targets if i.euclidean_distance(j) <= radius]
        if len(temp) > last:
            return False
        else:
            for j in temp:
                targets.remove(j)
            last = len(temp)
    return True

"Generates randomized targets"
def generate_targets(number_targets):
    file = open("targets.txt", "w")
    for i in range(number_targets):
        file.write(str(random.random() * 360) + " " + str((random.random() * 180) - 90) + "\n")

"Runs Randomized Testing With number_targets random targets and radius radius"
def run_test(radius, number_targets):
    generate_targets(50)
    file = open("targets.txt", "r")
    targets = []
    for i in file:
        target = i.split(" ")
        target[1] = target[1][:-1]
        targets.append(point.Point(float(target[0]), float(target[1])))

    for i in targets:
        for j in targets:
            if i != j:
                i.add_target_if_fov(radius, j)

    path = tg.get_optimal_path(tg.get_nodes(radius, targets))

    print(check_if_path_correct(path, targets, radius))
