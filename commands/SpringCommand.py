import adsk.core
import adsk.fusion
import adsk.cam
import math

# Import the entire apper package
import apper

# Alternatively you can import a specific function or class
from apper import AppObjects


class SpringCommand(apper.Fusion360CommandBase):

    # Run whenever a user makes any change to a value or selection in the addin UI
    # Commands in here will be run through the Fusion processor and changes will be reflected in  Fusion graphics area
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()
        
        springCoils = input_values['springCoils_input_id']
        widthSpring = input_values['widthSpring_input_id']
        springSpace = input_values['springSpace_input_id']
        springCoilThickness = input_values['springCoilThickness_input_id']
        materialThickness = input_values['materialThickness_input_id']
        
        all_selections = input_values.get('selection_input_id', None)
        if len(all_selections) > 0:
            ao.root_comp.isOriginFolderLightBulbOn = False
            the_first_selection = all_selections[0]
            Spring(0,0,0,the_first_selection, springCoils, widthSpring, springSpace, springCoilThickness, materialThickness ,0)
           # args.isValidResult = True
           # command.doExecute(False)

    # Run after the command is finished.
    # Can be used to launch another command automatically or do other clean up.
    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    # Run when any input is changed.
    # Can be used to check a value and then update the add-in UI accordingly
    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):

        pass

    # Run when the user presses OK
    # This is typically where your main program logic would go
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()
        springCoils = input_values['springCoils_input_id']
        widthSpring = input_values['widthSpring_input_id']
        springSpace = input_values['springSpace_input_id']
        springCoilThickness = input_values['springCoilThickness_input_id']
        materialThickness = input_values['materialThickness_input_id']
        
        all_selections = input_values.get('selection_input_id', None)
        if len(all_selections) > 0:
            ao.root_comp.isOriginFolderLightBulbOn = False
            the_first_selection = all_selections[0]
            Spring(0,0,0,the_first_selection, springCoils, widthSpring, springSpace, springCoilThickness, materialThickness ,0)
     
    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        ao = AppObjects()
        inputs.addSelectionInput('selection_input_id', 'Select a plane', 'Select Something')
        
        tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Spring')
        tabCmdInput2 = inputs.addTabCommandInput('tab_2', 'Spring Settings')
        
        tab1ChildInputs = tabCmdInput1.children
        tab2ChildInputs = tabCmdInput2.children
        
        # Create a default value using a string
        default_valueX = adsk.core.ValueInput.createByString('100 mm')
        default_valueY = adsk.core.ValueInput.createByString('50 mm')
        
       # default_offsetX = adsk.core.ValueInput.createByString('20 mm')
        #default_offsetY = adsk.core.ValueInput.createByString('10 mm')
        default_offset = adsk.core.ValueInput.createByString('5 mm')
        default_materialThickness = adsk.core.ValueInput.createByString('4 mm')
        
        default_springLength = adsk.core.ValueInput.createByString('15 mm')
        default_springCoilThickness = adsk.core.ValueInput.createByString('0.9 mm')
        default_springSpace = adsk.core.ValueInput.createByString('0.5 mm')
        
        # Get teh user's current units
        default_units = ao.units_manager.defaultLengthUnits

        tab1ChildInputs.addValueInput('materialThickness_input_id', 'Thickness',default_units , default_materialThickness)
        tab1ChildInputs.addValueInput('widthSpring_input_id', 'Spring Width', default_units, default_springLength)
        tab1ChildInputs.addValueInput('springCoilThickness_input_id', 'Spring Coil Thickness', default_units, default_springCoilThickness)
        tab1ChildInputs.addIntegerSpinnerCommandInput('springCoils_input_id', 'Spring Coils', 1, 60, 2, 3)
        tab1ChildInputs.addValueInput('springSpace_input_id', 'Spring space between', default_units, default_springSpace)


        
class Spring():

    def __init__(self,x,y,rotate,plane, springCoils, widthSpring, springSpace, springCoilThickness, materialThickness, extrudeOffset):
        ao = AppObjects()
        self._x = x
        self._y = 0.33
        self._rotate = rotate
        self._plane = plane
        self._springCoils = springCoils
        self._springWidth = widthSpring
        self._spaceBetween = springSpace
        self._coilThickness = springCoilThickness
        self._materialThickness = materialThickness
        self._extrudeOffset = extrudeOffset
        
        springOcc = self.createSpring()
        
        moveX = widthSpring/2 - ((springCoilThickness*3)/2) + self._x
        inputentities = adsk.core.ObjectCollection.create()
        inputentities.add(springOcc.component.bRepBodies.item(0))
        transform = adsk.core.Matrix3D.create()
        transform.translation = adsk.core.Vector3D.create(-moveX, self._y, 0)
       # transform.setToRotation()
       
        movefeatures = springOcc.component.features.moveFeatures  
        movefeatureinput = movefeatures.createInput(inputentities, transform)
        movefeatures.add(movefeatureinput)
        
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
        
        

        
        
        
        
        