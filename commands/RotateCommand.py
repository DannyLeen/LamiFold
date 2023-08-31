import adsk.core
import adsk.fusion
import adsk.cam
import math

# Import the entire apper package
import apper
# Alternatively you can import a specific function or class
from apper import AppObjects


class RotateCommand(apper.Fusion360CommandBase):
    
    
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()
        all_selections = input_values.get('selection_input_id', None)
        text_box_input = inputs.itemById('text_box_input_id')
        tab3 = inputs.itemById('tab_3')
        tab2 = inputs.itemById('tab_2')

        if len(all_selections) > 0:
            ao.root_comp.isOriginFolderLightBulbOn = False
            the_first_selection = all_selections[0]
            state = self.drawLayers(input_values, inputs)            
            text_box_input.text = state
               
        args.isValidResult = True


    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):

        checkBoxAngleValue = input_values.get('checkBoxAngle_input_id', None)
        angle_input = inputs.itemById('angle_input_id')
        ratchetSize_input = inputs.itemById('ratchetSize_input_id')
        tab3 = inputs.itemById('tab_3')
        tab2 = inputs.itemById('tab_2')
        roundBottom_input = inputs.itemById('checkRoundBottom_input_id')
        checkRoundRatchetValue = input_values['checkBoxRatchet_input_id']
        checkBoxRatchetSizeValue = input_values['checkBoxRatchetSize_input_id']
        button = inputs.itemById('button_input_id')
        if checkBoxAngleValue is True:
            angle_input.isVisible = True
            roundBottom_input.isVisible = False
        else:
            angle_input.isVisible = False
            roundBottom_input.isVisible = True
            
        if checkBoxRatchetSizeValue is True: 
            ratchetSize_input.isVisible = False
        else:
            ratchetSize_input.isVisible = True
        
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
        ao = AppObjects()
        all_selections = input_values.get('selection_input_id', None)
        text_box_input = inputs.itemById('text_box_input_id')

        
        if len(all_selections) > 0:
            ao.root_comp.isOriginFolderLightBulbOn = False
            the_first_selection = all_selections[0]
            state = self.drawLayers(input_values)            
            text_box_input.text = state
               
   
        args.isValidResult = True

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        ao = AppObjects()
        iconResources = './resources/button'
        self._sketch = None
        self._ent = None
        
        tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Rotate')
        tabCmdInput2 = inputs.addTabCommandInput('tab_2', 'Spring Settings')
        tabCmdInput3 = inputs.addTabCommandInput('tab_3', 'Ratchet Settings')
        tabCmdInput3.isVisible = False
        tabCmdInput2.isVisible = False
        tab1ChildInputs = tabCmdInput1.children
        tab2ChildInputs = tabCmdInput2.children
        tab3ChildInputs = tabCmdInput3.children
        
        tab1ChildInputs.addSelectionInput('selection_input_id', 'Select a plane', 'Select Something')
        # Create a default value using a string
        default_valueX = adsk.core.ValueInput.createByString('100 mm')
        default_valueY = adsk.core.ValueInput.createByString('50 mm')
        
       # default_offsetX = adsk.core.ValueInput.createByString('20 mm')
        default_ratchetSize = adsk.core.ValueInput.createByString('3 mm')
        default_offset = adsk.core.ValueInput.createByString('7 mm')
        default_materialThickness = adsk.core.ValueInput.createByString('4 mm')
        
        default_springLength = adsk.core.ValueInput.createByString('15 mm')
        default_springCoilThickness = adsk.core.ValueInput.createByString('0.9 mm')
        default_springSpace = adsk.core.ValueInput.createByString('0.5 mm')
        
        # Get teh user's current units
        default_units = ao.units_manager.defaultLengthUnits

        # Create a value input.  This will respect units and user defined equation input.
        tab1ChildInputs.addValueInput('width_input_id', 'Width', default_units, default_valueX)
        tab1ChildInputs.addValueInput('height_input_id', 'Height', default_units, default_valueY)
        
        tab1ChildInputs.addValueInput('offset_input_id', 'Internal offset',default_units , default_offset)
        tab1ChildInputs.addValueInput('materialThickness_input_id', 'Thickness',default_units , default_materialThickness)
        tab1ChildInputs.addBoolValueInput('checkBoxAngle_input_id', 'Constrain Angle?', True, '', True)
        roundBottom = tab1ChildInputs.addBoolValueInput('checkRoundBottom_input_id', 'Round Bottom', True, '', False)
        roundBottom.isVisible = False
        angle = tab1ChildInputs.addValueInput('angle_input_id', 'Angle', 'deg', adsk.core.ValueInput.createByString('90.0 deg'))
        tab1ChildInputs.addBoolValueInput('checkBoxRatchet_input_id', 'Add Ratchet system', True, '', False)
        button = tab1ChildInputs.addBoolValueInput('button_input_id', 'Add unlock button', True, '', False)
        button.isVisible = False
        debug = tab1ChildInputs.addBoolValueInput('checkDebug_input_id', 'debug:', True, '', False)
        debug.isVisible = False
        
        # Tab 2
        tab2ChildInputs.addValueInput('widthSpring_input_id', 'Spring Width', default_units, default_springLength)
        tab2ChildInputs.addValueInput('springCoilThickness_input_id', 'Spring Coil Thickness', default_units, default_springCoilThickness)
        tab2ChildInputs.addIntegerSpinnerCommandInput('springCoils_input_id', 'Spring Coils', 1, 60, 2, 3)
        tab2ChildInputs.addValueInput('springSpace_input_id', 'Spring space between', default_units, default_springSpace)
        
        # Tab 3
        buttonRowInput2 = tab3ChildInputs.addButtonRowCommandInput('ratchetShape_input_id', 'Ratchet Shape', False)
        buttonRowInput2.listItems.add('Sine', True, "./commands/resources/Ratchet/SineIcon")
        buttonRowInput2.listItems.add('Saw', False, "./commands/resources/Ratchet/SawIcon")
        buttonRowInput2.listItems.add('Saw Inverted', False, "./commands/resources/Ratchet/SawInvertedIcon")
        buttonRowInput2.listItems.add('Triangle', False, "./commands/resources/Ratchet/TriangleIcon")
        buttonRowInput2.listItems.add('Square', False, "./commands/resources/Ratchet/SquareIcon")
        
        tab3ChildInputs.addIntegerSpinnerCommandInput('amountOfIndents_input_id', 'Amount of indents', 1, 60, 1, 16)
        tab3ChildInputs.addBoolValueInput('checkBoxRatchetSize_input_id', 'Dynamic sizing', True, '', True)
        
        sizeInput = tab3ChildInputs.addValueInput('ratchetSize_input_id', 'Depth of ratchet indent', default_units, default_ratchetSize)
        sizeInput.isVisible = False
        
        inputs.addTextBoxCommandInput('text_box_input_id', 'Info: ', '', 1, True)

    def drawLayers(self, input_values, inputs):
        ao = AppObjects()
        # Input value -->
        materialThickness = input_values['materialThickness_input_id']
        angle = input_values['angle_input_id']
        checkBoxAngle = input_values['checkBoxAngle_input_id']
        checkDebug = input_values['checkDebug_input_id']
         # <-- Input value

        rotateOcc = apper.create_component(ao.root_comp, 'Rotate')
        
        id = apper.item_id(rotateOcc, "Rotate")
        rotateOcc.attributes.add("Rotate-" + id, "Thickness", str(materialThickness))
        
        if materialThickness > 0:
            occPartsBottom = self.drawRotateLayer(rotateOcc, input_values, 0,'BottomLayer')
            occPartsMid = self.drawRotateLayer(rotateOcc, input_values,materialThickness ,'MidLayer')
            occPartsTop = self.drawRotateLayer(rotateOcc, input_values, materialThickness*2 ,'TopLayer')
            
            if checkDebug is False:
                if checkBoxAngle:
                    occA = adsk.core.ObjectCollection.create()
                    occA.add(occPartsTop['occA'])
                    occA.add(occPartsMid['occB'])
                    occA.add(occPartsBottom['occA'])
                    rigidGroupsA = rotateOcc.component.rigidGroups
                    rigidGroupsA.add(occA, True)
                    
                    occsB = adsk.core.ObjectCollection.create()
                    occsB.add(occPartsTop['occB'])
                    occsB.add(occPartsMid['occA'])
                    occsB.add(occPartsBottom['occB'])
                    rigidGroupsB = rotateOcc.component.rigidGroups
                    rigidGroupsB.add(occsB, True)
                    
                    self.addJoint(occPartsTop['pointA'], occPartsTop['pointB'], angle)
                    splitBodyFeats = rotateOcc.component.features.splitBodyFeatures
                    splitBodyInput = splitBodyFeats.createInput(occPartsMid['occB'].component.bRepBodies.item(1), occPartsMid['occA'].component.bRepBodies.item(0),False)
                    splitBodies = splitBodyFeats.add(splitBodyInput)
                  
                    glueBody = splitBodies.bodies.item(0)
                     
                    centerBodyNotUsed = splitBodies.bodies.item(1)
                    centerBodyNotUsed.isLightBulbOn = False
                    centerBodyNotUsed.name = "Center not used"
                    glueBody.isLightBulbOn = False
                    glueBody.name = "GlueBody Keepout"
                    glueBody.attributes.add('KeepOut', 'RotateCenter' + id, str(materialThickness))
                    
                    attribsSpring = ao.design.findAttributes('KeepOut', 'Spring')
                    for attr in attribsSpring:     
                        springKeepOutBody = attr.parent
                        self.combine(rotateOcc, springKeepOutBody, glueBody)
                        attr.deleteMe()
                    self.combineCut(rotateOcc, occPartsTop['occA'].component.bRepBodies.item(0), occPartsTop['occB'].component.bRepBodies.item(0))
                    #self.combineCut(rotateOcc, occPartsMid['occA'].component.bRepBodies.item(0), occPartsMid['occB'].component.bRepBodies.item(1))
                    self.combineCut(rotateOcc, occPartsBottom['occA'].component.bRepBodies.item(0), occPartsBottom['occB'].component.bRepBodies.item(0))
                else:
                    #keepout definieren voor unconstrained = volledige mid body copy pasten als keepout
                    occA = adsk.core.ObjectCollection.create()
                    occA.add(occPartsTop['occA'])
                    occA.add(occPartsBottom['occA'])
                    rigidGroupsA = rotateOcc.component.rigidGroups
                    rigidGroupsA.add(occA, True)
                    self.addJoint(occPartsBottom['pointA'], occPartsMid['pointA'], 0)
        
       
        
        tab3 = inputs.itemById('tab_3')
        tab2 = inputs.itemById('tab_2')
        topLayer = occPartsTop['occA'].component
        if topLayer:
            if tab3.isActive or tab2.isActive:
                topLayer.opacity = 0.2
            else:
                topLayer.opacity = 1
                
            return 'All Good!'
        else:
            return 'materialThickness 0'

    def combineCut(self, occ, tool, target):
        combine_features = occ.component.features.combineFeatures
        combine_tools = adsk.core.ObjectCollection.create()
        combine_tools.add(tool)

        combine_input = combine_features.createInput(target, combine_tools)
        combine_input.isKeepToolBodies = True
        combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation #cut bodies
        combine_features.add(combine_input)
        
    def combine(self, occ, tool, target):
        combine_features = occ.component.features.combineFeatures
        combine_tools = adsk.core.ObjectCollection.create()
        combine_tools.add(tool)

        combine_input = combine_features.createInput(target, combine_tools)
        combine_input.isKeepToolBodies = False
        combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation 
        combineFeat = combine_features.add(combine_input)
       # return combineFeat.bodies.item(0)
        
    def drawRotateLayer(self, rotateOcc, input_values, offset, layerName):
    
        partAOcc, pointA  = self.partA(rotateOcc, input_values, offset, layerName)
        partBOcc, pointB = self.partB(rotateOcc, input_values, offset, layerName)
        
        return {'occA': partAOcc,'occB':partBOcc,'pointA':pointA, 'pointB':pointB}
        
    def partA(self, rotateOcc, input_values, offset, layerName):
        ao = AppObjects()
        # Input values -->
        offsetCircle = input_values['offset_input_id']
        materialThickness = input_values['materialThickness_input_id']
        checkDebug = input_values['checkDebug_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        partAOcc = apper.create_component(rotateOcc.component, layerName + ' PartA')
        extrudes = partAOcc.component.features.extrudeFeatures
        sketches = partAOcc.component.sketches
        
        sketch = sketches.addWithoutEdges(plane)
        sketchPoints = sketch.sketchPoints
        sketch.name = 'SketchPoint'
        point = adsk.core.Point3D.create(0, 0, materialThickness*3)
        sketchPoint = sketchPoints.add(point)

        if layerName == 'MidLayer':
            sketch = self.drawMidLayer(sketches, input_values)         

        if layerName == 'BottomLayer':
            sketch = self.drawBottomLayer(sketches, input_values)
       
        if layerName == 'TopLayer':
            sketch = self.drawTopLayer(sketches, input_values)
            
        if sketch and checkDebug is False:  
            profile = sketch.profiles.item(0)
            
            extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
            extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(offset))     
            extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput))
        
        return partAOcc, sketchPoint
    
    def partB(self,rotateOcc, input_values, offset, layerName):
        # Input values -->
        offsetCircle = input_values['offset_input_id']
        materialThickness = input_values['materialThickness_input_id']
        angle = input_values['angle_input_id']
        checkBoxAngle = input_values['checkBoxAngle_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        checkDebug = input_values['checkDebug_input_id']
        checkBoxRatchetValue = input_values['checkBoxRatchet_input_id']

        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        springSketch = None
        partBOcc = apper.create_component(rotateOcc.component, layerName + ' PartB')
        extrudes = partBOcc.component.features.extrudeFeatures
        sketches = partBOcc.component.sketches
        sketch = sketches.addWithoutEdges(plane)
        sketchPoints = sketch.sketchPoints
        sketch.name = 'SketchPoint'
        point = adsk.core.Point3D.create(0, 0, materialThickness*3)
        sketchPoint = sketchPoints.add(point)
        if  checkBoxAngle:
            if layerName == 'MidLayer' :
           
                sketch = sketches.addWithoutEdges(plane)
                sketch.name = 'Sketch MidLayer Part B'
                rectPointA = adsk.core.Point3D.create(0, 0, 0)
                rectPointB = adsk.core.Point3D.create(width , 0, 0)
                results = self.centerToCenterSlot(sketch, rectPointA, rectPointB, -height, -math.pi)
                
                extrude = self.addCenter(input_values, sketches, extrudes, offset, rotateOcc)
                if checkBoxRatchetValue:
                    sketchSingleShape = sketches.addWithoutEdges(plane)
                    sketchSingleShape.name = "ratchetShape"
                    sketchRatchet = self.addRatchet(input_values, sketchSingleShape, False)
                
                    profile = sketchRatchet.profiles.item(0)
                    extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                    extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
                    extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
                    extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(offset))
                    extrude2 = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput))
                
                
                    self.combine(rotateOcc, extrude.bodies.item(0), extrude2.bodies.item(0))
                
            if layerName == 'BottomLayer' or layerName == 'TopLayer' :
                sketch = sketches.addWithoutEdges(plane)
                sketch.name = 'Sketch '+ layerName +  ' Part B'   
                rectPointA = adsk.core.Point3D.create(0, 0, 0)
                rectPointB = adsk.core.Point3D.create(-width , 0, 0)
                results = self.centerToCenterSlot(sketch, rectPointA, rectPointB, -height, math.pi)
            
            if sketch.profiles.count > 0 and checkDebug is False:
                profile = sketch.profiles.item(0)
                extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
                extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
                extrudeInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(offset))
                extrude2 = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput))
        
        elif layerName == 'MidLayer':
            sketch = sketches.addWithoutEdges(plane)
            sketch.name = 'Sketch MidLayer Part B'
            rectPointA = adsk.core.Point3D.create(0, 0, 0)
            rectPointB = adsk.core.Point3D.create(width , 0, 0)
        
            self.addCenter(input_values, sketches, extrudes, offset, rotateOcc)
            
        return partBOcc, sketchPoint
       
    def drawMidLayer(self, sketches, input_values):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        checkRoundRatchetValue = input_values['checkBoxRatchet_input_id']
        amountOfIndents = input_values['amountOfIndents_input_id']
    
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
         
        sketch = sketches.addWithoutEdges(plane)
        sketch.name = 'Sketch Mid Layer Part A'
        lines = sketch.sketchCurves.sketchLines
        
        rectPointA = adsk.core.Point3D.create(0, 0, 0)
        rectPointB = adsk.core.Point3D.create(-width , 0, 0)
        results = self.centerToCenterSlot(sketch, rectPointA, rectPointB, height, math.pi) 
            
        if checkRoundRatchetValue == True and amountOfIndents > 1:
            #sketch = sketches.addWithoutEdges(plane)
           # sketch.name = 'ratchet'
            self.addRatchet(input_values, sketch, True)
        
        return sketch

    def drawBottomLayer(self, sketches, input_values):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        checkRoundBottom = input_values['checkRoundBottom_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        sketch = sketches.addWithoutEdges(plane)
        sketch.name = 'Sketch Bottom Layer Part A'
        if checkRoundBottom:
            circles = sketch.sketchCurves.sketchCircles
            circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), height/2)
        else:
            rectPointA = adsk.core.Point3D.create(0, 0, 0)
            rectPointB = adsk.core.Point3D.create(width , 0, 0)
            results = self.centerToCenterSlot(sketch, rectPointA, rectPointB, height, math.pi)
        
        return sketch   
            
    def drawTopLayer(self, sketches, input_values):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        sketch = sketches.addWithoutEdges(plane)
        sketch.name = 'Sketch Top Layer Part A'
        
        rectPointA = adsk.core.Point3D.create(0, 0, 0)
        rectPointB = adsk.core.Point3D.create(width , 0, 0)
        results = self.centerToCenterSlot(sketch, rectPointA, rectPointB, height, math.pi)
       
        return sketch
    
    def addRatchet(self, input_values, sketch, pattern):
        # Input values -->
        ratchetSizeValue = input_values['ratchetSize_input_id']
        checkBoxRatchetSizeValue = input_values['checkBoxRatchetSize_input_id']
        amountOfIndents = input_values['amountOfIndents_input_id']
        ratchetShapeValue = input_values['ratchetShape_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        offsetCircleAmount = input_values['offset_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        sketchPoints = sketch.sketchPoints
        point = adsk.core.Point3D.create(0, height/2 - offsetCircleAmount, 0)
        sketchPoint = sketchPoints.add(point)
        curveCollection = adsk.core.ObjectCollection.create()
        curveCollection.add(sketchPoint)
        offsetCircle = height/2 - offsetCircleAmount
        
        normal = sketch.xDirection.crossProduct(sketch.yDirection)
        normal.transformBy(sketch.transform)
        origin = sketch.origin
        origin.transformBy(sketch.transform)
        rotationMatrix = adsk.core.Matrix3D.create()
        step = 2 * math.pi / amountOfIndents
        pointColl = adsk.core.ObjectCollection.create()
        shapeColl = adsk.core.ObjectCollection.create()
        
        point1 = adsk.core.Point3D.create(0, offsetCircle, 0)  
          
        for i in range(1, int(amountOfIndents)):
            rotationMatrix.setToRotation(step * i, normal, origin)
            pointColl.add(sketch.copy(curveCollection, rotationMatrix))
        
        if checkBoxRatchetSizeValue:
            dist = curveCollection.item(0).geometry.distanceTo(pointColl.item(0).item(0).geometry)
            spacing = 0.2
            dist = dist - spacing
            
            if dist > (offsetCircleAmount*2 -0.7):
                dist = 0.4 # min size
            point2 = adsk.core.Point3D.create(0, offsetCircle + dist, 0)
            
        else:
            dist = ratchetSizeValue*2
            minValue = min(ratchetSizeValue, offsetCircleAmount -0.1)
            point2 = adsk.core.Point3D.create(0, offsetCircle+ minValue, 0)
            
            
        if ratchetShapeValue == "Sine":
            circles = sketch.sketchCurves.sketchCircles
            p1 = adsk.core.Point3D.create(0, 0, 0)
            p2 = adsk.core.Point3D.create(0, offsetCircle, 0)
            p3 = adsk.core.Point3D.create(0, offsetCircle +(dist /2), 0)
            
            radius = p1.distanceTo(pointColl.item(0).item(0).geometry)
            #bigCircle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius)
            shape = circles.addByCenterRadius(p2,dist/2)
            shapeColl.add(shape)
            if pattern:
                self.makePattern(sketch, shapeColl, amountOfIndents, normal, origin, rotationMatrix, step)
            
        if ratchetShapeValue == "Saw":
             lines = sketch.sketchCurves.sketchLines
             point3 = pointColl.item(pointColl.count -1).item(0).geometry
             point2 = adsk.core.Point3D.create(0, offsetCircle + dist/2, 0)
             line1  = lines.addByTwoPoints(point1, point2)
             line2 = lines.addByTwoPoints(point2, point3)
             line3 = lines.addByTwoPoints(point1, point3)
             shapeColl.add(line1)
             shapeColl.add(line2)
             shapeColl.add(line3)
             if pattern:
                self.makePattern(sketch, shapeColl, amountOfIndents, normal, origin, rotationMatrix, step)

             
        if ratchetShapeValue == "Saw Inverted":
             lines = sketch.sketchCurves.sketchLines
             point3 = pointColl.item(0).item(0).geometry
             point2 = adsk.core.Point3D.create(0, offsetCircle + dist/2, 0)
             
             line1  = lines.addByTwoPoints(point1, point2)
             line2 = lines.addByTwoPoints(point2, point3)
             line3 = lines.addByTwoPoints(point1, point3)

             shapeColl.add(line1)
             shapeColl.add(line2)
             shapeColl.add(line3)
             
             if pattern:
                self.makePattern(sketch, shapeColl, amountOfIndents, normal, origin, rotationMatrix, step)

             
        if ratchetShapeValue == "Square":
            lines = sketch.sketchCurves.sketchLines
            p1 = adsk.core.Point3D.create(0, offsetCircle, 0)
            p2 = adsk.core.Point3D.create(dist /2, offsetCircle +(dist /2), 0)
            rect = lines.addCenterPointRectangle(p1, p2)
            for lines in rect:
                shapeColl.add(lines)
            if pattern:
                self.makePattern(sketch, shapeColl, amountOfIndents, normal, origin, rotationMatrix, step)
            
        if ratchetShapeValue == "Triangle":
            lines = sketch.sketchCurves.sketchLines
            circles = sketch.sketchCurves.sketchCircles
            p1 = adsk.core.Point3D.create(0, 0, 0)
            p2 = adsk.core.Point3D.create(0, offsetCircle, 0)
            p3 = adsk.core.Point3D.create(0, offsetCircle +(dist /2), 0)
            
            radius = p1.distanceTo(pointColl.item(0).item(0).geometry)
            bigCircle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius)
            smallCircle= circles.addByCenterRadius(p2,dist/2)
            smallCircleCollection = adsk.core.ObjectCollection.create()
            smallCircleCollection.add(smallCircle)
            (returnValue, intersectingCurves, intersectionPoints) = bigCircle.intersections(smallCircleCollection)
            
            line1  = lines.addByTwoPoints(intersectionPoints.item(0), p3)
            line2 = lines.addByTwoPoints(intersectionPoints.item(1), p3)
            line3 = lines.addByTwoPoints(intersectionPoints.item(1), intersectionPoints.item(0))
            
            shapeColl.add(line1)
            shapeColl.add(line2)
            shapeColl.add(line3)
            
            bigCircle.deleteMe()
            smallCircle.deleteMe()

            if pattern:
                self.makePattern(sketch, shapeColl, amountOfIndents, normal, origin, rotationMatrix, step)
       
        return sketch
  
    def makePattern(self, sketch, shapeColl, amount, normal, origin, rotationMatrix, step):
        if shapeColl.count > 0:
            for j in range(1, int(amount)):
                rotationMatrix.setToRotation(step * j, normal, origin)
                sketch.copy(shapeColl, rotationMatrix)
            
    def addCenter(self, input_values, sketches,  extrudes, offset, rotateOcc):
        
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        offsetCircleAmount = input_values['offset_input_id']
        checkRoundRatchetValue = input_values['checkBoxRatchet_input_id']
        springCoils = input_values['springCoils_input_id']
       # widthSpring = input_values['widthSpring_input_id']
        springSpace = input_values['springSpace_input_id']
        springCoilThickness = input_values['springCoilThickness_input_id']
        materialThickness = input_values['materialThickness_input_id']
        checkDebug = input_values['checkDebug_input_id']

        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        extrude = None
        springSketch = None
        sketch = sketches.addWithoutEdges(plane)
        circles = sketch.sketchCurves.sketchCircles
        circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), height/2 - offsetCircleAmount)
        if checkDebug is False:
            extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))    
            try:    
                extrudeInputCut = extrudes.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)  
                extrudeInputCut.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)   
                extrudeInputCut.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(offset))    
                adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInputCut)) 
            except:
                if checkDebug:
                    pass
                    #print("nothing to extrude")
                else:
                    pass      
            if checkRoundRatchetValue == False:
                extrudeInputNewBody = extrudes.createInput(sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)  
                extrudeInputNewBody.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)   
                extrudeInputNewBody.startExtent = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(offset))    
                extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInputNewBody)) 
        
        if checkRoundRatchetValue:
            widthSpring = height/2 - offsetCircleAmount
            springHeight = springCoilThickness * (4 + (springCoils*2))

            offsetSpring = ((circle.radius*2) - springHeight) /2
            offsetSpring = offsetSpring- 1.35
            if springHeight > (circle.radius*2):
               # print("te groot")
                spring = None
            else:
                spring = Spring(input_values, 0, offsetSpring, 0, offset, rotateOcc)
                extrude = spring.createSpring()

        return extrude

    def addJoint(self, sketchPointA,sketchPointB, angle):
        ao = AppObjects()

        #Joint
        geo0 = adsk.fusion.JointGeometry.createByPoint(sketchPointB)
        geo1 = adsk.fusion.JointGeometry.createByPoint(sketchPointA)

        # Create joint input
        joints = ao.root_comp.joints
        jointInput = joints.createInput(geo0, geo1)
        # angleValue = adsk.core.ValueInput.createByString(math.radians(angle))
        angleValue = adsk.core.ValueInput.createByReal(angle)
        jointInput.angle = angleValue
        jointInput.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
        # Create the joint
        joint = joints.add(jointInput)
        revoluteMotion = joint.jointMotion
        if angle > 0:
            limits = revoluteMotion.rotationLimits
            limits.isMinimumValueEnabled = True
            limits.minimumValue = -angle
            limits.isMaximumValueEnabled = True
            limits.maximumValue = 0
                 
    def centerToCenterSlot(self, sketch, point1, point2, width, angle):
            sk = adsk.fusion.Sketch.cast(sketch)
        
            # Draw the centerline of the slot.
            lines = sk.sketchCurves.sketchLines
            centerLine = lines.addByTwoPoints(point1, point2)
            centerLine.isConstruction = True
            
            slotAngle = self.bearing(point1, point2) 
            offsetAngle = slotAngle + math.pi/2    
            offsetVec = adsk.core.Vector3D.create(math.cos(offsetAngle), math.sin(offsetAngle), 0)
            offsetVec.scaleBy(width/2)
            
            newPnt1 = adsk.core.Point3D.cast(point1.copy())
            newPnt1.translateBy(offsetVec)
            newPnt2 = adsk.core.Point3D.cast(point2.copy())
            newPnt2.translateBy(offsetVec)
            line1 = lines.addByTwoPoints(newPnt1, newPnt2)
        
            offsetVec.scaleBy(-1)    
            newPnt1 = adsk.core.Point3D.cast(point1.copy())
            newPnt1.translateBy(offsetVec)
            newPnt2 = adsk.core.Point3D.cast(point2.copy())
            newPnt2.translateBy(offsetVec)
            line2 = lines.addByTwoPoints(newPnt1, newPnt2)
            
            lines.addByTwoPoints(line2.endSketchPoint, line1.endSketchPoint)
            
            arcs = sketch.sketchCurves.sketchArcs
            arc1 = arcs.addByCenterStartSweep(centerLine.startSketchPoint, line1.startSketchPoint, angle)            
            
            return [centerLine, line1, line2, arc1]

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

