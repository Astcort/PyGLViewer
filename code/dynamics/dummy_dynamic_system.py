#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import numpy as np

from .abstract_dynamic_system import AbstractDynamicSystem

## Dummy dynamic system just to test
class DummyDynamicSystem(AbstractDynamicSystem):

    def __init__(self, mesh):
        ## Constructor
        # @param self
        # @param mesh  
        super().__init__()
        self.mesh = mesh

        # Animations parameters
        self.it = 60.
        self.delta = 1.
        self.period = 120.
        self.colours = np.copy(self.mesh.constColours)
        self.translationVector = np.tile([0.01, 0], self.mesh.nbVertices)

    def step(self):

        self.mesh.colours = (self.it / self.period) * self.colours
        self.mesh.positions += self.delta * self.translationVector

        self.it += self.delta
        if (self.it <= 0) or (self.it >= self.period):
            self.delta *= -1.
