#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import OpenGL.GL as GL
import numpy as np


## Class defining a mesh to render
class Mesh2DRenderable(AbstractRenderable):

    def __init__(self, positions, colours = None, \
                 indices = None):
        ## Constructor
        # Initialize the buffers required for a mesh
        # @param self
        # @param positions  1-D Numpy array concatenating
        #                   the 2D positions of the mesh
        # @param colours    1-D Numpy array concatenating the
        #                   vertices colours (r, g, b)
        # @param indices    1-D Numpy array for the triangles indices

        super().__init__()

        # Create the VAO
        self.glId = GL.glGenVertexArrays(1)
        GL.glBindVertexArrays(self.glId)

        # VBOs
        ## Ugly -- assumes the locations
        
        # Positions
        # (doubles needed for the simulations)
        # Data storing
        positionLocation = 0 # <--
        self.data["positions"] = np.array(data, np.float64)
        self.buffers["positions"] = GL.glGenBuffers(1)
        self.nbVertices = positions.rows()/2
        # Drawing instructions
        positions = np.array(self.data["positions"], np.float64, copy=False)
        positionId = self.buffers["positions"]
        GL.glEnableVertexAttribArray(positionLocation)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, positionId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, positions,
                        GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(positionLocation, 2 * self.nbVertices,
                                 GL.GL_DOUBLE, False, 0, None)

        # Colours
        if (colours = None):
            colours = 0.5 * np.ones(3 * self.nbVertices, dtype=np.float32)
        else:
            colours = np.array(colours, np.float32, copy=False)
            if (colours.rows() != (3 * self.nbVertices / 2)):
                raise Exception("Mesh2DRenderable - wrong buffer size")
        # Data
        colourLocation = 1
        self.data["colours"] = np.array(colours, np.float32)
        self.buffers["colours"] = GL.glGenBuffers(1)
        # Drawing instructions
        colours = np.array(self.data["colours"], np.float32, copy=False)
        colourId = self.buffers("colours")
        GL.glEnableVertexAttribArray(colourLocation)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, colourId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colours, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(colourLocation, 3 * self.nbVertices,
                                 GL.GL_FLOAT, False, 0, None)

        # Indexed drawing or not ?
        self.drawCommand = None
        self.drawArguments = None
        if index is None:
            self.drawCommand = GL.glDrawArrays
            self.drawArguments = (0, 1)
        else:
            # Data
            self.data["indices"] = np.array(index, np.int32)
            self.buffers["indices"] = GL.glGenBuffers(1)
            # Drawing instructions
            index = np.array(self.data["indices"], np.int32, copy=False)
            indexId = self.buffers("indices")
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, indexId)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, index, GL.GL_STATIC_DRAW)
            self.drawCommand = GL.glDrawElements
            self.drawArguments = (index.rows(), GL.GL_UNSIGNED_INT, None)

        # End of the VAO commands -- unbind everything
        GL.glBindVertexArray(0)
        GL.glBindBffer(GL.GL_ARRAY_BFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)


    def draw(self, primitive = GL.GL_TRIANGLES):
        ## Drawing function
        # @param self
        # @param primitive  Primitive type
        GL.glBindVertexArray(self.glId)
        self.drawCommand(primitive, *self.drawArguments)
        GL.glBindVertexArray(0)
            
            
