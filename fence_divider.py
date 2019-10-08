from geofencehelper import  GeofenceHelper
import random

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
    print(geojson)


if __name__ == '__main__':
    file = "/home/bree/repos/geofence_divider/geofence.txt"
    geo = GeofenceHelper(geofencefile=file)
    testfence = geo.geofence_to_coordinates['[testfence]']
    splitted_fences = []
    geo.divide_recursively(testfence, 3, splitted_fences)
    f_id = 1
    for fence in splitted_fences:
        print(f'[fence{f_id}]')
        f_id += 1
        for point in fence:
            print(f'{point.x},{point.y}')
    dump_to_geojson(splitted_fences)
