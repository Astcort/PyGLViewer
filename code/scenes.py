#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np

from graphics import *
from dynamics import *
from geom import *



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

    squareMesh = Mesh2D(positions, indices, colours)
    squareMeshRenderable = Mesh2DRenderable(squareMesh)
    
    viewer.addRenderable(squareMeshRenderable)

def dynamicTest(viewer):


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

    squareMesh = Mesh2D(positions, indices, colours)
    dyn = DummyDynamicSystem(squareMesh)
    viewer.addDynamicSystem(dyn)
    
    squareMeshRenderable = Mesh2DRenderable(squareMesh)
    viewer.addRenderable(squareMeshRenderable)



def rodTest(viewer):

    positions = np.array([-1., 1.,
                          -1., 0.,
                          -0.5, -0.25],
                         np.float64)
    colours = np.array([1., 0., 0.,
                        0., 1., 0.,
                        0., 0., 1.])

    rod = Rod2D(positions, colours)
    #dyn = DummyDynamicSystem(rod)
    #viewer.addDynamicSystem(dyn)

    rodRenderable = Rod2DRenderable(rod, 0.005)
    viewer.addRenderable(rodRenderable)
    
