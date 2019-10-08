from geofencehelper import  GeofenceHelper
import random
import os

def dump_to_geojson(fences):
    geojson = '['
    fence_dicts = []
    for id,fence in enumerate(fences):
        path = [[point.x,point.y] for point in fence]
        fence_dict = '{' + f' "name": "fence{id}", "color": "#33cccc", "id": {random.randint(0,4000)},"path": {path}' +'}\n'
        fence_dicts.append(fence_dict)
    geojson += ','.join(fence_dicts)
    geojson += ']'
    with open(f"./out/geojson.json", 'w') as geojson_file:
        geojson_file.write(geojson)


if __name__ == '__main__':

    # geofence file with exactly 4 coords.
    FILE = "/home/bree/repos/geofence_divider/geofence.txt"
    FENCE_NAME = '[testfence]'
    # name of the resulting geofences, they will be enumerated like this: fr_quest1, fr_quest2, fr_quest3, ...
    OUT_FENCE_BASENAE = 'fr_quest'

    # 1 split = 4 fences, 2 splits = 16 fences, 3 splits = 64 fences, etc.
    SPLITS = 3

    geofence_helper = GeofenceHelper(geofencefile=FILE)
    geofence = geofence_helper.geofence_to_coordinates[FENCE_NAME]

    splitted_fences = []
    geofence_helper.divide_recursively(geofence, SPLITS, splitted_fences)
    f_id = 1
    if not os.path.exists('./out'):
        os.mkdir('./out')
    for fence in splitted_fences:
        with open(f"./out/{OUT_FENCE_BASENAE}{f_id}.txt", 'w') as geofence_file:
            geofence_file.write(f'[{OUT_FENCE_BASENAE}{f_id}]\n')
            f_id += 1
            points = []
            for point in fence:
                points.append(f'{point.x},{point.y}')
            geofence_file.write('\n'.join(points))
    dump_to_geojson(splitted_fences)
