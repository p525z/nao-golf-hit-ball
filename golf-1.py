# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 22:12:44 2018

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

    #放下左手
    motionProxy.openHand('LHand')
    names2 = ["LShoulderPitch","LElbowRoll"]
    angleLists2 = [[34.5 * almath.TO_RAD,119.5 * almath.TO_RAD],[-36.5 * almath.TO_RAD,-88.4 * almath.TO_RAD]]
    timeLists2 = [[1.0,3.0],[1.0,3.0]]
    isAbsolute2 = True
    motionProxy.angleInterpolation(names2, angleLists2, timeLists2, isAbsolute2)

    #调整右手
    names3 = "RShoulderRoll","RWristYaw"
    angleLists3 = [[-9.4 * almath.TO_RAD,-9.4 * almath.TO_RAD],
    [104.2 * almath.TO_RAD, 35.0 * almath.TO_RAD]]
    timeLists3 = [[1.0,2.0],[1.0,2.0]]
    isAbsolute3 = True
    motionProxy.angleInterpolation(names3, angleLists3, timeLists3, isAbsolute3)
    time.sleep(3)
    
    #挥球
    names4 = "RWristYaw"
    angleLists4 = [35.0 * almath.TO_RAD, -50.2 * almath.TO_RAD]
    timeLists4 = [1.0,1.4]
    isAbsolute4 = True
    motionProxy.angleInterpolation(names4, angleLists4, timeLists4, isAbsolute4)

    #双手握杆
    names5 = ["RWristYaw","RShoulderPitch","RElbowRoll","RShoulderRoll"]
    angleLists5 = [[50.2 * almath.TO_RAD,104.2 * almath.TO_RAD],
    [26.5 * almath.TO_RAD,0.0 * almath.TO_RAD],
    [36.5 * almath.TO_RAD,2.0 * almath.TO_RAD],
    [-8.6 * almath.TO_RAD,4.2 * almath.TO_RAD]]
    timeLists5 = [[1.0,2.0],[1.0,2.0],[1.0,2.0],[2.0,3.0]]
    isAbsolute5 = True
    motionProxy.angleInterpolation(names5, angleLists5, timeLists5, isAbsolute5)

    motionProxy.openHand('LHand')
    names6 = ["LShoulderPitch","LElbowRoll"]
    angleLists6 = [[84.5 * almath.TO_RAD,0.0 * almath.TO_RAD],
    [-88.4 * almath.TO_RAD,2.0 * almath.TO_RAD]]
    timeLists6 = [[1.0,3.0],[1.0,3.0]]
    isAbsolute6 = True
    motionProxy.angleInterpolation(names6, angleLists6, timeLists6, isAbsolute6)
    motionProxy.closeHand('LHand')
    #收杆
    names7 = ["LElbowRoll","RElbowRoll","RShoulderRoll","LShoulderRoll","RShoulderPitch","LShoulderPitch"]
    angleLists7 = [[-2.0 * almath.TO_RAD, -88.4 * almath.TO_RAD],
    [2.0 * almath.TO_RAD, 88.4 * almath.TO_RAD],
    [6.2 * almath.TO_RAD,-2.2 * almath.TO_RAD],
    [8.6 * almath.TO_RAD,2.2 * almath.TO_RAD],
    [0.0 * almath.TO_RAD,119.5 * almath.TO_RAD],
    [0.0 * almath.TO_RAD,119.5 * almath.TO_RAD]]
    timeLists7 = [[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],
    [1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0]]
    isAbsolute7= True
    motionProxy.angleInterpolation(names7, angleLists7, timeLists7, isAbsolute7)
    
firstHit("192.168.1.101")