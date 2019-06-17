#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import OpenGL.GL as GL


## Class defining an object to render
class AbstractRenderable:
    
    def __init__(self):
        ## Constructor
        # Should allocate the buffers
        # @param self

        # Id of the VAO
        self.glId = None
        # Buffers and data in a dict
        self.data = {}
        self.buffers = {}

    @abstractmethod
    def draw(self):
        ## Call to draw
        # @param self
        pass

    def __del__(self):
        ## Desctructor
        # Release the buffers
        # @param self
        if self.glId is not None:
            GL.glDeleteVertexArrays(1, [self.glId])
            GL.glDeleteBuffers(len(self.buffers),
                               [buf for buf in self.buffers.values()])
