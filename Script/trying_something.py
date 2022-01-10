import textwrap
import Lowland

geogr = """\
           WWW
           WLW
           WWW"""
geogr = textwrap.dedent(geogr)

newGeogr = geogr.split()

geogrDict = {}
for i in range(len(newGeogr)):
    for j in range(len(newGeogr[0])):
        geogrDict['({0}, {1})'.format(i+1, j+1)] = newGeogr[i][j]
print(geogrDict)

