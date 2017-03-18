import fiona
import os

cwd = os.getcwd()
print (cwd)

shapefile = './app/data/pshape/CanadaPostalCodePolygons.shp'
shapefile = './app/data/arcgis/gfsa000b11a_e.shp'


def get_fsa():
    print ('Parsing shapefiles for %s' % shapefile)
    layer = fiona.open(shapefile)
    # print (layer['geometries'])

    for f in layer:
        d = dict(f['properties'])
        if d['PRNAME'] == 'Ontario' and d['CFSAUID'] == 'M4Y':
            return f['geometry']


# with fiona.drivers():
#     for layername in fiona.listlayers('./pshape'):
#         with fiona.open('./pshape/', layer=layername) as src:
#             print(layername, len(src))
