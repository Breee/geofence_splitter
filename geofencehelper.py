from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class GeofenceHelper(object):
    def __init__(self, geofencefile):
        logger.info("Initializing GeofenceHelper")
        self.geofences = dict()
        self.geofence_to_coordinates = GeofenceHelper.read_geofence_file(geofencefile)
        for geofence, coordinates in self.geofence_to_coordinates.items():
            self.geofences[geofence] = Polygon([(c.x, c.y) for c in coordinates])

    @staticmethod
    def read_geofence_file(geofence_file) -> Dict[str, List[Point]]:
        """
        Method which reads a geofence file and returns a dictionary with a mapping GEOFENCE -> COORDINATES
        :param geofence_file: A file containing a geofence.
        :return: Dict[str, List[Point]]
        """
        logger.info("Reading geofence file: %s" % geofence_file)
        current_fence = 'unnamed'
        geofence_to_coordinates = dict()
        with open(geofence_file, 'r') as fence:
            for line in fence:
                if line.startswith('['):
                    current_fence = line.replace("\n", '')
                else:
                    line = line.replace("\n", '')
                    lat, lon = line.split(",")
                    if current_fence not in geofence_to_coordinates:
                        geofence_to_coordinates[current_fence] = []
                    geofence_to_coordinates[current_fence].append(Point(float(lat), float(lon)))
        return geofence_to_coordinates

    def is_in_any_geofence(self, coordinate: Point):
        for name, geofence in self.geofences.items():
            if coordinate.within(geofence):
                logger.debug("coordinate: %s is in geofence: %s" % (coordinate, name))
                return True
        logger.debug("coordinate: %s not in any geofence" % coordinate)
        return False

    def filter_coordinates(self, coordinates: List[Point]) -> Tuple[List[Point], List[Point]]:
        inside = []
        outside = []
        for coord in coordinates:
            if self.is_in_any_geofence(coord):
                inside.append(coord)
            else:
                outside.append(coord)
        return inside, outside

    def calc_midpoint(self, point1: Point, point2: Point) -> Point:
        return Point((point1.x + point2.x) / 2, (point1.y + point2.y) / 2)

    def divide_fence(self, coordinates: List[Point]) -> List[List[Point]]:
        assert len(coordinates) == 4, 'You can only devide fences with 4 coordinates (rectangles), '
        a = coordinates[0]
        b = coordinates[1]
        c = coordinates[2]
        d = coordinates[3]

        e = self.calc_midpoint(a,b)
        f = self.calc_midpoint(a,d)
        h = self.calc_midpoint(b,c)
        i = self.calc_midpoint(c,d)
        g = self.calc_midpoint(e,i)

        fence1 = [a,e,g,f]
        fence2 = [e,b,h,g]
        fence3 = [f,g,i,d]
        fence4 = [g,h,c,i]

        return [fence1,fence2,fence3,fence4]

    def divide_recursively(self, coordinates : List[Point], num_splits: int, fence_list):
        fences = self.divide_fence(coordinates)
        num_splits -= 1
        if num_splits == 0:
            for fence in fences:
                fence_list.append(fence)
            return fences
        else:
            for fence in fences:
                self.divide_recursively(fence, num_splits, fence_list)




