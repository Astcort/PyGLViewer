#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


## Abstract class defining a time-stepper 
class AbstractDynamicSystem(metaclass=ABCMeta):

    def __init__(self):
        ## Constructor
        # @param self
        pass

    @abstractmethod
    def step(self):
        ## Step of the dynamic system
        # @param self
        pass

    def __del__(self):
        pass
