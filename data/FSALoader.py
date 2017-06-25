import database_operations as dbo
import fiona
import os

"""
In order to load into DB:
Polygon must be in format:

POLYGON((0 0,4 0,4 4,0 4,0 0),(1 1, 2 1, 2 2, 1 2,1 1))

MultiPolygon must be in format:

MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))
"""

class FSALoader():
    def __init__(self):
        self.conn = dbo.getConnection()
        self.filepath = "fsa_src/gfsa000b11a_e.shp"

    def polygon_str(self, coords):
        poly_strs = [str(p[0]) + ' ' + str(p[1]) for p in coords]
        poly_str = 'POLYGON((' + ','.join(poly_strs) + '))'
        return poly_str

    def multipolygon_str(self, polygons):
        poly_strs = []
        for polygon in polygons:
            base_poly_strs = [str(p[0]) + ' ' + str(p[1]) for p in polygon]
            poly_str = '((' + ','.join(base_poly_strs) + '))'
            poly_strs.append(poly_str)

        multipoly_str = 'MULTIPOLYGON(' + ', '.join(poly_strs) + ')'
        return multipoly_str

    def loadShapefile(self):
        print ('Parsing shapefile %s' % self.filepath)
        layer = fiona.open(self.filepath)

        poly_data = []
        multipoly_data = []
        for f in layer:
            d = dict(f['properties'])

            province = d['PRNAME']
            fsa = d['CFSAUID']
            geometry = f['geometry']

            ## convert tuple coordinates to list coordinates
            if geometry['type'] == 'Polygon':
                poly_str = self.polygon_str(geometry['coordinates'][0])
                poly_data.append((fsa, province, poly_str, None))
            elif geometry['type'] == 'MultiPolygon':
                coordinates = [polygon[0] for polygon in geometry['coordinates']]
                multipoly_str = self.multipolygon_str(coordinates)
                multipoly_data.append((fsa, province, multipoly_str, None))


        poly_query = "INSERT INTO fsa_polys VALUES (%s, %s, %s, %s)"
        multipoly_query = "INSERT INTO fsa_multi_polys VALUES (%s, %s, %s, %s)"

        dbo.execute_query(self.conn, poly_query, poly_data,
                                    multiple=True)
        dbo.execute_query(self.conn, multipoly_query, multipoly_data,
                                    multiple=True)
        self.conn.close()
        return



loader = FSALoader()
loader.loadShapefile()
