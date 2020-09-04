#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import OpenGL.GL as GL
import numpy as np
import numpy.linalg as la

from geom.mesh2D import Mesh2D
from .mesh2D_renderable import Mesh2DRenderable


## Class rendering a rod
## Creates a mesh from a rod to give it a thickness
## as GLLineWidth has no standard implementation...
class Rod2DRenderable(Mesh2DRenderable):


    def __init__(self, rod, thickness = 0.01):
        ## Constructor
        # Generates a mesh around the rod and
        # initialized the GPU buffers
        # @param self
        # @param rod
        # @param thickness

        self.glId = None
        
        self.rod = rod
        self.thickness = thickness

        # Init mesh
        nbVerticesRod = rod.nbVertices
        nbVerticesMesh = 4 * (nbVerticesRod - 1)
        positions = np.zeros(2 * nbVerticesMesh, np.float64)
        colours = np.zeros(3 * nbVerticesMesh, np.float32)
        ## Indices
        indices = []
        currTopId = 0
        currBotId = 1
        for col in range(int(nbVerticesMesh / 2) - 1):
            nextTopId = currTopId + 2
            nextBotId = currBotId + 2
            # First triangle
            indices.append(currTopId)
            indices.append(currBotId)
            indices.append(nextTopId)
            # Second triangle
            indices.append(currBotId)
            indices.append(nextBotId)
            indices.append(nextTopId)

            currTopId = nextTopId
            currBotId = nextBotId
        

        self.mesh = Mesh2D(positions, indices, colours)
        self.updateMeshPositions()
        self.updateMeshColours()
        
        # Init mesh renderable
        super().__init__(self.mesh)



    def updateMeshPositions(self):
        ## Compute the positions of the mesh from the rod
        # Just adds a thickness to the segments
        # @param self

        # Data
        positions = self.rod.constPositions
        meshPositions = self.mesh.positions

        currVertex = positions[0:2]
        for vId in range(1, self.rod.nbVertices):
            nextVertex = positions[2*vId:2*(vId+1)]

            tg = np.array([-nextVertex[1] + currVertex[1],
                           nextVertex[0] - currVertex[0]])
            tgNorm = la.norm(tg)

            eId = vId - 1            
            if (tgNorm != 0.):
                tg *= self.thickness / tgNorm
            meshPositions[8 * eId    :8 * eId + 2] = currVertex + tg
            meshPositions[8 * eId + 2:8 * eId + 4] = currVertex - tg
            meshPositions[8 * eId + 4:8 * eId + 6] = nextVertex + tg
            meshPositions[8 * eId + 6:8 * eId + 8] = nextVertex - tg
            
            currVertex = nextVertex
            
    def updateMeshColours(self):
        ## Compute the colours of the mesh from the rod
        #  Simply report them to the extended vertices
        # @param self

        # Data
        colours = self.rod.constColours
        meshColours = self.mesh.colours

        # Border case
        col = colours[0:3]
        meshColours[0:3] = col
        meshColours[3:6] = col
        for vId in range(1, self.rod.nbVertices):
            col = colours[3 * vId: 3 * vId + 3]
            rg = 2 if (vId == self.rod.nbVertices - 1) else 4
            for i in range(rg):
                vmId = 4 * vId - 2 + i
                meshColours[3 * vmId: 3 * vmId + 3] = col
                
        
            
    def updatePositionsBuffer(self):
        ## Update the GPU colour buffer
        # @param self
        if (not self.rod.positionsUpdated):
            return
        self.updateMeshPositions()
        super().updatePositionsBuffer()
        self.rod.positionsUpdated = self.mesh.positionsUpdated
        
    def updateColoursBuffer(self):
        ## Update the GPU colour buffer
        # @param self
        if (not self.rod.coloursUpdated):
            return
        self.updateMeshColours()
        super().updateColoursBuffer()
        self.rod.coloursUpdated = self.mesh.coloursUpdated
        
    def __del__(self):
        super().__del__()
