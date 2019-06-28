#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np
from .rod2D import Rod2D



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
    
