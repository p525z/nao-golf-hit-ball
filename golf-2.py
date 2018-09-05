#coding:utf-8

#import numpy as np
import math
import time
import sys
import os
import almath
import vision_definitions as vd
from naoqi import ALProxy

class NaoVision(object):
    def __init__ (self, IP, cameraId = 1):
        self._IP = IP
        self._cameraId = cameraId
        self.ballX = 1.0
        self.ballY = 0.0
        self.alpha = 0.0
        self._cameraProxy = ALProxy("ALVideoDevice", self._IP, 9559)
        self._motionProxy = ALProxy("ALMotion", self._IP, 9559)
        self._cameraProxy.setActiveCamera(self._cameraId)
        self._postureProxy = ALProxy("ALRobotPosture", self._IP, 9559)
        self.tracker = ALProxy("ALTracker", IP, 9559)

    def findMark(self):
        landMarkProxy = ALProxy("ALLandMarkDetection", self._IP, 9559)
        landMarkProxy.subscribe("Test_LandMark", 500, 0.0 )
        memoryProxy = ALProxy("ALMemory", self._IP, 9559)

        for i in range(10):
            time.sleep(0.5)
            val = memoryProxy.getData("LandmarkDetected")
            print "\n****\n"
            if(val and isinstance(val, list) and len(val) >= 2):
                markInfo = val[1]
                try:
                    for mark in markInfo:
                        markShapeInfo = mark[0]
                        self.alpha = markShapeInfo[1]
                        print "alpha %.3f - beta %.3f" % (self.alpha, markShapeInfo[2])
                        landMarkProxy.unsubscribe("Test_LandMark")
                        return True
                except Exception, e:
                    print "Landmarks detected, but it seems getData is invalid. ALValue ="
                    print markShapeInfo
                    print "Error: %s" % (str(e))
            else:
                print "Error with getData. ALValue = %s" % (str(val))
        else:
            landMarkProxy.unsubscribe("Test_LandMark")
            return False

    def redballTrack(self,ballSize):
        self.tracker.setRelativePosition([-0.12, 0.0, 0.0, 0.05, 0.02, 0.3])
        self.tracker.registerTarget("RedBall", ballSize)
        self.tracker.setMode("Move")
        self._motionProxy.setMoveArmsEnabled(False,False)

        times = 1.2
        flag = True
        try:
            for i in range(30):
                self.tracker.track("RedBall")
                print(i)
                print(flag)
                time.sleep(times)
                if self.tracker.isTargetLost() == True:
                    flag = False
                    times = 0.2
            redball = self.tracker.getTargetPosition()
            print(redball)
            if len(redball) > 0:
                self.ballX = round(redball[0],2)
                print(self.ballX)
                self.ballY = redball[1]
                flag = True
                if self.ballX > 0.25:
                    print('in')
                    self._motionProxy.moveTo(self.ballX - 0.15,0.0,-0.2,self.config)
        except KeyboardInterrupt:
            print "Stopping..."

        self.tracker.stopTracker()
        self.tracker.unregisterAllTargets()
        return flag

class golfSwing(object):
    def __init__(self,IP,cameraId):
        self._IP = IP
        self._motionProxy = ALProxy("ALMotion", self._IP, 9559)
        

    def hitBall(self):
        names = ["LElbowRoll","LShoulderPitch"]#放下左手
        angleLists = [[-51.9 * almath.TO_RAD, -23.6 * almath.TO_RAD],[53.8 * almath.TO_RAD,93.5 * almath.TO_RAD]]
        timeLists = [[1.0,2.0],[1.0,2.0]]
        self._motionProxy.angleInterpolation(names, angleLists, timeLists, True)

        #准备挥球
        names = ["RShoulderPitch","RShoulderRoll","RElbowRoll","RElbowYaw","RWristYaw"]
        angleLists = [[53.8 * almath.TO_RAD,48.6 * almath.TO_RAD],
                   [-2.2 * almath.TO_RAD,-4.0 * almath.TO_RAD],
                   [51.9 * almath.TO_RAD, 85.1 * almath.TO_RAD],
                   [67.4 * almath.TO_RAD, 14.1 * almath.TO_RAD],
                   [104.1 * almath.TO_RAD, 38.7 * almath.TO_RAD]]
        timeLists = [[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0]]
        self._motionProxy.angleInterpolation(names, angleLists, timeLists, True)
        time.sleep(3)

        #挥球
        names = "RWristYaw"
        angleLists = [38.7 * almath.TO_RAD, -1.0 * almath.TO_RAD]
        timeLists = [1.0,2.0]
        self._motionProxy.angleInterpolation(names, angleLists, timeLists, True)

        #收手
        names = ["RShoulderPitch","RElbowYaw","RElbowRoll","RShoulderRoll","RWristYaw"]
        angleLists = [[48.6 * almath.TO_RAD,53.8 * almath.TO_RAD],
                   [14.1 * almath.TO_RAD, 88.2* almath.TO_RAD],
                   [85.1 * almath.TO_RAD, 51.9 * almath.TO_RAD],
                   [-4.0 * almath.TO_RAD,-2.2 * almath.TO_RAD],
                   [38.7 * almath.TO_RAD, 104.1 * almath.TO_RAD]]
        timeLists = [[1.0,3.0],[3.0,4.0],[5.0,6.0],[5.0,6.0],[5.0,6.0]]
        self._motionProxy.angleInterpolation(names, angleLists, timeLists, True)

        names = ["LElbowRoll","LShoulderPitch"]
        angleLists = [[-23.6 * almath.TO_RAD, -51.9 * almath.TO_RAD],[93.5 * almath.TO_RAD,53.8 * almath.TO_RAD]]
        timeLists = [[1.0,2.0],[1.0,2.0]]
        self._motionProxy.angleInterpolation(names, angleLists, timeLists, True)

    def firstHit(self):
