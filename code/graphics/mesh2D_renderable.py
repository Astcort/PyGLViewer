#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from .abstract_renderable import AbstractRenderable
import OpenGL.GL as GL
import numpy as np


## Class rendering a mesh
class Mesh2DRenderable(AbstractRenderable):

    def __init__(self, mesh):
        ## Constructor
        # Initialize the GPU buffers required for a mesh
        # @param self
        # @param mesh

        super().__init__()

        
        self.mesh = mesh

        
        # Create the VAO
        self.glId = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.glId)

        # VBOs
        ## Ugly -- assumes the locations
        
        # Positions
        # (doubles needed for the simulations)
        # Data storing
        self.locations["positions"] = 0 # <--
        self.buffers["positions"] = GL.glGenBuffers(1)
        # Send data
        self.updatePositionsBuffer()
        # Drawing instructions
        GL.glVertexAttribPointer(self.locations["positions"], 2,
                                 GL.GL_DOUBLE, False, 0, None)

        # Data
        self.locations["colours"] = 1 # <--
        self.buffers["colours"] = GL.glGenBuffers(1)
        # Send data
        self.updateColoursBuffer()
        # Drawing instructions
        GL.glVertexAttribPointer(self.locations["colours"], 3,
                                 GL.GL_FLOAT, False, 0, None)

        # Indexed drawing
        # Data
        self.buffers["indices"] = GL.glGenBuffers(1)
        # Drawing instructions
        indicesId = self.buffers["indices"]
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, indicesId)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.mesh.indices, GL.GL_STATIC_DRAW)
        self.drawCommand = GL.glDrawElements
        self.drawArguments = (self.mesh.indices.size, GL.GL_UNSIGNED_INT, None)

        # End of the VAO commands -- unbind everything
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)


    def updatePositionsBuffer(self):
        ## Update the GPU colour buffer
        # @param self
        positionLocation = self.locations["positions"]
        positions = np.array(self.mesh.getPositions(), np.float64, copy=False)
        positionId = self.buffers["positions"]
        GL.glEnableVertexAttribArray(positionLocation)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, positionId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, positions,
                        GL.GL_STATIC_DRAW)
        
    def updateColoursBuffer(self):
        ## Update the GPU colour buffer
        # @param self
        colourLocation = self.locations["colours"]
        colours = np.array(self.mesh.getColours(), np.float32, copy=False)
        colourId = self.buffers["colours"]
        GL.glEnableVertexAttribArray(colourLocation)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, colourId)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colours, GL.GL_STATIC_DRAW)


    def getNbVertices(self):
        ## Getter on the number of vertices
        return self.mesh.getNbVertices()
    
    def getPositions(self):
        ## Getter on the positions
        # @param self
        # @return The positions
        return self.mesh.getPositions()
    
    def getColours(self):
        ## Getter on the colours
        # @param self
        # @return The colours
        return self.mesh.getColours()
    
    def getColors(self):
        ## Getter on the colours (US)
        # @param self
        # @return The colours
        return self.getColours()


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

        self.updatePositionsBuffer()
        self.updateColoursBuffer()
        
        # Draw
        GL.glBindVertexArray(self.glId)
        self.drawCommand(primitive, *self.drawArguments)
        GL.glBindVertexArray(0)
            
            
    def __del__(self):
        super().__del__()
