#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import OpenGL.GL as GL
import glfw
import numpy as np
from itertools import cycle

from graphics.camera import Camera
from graphics.shader import Shader

## GLFW viewer 
class Viewer:

    def __init__(self, width=1280, height=960,
                 bgColor = np.array([0.3, 0.3, 0.3])):
        ## Init the window
        # @param self
        # @param width
        # @param height

        # OpenGL parameters
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)

        # Create the window
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

        # Trackball
        self.trackball = Camera(self.window)

        # Render mode
        self.fillModes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])

    def run(self):
        ## Main loop
        # @param self
        
        while not glfw.window_should_close(self.window):
            # Clear
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            # MVP
            windowSize = glfw.get_window_size(self.window)
            modelMatrix = np.identity(4, dtype="float")
            viewMatrix = self.trackball.viewMatrix()
            projectionMatrix = self.trackball.projectionMatrix(windowSize)

            # Animate
            if self.dynamicOn:
                for ds in self.dynamicSystems:
                    ds.step()

            # Draw
            for renderable in self.renderables:
                renderable.draw(modelMatrix, viewMatrix, projectionMatrix,
                                self.shaderProgram)
            glfw.swap_buffers(self.window)

            # Events
            glfw.poll_events()
            

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
        # "Q" or echap to quit
        # "T" to toggle the rendering mode
        # "W" to go up
        # "A" to go left
        # "S" to go down
        # "D" to go right
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
                return
            
            if key == glfw.KEY_T:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fillModes))
                return
            
            if (key == glfw.KEY_W) or (key == glfw.KEY_A) \
               or (key == glfw.KEY_S) or (key == glfw.KEY_D):
                oldMousePos = self.trackball.mousePos
                if key == glfw.KEY_W:
                    self.trackball.mousePos = oldMousePos + np.array([0., -delta])
                elif key == glfw.KEY_A:
                    self.trackball.mousePos = oldMousePos + np.array([-delta, 0.])
                elif key == glfw.KEY_S:
                    self.trackball.mousePos = oldMousePos + np.array([0., delta])
                else:
                    self.trackball.mousePos = oldMousePos + np.array([delta, 0.])
                self.trackball.translate(oldMousePos, self.trackball.mousePos)
                
