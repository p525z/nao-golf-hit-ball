# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 22:19:28 2018

@author: LENOVO
"""

import time
import sys
import os
import almath
import vision_definitions as vd
from naoqi import ALProxy

def firstHit(IP):
    motionProxy = ALProxy("ALMotion", IP, 9559)
    motionProxy.wakeUp()
    names = ["LElbowRoll","RElbowRoll","RElbowYaw","LElbowYaw","RShoulderRoll",
    "LShoulderRoll","RShoulderPitch","LShoulderPitch","RWristYaw","LWristYaw",]
    angleLists = [[-24.0 * almath.TO_RAD, -88.4 * almath.TO_RAD],
    [24.0 * almath.TO_RAD, 88.4 * almath.TO_RAD],[67.6 * almath.TO_RAD, 95.1 * almath.TO_RAD],[-67.6 * almath.TO_RAD, -95.1 * almath.TO_RAD],
    [-9.4 * almath.TO_RAD,-2.2 * almath.TO_RAD],[9.4 * almath.TO_RAD,2.2 * almath.TO_RAD],[86.9 * almath.TO_RAD,119.5 * almath.TO_RAD],
    [86.9 * almath.TO_RAD,119.5 * almath.TO_RAD],[6.0 * almath.TO_RAD,104.2 * almath.TO_RAD],
    [6.0* almath.TO_RAD,-104.2 * almath.TO_RAD]]
    timeLists = [[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],
    [1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0]]
    isAbsolute= True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    #抬手
    names1 = ["RShoulderPitch","LShoulderPitch","RElbowRoll","LElbowRoll"]
    angleLists1 = [[119.5 * almath.TO_RAD,26.5 * almath.TO_RAD],[119.5 * almath.TO_RAD,26.5 * almath.TO_RAD],
    [88.4 * almath.TO_RAD, 36.5 * almath.TO_RAD],[-88.4 * almath.TO_RAD,-36.5 * almath.TO_RAD]]
    timeLists1 = [[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0]]
    isAbsolute1 = True
    motionProxy.angleInterpolation(names1, angleLists1, timeLists1, isAbsolute1)
    time.sleep(1)   
    motionProxy.openHand('RHand')
    motionProxy.openHand('LHand')
    time.sleep(1)
    motionProxy.closeHand('RHand')
    motionProxy.closeHand('LHand')

    
    
    
firstHit("192.168.1.101")