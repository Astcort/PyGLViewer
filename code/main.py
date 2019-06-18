#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import glfw
import numpy as np

from graphics import *
from scenes import *



if __name__ == '__main__':

    # Initialization
    glfw.init()
    viewer=Viewer(height=960, width=1280,
                  bgColor = np.array([0.4, 0.4, 0.4]))

    # Loading the scene
    #baseTest(viewer)
    indexedTest(viewer)

    # Main loop
    viewer.run()

    # End
    glfw.terminate()
