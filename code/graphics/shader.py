#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import os
import OpenGL.GL as GL

## Shader class
# Class loading and destroying the shader programs
class Shader:
    
    def __init__(self, vertexShaderStr, fragmentShaderStr):
        ## Constructor
        # Compile and attach the shaders.
        # @param self 
        # @param vertexShaderStr    String either containing the filepath to the shader
        # @param fragmentShaderStr  String either containing the filepath to the shader

        # Compile the shaders
        vertShader = self._compileShader(vertexShaderStr, GL.GL_VERTEX_SHADER)
        fragShader = self._compileShader(fragmentShaderStr, GL.GL_FRAGMENT_SHADER)
        # Attach
        self.glId = GL.glCreateProgram()
        GL.glAttachShader(self.glId, vertShader)
        GL.glAttachShader(self.glId, fragShader)
        # Link
        GL.glLinkProgram(self.glId)
        # Release
        GL.glDeleteShader(vertShader)
        GL.glDeleteShader(fragShader)

        # Check
        status = GL.glGetProgramiv(self.glId, GL.GL_LINK_STATUS)
        if not status:
            log = GL.glGetProgramInfoLog(self.glId).decode('ascii')
            GL.glDeleteProgram(self.glId)
            self.glId = None
            strError = "Shader - Shader program initialization failed : \n" + str(log)
            raise Exception(strError)

    @staticmethod
    def _compileShader(shaderStr, shaderType):
        ## Shader loader and compiler
        # Load and compile the shader code.
        # @param shaderStr   String either containing the filepath to the shader
        # @param shaderType  GL type indicating the shader type
        
        # Load and compile
        shaderCode = None
        if (os.path.exists(shaderStr)) :
            shaderCode = open(shaderStr, 'r').read()
        else:
            strError = "Shader - Shader not found : " + str(shaderStr)
            raise Exception(strError)
        shader = GL.glCreateShader(shaderType)
        GL.glShaderSource(shader, shaderCode)
        GL.glCompileShader(shader)
        # Check all is ok
        status = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
        if not status:
            log = GL.glGetShaderInfoLog(shader).decode('ascii')
            GL.glDeleteShader(shader)
            strError = "Shader - Compilation failed : " + str(shaderType) \
                       + "\n" + str(log)
            raise Exception(strError)
        return shader


    def __del(self):
        ## Destrutor
        # Unlink the program and delete it
        # @param self
        GL.glUseProgram(0)
        if self.glId is not None:
            GL.glDeleteProgram(self.glId)
        
    