class Spring():

    def __init__(self,input_values, xOffset,yOffset,rotate,extrudeOffset, occ):
       
        self._height = input_values['height_input_id']
        self._offsetCircleAmount = input_values['offset_input_id']
        self._checkRoundRatchetValue = input_values['checkBoxRatchet_input_id']
        self._springCoils = input_values['springCoils_input_id']
       
        self._springWidth = input_values['widthSpring_input_id']
        self._spaceBetween = input_values['springSpace_input_id']
        self._springCoilThickness = input_values['springCoilThickness_input_id']
        self._materialThickness = input_values['materialThickness_input_id']
        self._checkDebug = input_values['checkDebug_input_id']
        self._button = input_values['button_input_id']
        all_selections = input_values.get('selection_input_id', None)
        self._plane = all_selections[0]

        self._x = -self._springWidth/2 + (self._springCoilThickness*1.5) +xOffset
        self._y = yOffset - (self._springCoilThickness *2)
        self._rotate = rotate
        self._occ = occ
        self._extrudeOffset = extrudeOffset
        moveX = self._springWidth/2 - ((self._springCoilThickness*3)/2) + self._x
           
    def createSpring(self):
        ao = AppObjects()
        
        #print(self._occ)
        springOcc = apper.create_component(self._occ.component, 'Spring')
        mainBodyComponent = springOcc.component
        sketches = mainBodyComponent.sketches
        sketch = sketches.addWithoutEdges(self._plane)
        
        rectAroundSpringOffset = 0.01
        points = []
        points2 = []
        points3 = []
        points4 = []
        arcs = sketch.sketchCurves.sketchArcs
        spaceDivider = self._springCoilThickness * 3
        
        sketch = sketches.addWithoutEdges(self._plane)
        circles = sketch.sketchCurves.sketchCircles
        circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), self._height/2 - self._offsetCircleAmount)
        
        for i in range(self._springCoils * 4):
            points.append(adsk.core.Point3D.create(self._x + 0, self._y+ i * self._springCoilThickness /2, 0))
            points2.append(adsk.core.Point3D.create(self._x+ self._springWidth /2 -(self._spaceBetween /2) -spaceDivider, self._y+ i * self._springCoilThickness /2, 0))
            
        for i in range(self._springCoils * 4):
            points3.append(adsk.core.Point3D.create(self._x+ self._springWidth/2 +(self._spaceBetween /2), self._y+ i * self._springCoilThickness /2, 0))
            points4.append(adsk.core.Point3D.create(self._x+ self._springWidth -(self._springCoilThickness*3) , self._y+ i * self._springCoilThickness /2, 0))
        
        leftArcsArray = self.pointsToSpring(sketch, points,points2)
        rightArcArray = self.pointsToSpring(sketch, points4,points3)
        lines = sketch.sketchCurves.sketchLines
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
        
        pointsRight = sideWallRighTop.asInfiniteLine().intersectWithCurve(circle.geometry)
        lines.addByTwoPoints(pointsRight.item(pointsRight.count -1), sidwallRightEndPoint)
        
        guideLeftEndPoint = adsk.core.Point3D.cast(sidwallLeftEndPoint.copy())
        guideLeftEndPoint.translateBy(offsetVec)
        
        # Top line 
        #sideWallLeftTop = lines.addByTwoPoints(sidwallLeftEndPoint, guideLeftEndPoint)
        sideWallLeftTop = adsk.core.Line3D.create(sidwallLeftEndPoint, guideLeftEndPoint)
        
       # topLine = lines.addByTwoPoints(guideRightEndPoint, guideLeftEndPoint)
       
        points = sideWallLeftTop.asInfiniteLine().intersectWithCurve(circle.geometry)
        lines.addByTwoPoints(points.item(0), sidwallLeftEndPoint)
   
        #bottom
        offsetVec = adsk.core.Vector3D.create(0,-self._springCoilThickness*2 , 0)
       
        bottomLeftStartPoint = sidwallLeftStartPoint
        bottomLeftEndPoint = adsk.core.Point3D.cast(bottomLeftStartPoint.copy())
        bottomLeftEndPoint.translateBy(offsetVec)
        
        sidewallLeftBottom = adsk.core.Line3D.create(bottomLeftStartPoint, bottomLeftEndPoint)
        pointsInsideA = sidewallLeftBottom.asInfiniteLine().intersectWithCurve(circle.geometry)
        lines.addByTwoPoints(pointsInsideA.item(0), bottomLeftStartPoint)
        
        bottomRightStartPoint = sidwallRightStartPoint
        bottomRightEndPoint = adsk.core.Point3D.cast(bottomRightStartPoint.copy())
        bottomRightEndPoint.translateBy(offsetVec)
        
        sidewallRightBottom =  adsk.core.Line3D.create(bottomRightStartPoint, bottomRightEndPoint)
       
        pointsInsideB = sidewallRightBottom.asInfiniteLine().intersectWithCurve(circle.geometry)
        lines.addByTwoPoints(pointsInsideB.item(pointsInsideB.count-1), bottomRightStartPoint)
        
        sketchGlue = sketches.addWithoutEdges(self._plane)
        sketchGlue.name = "sketchGlue"
        glueLines = sketchGlue.sketchCurves.sketchLines
        glueLines.addThreePointRectangle(sidwallRightStartPoint, sidwallLeftStartPoint, adsk.core.Point3D.create(0, self._height/2 - (self._offsetCircleAmount/2), 0))
        
        extrudes = mainBodyComponent.features.extrudeFeatures
        extrudeInput = extrudes.createInput(sketchGlue.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(self._extrudeOffset))
        extrudeInput.startExtent = start_from
        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
        glueBody = extrude.bodies.item(0)
        glueBody.name = "Glue"
        glueBody.attributes.add('KeepOut', 'Spring', str(self._materialThickness))
        
        
        if self._button:
            sketchButton = sketches.addWithoutEdges(self._plane)
            sketchButton.name = "sketchButton"
            glueLines = sketchButton.sketchCurves.sketchLines
            glueLines.addThreePointRectangle(sidwallRightStartPoint, sidwallLeftStartPoint, adsk.core.Point3D.create(0, self._height/2, 0))
            
            extrudes = mainBodyComponent.features.extrudeFeatures
            extrudeInput = extrudes.createInput(sketchButton.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation)
            extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
            extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(0))
            extrudeInput.startExtent = start_from
            extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
            
            sketchButtonbody = sketches.add(self._plane)
            sketchButtonbody.name = "sketchButton"
            circles = sketchButtonbody.sketchCurves.sketchCircles
            circle = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), self._height/2)
            glueLines = sketchButtonbody.sketchCurves.sketchLines
            glueLines.addThreePointRectangle(adsk.core.Point3D.create(sidwallRightStartPoint.x , sidwallRightStartPoint.y +.2, sidwallRightStartPoint.z) , adsk.core.Point3D.create(sidwallLeftStartPoint.x, sidwallLeftStartPoint.y + .2, sidwallLeftStartPoint.z) , adsk.core.Point3D.create(0, self._height/2, 0))
        
            extrudes = mainBodyComponent.features.extrudeFeatures
            sketchEntities = adsk.core.ObjectCollection.create()
            sketchEntities.add(sketchButtonbody.profiles.item(1))
            sketchEntities.add(sketchButtonbody.profiles.item(3))
            extrudeInput = extrudes.createInput(sketchEntities, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
            extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(0))
            extrudeInput.startExtent = start_from
            extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
            
            glueBody = extrude.bodies.item(0)
            glueBody.name = "button"
 
        all = adsk.core.ObjectCollection.create()
        for c in sketch.sketchCurves:
            all.add(c)
        for p in sketch.sketchPoints:
            all.add(p)
            
        normal = sketch.xDirection.crossProduct(sketch.yDirection)
        normal.transformBy(sketch.transform)
        origin = sketch.origin
        origin.transformBy(sketch.transform)
        mat = adsk.core.Matrix3D.create()
        mat.setToRotation(math.pi , normal, origin)
        sketch.move(all, mat)
        
        #print(guideRightEndPoint.distanceTo(bottomRightEndPoint))
        
 
        extrudes = mainBodyComponent.features.extrudeFeatures
        extrudeInput = extrudes.createInput(sketch.profiles.item(sketch.profiles.count -2), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        
        start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(self._extrudeOffset))

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
        
        