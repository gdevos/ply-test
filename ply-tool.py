#!/usr/bin/python
'''
Gerard de Vos

Usage: ./ply-tool.py -h

A few simple tests handling PLY polygon files
http://www.dcs.ed.ac.uk/teaching/cs4/www/graphics/Web/ply.html

Uses https://github.com/dranjan/python-plyfile and, in turn, NumPy
Shapely does the hard Geo work http://toblerity.org/shapely/manual.html
'''

from argparse import ArgumentParser

import numpy

from plyfile import PlyData, PlyElement

from shapely.geometry import Polygon, Point, MultiPoint
from shapely.wkt import dumps, loads

def main():
    parser = ArgumentParser()

    # subparsers for 'intersection' and 'write'
    subparsers = parser.add_subparsers(help='subcommands')

    # intersection command
    intersection_parser = subparsers.add_parser('intersection', help='Determine intersection')
    intersection_parser.add_argument('plyfile', action='store', help='Input PLY filename')
    intersection_parser.add_argument('boundingbox', help='string in WKT POLYGON format for the bounding box e.g. "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))" ')
    intersection_parser.add_argument('outfile', help='output filename')
    intersection_parser.set_defaults(func=intersection)

    # write command
    write_parser = subparsers.add_parser('write', help='Write new PLY file from intermediary file')
    write_parser.add_argument('infile', action='store', help='Intermediary filename')
    write_parser.add_argument('output_ply_file', help='Output PLY filename')
    write_parser.set_defaults(func=write)

    # simple fileinfo functions
    fileinfo_parser = subparsers.add_parser('fileinfo', help='Show some info on PLY file')
    fileinfo_parser.add_argument('plyfile', help='Input PLY filename')
    fileinfo_parser.set_defaults(func=fileinfo)

    args = parser.parse_args()
    #print args

    # Call whatever function was supplied as the subcommand
    args.func(args)

def intersection(args):
    '''
    Reads ply, applies boundingbox and writes matching polygon/cuboid
    '''
    # ./ply-tool.py intersection test_data/house1.ply "POLYGON ((30 10, 80 80, 20 40, 0 10, 30 10))" bla2

    print "Plyfile=", args.plyfile
    print "Boundingbox=", args.boundingbox
    print "Outfile=", args.outfile

    # Open outfile for appending
    outf = open(args.outfile, 'a')

    # Load WKT into shapely polygon
    bbox = Polygon(loads(args.boundingbox))
    #print bbox
    #print bbox.area
    #print bbox.length

    # Reading the PLY file
    ply = PlyData.read(args.plyfile)

    # Loop through polygons
    poly_count = ply['polygon'].count
    for poly_i in range(0,poly_count):
        # List of vertice tuples
        vtcs = ply['vertex'][ply['polygon'][poly_i].tolist()].tolist()
        # into shapely Polygon
        poly = Polygon(vtcs)
        #print poly
        # Shapely intersects() does the job nicely
        print "Polygon", poly_i, "intersects=", bbox.intersects(poly)
        if bbox.intersects(poly):
            # to WKT
            polywkt = dumps(poly) + '\n'
            print "Adding to file", polywkt
            outf.write(polywkt)

    # Loop through cuboids
    cube_count = ply['cuboid'].count
    for cub_i in range(0,cube_count):
        # List of vertice tuples
        vtcs = ply['vertex'][ply['cuboid'][cub_i].tolist()].tolist()
        print vtcs
        # into multipoint for now. should be polyhedron(?) I think but shapely doesn't have that
        mp = MultiPoint(vtcs)
        print mp
        # Shapely intersects() does the job nicely
        print "Cuboid", cub_i, "intersects=", bbox.intersects(mp)
        if bbox.intersects(mp):
            # to WKT
            mpwkt = dumps(mp) + '\n'
            print "Adding to file", mpwkt
            outf.write(mpwkt)

    #write intermediary file
    outf.close()

def write(args):
    '''
    Reads intermediary WKT file and writes it as a PLY file
    '''
    #./ply-tool.py write intermediaryfile outfile.ply
    print "intermediaryfile=", args.infile
    print "output_ply_file=", args.output_ply_file

    # read infile elements
    inf = open(args.infile, 'r')

    outf_vertices = []
    outf_vertices2 = []
    outf_polygons = []
    outf_polygons_len = []
    outf_cuboids = []

    vertex_index = 0
    # for line in infile. get data into structured numpy arrays
    for line in inf:
        ob = loads(line)
        if type(ob) is Polygon:
            vertex_list = list(ob.exterior.coords)
            #numpy.array([vertex_index])=ob
            outf_polygons_len.append(len(vertex_list))
            poly_indices = []
            for v in vertex_list:
                # add v to vertex list
                outf_vertices.append(v)
                #print vertex_index, v
                poly_indices.append(vertex_index)

                # add index_counter to vertex_index
                vertex_index += 1
            outf_polygons.append(poly_indices)
            #outf_polys = numpy.array(poly_indices,
            #                         dtype=[('vertex_indices', 'i4', len(poly_indices)])

        elif type(ob) is MultiPoint:
            # Getting the vertices from the Point objects
            vertex_list = []
            for i in list(ob.geoms):
                vertex_list.append(list(i.coords)[0])
                #print list(i.coords[0])
            cuboid_indices = []
            for v in vertex_list:
                outf_vertices2.append(v)
                cuboid_indices.append(vertex_index)
                vertex_index += 1
            outf_cuboids.append(cuboid_indices)
        else:
            print "Unknown shape"

    # create ply datastructure
    # Vertices elements

    outf_vertices.extend(outf_vertices2)
    print "Vertices=", outf_vertices
    vertex = numpy.array(outf_vertices,
                         dtype=[('x', 'f4'), ('y', 'f4'),
                                ('z', 'f4')])
    ver = PlyElement.describe(vertex, 'vertex')

    print "Polygons=", outf_polygons
    print "Polygon items=", tuple(outf_polygons_len)
    #polygon = numpy.array(outf_polygons,
    #                      dtype=[('vertex_indices', 'i4', ())])
    polygon_array = numpy.empty(len(outf_polygons), dtype=[('vertex_indices', 'i4', ())])
    polygon_array['vertex_indices'] = outf_polygons
    pol = PlyElement.describe(polygon_array, 'polygon')

    #cuboids = numpy.array etc etc

    # write PLY file
    PlyData([ver,pol], text=True).write(args.output_ply_file)

    inf.close()


def fileinfo(args):
    ply = PlyData.read(args.plyfile)
    vertices_count(ply)
    vertices_print(ply,10)
    vertices_bounds(ply)

def vertices_count(ply):
    '''
    Prints a count of the number of vertices in the file
    '''

    print "Number of vertices =", ply['vertex'].count

def vertices_print(ply,count):
    '''
    Prints the first 'count' of vertices in the file
    '''

    for i in range(0,count):
        print "Vertex", i, "=", ply['vertex'][i]

def vertices_bounds(ply):
    '''
    Gets min and max of vertices in the file and prints them
    '''
    xyz = ['x','y','z']
    for i in xyz:
        #print i,"=", ply['vertex'][i]
        print i,"min =", ply['vertex'][i].min()
        print i,"max =", ply['vertex'][i].max()

main()
