#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np

from graphics import *



def baseTest(viewer):

    # Basic triangle
    positions = np.array([0., 0.,    # x0, y0
                          1., 0.,    # x1, y1
                          0., 1.],   # x2, y2
                         np.float64) # ! Type (default is float)
    colours = np.array([1., 0., 0.,  # r, g, b
                        0., 1., 0.,  # r, g, b
                        0., 0., 1.]) # r, g, b
    triangleMesh = Mesh2DRenderable(positions, colours)
    viewer.addRenderable(triangleMesh)

def indexedTest(viewer):

    # Indexed square
    positions = np.array([0., 0.,
                          1., 0.,
                          0., 1.,
                          1., 1.],
                         np.float64)
    colours = np.array([1., 0., 0.,
                        0., 0., 1.,
                        0., 1., 0.,
                        1., 1., 1.])
    indices = np.array([0, 1, 2,   # First triangle
                        1, 2, 3])  # Second triangle

    squareIndexedMesh = Mesh2DRenderable(positions, colours, indices)
    viewer.addRenderable(squareIndexedMesh)
