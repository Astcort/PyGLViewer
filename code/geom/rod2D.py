#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np


## Class defining a 2D rod parameterized by the nodes positions
class Rod2D:

    def __init__(self, positions, colours = None):
        ## Constructor
        # @param positions  1-D Numpy array concatenating
        #                   the 2D positions of the mesh
        # @param indices    1-D Numpy array for the triangles indices (triplets)
        # @param colours    1-D Numpy array concatenating the
        #                   vertices colours (r, g, b)

        # Register the data and make sure of the types
        self.nbVertices = int(positions.size / 2)
        self.positions = np.array(positions, np.float64)

        self.colours = None
        if (colours is None):
            self.colours = 0.5 * np.ones(3 * self.nbVertices, dtype=np.float32)
        else:
            self.colours = np.array(colours, np.float32)
            if (colours.size != (3 * self.nbVertices)):
                raise Exception("Wrong buffer size")
            
    def getNbVertices(self):
        ## Getter on the number of vertices
        return self.nbVertices
    
    def getPositions(self):
        ## Getter on the positions
        # @param self
        # @return The positions
        return self.positions
    
    def getColours(self):
        ## Getter on the colours
        # @param self
        # @return The colours
        return self.colours
    
