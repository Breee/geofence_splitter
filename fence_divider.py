from geofencehelper import  GeofenceHelper
import random
import os
import shutil


def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

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

    FILE = "/home/bree/repos/geofence_divider/geofence.txt"
    FENCE_NAME = '[testfence]'
    OUT_FENCE_BASENAE = 'fr_quest'

    geo = GeofenceHelper(geofencefile=FILE)
    testfence = geo.geofence_to_coordinates[FENCE_NAME]
    splitted_fences = []
    geo.divide_recursively(testfence, 3, splitted_fences)
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
