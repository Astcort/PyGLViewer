#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np
from .rod2D import Rod2D

import pyassimp

## Class defining a 2D mesh
class Mesh2D(Rod2D):

    def __init__(self, positions, indices, colours = None):
        ## Constructor
        # @param positions  1-D Numpy array concatenating
        #                   the 2D positions of the mesh
        # @param indices    1-D Numpy array for the triangles indices (triplets)
        # @param colours    1-D Numpy array concatenating the
        #                   vertices colours (r, g, b)

        super().__init__(positions, colours)        
        self.indices = np.array(indices, np.int32)
    


def loadMeshes(filename):
    ## Loader function
    # @param filename  Path to the file containing the meshes
    #
    # @return A list of Mesh2D
    #         Warning : The process to make them 2D is very naive:
    #                      the Z component is cut.
    #                   So be careful when you create the meshes to test
    #                      (no depth, triangular) and when you export (aligned with the
    #                      plane xy)
    
    options = pyassimp.postprocess.aiProcess_JoinIdenticalVertices \
              | pyassimp.postprocess.aiProcess_Triangulate
    meshesAssimp = pyassimp.load(filename, options)

    meshes2D = []
    for mA in meshesAssimp.meshes:
        # 3D to 2D
        positions = np.reshape(np.reshape(mA.vertices, (-1, 3))[:, :2], (-1))
        indices = np.reshape(mA.faces, (-1))
        meshes2D.append(Mesh2D(positions, indices))

    pyassimp.release(meshesAssimp)
    return meshes2D
