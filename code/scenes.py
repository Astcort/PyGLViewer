#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# This file is part of SimulationTeachingElan, a python code used for teaching at Elan Inria.
#
# Copyright 2020 Mickael Ly <mickael.ly@inria.fr> (Elan / Inria - Université Grenoble Alpes)
# SimulationTeachingElan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SimulationTeachingElan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SimulationTeachingElan.  If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np

from graphics import *
from dynamics import *
from geom import *



def indexedTest(viewer):
    """
    @brief Demonstration for a basic static rendering
           Renders a simple square 
    """

    # Indexed square
    positions = np.array([0., 0.,   # x0, y0
                          1., 0.,   # x1, y1
                          0., 1.,   # x2, y2
                          1., 1.],  # x3, y3
                         np.float64)
    colours = np.array([1., 0., 0.,  # (r, g, b) for vertex 0
                        0., 0., 1.,  # (r, g, b) for vertex 1
                        0., 1., 0.,  # ...
                        1., 1., 1.]) # ...
    indices = np.array([0, 1, 2,   # First triangle composed by vertices 0, 1 and 2
                        1, 2, 3])  # Second triangle composed by vertices 1, 2 and 3

    # Create the object
    squareMesh = Mesh2D(positions, indices, colours)
    # Create the correspondung GPU object
    squareMeshRenderable = Mesh2DRenderable(squareMesh)
    # Add it to the list of objects to render
    viewer.addRenderable(squareMeshRenderable)

def dynamicTest(viewer):
    """
    @brief Demonstration for a basic dynamic rendering
           Renders a simple square, moved by a dummy dynamic system
    """

    # Indexed square
    positions = np.array([0., 0.,   # x0, y0
                          1., 0.,   # x1, y1
                          0., 1.,   # x2, y2
                          1., 1.],  # x3, y3
                         np.float64)
    colours = np.array([1., 0., 0.,  # (r, g, b) for vertex 0
                        0., 0., 1.,  # (r, g, b) for vertex 1
                        0., 1., 0.,  # ...
                        1., 1., 1.]) # ...
    indices = np.array([0, 1, 2,   # First triangle composed by vertices 0, 1 and 2
                        1, 2, 3])  # Second triangle composed by vertices 1, 2 and 3

    # Create the object
    squareMesh = Mesh2D(positions, indices, colours)
    # Create the correspondung GPU object
    squareMeshRenderable = Mesh2DRenderable(squareMesh)
    # Add it to the list of objects to render
    viewer.addRenderable(squareMeshRenderable)

    # Create a dynamic system
    dyn = DummyDynamicSystem(squareMesh)
    # And add it to the viewer
    # Each frame will perform a call to the 'step' method of the viewer
    viewer.addDynamicSystem(dyn)
    


def rodTest(viewer):

    """
    @brief Demonstration for a rendering of a rod object
           Specific case, as a rod is essentialy a line, we
           need to generate a mesh over it to git it a thickness
           + demonstration of the scaling matrix for the rendering
    """
    positions = np.array([-1., 1.,
                          -1., 0.,
                          -0.5, -0.25],
                         np.float64)
    colours = np.array([1., 0., 0.,
                        0., 1., 0.,
                        0., 0., 1.])

    rod = Rod2D(positions, colours)

    rodRenderable = Rod2DRenderable(rod, thickness = 0.005)
    viewer.addRenderable(rodRenderable)
    
    positionsScaled = np.array([0., 1.,
                                0., 0.,
                                0.5, -0.25],
                               np.float64)
    rodScaled = Rod2D(positionsScaled, colours)

    rodRenderableScaled = Rod2DRenderable(rodScaled, thickness = 0.005)
    rodRenderableScaled.modelMatrix[0, 0] = 2.   # scale in X
    rodRenderableScaled.modelMatrix[1, 1] = 0.75 # scale in Y
    viewer.addRenderable(rodRenderableScaled)
