import math

class Point:

    def __init__(self, right_ascension, declination):
        self.right_ascension = right_ascension
        self.declination = declination + 90
        self.points_in_fov = dict()

    def in_fov_at_point(self, radius, point):
        if self.euclidean_distance(point) <= 2 * radius:
            return True
        return False

    def euclidean_distance(self, point):
        return math.sqrt((self.right_ascension - point.right_ascension)**2 + (self.declination - point.declination)**2)

    def add_target_if_fov(self, radius, point):
        if self.in_fov_at_point(radius, point):
            if radius is self.points_in_fov.keys():
                checker = []
                to_add = []
                for i in self.points_in_fov[radius].append(point):
                    for j in i:
                        if j.in_fov_at_point(radius, point):
                            checker.append(j)
                    if len(checker) == len(i):
                        i.append(point)
                    else:
                        checker.append(point)
                        to_add.append(checker)
                        checker = []
                self.points_in_fov[radius].extend(to_add + [self])
            else:
                self.points_in_fov[radius] = [[point, self]]
            return True
        return False

    def __eq__(self, other):
        if self.right_ascension == other.right_ascension and self.declination == other.declination:
            return True
        return False

    def __ne__(self, other):
        if self.right_ascension != other.right_ascension or self.declination != other.declination:
            return True
        return False

class FOVNode:

    def __init__(self, center, targets):
        self.center = center
        self.targets = targets
        self.adjacency_list = []
