#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np


## Class defining a 2D rod parameterized by the nodes positions
class Rod2D(object):

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

        # Fields to lighten the redraw
        self.positionsUpdated = True
        self.coloursUpdated = True



    def __getattribute__(self, name):
        ## Attribute accessor
        # Overload it to have "const" accessor to the posititions and colours :
        # * positions or colours : "non-const" accessor,
        #     trigger the buffer update
        # * constPositions or constColours  : "const" accessor,
        #     does not trigger the buffer update

        if (name == "positions"):
            self.positionsUpdated = True
        elif (name == "constPositions"):
            return object.__getattribute__(self, "positions")
        elif ((name == "colours") or (name == "colors")):
            self.coloursUpdated = True
            return object.__getattribute__(self, "colours")
        elif ((name == "constColours") or (name == "constColors")):
            return object.__getattribute__(self, "colours")
        
        return object.__getattribute__(self, name)
            


    def __setattr__(self, name, value):
        ## Attribute setter
        # Overload it to have "const" accessor to the posititions and colours :
        # * positions or colours : "non-const" accessor,
        #     set trigger the buffer update
        # * constPositions or constColours  : "const" accessor,
        #     fails

        if (name == "positions"):
            self.positionsUpdated = True
        elif ((name == "colours") or (name == "colors")):
            self.coloursUpdated = True
            object.__setattr__(self, "colours", value)
            return
        elif (name == "constPositions") or \
             (name == "constColours") or (name == "constColors"):
            raise Exception("Tried to set a const field")
        
        object.__setattr__(self, name, value)
            

