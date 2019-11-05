import math

"""Point Class, used for targets and center points of FOV's"""
class Point:

    """Constructor, based on right_ascension and declination of the point.
       To allow for "nice" distancing, we add 90 to the declination when we store
       so that the range of values for the point's coordinates are [0, 360) degrees
       for right_ascension and [0, 180] degrees for declination"""
    def __init__(self, right_ascension, declination):
        self.right_ascension = right_ascension
        self.declination = declination + 90
        self.points_in_fov = dict()

    """Method to check if the given point is within the given radius of self"""
    def in_fov_at_point(self, radius, point):
        if self.euclidean_distance(point) <= 2 * radius:
            return True
        return False

    """Method to get the simple euclidean distance between self and the given point"""
    def euclidean_distance(self, point):
        return math.sqrt((self.right_ascension - point.right_ascension)**2 + (self.declination - point.declination)**2)

    """Method to add target to self.points_in_fov if it is within the given radius of the point"""
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

    """Equals override for point"""
    def __eq__(self, other):
        if self.right_ascension == other.right_ascension and self.declination == other.declination:
            return True
        return False

    """Not equals override for point"""
    def __ne__(self, other):
        if self.right_ascension != other.right_ascension or self.declination != other.declination:
            return True
        return False

"""FOVNode Class, gives node that contains given targets and is located at a center point"""
class FOVNode:

    """Simple Constructor that stores the center point and targets for the FOVNode"""
    def __init__(self, center, targets):
        self.center = center
        self.targets = targets
        self.adjacency_list = []