#        names = ["LElbowRoll","RElbowRoll","RElbowYaw","LElbowYaw","RShoulderRoll",
#        "LShoulderRoll","RShoulderPitch","LShoulderPitch","RWristYaw","LWristYaw",]
#        angleLists = [[-24.0 * almath.TO_RAD, -88.4 * almath.TO_RAD],
#        [24.0 * almath.TO_RAD, 88.4 * almath.TO_RAD],[67.6 * almath.TO_RAD, 95.1 * almath.TO_RAD],[-67.6 * almath.TO_RAD, -95.1 * almath.TO_RAD],
#        [-9.4 * almath.TO_RAD,-2.2 * almath.TO_RAD],[9.4 * almath.TO_RAD,2.2 * almath.TO_RAD],[86.9 * almath.TO_RAD,119.5 * almath.TO_RAD],
#        [86.9 * almath.TO_RAD,119.5 * almath.TO_RAD],[6.0 * almath.TO_RAD,104.2 * almath.TO_RAD],
#        [6.0* almath.TO_RAD,-104.2 * almath.TO_RAD]]
#        timeLists = [[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],
#        [1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0]]
#        isAbsolute= True
#        self._motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
#
#        self._motionProxy.openHand('RHand')
#        self._motionProxy.openHand('LHand')
#        time.sleep(1)
#        self._motionProxy.closeHand('RHand')
#        self._motionProxy.closeHand('LHand')

        #抬手
        names1 = ["RShoulderPitch","LShoulderPitch","RElbowRoll","LElbowRoll"]
        angleLists1 = [[119.5 * almath.TO_RAD,26.5 * almath.TO_RAD],[119.5 * almath.TO_RAD,26.5 * almath.TO_RAD],
        [88.4 * almath.TO_RAD, 36.5 * almath.TO_RAD],[-88.4 * almath.TO_RAD,-36.5 * almath.TO_RAD]]
        timeLists1 = [[1.0,3.0],[1.0,3.0],[1.0,3.0],[1.0,3.0]]
        isAbsolute1 = True
        self._motionProxy.angleInterpolation(names1, angleLists1, timeLists1, isAbsolute1)
        time.sleep(1)

        #放下左手
        self._motionProxy.openHand('LHand')
        names2 = ["LShoulderPitch","LElbowRoll"]
        angleLists2 = [[34.5 * almath.TO_RAD,119.5 * almath.TO_RAD],[-36.5 * almath.TO_RAD,-88.4 * almath.TO_RAD]]
        timeLists2 = [[1.0,3.0],[1.0,3.0]]
        isAbsolute2 = True
        self._motionProxy.angleInterpolation(names2, angleLists2, timeLists2, isAbsolute2)

        #调整右手
        names3 = "RShoulderRoll","RWristYaw"
        angleLists3 = [[-9.4 * almath.TO_RAD,-9.4 * almath.TO_RAD],
        [104.2 * almath.TO_RAD, 35.0 * almath.TO_RAD]]
        timeLists3 = [[1.0,2.0],[1.0,2.0]]
        isAbsolute3 = True
        self._motionProxy.angleInterpolation(names3, angleLists3, timeLists3, isAbsolute3)
        time.sleep(3)
        
        #挥球
        names4 = "RWristYaw"
        angleLists4 = [35.0 * almath.TO_RAD, -50.2 * almath.TO_RAD]
        timeLists4 = [1.0,1.4]
        isAbsolute4 = True
        self._motionProxy.angleInterpolation(names4, angleLists4, timeLists4, isAbsolute4)

        #双手握杆
        names5 = ["RWristYaw","RShoulderPitch","RElbowRoll","RShoulderRoll"]
        angleLists5 = [[50.2 * almath.TO_RAD,104.2 * almath.TO_RAD],
        [26.5 * almath.TO_RAD,0.0 * almath.TO_RAD],
        [36.5 * almath.TO_RAD,2.0 * almath.TO_RAD],
        [-8.6 * almath.TO_RAD,4.2 * almath.TO_RAD]]
        timeLists5 = [[1.0,2.0],[1.0,2.0],[1.0,2.0],[2.0,3.0]]
        isAbsolute5 = True
        self._motionProxy.angleInterpolation(names5, angleLists5, timeLists5, isAbsolute5)

        self._motionProxy.openHand('LHand')
        names6 = ["LShoulderPitch","LElbowRoll"]
        angleLists6 = [[84.5 * almath.TO_RAD,0.0 * almath.TO_RAD],
        [-88.4 * almath.TO_RAD,2.0 * almath.TO_RAD]]
        timeLists6 = [[1.0,3.0],[1.0,3.0]]
        isAbsolute6 = True
        self._motionProxy.angleInterpolation(names6, angleLists6, timeLists6, isAbsolute6)
        self._motionProxy.closeHand('LHand')
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
        self._motionProxy.angleInterpolation(names7, angleLists7, timeLists7, isAbsolute7)

