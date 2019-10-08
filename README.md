# geofence_splitter

1.  create venv
```
python3 -m venv venv
```
use it:
```
source venv/bin/activate
```

2. install requirements
```
python3 -m pip install -r requirements.txt
```

3. create geofence file:
```
[testfence]
48.0364214388757,7.7864475572312
48.0357327376794,7.8880710923875
47.9654368544995,7.9200001085007
47.9663563728372,7.7569218003953
```

4. configure `fence_divider.py`
At the bottom you see at the top of main function
```
    # geofence file with exactly 4 coords.
    FILE = "/home/bree/repos/geofence_divider/geofence.txt"
    FENCE_NAME = '[testfence]'
    # name of the resulting geofences, they will be enumerated like this: fr_quest1, fr_quest2, fr_quest3, ...
    OUT_FENCE_BASENAME = 'fr_quest'

    # 1 split = 4 fences, 2 splits = 16 fences, 3 splits = 64 fences, etc.
    SPLITS = 3
```

- FILE is your geofence file
- FENCE_NAME is the name of the geofence, including the brackets
- OUT_FENCE_BASENAME is the basename of the generated geofences.
- SPLITS is the amount of splits made. One split devides a geofence into 4 geofences. Two splits do the same recursively to every of the 4 geofences, so we end up with a total of 16. Three splits repeat and you end up with 64. Four will be 256.

5. run the script
`python3 fence_divider.py`

The output files are located in directory `out`
there is also a file `geojson.json`  which you can load on this site: [http://geo.jasparke.net/](http://geo.jasparke.net/) 
use it to verify that everything went as expected.
