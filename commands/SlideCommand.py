import adsk.core
import adsk.fusion
import adsk.cam
import math

# Import the entire apper package
import apper

# Alternatively you can import a specific function or class
from apper import AppObjects



class SlideCommand(apper.Fusion360CommandBase):

    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        
        all_selections = input_values.get('selection_input_id', None)
        if len(all_selections) > 0:
            
            the_first_selection = all_selections[0]
            self.drawLayers(input_values, inputs)
        
        args.isValidResult = True

    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):

        tab3 = inputs.itemById('tab_3')
        tab2 = inputs.itemById('tab_2')
        checkRoundRatchetValue = input_values['checkBoxRatchet_input_id']

        button = inputs.itemById('button_input_id')

        
        if checkRoundRatchetValue is True:
             tab3.isEnabled = True
             tab3.isVisible = True
             tab2.isEnabled = True
             tab2.isVisible = True
             button.isVisible = True
             
        else:
            tab3.isVisible = False
            tab3.isEnabled = False
            tab2.isEnabled = False
            tab2.isVisible = False
            button.isVisible = False

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        all_selections = input_values.get('selection_input_id', None)
        if len(all_selections) > 0:
            
            the_first_selection = all_selections[0]
            self.drawLayers(input_values, inputs)

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        ao = AppObjects()
        inputs.addSelectionInput('selection_input_id', 'Select a plane', 'Select Something')
        
        tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Slide')
        tabCmdInput2 = inputs.addTabCommandInput('tab_2', 'Spring Settings')
        tabCmdInput3 = inputs.addTabCommandInput('tab_3', 'Ratchet Settings')

        tab1ChildInputs = tabCmdInput1.children
        tab2ChildInputs = tabCmdInput2.children
        tab3ChildInputs = tabCmdInput3.children

        
        # Create a default value using a string
        default_valueX = adsk.core.ValueInput.createByString('100 mm')
        default_valueY = adsk.core.ValueInput.createByString('50 mm')
        default_ratchetSize = adsk.core.ValueInput.createByString('2 mm')

        default_slotWidth = adsk.core.ValueInput.createByString('20 mm')
        default_slotWidthOffset = adsk.core.ValueInput.createByString('10 mm')
        default_materialThickness = adsk.core.ValueInput.createByString('4 mm')
        
        default_springLength = adsk.core.ValueInput.createByString('15 mm')
        default_springCoilThickness = adsk.core.ValueInput.createByString('0.9 mm')
        default_springSpace = adsk.core.ValueInput.createByString('0.5 mm')
        default_springOffset = adsk.core.ValueInput.createByString('4 mm')
        default_buttonSize = adsk.core.ValueInput.createByString('5 mm')
        # Get teh user's current units
        default_units = ao.units_manager.defaultLengthUnits

        # Create a value input.  This will respect units and user defined equation input.
        tab1ChildInputs.addValueInput('width_input_id', 'Width', default_units, default_valueX)
        tab1ChildInputs.addValueInput('height_input_id', 'Height', default_units, default_valueY)
        
        tab1ChildInputs.addValueInput('slotHeight_input_id', 'Slot width',default_units , default_slotWidth)
        tab1ChildInputs.addValueInput('slotWidthOffset_input_id', 'Slot width offset',default_units , default_slotWidthOffset)
        tab1ChildInputs.addValueInput('buttonSize_input_id', 'buttonSize offset',default_units , default_buttonSize)
        tab1ChildInputs.addValueInput('materialThickness_input_id', 'Thickness',default_units , default_materialThickness)
        tab1ChildInputs.addBoolValueInput('checkBoxRatchet_input_id', 'Add Ratchet system', True, '', True)
        tab1ChildInputs.addBoolValueInput('button_input_id', 'Add unlock button', True, '', True)

        # Tab 2
        tab2ChildInputs.addValueInput('springCoilThickness_input_id', 'Spring Coil Thickness', default_units, default_springCoilThickness)
        tab2ChildInputs.addValueInput('springOffset_input_id', 'Spring Offset', default_units, default_springOffset)
        tab2ChildInputs.addIntegerSpinnerCommandInput('springCoils_input_id', 'Spring Coils', 1, 60, 2, 5)
        tab2ChildInputs.addValueInput('springSpace_input_id', 'Spring space between', default_units, default_springSpace)
        
        # Tab 3
        buttonRowInput2 = tab3ChildInputs.addButtonRowCommandInput('ratchetShape_input_id', 'Ratchet Shape', False)
        buttonRowInput2.listItems.add('Sine', True, "./commands/resources/Ratchet/SineIcon")
        buttonRowInput2.listItems.add('Saw', False, "./commands/resources/Ratchet/SawIcon")
        buttonRowInput2.listItems.add('Saw Inverted', False, "./commands/resources/Ratchet/SawInvertedIcon")
        buttonRowInput2.listItems.add('Triangle', False, "./commands/resources/Ratchet/TriangleIcon")
        buttonRowInput2.listItems.add('Square', False, "./commands/resources/Ratchet/SquareIcon")
        
        tab3ChildInputs.addIntegerSpinnerCommandInput('amountOfIndents_input_id', 'Amount of indents', 1, 60, 1, 5)
        
        sizeInput = tab3ChildInputs.addValueInput('ratchetSize_input_id', 'Depth of ratchet indent', default_units, default_ratchetSize)
        sizeInput.isVisible = False
        
        inputs.addTextBoxCommandInput('text_box_input_id', 'Info: ', '', 1, True)


    def drawLayers(self, input_values, inputs):
        ao = AppObjects()
        sliderOcc = apper.create_component(ao.root_comp, 'Slider')
        sliderComponent = sliderOcc.component
        
        pointA = self.outerPart(input_values, sliderComponent)
        shape = self.ratchetPart(input_values, sliderComponent)
        innerSliderOcc, pointB = self.innerSlidePart(input_values, sliderComponent, shape)
        topBottomOcc = self.topAndBottom(input_values, sliderComponent)
        
        
        occs = adsk.core.ObjectCollection.create()
        occs.add(innerSliderOcc)
        occs.add(topBottomOcc)
        rigidGroups = sliderComponent.rigidGroups
        rigidGroups.add(occs, True)
        
        self.addJoint(input_values, pointA, pointB)
        
        tab3 = inputs.itemById('tab_3')
        tab2 = inputs.itemById('tab_2')
        topLayer = topBottomOcc.component
        if topLayer:
            if tab3.isActive or tab2.isActive:
                topLayer.opacity = 0.2
            else:
                topLayer.opacity = 1
                    
          
    def ratchetPart(self, input_values, comp):
        # Input values -->
        ratchetSizeValue = input_values['ratchetSize_input_id']
        amountOfIndents = input_values['amountOfIndents_input_id']
        ratchetShapeValue = input_values['ratchetShape_input_id']
        slotHeight = input_values['slotHeight_input_id']
        slotWidthOffset = input_values['slotWidthOffset_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        extrudes = comp.features.extrudeFeatures
        sketches = comp.sketches
        
        pointColl = adsk.core.ObjectCollection.create()
        shapeColl = adsk.core.ObjectCollection.create()
        
        offsetY = (height -slotHeight) /2 
        depth = ratchetSizeValue
        
        sketcRatchetShape = sketches.addWithoutEdges(plane)
        sketcPoints= sketches.addWithoutEdges(plane)
        sketcRatchetShapeMultiple = sketches.addWithoutEdges(plane)
        offset = slotWidthOffset*2
        distance = ((width - offset - slotHeight ) /(amountOfIndents -1) ) 
        amount = 0
        result = math.floor((width-offset) / (depth*2))
        
        if amountOfIndents >= result:
            amountOfIndents = result

        for i in range(0, int(amountOfIndents)):
            point = adsk.core.Point3D.create(slotWidthOffset +(slotHeight/2) +amount, offsetY, 0)
            #sketcPoints.sketchPoints.add(point)
            pointColl.add(point)
            amount += distance
        
        point1 = adsk.core.Point3D.create(slotWidthOffset, offsetY, 0)  
        if ratchetShapeValue == "Sine":
    
            circles = sketcRatchetShape.sketchCurves.sketchCircles
            offset = (slotWidthOffset*2) + slotHeight
            distance = (width - offset ) /(amountOfIndents -1) 
            p2 = adsk.core.Point3D.create(slotWidthOffset +(slotHeight/2), offsetY, 0)
            shape = circles.addByCenterRadius(p2,depth)
            shapeColl.add(shape)
            self.makePattern(sketcRatchetShapeMultiple, shapeColl, amountOfIndents, distance)
            
        if ratchetShapeValue == "Saw":
            lines = sketcRatchetShape.sketchCurves.sketchLines
            point3 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/1.5), offsetY, 0)  

            point2 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/3), offsetY - depth, 0)
            point1 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/3), offsetY, 0)  
            line1  = lines.addByTwoPoints(point1, point2)
            line2 = lines.addByTwoPoints(point2, point3)
            line3 = lines.addByTwoPoints(point1, point3)
            shapeColl.add(line1)
            shapeColl.add(line2)
            shapeColl.add(line3)
            self.makePattern(sketcRatchetShapeMultiple, shapeColl, amountOfIndents , distance)

            
        if ratchetShapeValue == "Saw Inverted":
            lines = sketcRatchetShape.sketchCurves.sketchLines
            
            point3 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/3), offsetY, 0)  
            point2 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/1.5), offsetY - depth, 0)
            point1 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/1.5), offsetY, 0)  
            
            line1  = lines.addByTwoPoints(point1, point2)
            line2 = lines.addByTwoPoints(point2, point3)
            line3 = lines.addByTwoPoints(point1, point3)

            shapeColl.add(line1)
            shapeColl.add(line2)
            shapeColl.add(line3)
    
            self.makePattern(sketcRatchetShapeMultiple, shapeColl, amountOfIndents , distance)

            
        if ratchetShapeValue == "Square":
            offset = (slotWidthOffset*2) + slotHeight
            distance = (width - offset ) /(amountOfIndents -1) 

            lines = sketcRatchetShape.sketchCurves.sketchLines
            p1 = adsk.core.Point3D.create(slotWidthOffset+(slotHeight/2), offsetY, 0)
            p2 = adsk.core.Point3D.create(slotWidthOffset+ +(slotHeight/2) +depth, offsetY +depth , 0)
            rect = lines.addCenterPointRectangle(p1, p2)
            for lines in rect:
                shapeColl.add(lines)
            
            self.makePattern(sketcRatchetShapeMultiple, shapeColl, amountOfIndents, distance)   
                        
        if ratchetShapeValue == "Triangle":
            lines = sketcRatchetShape.sketchCurves.sketchLines
            point3 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/3), offsetY, 0)  
            point2 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/2), offsetY - depth, 0)
            point1 = adsk.core.Point3D.create(slotWidthOffset + (slotHeight/1.5), offsetY, 0)  
            
            line1  = lines.addByTwoPoints(point1, point2)
            line2 = lines.addByTwoPoints(point2, point3)
            line3 = lines.addByTwoPoints(point1, point3)
            shapeColl.add(line1)
            shapeColl.add(line2)
            shapeColl.add(line3)
            self.makePattern(sketcRatchetShapeMultiple, shapeColl, amountOfIndents , distance)
            
        for profile in sketcRatchetShapeMultiple.profiles:
            try:
                extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
                extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
                extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))
                extrudes.add(extrudeInput)
            except:
                print('nothing to cut')   
                
        return sketcRatchetShape       
        
    def makePattern(self, sketch, shapeColl, qty, distance):
        if shapeColl.count > 0:
            amount = 0
            for j in range(0, int(qty)):
                
             #   print("move: " + str(j))
                transform = adsk.core.Matrix3D.create()
                transform.translation = adsk.core.Vector3D.create(amount, 0 , 0)
                sketch.copy(shapeColl, transform)
                amount += distance
             
    def outerPart(self, input_values, comp):
        # Input values -->
        ratchetSizeValue = input_values['ratchetSize_input_id']
        ratchetShapeValue = input_values['ratchetShape_input_id']
        slotHeight = input_values['slotHeight_input_id']
        slotWidthOffset = input_values['slotWidthOffset_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        extrudes = comp.features.extrudeFeatures
        
        sketches = comp.sketches
        sketchOuter = sketches.addWithoutEdges(plane)
        linesOuter = sketchOuter.sketchCurves.sketchLines
        rectPoint = adsk.core.Point3D.create(width,height, 0)
        outerRectangle = linesOuter.addTwoPointRectangle(adsk.core.Point3D.create(0,0,0), rectPoint)
        shapeColl = adsk.core.ObjectCollection.create()
        pointColl = adsk.core.ObjectCollection.create()
        profile = sketchOuter.profiles.item(0)
        
        extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))
        extrudes.add(extrudeInput)
        
        offsetY = (height -slotHeight) /2 
        depth = ratchetSizeValue
        sketchInner = sketches.addWithoutEdges(plane)
        linesInner = sketchInner.sketchCurves.sketchLines
        
        slot = linesInner.addTwoPointRectangle(  adsk.core.Point3D.create(slotWidthOffset,offsetY,0), adsk.core.Point3D.create(width -slotWidthOffset,slotHeight +offsetY,0))
        
        extrudeInput = extrudes.createInput(sketchInner.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))
        extrudes.add(extrudeInput)
        pointA = linesInner.item(0).startSketchPoint
        
        return pointA
        
    def innerSlidePart(self, input_values,  compSlider, shape):
        
        # Input values -->
        ratchetSizeValue = input_values['ratchetSize_input_id']
        amountOfIndents = input_values['amountOfIndents_input_id']
        ratchetShapeValue = input_values['ratchetShape_input_id']
        slotHeight = input_values['slotHeight_input_id']
        slotWidthOffset = input_values['slotWidthOffset_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        innerSliderOcc = apper.create_component(compSlider, 'Inner Slider')
        comp = innerSliderOcc.component
        
        extrudes = comp.features.extrudeFeatures
        offsetY = (height -slotHeight)/2 

        sketches = comp.sketches
        sketchInnerSlide = sketches.addWithoutEdges(plane)
        linesSlideInner = sketchInnerSlide.sketchCurves.sketchLines
        rectPoint = adsk.core.Point3D.create(width,height, 0)
        slot = linesSlideInner.addTwoPointRectangle(adsk.core.Point3D.create(slotWidthOffset,offsetY,0), adsk.core.Point3D.create(slotWidthOffset + slotHeight,slotHeight +offsetY,0))
        profileRectInner = sketchInnerSlide.profiles.item(0)
        
        for profile in shape.profiles:    
        
            extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
            extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))
            ratchetShape = extrudes.add(extrudeInput)
 
        extrudeInput = extrudes.createInput(profileRectInner, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))
        innerPart = extrudes.add(extrudeInput)
        
        apper.combine_feature(innerPart.bodies.item(0), ratchetShape.bodies, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        
        spring = Spring(input_values, slotWidthOffset,offsetY, comp)
        extrude = spring.createSpring()
        pointB = linesSlideInner.item(0).startSketchPoint
        
        return innerSliderOcc, pointB
  
    def topAndBottom(self, input_values, compSlider):
        # Input values -->
        ratchetSizeValue = input_values['ratchetSize_input_id']
        amountOfIndents = input_values['amountOfIndents_input_id']
        ratchetShapeValue = input_values['ratchetShape_input_id']
        slotHeight = input_values['slotHeight_input_id']
        slotWidthOffset = input_values['slotWidthOffset_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        buttonSize = input_values['buttonSize_input_id']
        button = input_values['button_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        topBottomSliderOcc = apper.create_component(compSlider, 'Top and Bottom')
        comp = topBottomSliderOcc.component
        
        extrudes = comp.features.extrudeFeatures
        offsetY = (height -slotHeight) /2 

        sketches = comp.sketches
        sketchButtonTop = sketches.addWithoutEdges(plane)
        linesButtonTop = sketchButtonTop.sketchCurves.sketchLines
        rectPoint = adsk.core.Point3D.create(width,height, 0)
        offset = buttonSize
        
        buttonTop = linesButtonTop.addTwoPointRectangle(adsk.core.Point3D.create(slotWidthOffset-offset,offsetY-offset,0), adsk.core.Point3D.create(slotWidthOffset + slotHeight+offset,slotHeight +offsetY+offset,0))
        profileButtonTop = sketchButtonTop.profiles.item(0)
        
        extrudeInput = extrudes.createInput(profileButtonTop, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(0))
        top = extrudes.add(extrudeInput)
        
        sketches = comp.sketches
        sketchButtonBottom = sketches.addWithoutEdges(plane)
        linesButtonBottom = sketchButtonBottom.sketchCurves.sketchLines
        buttonBottom = linesButtonBottom.addTwoPointRectangle(adsk.core.Point3D.create(slotWidthOffset-offset,offsetY-offset,0), adsk.core.Point3D.create(slotWidthOffset + slotHeight +offset ,slotHeight +offsetY +offset,0))
        profileButtonBottom = sketchButtonBottom.profiles.item(0)
        
        extrudeInput = extrudes.createInput(profileButtonBottom, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness*2))
        top = extrudes.add(extrudeInput)
        if button:
            buttonSketch = sketches.addWithoutEdges(plane)
            linesButtonBottom = buttonSketch.sketchCurves.sketchLines
            button = linesButtonBottom.addTwoPointRectangle(adsk.core.Point3D.create(slotWidthOffset-offset +0.9,offsetY-offset   ,0), adsk.core.Point3D.create(slotWidthOffset + slotHeight +offset -0.9 ,slotHeight +offsetY +offset -1.5,0))
            profileButton = buttonSketch.profiles.item(0)
            extrudeInput = extrudes.createInput(profileButton, adsk.fusion.FeatureOperations.CutFeatureOperation)
            extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
            extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(0))
            top = extrudes.add(extrudeInput)
            
            buttonSketch = sketches.addWithoutEdges(plane)
            linesButtonBottom = buttonSketch.sketchCurves.sketchLines
            button = linesButtonBottom.addTwoPointRectangle(adsk.core.Point3D.create(slotWidthOffset-offset +0.9,offsetY-offset   ,0), adsk.core.Point3D.create(slotWidthOffset + slotHeight +offset -0.9 ,slotHeight +offsetY +offset -1.7,0))
            profileButton = buttonSketch.profiles.item(0)
            extrudeInput = extrudes.createInput(profileButton, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
            extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(0))
            top = extrudes.add(extrudeInput)
     
        
        return topBottomSliderOcc
        
    def addJoint(self,input_values,  sketchPointA,sketchPointB):
       
        # Input values -->
        slotWidthOffset = input_values['slotWidthOffset_input_id']
        slotHeight = input_values['slotHeight_input_id']
        width = input_values['width_input_id']
        # <-- Input values
        
        ao = AppObjects()
        #Joint
        geo0 = adsk.fusion.JointGeometry.createByPoint(sketchPointB)
        geo1 = adsk.fusion.JointGeometry.createByPoint(sketchPointA)

        # Create joint input
        joints = ao.root_comp.joints
        jointInput = joints.createInput(geo0, geo1)
        # angleValue = adsk.core.ValueInput.createByString(math.radians(angle))
    
        jointInput.setAsSliderJointMotion(adsk.fusion.JointDirections.XAxisJointDirection)
        # Create the joint
        joint = joints.add(jointInput)
        
        sliderMotion = joint.jointMotion
        limits = sliderMotion.slideLimits
        limits.isMinimumValueEnabled = True
        limits.minimumValue = slotWidthOffset - (slotHeight /2)
        limits.isMaximumValueEnabled = True
        limits.maximumValue = width - (slotWidthOffset*2) - slotHeight 
        sliderMotion.slideValue = width/2 -(slotWidthOffset*2)

            
class Spring():

    def __init__(self,input_values, xOffset,yOffset, comp):
       
        self._springCoils = input_values['springCoils_input_id']
       
        self._springWidth = input_values['slotHeight_input_id']
        self._spaceBetween = input_values['springSpace_input_id']
        self._springCoilThickness = input_values['springCoilThickness_input_id']
        self._materialThickness = input_values['materialThickness_input_id']
        self._slotHeight = input_values['slotHeight_input_id'] 
        all_selections = input_values.get('selection_input_id', None)
        self._plane = all_selections[0]
        self._slotWidthOffset = input_values['slotWidthOffset_input_id']
        self._width = input_values['width_input_id']
        self._height = input_values['height_input_id']
        self._offsetSidesSpring = input_values['springOffset_input_id']
        self._springWidth = self._springWidth - (self._offsetSidesSpring *2)
        
        self._x = -self._springWidth/2 + (self._springCoilThickness*1.5) +xOffset +(self._slotHeight /2) 
        self._y = yOffset - (self._springCoilThickness *2)+(self._slotHeight /2)
    
        self._comp = comp
                 
    def createSpring(self):
        ao = AppObjects()
        mainBodyComponent = self._comp
        sketches = mainBodyComponent.sketches
        sketch = sketches.addWithoutEdges(self._plane)
        offsetY = (self._height -self._slotHeight) /2 
        
        rectAroundSpringOffset = 0.01
        points = []
        points2 = []
        points3 = []
        points4 = []
        arcs = sketch.sketchCurves.sketchArcs
        spaceDivider = self._springCoilThickness * 3
   
        lines = sketch.sketchCurves.sketchLines
      #  rect = lines.addTwoPointRectangle(adsk.core.Point3D.create(self._slotWidthOffset +self._offsetSidesSpring, offsetY +self._offsetSidesSpring, 0), adsk.core.Point3D.create(self._slotWidthOffset +self._slotHeight -self._offsetSidesSpring, self._slotHeight +offsetY -self._offsetSidesSpring , 0))
       # rect2 = lines.addTwoPointRectangle(adsk.core.Point3D.create(self._slotWidthOffset +self._offsetSidesSpring-rectAroundSpringOffset, offsetY +self._offsetSidesSpring, 0), adsk.core.Point3D.create(self._slotWidthOffset +self._slotHeight -self._offsetSidesSpring+rectAroundSpringOffset, self._slotHeight +offsetY -self._offsetSidesSpring , 0))

        #circles = sketch.sketchCurves.sketchCircles

        #circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), self._height/2 )
        
        for i in range(self._springCoils * 4):
            points.append(adsk.core.Point3D.create(self._x + 0, self._y+ i * self._springCoilThickness /2, 0))
            points2.append(adsk.core.Point3D.create(self._x+ self._springWidth /2 -(self._spaceBetween /2) -spaceDivider, self._y+ i * self._springCoilThickness /2, 0))
            
        for i in range(self._springCoils * 4):
            points3.append(adsk.core.Point3D.create(self._x+ self._springWidth/2 +(self._spaceBetween /2), self._y+ i * self._springCoilThickness /2, 0))
            points4.append(adsk.core.Point3D.create(self._x+ self._springWidth -(self._springCoilThickness*3) , self._y+ i * self._springCoilThickness /2, 0))
        
        leftArcsArray = self.pointsToSpring(sketch, points,points2)
        rightArcArray = self.pointsToSpring(sketch, points4,points3)
      
        #close inner structure
        lines.addByTwoPoints(leftArcsArray[0][0][1].endSketchPoint, rightArcArray[0][0][1].startSketchPoint)  
        lines.addByTwoPoints(leftArcsArray[0][-1][1].startSketchPoint, rightArcArray[0][-1][1].endSketchPoint)  
        
        #sideWall left spring
        offsetVec = adsk.core.Vector3D.create(-self._springCoilThickness*1.5 - rectAroundSpringOffset , 0 , 0)
        offsetVec2 = adsk.core.Vector3D.create(-self._springCoilThickness*1.5 , 0 , 0)
        
        sidwallLeftStartPoint = adsk.core.Point3D.cast(leftArcsArray[1][0][1].endSketchPoint.geometry.copy())
        sidwallLeftStartPoint.translateBy(offsetVec2)
        
        sidwallLeftEndPoint = adsk.core.Point3D.cast(leftArcsArray[1][-1][1].startSketchPoint.geometry.copy())
        sidwallLeftEndPoint.translateBy(offsetVec)
        
        #lines.addByTwoPoints(sidwallLeftStartPoint, sidwallLeftEndPoint) 
        bottomLeftSmall = lines.addByTwoPoints(sidwallLeftStartPoint, leftArcsArray[1][0][1].endSketchPoint) 
        
        topLeftSmall = lines.addByTwoPoints(leftArcsArray[1][-1][1].startSketchPoint, sidwallLeftEndPoint)  
        
        #sideWall right spring
        offsetVec = adsk.core.Vector3D.create(self._springCoilThickness*1.5 +rectAroundSpringOffset , 0 , 0)
        offsetVec2 = adsk.core.Vector3D.create(self._springCoilThickness*1.5 , 0 , 0)
        
        sidwallRightStartPoint = adsk.core.Point3D.cast(rightArcArray[1][0][1].startSketchPoint.geometry.copy())
        sidwallRightStartPoint.translateBy(offsetVec2)
        
        sidwallRightEndPoint = adsk.core.Point3D.cast(rightArcArray[1][-1][1].endSketchPoint.geometry.copy())
        sidwallRightEndPoint.translateBy(offsetVec)
        
        #lines.addByTwoPoints(sidwallRightStartPoint, sidwallRightEndPoint)   
        
        #connected to arc top goes to right
        bottomRightSmall= lines.addByTwoPoints(sidwallRightStartPoint, rightArcArray[1][0][1].startSketchPoint) 
        topRightSmall = lines.addByTwoPoints(rightArcArray[1][-1][1].endSketchPoint, sidwallRightEndPoint)  
        
        # sliding guide right
        offsetVec = adsk.core.Vector3D.create(0,self._springCoilThickness , 0)
        guideRightEndPoint = adsk.core.Point3D.cast(sidwallRightEndPoint.copy())
        guideRightEndPoint.translateBy(offsetVec)
      
        #sideWallRighTop = lines.addByTwoPoints(sidwallRightEndPoint, guideRightEndPoint)  
        sideWallRighTop = adsk.core.Line3D.create(sidwallRightEndPoint, guideRightEndPoint)
        
        #pointsRight = sideWallRighTop.asInfiniteLine().intersectWithCurve(circle.geometry)
        sideWallRightBottom = adsk.core.Point3D.create(sidwallRightEndPoint.x, offsetY,0)
        lines.addByTwoPoints(sideWallRightBottom, sidwallRightEndPoint)
        
        guideLeftEndPoint = adsk.core.Point3D.cast(sidwallLeftEndPoint.copy())
        guideLeftEndPoint.translateBy(offsetVec)
        
        # Top line 
        #sideWallLeftTop = lines.addByTwoPoints(sidwallLeftEndPoint, guideLeftEndPoint)
        sideWallLeftTop = adsk.core.Line3D.create(sidwallLeftEndPoint, guideLeftEndPoint)
        
       # topLine = lines.addByTwoPoints(guideRightEndPoint, guideLeftEndPoint)
       
        #points = sideWallLeftTop.asInfiniteLine().intersectWithCurve(circle.geometry)
        sideWallLeftBottom = adsk.core.Point3D.create(sidwallLeftEndPoint.x, offsetY,0)
        lines.addByTwoPoints(sideWallLeftBottom, sidwallLeftEndPoint)
   
        #bottom
        offsetVec = adsk.core.Vector3D.create(0,-self._springCoilThickness*2 , 0)
       
        bottomLeftStartPoint = sidwallLeftStartPoint
        bottomLeftEndPoint = adsk.core.Point3D.create(bottomLeftStartPoint.x, offsetY,0)
        lines.addByTwoPoints(bottomLeftStartPoint, bottomLeftEndPoint)
       # bottomLeftEndPoint = adsk.core.Point3D.cast(bottomLeftStartPoint.copy())
       # bottomLeftEndPoint.translateBy(offsetVec)
        
        #sidewallLeftBottom = adsk.core.Line3D.create(bottomLeftStartPoint, bottomLeftEndPoint)
        #pointsInsideA = sidewallLeftBottom.asInfiniteLine().intersectWithCurve(circle.geometry)
       # lines.addByTwoPoints(pointsInsideA.item(0), bottomLeftStartPoint)
        
        bottomRightStartPoint = sidwallRightStartPoint
        bottomRightEndPoint = adsk.core.Point3D.create(bottomRightStartPoint.x, offsetY,0)
        lines.addByTwoPoints(bottomRightStartPoint, bottomRightEndPoint)
        #bottomRightEndPoint = adsk.core.Point3D.cast(bottomRightStartPoint.copy())
       # bottomRightEndPoint.translateBy(offsetVec)
        
       # sidewallRightBottom =  adsk.core.Line3D.create(bottomRightStartPoint, bottomRightEndPoint)
       
       # pointsInsideB = sidewallRightBottom.asInfiniteLine().intersectWithCurve(circle.geometry)
        lines.addByTwoPoints(sideWallLeftBottom, sideWallRightBottom)
    
        
        # sketchEntities = adsk.core.ObjectCollection.create()
        
 
        # all = adsk.core.ObjectCollection.create()
        # for c in sketch.sketchCurves:
        #     all.add(c)
        # for p in sketch.sketchPoints:
        #     all.add(p)
            
        # normal = sketch.xDirection.crossProduct(sketch.yDirection)
        # normal.transformBy(sketch.transform)
        # origin = sketch.origin
        # origin.transformBy(sketch.transform)
        # mat = adsk.core.Matrix3D.create()
        # mat.setToRotation(math.pi , normal, origin)
        # sketch.move(all, mat)
        
        #print(guideRightEndPoint.distanceTo(bottomRightEndPoint))
        
        if True:
            for profile in sketch.profiles:
                extrudes = mainBodyComponent.features.extrudeFeatures
                extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
                extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
                
                start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(self._materialThickness))

                extrudeInput.startExtent = start_from

                extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
            
        return extrude

    def pointsToSpring(self, sketch, points,  points2):
        lines = sketch.sketchCurves.sketchLines
        smallArcs = []
        bigArcs = []
        for i , point in enumerate(points):
         #   if i == 0:
          #      self.centerToCenterSlot(sketch,points[i], points2[i], coilThickness , math.pi)
           #     self.centerToCenterSlot(sketch,points[i], points2[i], coilThickness*3, 1.91113553)
            
            
            if i %8 == 0:
                smallArcs.append(self.centerToCenterSlot(sketch,points[i], points2[i], self._springCoilThickness , math.pi))
                bigArcs.append(self.centerToCenterSlot(sketch,points[i], points2[i], self._springCoilThickness*3, math.pi))
                
            elif i%4 == 0:
                smallArcs.append(self.centerToCenterSlot(sketch,points2[i], points[i], self._springCoilThickness, math.pi))
                bigArcs.append(self.centerToCenterSlot(sketch,points2[i], points[i], self._springCoilThickness*3, math.pi))

                
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