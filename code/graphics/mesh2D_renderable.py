#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from .abstract_renderable import AbstractRenderable
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
        GL.glBindVertexArray(self.glId)

        # VBOs
        ## Ugly -- assumes the locations
        
        # Positions
        # (doubles needed for the simulations)
        # Data storing
        self.locations["positions"] = 0 # <--
        self.data["positions"] = np.array(positions, np.float64)
        self.buffers["positions"] = GL.glGenBuffers(1)
        self.nbVertices = int(positions.size / 2)
        # Send data
        self.updatePositionsBuffer()
        # Drawing instructions
        GL.glVertexAttribPointer(self.locations["positions"], 2,
                                 GL.GL_DOUBLE, False, 0, None)

        # Colours
        if (colours is None):
            colours = 0.5 * np.ones(3 * self.nbVertices, dtype=np.float32)
        else:
            colours = np.array(colours, np.float32, copy=False)
            if (colours.size != (3 * self.nbVertices)):
                raise Exception("Mesh2DRenderable - wrong buffer size")
        # Data
        self.locations["colours"] = 1 # <--
        self.data["colours"] = np.array(colours, np.float32)
        self.buffers["colours"] = GL.glGenBuffers(1)
        # Send data
        self.updateColourBuffer()
        # Drawing instructions
        GL.glVertexAttribPointer(self.locations["colours"], 3,
                                 GL.GL_FLOAT, False, 0, None)

        # Indexed drawing or not ?
        self.drawCommand = None
        self.drawArguments = None
        if indices is None:
            self.drawCommand = GL.glDrawArrays
            self.drawArguments = (0, self.nbVertices)
        else:
            # Data
            self.data["indices"] = np.array(indices, np.int32)
            self.buffers["indices"] = GL.glGenBuffers(1)
            # Drawing instructions
            indices = np.array(self.data["indices"], np.int32, copy=False)
            indicesId = self.buffers["indices"]
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, indicesId)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)
            self.drawCommand = GL.glDrawElements
            self.drawArguments = (indices.size, GL.GL_UNSIGNED_INT, None)

        # End of the VAO commands -- unbind everything
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)


    def updatePositionsBuffer(self):
        ## Update the GPU colour buffer
        # @param self
        positionLocation = self.locations["positions"]
        positions = np.array(self.data["positions"], np.float64, copy=False)
        positionId = self.buffers["positions"]
        GL.glEnableVertexAttribArray(positionLocation)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, positionId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, positions,
                        GL.GL_STATIC_DRAW)
        
    def updateColourBuffer(self):
        ## Update the GPU colour buffer
        # @param self
        colourLocation = self.locations["colours"]
        colours = np.array(self.data["colours"], np.float32, copy=False)
        colourId = self.buffers["colours"]
        GL.glEnableVertexAttribArray(colourLocation)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, colourId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colours, GL.GL_STATIC_DRAW)


    def getNbVertices(self):
        ## Getter on the number of vertices
        return self.nbVertices
    
    def getPositions(self):
        ## Getter on the positions
        # @param self
        # @return The positions
        return self.data["positions"]
    
    def setPositions(self, newPos):
        ## Setter on the positions & update the buffer
        # @param self
        # @param newPos
        self.data["positions"] = newPos
        self.updatePositionsBuffer()

        
    def getColours(self):
        ## Getter on the colours
        # @param self
        # @return The colours
        return self.data["colours"]
    
    def getColors(self):
        ## Getter on the colours (US)
        # @param self
        # @return The colours
        return self.getColours()
    
    def setColours(self, newCol):
        ## Setter on the colours & update the buffer
        # @param self
        # @param newCol
        self.data["colours"] = newCol
        self.updateColourBuffer()
    
    
    def setColors(self, newCol):
        ## Setter on the colours (US) & update the buffer
        # @param self
        # @param newCol
        self.setColours(newCol)
    


    def draw(self, modelMatrix, viewMatrix, projectionMatrix,
             shaderProgram, primitive = GL.GL_TRIANGLES):
        ## Drawing function
        # @param self
        # @param projectionMatrix
        # @param viewMatrix
        # @param modelMatrix
        # @param shaderProgram
        # @param primitive

        
        # Send uniforms
        names = ["modelMatrix",
                 "viewMatrix",
                 "projectionMatrix"]
        locations = {n: GL.glGetUniformLocation(shaderProgram.glId, n)
                     for n in names}
        GL.glUseProgram(shaderProgram.glId)       

        
        GL.glUniformMatrix4fv(locations["modelMatrix"], 1, True, modelMatrix)
        GL.glUniformMatrix4fv(locations["viewMatrix"], 1, True, viewMatrix)
        GL.glUniformMatrix4fv(locations["projectionMatrix"], 1, True, projectionMatrix)
        
        # Draw
        GL.glBindVertexArray(self.glId)
        self.drawCommand(primitive, *self.drawArguments)
        GL.glBindVertexArray(0)
            
            
    def __del__(self):
        super().__del__()
