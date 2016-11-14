#!/usr/bin/python
'''
Gerard de Vos

Usage: python ply-test.py datafile.ply

A few simple tests handling PLY polygon files
http://www.dcs.ed.ac.uk/teaching/cs4/www/graphics/Web/ply.html

Uses https://github.com/dranjan/python-plyfile and, in turn, NumPy
'''

from argparse import ArgumentParser

import numpy

from plyfile import PlyData

def main():
    parser = ArgumentParser()
    parser.add_argument('ply_filename')

    args = parser.parse_args()

    # read the file
    ply = PlyData.read(args.ply_filename)

    # The tests
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
