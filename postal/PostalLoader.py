import fiona

shapefile = './pshape/CanadaPostalCodePolygons.shp'
shapefile = './arcgis/gfsa000b11a_e.shp'

print ('Parsing shapefiles for %s' % shapefile)
layer = fiona.open(shapefile)
# print (layer['geometries'])




i=0
for f in layer:
    d = dict(f['properties'])
    print (d)
    # print (f['geometry'])
    i+=1
    if i == 1:
        break

#
# with fiona.drivers():
#     for layername in fiona.listlayers('./pshape'):
#         with fiona.open('./pshape/', layer=layername) as src:
#             print(layername, len(src))
