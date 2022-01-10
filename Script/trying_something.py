import textwrap
import Lowland

geogr = """\
           WWW
           WLD
           WWW"""
geogr = textwrap.dedent(geogr)

newGeogr = geogr.split()

geogrDict = {}
emptyGeogrDict = {}
for i in range(len(newGeogr)):
    for j in range(len(newGeogr[0])):
        geogrDict['({0}, {1})'.format(i+1, j+1)] = newGeogr[i][j]
        if newGeogr[i][j] != 'W':
            emptyGeogrDict['({0}, {1})'.format(i+1, j+1)] = []
print(geogrDict)
print(emptyGeogrDict)

