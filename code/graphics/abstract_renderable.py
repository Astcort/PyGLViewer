#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import OpenGL.GL as GL
from abc import ABCMeta, abstractmethod
import numpy as np


## Abstract class defining an object to render
class AbstractRenderable(metaclass=ABCMeta):
    
    def __init__(self):
        ## Constructor
        # Should allocate the buffers
        # @param self

        # Id of the VAO
        self.glId = None
        # Buffers and data in a dict
        self.data = {}
        self.buffers = {}
        self.locations = {}

    @abstractmethod
    def draw(self, modelMatrix, viewMatrix, projectionMatrix,
             shaderProgram, primitive = GL.GL_TRIANGLES):
        ## Call to draw
        # @param self
        pass


    def __del__(self):
        ## Desctructor
        # Release the buffers
        # @param self
        if self.glId is not None:
            GL.glDeleteVertexArrays(1, np.array([self.glId]))
            GL.glDeleteBuffers(len(self.buffers),
                               np.array([buf for buf in self.buffers.values()]))
