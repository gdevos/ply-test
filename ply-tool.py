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

from plyfile import PlyData

from shapely.geometry import Polygon, Point
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
    write_parser.add_argument('outputPLYfile', help='Output PLY filename')
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
        print "Polygon", poly_i, "intersects=", poly.intersects(bbox)
        if poly.intersects(bbox):
            # to WKT
            polywkt = dumps(poly) + '\n'
            print "Adding to file", polywkt
            outf.write(polywkt)
        #if poly_i intersects(boundingbox)
            #add poly_i to intermediary list

    # Loop through cuboids
    cube_count = ply['cuboid'].count
    for cub_i in range(0,cube_count):
        print "Cuboid=", ply['cuboid'][cub_i]
        for i in ply['cuboid'][cub_i].tolist():
            print "Vertex=", ply['vertex'][i]
        #if cub_i intersects(boundingbox)
            #add cub_i to intermediary list

    #write intermediary file
    outf.close()

def write(args):
    '''
    Reads intermediary WKT file and writes it as a PLY file
    '''

    # read infile elements

    # create ply datastructure

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
