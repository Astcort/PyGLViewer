#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import OpenGL.GL as GL
import glfw
import numpy as np
import time
from itertools import cycle

from PIL import Image

from graphics.camera import Camera
from graphics.shader import Shader

## GLFW viewer 
class Viewer:

    def __init__(self, width = 1280, height = 960,
                 bgColor = np.array([0.6, 0.6, 0.6]),
                 maxFPS = 60,
                 offline = False,
                 frameByFrame = False,
                 recordingFreq = 0):
        ## Init the window
        # @param self
        # @param width
        # @param height
        # @param bgColor
        # @param maxFPS         Set to 0 to unblock the FPS
        # @param offline        Set the "offline" mode : only draw when asked
        #                       (Default : False - disabled)
        #                       (useful for doing computations only)
        # @param framebyFrame   Set the frame by frame mode
        #                       (Default : False - disabled)
        # @param recordingFreq  Recording mode : takes a screenshot every recordingFreq frame
        #                       (Default : 0 - disabled)

        # FPS
        self.maxFPS = maxFPS
        self.timeLastUpdate = glfw.get_time()

        # "Offline mode"
        self.offline = offline
        self.requestDraw = False

        # Frame by frame
        self.frameByFrame = frameByFrame
        self.requestFrame = False

        # Screenshot
        self.requestScreenshot = False
        self.screenshotName = "screenshot_"
        self.screenshotId = 0
        self.recordingFreq = recordingFreq
        self.autoScreenshot = (recordingFreq > 0)
        self.screenshotFrameCounter = 0

        # OpenGL parameters
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)

        # Create the window
        self.width = width
        self.height = height
        self.window = glfw.create_window(width, height,
                                         'Viewer', None, None)
        glfw.make_context_current(self.window)

        # Link the callbacks
        glfw.set_key_callback(self.window, self.keyCallback)
        
        # Debug print
        print("OpenGL   : ", GL.glGetString(GL.GL_VERSION).decode())
        print("GLSL     : ", GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode())
        print("Renderer : ", GL.glGetString(GL.GL_RENDERER).decode())


        # Viewport
        GL.glClearColor(bgColor[0], bgColor[1],
                        bgColor[2], 1.0) # Background
        GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE) # Not needed in 2D


        # Flat shader loading
        self.shaderProgram = Shader("./shaders/flat2D.vert",
                                    "./shaders/flat2D.frag")

        # Renderables
        self.renderables = []

        # Dynamic systems
        self.dynamicOn = True
        self.dynamicSystems = []

        # Camera
        self.camera = Camera(self.window)

        # Render mode
        self.fillModes = cycle([GL.GL_LINE, GL.GL_FILL])

    def run(self):
        ## Main loop
        # @param self
        
        while not glfw.window_should_close(self.window):

            try:
                # FPS Limiter
                if (self.maxFPS > 0):
                    timeNewUpddate = glfw.get_time()
                    if (timeNewUpddate < (self.timeLastUpdate + 1. / self.maxFPS)):
                        continue
                    self.timeLastUpdate = timeNewUpddate

                if (not self.frameByFrame) or (self.requestFrame):
                    
                    self.requestFrame = False

                    # Clear
                    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                    # MVP
                    windowSize = glfw.get_window_size(self.window)
                    viewMatrix = self.camera.viewMatrix()
                    projectionMatrix = self.camera.projectionMatrix(windowSize)

                    # Animate
                    if self.dynamicOn:
                        for ds in self.dynamicSystems:
                            ds.step()

                    # Draw
                    if (not self.offline) or (self.requestDraw):
                        self.requestDraw = False
                        for renderable in self.renderables:
                            renderable.draw(viewMatrix, projectionMatrix,
                                            self.shaderProgram)
                        glfw.swap_buffers(self.window)

                        if (self.requestScreenshot) \
                           or ((self.autoScreenshot) and \
                               (self.recordingFreq > 0) and \
                               (self.screenshotFrameCounter == 0)):
                            
                            self.requestScreenshot = False
                            
                            GL.glReadBuffer(GL.GL_FRONT)
                            pixels = GL.glReadPixels(0, 0,\
                                                     self.width, self.height, \
                                                     GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
                            image = Image.frombytes("RGB", (self.width, self.height), pixels)
                            image = image.transpose( Image.FLIP_TOP_BOTTOM)
                            filename = self.screenshotName + str(self.screenshotId).zfill(9) + ".png"
                            image.save(filename)
                            self.screenshotId += 1
                        
                        if (self.recordingFreq > 0):
                            self.screenshotFrameCounter \
                                = (self.screenshotFrameCounter + 1) % self.recordingFreq
                # Events
                glfw.poll_events()
                
            except KeyboardInterrupt:
                glfw.set_window_should_close(self.window, True)
            

    def addRenderable(self, *renderables):
        ## Add new renderables to render
        # @param self
        # @param renderables
        self.renderables.extend(renderables) 
        

    def addDynamicSystem(self, *ds):
        ## Add new renderables to render
        # @param self
        # @param ds
        self.dynamicSystems.extend(ds)
        

    def keyCallback(self, win, key, scancode, action, mods):
        ## Key callback
        # NB : Doc for AZERTY keyboard
        # "Q" or echap to quit
        # "T" to toggle the rendering mode
        #
        # "W" to go up
        # "A" to go left
        # "S" to go down
        # "D" to go right
        #
        # "Enter" to pause/play the animations
        #
        # "O" to toggle the "offline" mode
        # "P" to ask to draw in the "offline" mode
        #
        # "F" to toggle the frame by frame mode
        # "G" to compute a frame in the frame by frame mode
        #
        # "C" (No recording mode) to take a screenshot
        #     (Recording mode) Toggle the recording
        #
        # @param self
        # @param win
        # @param key
        # @param scancode
        # @param action
        # @param mods

        delta = 2.
        if action == glfw.PRESS or action == glfw.REPEAT:
            
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.window, True)

            elif key == glfw.KEY_ENTER:
                self.dynamicOn = not self.dynamicOn
            
            elif key == glfw.KEY_T:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fillModes))

            elif key == glfw.KEY_O:
                self.offline = not self.offline
                if (self.offline):
                    self.requestDraw = False

            elif key == glfw.KEY_P:
                self.requestDraw = True
                
            elif key == glfw.KEY_F:
                self.frameByFrame = not self.frameByFrame
                if (self.frameByFrame):
                    self.requestFrame = False

            elif key == glfw.KEY_G:
                self.requestFrame = True

            elif key == glfw.KEY_C:
                if (self.recordingFreq == 0):
                    self.requestScreenshot = True
                else:
                    self.autoScreenshot = not self.autoScreenshot
            
            elif (key == glfw.KEY_W) or (key == glfw.KEY_A) \
               or (key == glfw.KEY_S) or (key == glfw.KEY_D):
                oldMousePos = self.camera.mousePos
                if key == glfw.KEY_W:
                    self.camera.mousePos = oldMousePos + np.array([0., -delta])
                elif key == glfw.KEY_A:
                    self.camera.mousePos = oldMousePos + np.array([delta, 0.])
                elif key == glfw.KEY_S:
                    self.camera.mousePos = oldMousePos + np.array([0., delta])
                else:
                    self.camera.mousePos = oldMousePos + np.array([-delta, 0.])
                self.camera.translate(oldMousePos, self.camera.mousePos)
                
