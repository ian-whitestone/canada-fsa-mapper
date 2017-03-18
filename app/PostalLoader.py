import fiona
import os

cwd = os.getcwd()
print (cwd)

shapefile = './app/data/pshape/CanadaPostalCodePolygons.shp'
shapefile = './app/data/arcgis/gfsa000b11a_e.shp'


def getCanadaFSA():
    print ('Parsing shapefiles for %s' % shapefile)
    layer = fiona.open(shapefile)

    fsa_list = []
    for f in layer:
        d = dict(f['properties'])

        if d['PRNAME'] == 'Ontario' and d['CFSAUID'][0] == 'M':
            geom = f['geometry']

            ## convert tuple coordinates to list coordinates
            if geom['type'] == 'Polygon':
                # print (geom)
                pass
            elif geom['type'] == 'MultiPolygon':
                coordinates = [[[list(tuple_coord) for tuple_coord in polygon[0]]] for polygon in geom['coordinates']]
                geom['coordinates'] = coordinates
            fsa_list.append(geom)
    return fsa_list

# get_fsa()

# with fiona.drivers():
#     for layername in fiona.listlayers('./pshape'):
#         with fiona.open('./pshape/', layer=layername) as src:
#             print(layername, len(src))
