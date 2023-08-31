import adsk.core
import adsk.fusion
import math

import apper
from apper import AppObjects


class Spring(apper.Fusion360CommandBase):

    def __init__(self,x,y,rotate,plane, springCoils, widthSpring, springSpace, springCoilThickness, materialThickness, extrudeOffset):
        ao = AppObjects()
        self._x = x
        self._y = y
        self._rotate = rotate
        self._plane = plane
        self._springCoils = springCoils
        self._springWidth = widthSpring
        self._spaceBetween = springSpace
        self._coilThickness = springCoilThickness
        self._materialThickness = materialThickness
        self._extrudeOffset = extrudeOffset
        
        springOcc = self.createSpring()
        print(springOcc.name)
    #     inputentities = adsk.core.ObjectCollection.create()
    #     inputentities.add(springOcc.component)
    #     transform = adsk.core.Matrix3D.create()
    #     transform.translation = adsk.core.Vector3D.create(self._x, self._y, 0)
    #    # transform.setToRotation()
    #     movefeatures = ao.root_comp.features.moveFeatures
    #     movefeatureinput = movefeatures.createInput(inputentities, transform)
    #     movefeatures.add(movefeatureinput)
        
    def createSpring(self):
        ao = AppObjects()
        mainBodyOcc = ao.root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        mainBodyComponent = mainBodyOcc.component
        mainBodyOcc.component.name = 'Spring'
    
        sketches = mainBodyComponent.sketches
        sketch = sketches.addWithoutEdges(self._plane)
        

        points = []
        points2 = []
        points3 = []
        points4 = []
        arcs = sketch.sketchCurves.sketchArcs
        spaceDivider = self._coilThickness * 3

        for i in range(self._springCoils * 4):
            points.append(adsk.core.Point3D.create(0, i * self._coilThickness /2, 0))
            points2.append(adsk.core.Point3D.create(self._springWidth /2 -(self._spaceBetween /2) -spaceDivider, i * self._coilThickness /2, 0))
            
        for i in range(self._springCoils * 4):
            points3.append(adsk.core.Point3D.create(self._springWidth/2 +(self._spaceBetween /2), i * self._coilThickness /2, 0))
            points4.append(adsk.core.Point3D.create(self._springWidth -(self._coilThickness*3) , i * self._coilThickness /2, 0))
            
        leftArcsArray = self.pointsToSpring(sketch, points,points2)
        rightArcArray = self.pointsToSpring(sketch, points4,points3)
        lines = sketch.sketchCurves.sketchLines
        #close inner structure
        lines.addByTwoPoints(leftArcsArray[0][0][1].endSketchPoint, rightArcArray[0][0][1].startSketchPoint)  
        lines.addByTwoPoints(leftArcsArray[0][-1][1].startSketchPoint, rightArcArray[0][-1][1].endSketchPoint)  
        
        #sideWall left spring
        offsetVec = adsk.core.Vector3D.create(-self._coilThickness*1.5, 0 , 0)
        sidwallLeftStartPoint = adsk.core.Point3D.cast(leftArcsArray[1][0][1].endSketchPoint.geometry.copy())
        sidwallLeftStartPoint.translateBy(offsetVec)
        sidwallLeftEndPoint = adsk.core.Point3D.cast(leftArcsArray[1][-1][1].startSketchPoint.geometry.copy())
        sidwallLeftEndPoint.translateBy(offsetVec)
        
        #lines.addByTwoPoints(sidwallLeftStartPoint, sidwallLeftEndPoint) 
        lines.addByTwoPoints(sidwallLeftStartPoint, leftArcsArray[1][0][1].endSketchPoint) 
        lines.addByTwoPoints(leftArcsArray[1][-1][1].startSketchPoint, sidwallLeftEndPoint)  
        
        #sideWall right spring
        offsetVec = adsk.core.Vector3D.create(self._coilThickness*1.5, 0 , 0)
        sidwallRightStartPoint = adsk.core.Point3D.cast(rightArcArray[1][0][1].startSketchPoint.geometry.copy())
        sidwallRightStartPoint.translateBy(offsetVec)
        sidwallRightEndPoint = adsk.core.Point3D.cast(rightArcArray[1][-1][1].endSketchPoint.geometry.copy())
        sidwallRightEndPoint.translateBy(offsetVec)
        
        #lines.addByTwoPoints(sidwallRightStartPoint, sidwallRightEndPoint)   
        lines.addByTwoPoints(sidwallRightStartPoint, rightArcArray[1][0][1].startSketchPoint) 
        lines.addByTwoPoints(rightArcArray[1][-1][1].endSketchPoint, sidwallRightEndPoint)  
        
        # sliding guide right
        offsetVec = adsk.core.Vector3D.create(0,self._coilThickness*3, 0)
        guideRightEndPoint = adsk.core.Point3D.cast(sidwallRightEndPoint.copy())
        guideRightEndPoint.translateBy(offsetVec)
        
        lines.addByTwoPoints(sidwallRightEndPoint, guideRightEndPoint)  
        guideLeftEndPoint = adsk.core.Point3D.cast(sidwallLeftEndPoint.copy())
        guideLeftEndPoint.translateBy(offsetVec)
        
        lines.addByTwoPoints(sidwallLeftEndPoint, guideLeftEndPoint)
        lines.addByTwoPoints(guideRightEndPoint, guideLeftEndPoint)
        
        #bottom
        offsetVec = adsk.core.Vector3D.create(0,-self._coilThickness*2, 0)
        bottomLeftStartPoint = sidwallLeftStartPoint
        bottomLeftEndPoint = adsk.core.Point3D.cast(bottomLeftStartPoint.copy())
        bottomLeftEndPoint.translateBy(offsetVec)
        
        lines.addByTwoPoints(bottomLeftStartPoint, bottomLeftEndPoint)
        
        bottomRightStartPoint = sidwallRightStartPoint
        bottomRightEndPoint = adsk.core.Point3D.cast(bottomRightStartPoint.copy())
        bottomRightEndPoint.translateBy(offsetVec)
        
        lines.addByTwoPoints(bottomRightStartPoint, bottomRightEndPoint)
        lines.addByTwoPoints(bottomLeftEndPoint, bottomRightEndPoint)

        
        extrudes = mainBodyComponent.features.extrudeFeatures
        extrudeInput = extrudes.createInput(sketch.profiles.item(1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        
        start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(self._extrudeOffset))

        extrudeInput.startExtent = start_from

        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
        
        return mainBodyOcc


    def pointsToSpring(self, sketch, points,  points2):
        lines = sketch.sketchCurves.sketchLines
        smallArcs = []
        bigArcs = []
        for i , point in enumerate(points):
         #   if i == 0:
          #      self.centerToCenterSlot(sketch,points[i], points2[i], coilThickness , math.pi)
           #     self.centerToCenterSlot(sketch,points[i], points2[i], coilThickness*3, 1.91113553)
            
            
            if i %8 == 0:
                smallArcs.append(self.centerToCenterSlot(sketch,points[i], points2[i], self._coilThickness , math.pi))
                bigArcs.append(self.centerToCenterSlot(sketch,points[i], points2[i], self._coilThickness*3, math.pi))
                
            elif i%4 == 0:
                smallArcs.append(self.centerToCenterSlot(sketch,points2[i], points[i], self._coilThickness, math.pi))
                bigArcs.append(self.centerToCenterSlot(sketch,points2[i], points[i], self._coilThickness*3, math.pi))

                
            if i%2 == 0 and i < len(points) -4:
                lines.addByTwoPoints(points[i+1], points2[i+1])
                
        return [smallArcs, bigArcs]
    
    
    def centerToCenterSlot(self, sketch, point1, point2, width, angle):
        try:
            sk = adsk.fusion.Sketch.cast(sketch)

            lines = sk.sketchCurves.sketchLines
            centerLine = lines.addByTwoPoints(point1, point2)
            centerLine.isConstruction = True
            
            slotAngle = self.bearing(point1, point2) 
            offsetAngle = slotAngle + math.pi/2    
            offsetVec = adsk.core.Vector3D.create(math.cos(offsetAngle), math.sin(offsetAngle), 0)
            offsetVec.scaleBy(width/2)
            
            newPnt = adsk.core.Point3D.cast(point1.copy())
            newPnt.translateBy(offsetVec)
     
            arcs = sk.sketchCurves.sketchArcs
            arc = arcs.addByCenterStartSweep(point1, newPnt, angle)

    
            return [centerLine, arc]
        except:
            return None
        
    # Returns the angle defined by two points where they are assumed to be on the X-Y plane and the zero
    # angle is defined by the x-axis.
    def bearing(self, point1, point2):
        pointDist = point1.distanceTo(point2)
        # Determine which quadrant the point is in.
        if point2.x >= point1.x and point2.y >= point1.y:
            # First quadrant
            return math.acos((point2.x - point1.x) / pointDist)
        elif point2.x < point1.x and point2.y >= point1.y:
            # Second quadrant
            return math.acos((point2.x - point1.x) / pointDist)
        elif point2.x >= point1.x and point2.y < point1.y:
            # Third quadrant
            return (math.pi * 2) - math.acos((point2.x - point1.x) / pointDist)
        else:
            # Fourth quadrant
            return (math.pi * 2) - math.acos((point2.x - point1.x) / pointDist)