class NaoActive(NaoVision,golfSwing):
    def __init__(self, IP,cameraId=1):
        super(NaoActive, self).__init__(IP,cameraId)
        self._memoryProxy = ALProxy("ALMemory", self._IP, 9559)
        self.angleList = [-0.8,0.8,0.8,-0.8]
        self.last = -0.8
        self.config = [["MaxStepX",0.04],
                        ["MaxStepY",0.12],
                        ["MaxStepTheta",0.4],
                        ["MaxStepFrequency",0.5],
                        ["StepHeight",0.02],
                        ["TorsoWx",0.0],
                        ["TorsoWy",0.0]]

    def mainControl(self):
#        self.firstHit()#第一次击球
#        self._motionProxy.setMoveArmsEnabled(False,False)
#        self._motionProxy.moveTo(0.0,0.0,-1.5,self.config)
#        self._motionProxy.moveTo(0.0,-0.15,0.0,self.config)
#        self._motionProxy.moveTo(0.6,0.0,-0.2,self.config)
#        time.sleep(0.2)
#        self._motionProxy.moveTo(0.6,0.0,-0.2,self.config)
        while True:
            self.headActive("HeadPitch",0.15)#朝前看
            for angle in self.angleList:
                if self.redballTrack(0.021) == False:#没找到球，转头
                    self._motionProxy.moveTo(0.0,0.0,angle,self.config)
                    #self.headActive("HeadYaw",angle)
                else:#找到球，找mark
                    print('findball')
                    self.headActive("HeadPitch",-1.2)#抬头找Mark
                    for angle in self.angleList:
                        print('Mark')
                        if self.findMark() == True:#找到mark，碎步微调
                            #head = (self.last + angle)/2
                            head = self._memoryProxy.getData("Device/SubDeviceList/HeadYaw/Position/Sensor/Value")
                            print(head)
                            moveX = self.ballX*(1 - math.cos(head + self.alpha))
                            moveY = self.ballX*math.sin(head + self.alpha)
                            moveAlpha = head + self.alpha
                            print(moveX,moveY)
                            self._motionProxy.moveTo(moveX,-moveY,moveAlpha,self.config) 
                            #看球看Mark确认三点一线
                            #self.hitBall()
                            print("HitBall")
                            break
                        else:#没找到Mark，转头
                            self.headActive("HeadYaw",angle)
                            self.last = angle
                    break #重新找球
            else:#没找到球，盲走一段距离
                self._motionProxy.moveTo(0.25,0.0,-0.2,self.config)

    def headActive(self,name,angle):
        self._motionProxy.setStiffnesses("Head",1.0)
        print(angle)

        fractionMaxSpeed = 0.1
        self._motionProxy.setAngles(name,angle,fractionMaxSpeed)

        time.sleep(1)
        self._motionProxy.setStiffnesses("Head",0.5)

nao = NaoActive("192.168.1.101")
nao.mainControl()
