import adsk.core
import adsk.fusion
import adsk.cam
import math

# Import the entire apper package
import apper

# Alternatively you can import a specific function or class
from apper import AppObjects


class HingeCommand(apper.Fusion360CommandBase):

    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        all_selections = input_values.get('selection_input_id', None)

        if len(all_selections) > 0:

            self.drawLayers(input_values)

           # #text_box_input = inputs.itemById('text_box_input_id')
           # text_box_input.text = state
            
            args.isValidResult = True
            
    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        
        tab2 = inputs.itemById('tab_2')
        checkLockValue = input_values['springLockCheckBox_input_id']

        unlock = inputs.itemById('springUnlockCheckBox_input_id')

        
        if checkLockValue is True:
             tab2.isEnabled = True
             tab2.isVisible = True
             unlock.isVisible = True
             
        else:
            tab2.isEnabled = False
            tab2.isVisible = False
            unlock.isVisible = False
            
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        all_selections = input_values.get('selection_input_id', None)

        if len(all_selections) > 0:

            self.drawLayers(input_values)

            #text_box_input = inputs.itemById('text_box_input_id')
            #text_box_input.text = state
            
            #args.isValidResult = True
           
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        ao = AppObjects()
        tabCmdInput1 = inputs.addTabCommandInput('tab_1', 'Fold')
        tabCmdInput2 = inputs.addTabCommandInput('tab_2', 'Spring Settings')

        tab1ChildInputs = tabCmdInput1.children
        tab2ChildInputs = tabCmdInput2.children
        # Create a default value using a string
        default_valueX = adsk.core.ValueInput.createByString('50 mm')
        default_valueY = adsk.core.ValueInput.createByString('120 mm')
        default_materialThickness = adsk.core.ValueInput.createByString('4 mm')
        default_hingeLength = adsk.core.ValueInput.createByString('25 mm')
        default_penLength = adsk.core.ValueInput.createByString('5 mm')
        default_hingeOffset = adsk.core.ValueInput.createByString('10 mm')
        default_springOffset = adsk.core.ValueInput.createByString('4 mm')
        default_springLength = adsk.core.ValueInput.createByString('15 mm')
        default_springCoilThickness = adsk.core.ValueInput.createByString('0.9 mm')
        default_springSpace = adsk.core.ValueInput.createByString('0.5 mm')
        default_zero = adsk.core.ValueInput.createByString('0 mm')
        default_moveX = adsk.core.ValueInput.createByString('25 mm')
        default_moveY = adsk.core.ValueInput.createByString('-25 mm')
        # Get teh user's current units
        default_units = ao.units_manager.defaultLengthUnits

        tab1ChildInputs.addSelectionInput('selection_input_id', 'Select a plane', 'Select Something')
           
        # Create a value input.  This will respect units and user defined equation input.
        tab1ChildInputs.addValueInput('width_input_id', 'Width', default_units, default_valueX)
        tab1ChildInputs.addValueInput('height_input_id', 'Height', default_units, default_valueY)
        tab1ChildInputs.addValueInput('materialThickness_input_id', 'Thickness',default_units , default_materialThickness)
        tab1ChildInputs.addIntegerSpinnerCommandInput('amountOfHinges_input_id', 'Amount of Hinges', 1, 10, 1, 2)
        tab1ChildInputs.addValueInput('hingeOffset_input_id', 'Hinge offset from sides', default_units, default_hingeOffset)
        tab1ChildInputs.addValueInput('hingeLength_input_id', 'Hinge length', default_units, default_hingeLength)
        tab1ChildInputs.addValueInput('hingePenLength_input_id', 'Hinge pen length', default_units, default_penLength)


        tab1ChildInputs.addBoolValueInput('springLockCheckBox_input_id', 'Add Lock', True, '', True)
        unlock = tab1ChildInputs.addBoolValueInput('springUnlockCheckBox_input_id', 'Add Unlock button', True)

       # tab1ChildInputs.addTextBoxCommandInput('text_box_input_id', 'State: ', '', 1, True)
        
        # x = tab1ChildInputs.addValueInput('moveX_input_id', 'Move X', default_units, default_moveX)
        # y = tab1ChildInputs.addValueInput('moveY_input_id', 'Move Y', default_units, default_moveY)
        # a = angle = tab1ChildInputs.addValueInput('angle_input_id', 'Angle', 'deg', adsk.core.ValueInput.createByString('90.0 deg'))
        # x.visible = False
        # y.visible = False
        # a.visible = False
        # Tab 2
        tab2ChildInputs.addValueInput('springCoilThickness_input_id', 'Spring Coil Thickness', default_units, default_springCoilThickness)
        tab2ChildInputs.addValueInput('springOffset_input_id', 'Spring Offset', default_units, default_springOffset)
        tab2ChildInputs.addIntegerSpinnerCommandInput('springCoils_input_id', 'Spring Coils', 1, 60, 2, 5)
        tab2ChildInputs.addValueInput('springSpace_input_id', 'Spring space between', default_units, default_springSpace)
        inputs.addTextBoxCommandInput('text_box_input_id', 'Info: ', '', 1, True)

    # Draw all layers
    def drawLayers(self, input_values):  
        ao = AppObjects()
        
        hingeOcc = apper.create_component(ao.root_comp, 'Hinge')
        hingeComponent = hingeOcc.component
        
        extrudeBottom, comp = self.drawBottomLayer(input_values, hingeComponent)
        
        self.drawMidLayer(input_values, hingeComponent)
        self.drawTopLayer(input_values, hingeComponent)
        state, extrudeBodies = self.drawhinges(input_values, hingeComponent)
        if extrudeBodies.count >0:
            try:
                combine_features = comp.features.combineFeatures
                combine_input = combine_features.createInput(extrudeBottom.bodies.item(0), extrudeBodies)
                combine_input.isKeepToolBodies = False
                combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation 
                combine_features.add(combine_input) 
            except:
                print('failed combine')    
     
    def drawhinges(self, input_values, hingeComponent):
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        hingeOffset = input_values['hingeOffset_input_id']
        height = input_values['height_input_id']
        extrudeBodies = adsk.core.ObjectCollection.create()
        if amountOfHinges == 1:
            xPos = height/2 - ((hingeLength + (hingePenLength*2))/2)
            extrude = self.drawHinge(input_values, hingeComponent, xPos, 'Top')
            for body in extrude.bodies:
                extrudeBodies.add(body)
            state = 'succes'
        else:
            offsetX = self.calculateOffset(input_values, amountOfHinges)
            xPos = hingeOffset -hingePenLength
            
            if offsetX < (hingePenLength *2):
                amountOfHinges = 2
                offsetX = self.calculateOffset(input_values, amountOfHinges)
                state = 'error'
            else:
                
                for hinge in range(0, amountOfHinges):
                    if hinge == 0:
                        self.drawHinge(input_values, hingeComponent, xPos, 'Top')
                        xPos = xPos+ hingeLength +offsetX 
                    elif hinge == amountOfHinges-1:
                        extrude = self.drawHinge(input_values, hingeComponent, xPos, 'Bottom')
                        for body in extrude.bodies:
                            extrudeBodies.add(body)
                    else:
                        self.drawHinge(input_values, hingeComponent, xPos, 'Middle')

                        xPos = xPos+ hingeLength +offsetX 
                state = 'succes'
       
        return state, extrudeBodies
        
    def calculateOffset(self, input_values, amountOfHinges):
        hingeOffset = input_values['hingeOffset_input_id']
        hingeLength = input_values['hingeLength_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        
        r1 = height - (hingeOffset*2)
        r2 = r1 - (hingeLength * amountOfHinges)
        offsetX = r2/(amountOfHinges-1) 
        
        return offsetX
    
    # Bottom Layer          
    def drawBottomLayer(self, input_values, comp):
      
        bottomOcc = apper.create_component(comp, 'Bottom Layer')
        bottomComponent = bottomOcc.component
        
        self.drawBottomRight(input_values, bottomComponent)
        extrude = self.drawBottomLeft(input_values, bottomComponent)
    
        return extrude, bottomComponent
        
    def drawBottomRight(self, input_values, comp):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingeOffset = input_values['hingeOffset_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        sketches = comp.sketches
        sketch = sketches.addWithoutEdges(plane)
        lines = sketch.sketchCurves.sketchLines
        
        start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(0))   
        rectPoint = adsk.core.Point3D.create(height, width, 0)
        lines.addTwoPointRectangle(adsk.core.Point3D.create(0,0,0), rectPoint)
        extrude = self.extrudeProfile(comp, sketch.profiles.item(0), materialThickness, start_from)
        return extrude
                  
    def drawBottomLeft(self, input_values, comp):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        sketches = comp.sketches
        sketch = sketches.addWithoutEdges(plane)
        lines = sketch.sketchCurves.sketchLines
        start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(0))   
        rectPoint = adsk.core.Point3D.create(height, -(width + materialThickness), 0)
        lines.addTwoPointRectangle(adsk.core.Point3D.create(0,- materialThickness,0), rectPoint)
        extrude = self.extrudeProfile(comp, sketch.profiles.item(0), materialThickness, start_from)
        
        return extrude

    # Mid Layer
    def drawMidLayer(self, input_values, comp):
        
        midOcc = apper.create_component(comp, 'Middle Layer')
        midComponent = midOcc.component
       
        self.drawMidRight(input_values, midComponent)
        self.drawMidLeft(input_values, midComponent)
        
    def drawMidRight(self, input_values, comp):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingeOffset = input_values['hingeOffset_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values

        diagonal = math.sqrt(2*materialThickness*materialThickness)
        offsetThickness = diagonal - materialThickness 
        hingeLengthSmall = hingeLength - (hingePenLength*2)
        
        sketches = comp.sketches
        sketch = sketches.addWithoutEdges(plane)
        lines = sketch.sketchCurves.sketchLines
        start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))   
        rectPoint = adsk.core.Point3D.create(height, width, 0)
        lines.addTwoPointRectangle(adsk.core.Point3D.create(0,0,0), rectPoint)
        self.extrudeProfile(comp, sketch.profiles.item(0), materialThickness, start_from)   
    
    def drawMidLeft(self, input_values, comp):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        hingeOffset = input_values['hingeOffset_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
    
        sketches = comp.sketches
        sketch = sketches.addWithoutEdges(plane)
        lines = sketch.sketchCurves.sketchLines
        start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))   
        rectPoint = adsk.core.Point3D.create(height, -(width + materialThickness), 0)
        lines.addTwoPointRectangle(adsk.core.Point3D.create(0,- materialThickness,0), rectPoint)
        
        self.extrudeProfile(comp, sketch.profiles.item(0), materialThickness, start_from)
        
    # Top Layer    
    def drawTopLayer(self, input_values,comp ):
        topOcc = apper.create_component(comp, 'Top Layer')
        topComponent = topOcc.component

        self.drawTopRight(input_values, topComponent)
        self.drawTopLeft(input_values, topComponent)       
    
    def drawTopRight(self, input_values, comp):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values

        sketches = comp.sketches
        sketch = sketches.addWithoutEdges(plane)
        lines = sketch.sketchCurves.sketchLines
        start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness*2))   
        rectPoint = adsk.core.Point3D.create(height, width, 0)
        lines.addTwoPointRectangle(adsk.core.Point3D.create(0,0,0), rectPoint)
        self.extrudeProfile(comp, sketch.profiles.item(0), materialThickness, start_from)
    
    def drawTopLeft(self, input_values, comp):
        # Input values -->
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values
        
        sketches = comp.sketches
        sketch = sketches.addWithoutEdges(plane)
        lines = sketch.sketchCurves.sketchLines
        start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness*2))   
        rectPoint = adsk.core.Point3D.create(height, -(width + materialThickness), 0)
        lines.addTwoPointRectangle(adsk.core.Point3D.create(0,- materialThickness,0), rectPoint)
        
        self.extrudeProfile(comp, sketch.profiles.item(0), materialThickness, start_from)
        
    
    def drawHinge(self, input_values, comp, xPos, position):
        
        self.cutTopBodyHinge(input_values,comp, xPos)
        self.cutMidBodyHinge(input_values,comp, xPos)
        self.drawMidBodyHinge(input_values,comp, xPos, position)
        self.cutBottomBodyHinge(input_values,comp, xPos)
        extrude = self.drawBottomBodyHinge(input_values,comp, xPos)
        return extrude
   
    def cutMidBodyHinge(self, input_values, comp, xPos):
        # Input values -->
        materialThickness = input_values['materialThickness_input_id']
        hingeX = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        lockCheckBox = input_values['springLockCheckBox_input_id']
        hingeOffset = input_values['hingeOffset_input_id']
        width = input_values['width_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values    
        
        startPointY = materialThickness
        sketches = comp.sketches
        xOffset =  hingePenLength + xPos
        rectPoint = adsk.core.Point3D.create(hingeX +xOffset, (materialThickness*3) - startPointY,0)
        diagonal = math.sqrt(2*materialThickness*materialThickness)
        
        sketchMid = sketches.addWithoutEdges(plane)
        linesMid = sketchMid.sketchCurves.sketchLines
        mainBodyMid = linesMid.addTwoPointRectangle(adsk.core.Point3D.create(xOffset,-startPointY,0), rectPoint)
        bottomPinMidLayer = linesMid.addTwoPointRectangle(rectPoint, adsk.core.Point3D.create(hingeX+hingePenLength+xOffset, rectPoint.y -diagonal,0))
        topPinMidLayer = linesMid.addTwoPointRectangle(adsk.core.Point3D.create(xOffset, rectPoint.y ,0), adsk.core.Point3D.create(xOffset-hingePenLength , rectPoint.y -diagonal,0))
        
        if lockCheckBox:
            startPointA = adsk.core.Point3D.create(xOffset,-startPointY,0)
            endPointA = adsk.core.Point3D.create(hingeX +xOffset,-startPointY -(width -hingeOffset),0)
            linesMid.addTwoPointRectangle(startPointA, endPointA)
            startPointB = adsk.core.Point3D.create(hingeX +xOffset +hingePenLength,-startPointY -(width -hingeOffset),0)
            endPointB = adsk.core.Point3D.create(xOffset -hingePenLength,-startPointY -(width -hingeOffset)+(materialThickness*3),0) # width internal slider
            linesMid.addTwoPointRectangle(startPointB, endPointB)
            
        profilesMid = adsk.core.ObjectCollection.create()
        for profile in sketchMid.profiles:
            profilesMid.add(profile)
            
        start_fromMid = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))  
        self.cutProfile(comp, profilesMid, materialThickness, start_fromMid)
    
    def drawMidBodyHinge(self, input_values, comp, xPos, position):
        # Input values -->
        materialThickness = input_values['materialThickness_input_id']
        hingeX = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        lockCheckBox = input_values['springLockCheckBox_input_id']
        hingeOffset = input_values['hingeOffset_input_id']
        width = input_values['width_input_id']
        # moveY = input_values['moveY_input_id']
        # moveX = input_values['moveX_input_id']
        
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values    
        
        startPointY = materialThickness
        sketches = comp.sketches
        xOffset =  hingePenLength + xPos
        rectPoint = adsk.core.Point3D.create(hingeX +xOffset, (materialThickness*3) - startPointY,0)
        diagonal = math.sqrt(2*materialThickness*materialThickness)
        
        sketchMid = sketches.addWithoutEdges(plane)
        linesMid = sketchMid.sketchCurves.sketchLines
        mainBodyMid = linesMid.addTwoPointRectangle(adsk.core.Point3D.create(xOffset,-startPointY,0), rectPoint)
        bottomPinMidLayer = linesMid.addTwoPointRectangle(rectPoint, adsk.core.Point3D.create(hingeX+hingePenLength+xOffset, rectPoint.y -materialThickness,0))
        topPinMidLayer = linesMid.addTwoPointRectangle(adsk.core.Point3D.create(xOffset, rectPoint.y ,0), adsk.core.Point3D.create(xOffset-hingePenLength , rectPoint.y -materialThickness,0))
        
        if lockCheckBox:
            startPointA = adsk.core.Point3D.create(xOffset,-startPointY,0)
            endPointA = adsk.core.Point3D.create(hingeX +xOffset,-startPointY -(width -hingeOffset) + materialThickness,0)
            linesMid.addTwoPointRectangle(startPointA, endPointA)
            
            startPointB = adsk.core.Point3D.create(hingeX +xOffset +hingePenLength,-startPointY -(width -hingeOffset)+materialThickness,0)
            endPointB = adsk.core.Point3D.create(xOffset -hingePenLength,-startPointY -(width -hingeOffset)+(materialThickness*3),0) # width internal slider
            linesMid.addTwoPointRectangle(startPointB, endPointB)
        
        profilesMid = adsk.core.ObjectCollection.create()
        for profile in sketchMid.profiles:
            profilesMid.add(profile)
            
        start_fromMid = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))  
        extrudeBody = self.extrudeProfile(comp, profilesMid, materialThickness, start_fromMid)
        
        if lockCheckBox:
            if position == 'Top' or position == 'Bottom':
                spring = Spring(input_values, xPos +hingePenLength,materialThickness*2, comp, position)
                extrudeRatchet = spring.createSpring()
    
            #self.combine(comp, extrudeBody.bodies.item(0), extrudeRatchet.bodies.item(0))
        
    def combine(self, comp, tool, target):
        combine_features = comp.features.combineFeatures
        combine_tools = adsk.core.ObjectCollection.create()
        combine_tools.add(tool)

        combine_input = combine_features.createInput(target, combine_tools)
        combine_input.isKeepToolBodies = False
        combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation 
        combine_features.add(combine_input)     
        
    def cutTopBodyHinge(self, input_values, comp, xPos):
        # Input values -->
        materialThickness = input_values['materialThickness_input_id']
        hingeX = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        lockCheckBox = input_values['springLockCheckBox_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values    
        startPointY = materialThickness
        sketches = comp.sketches
        xOffset =  hingePenLength + xPos
        rectPoint = adsk.core.Point3D.create(hingeX +xOffset, (materialThickness*3) - startPointY,0)
        diagonal = math.sqrt(2*materialThickness*materialThickness)
        profilesTop = adsk.core.ObjectCollection.create()
        
        sketchTop = sketches.addWithoutEdges(plane)
        linesTop = sketchTop.sketchCurves.sketchLines
        
        mainBodyTop = linesTop.addTwoPointRectangle(adsk.core.Point3D.create(xOffset,-startPointY,0), rectPoint)

        for profile in sketchTop.profiles:
            profilesTop.add(profile)
            
        start_fromTop = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness*2)) 
        self.cutProfile(comp, profilesTop, materialThickness, start_fromTop)
            
    def cutBottomBodyHinge(self, input_values, comp, xPos):
        # Input values -->
        materialThickness = input_values['materialThickness_input_id']
        hingeX = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        lockCheckBox = input_values['springLockCheckBox_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values    
        startPointY = materialThickness
        sketches = comp.sketches
        xOffset =  hingePenLength + xPos
        rectPoint = adsk.core.Point3D.create(hingeX +xOffset, (materialThickness*3) - startPointY,0)
        diagonal = math.sqrt(2*materialThickness*materialThickness)
        
        sketches = comp.sketches
        sketchBottom = sketches.addWithoutEdges(plane)
        linesBottom = sketchBottom.sketchCurves.sketchLines
        
        mainBodyBottom = linesBottom.addTwoPointRectangle(adsk.core.Point3D.create(xOffset,-startPointY,0), rectPoint)
        bottomPinBottomLayer = linesBottom.addTwoPointRectangle(rectPoint, adsk.core.Point3D.create(hingeX+hingePenLength+xOffset, rectPoint.y -(materialThickness *0.8),0))
        topPinBottomLayer = linesBottom.addTwoPointRectangle(adsk.core.Point3D.create(xOffset, rectPoint.y ,0), adsk.core.Point3D.create(xOffset-hingePenLength , rectPoint.y -(materialThickness *0.8),0))

        profilesBottom = adsk.core.ObjectCollection.create()
        for profile in sketchBottom.profiles:
            profilesBottom.add(profile)
            
        start_fromBottom = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(0))      
        self.cutProfile(comp, profilesBottom, materialThickness, start_fromBottom)
        
    def drawBottomBodyHinge(self, input_values, comp, xPos):
        # Input values -->
        materialThickness = input_values['materialThickness_input_id']
        hingeX = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        lockCheckBox = input_values['springLockCheckBox_input_id']
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        all_selections = input_values.get('selection_input_id', None)
        plane = all_selections[0]
        # <-- Input values    
        startPointY = materialThickness
        sketches = comp.sketches
        xOffset =  hingePenLength + xPos
        rectPoint = adsk.core.Point3D.create(hingeX +xOffset, (materialThickness*3) - startPointY,0)
        diagonal = math.sqrt(2*materialThickness*materialThickness)
        
        sketches = comp.sketches
        sketchBottom = sketches.addWithoutEdges(plane)
        linesBottom = sketchBottom.sketchCurves.sketchLines
        
        mainBodyBottom = linesBottom.addTwoPointRectangle(adsk.core.Point3D.create(xOffset,-startPointY,0), rectPoint)

        profilesBottom = adsk.core.ObjectCollection.create()
        for profile in sketchBottom.profiles:
            profilesBottom.add(profile)
            
        start_fromBottom = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(0))      
        extrude = self.extrudeProfile(comp, profilesBottom, materialThickness, start_fromBottom)
        
        return extrude
    
    
    def extrudeProfile(self, comp, profiles, materialThickness, start_from):
        
        extrudes = comp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = start_from 

        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
        
        return extrude
                
    def cutProfile(self, comp, profiles, materialThickness, start_from):
        
        extrudes = comp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = start_from 

        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
        
            
class Spring():

    def __init__(self,input_values, xOffset,yOffset, comp, position):
       
        self._springCoils = input_values['springCoils_input_id']
        self._hingeHeight = input_values['hingeLength_input_id']
        self._springWidth = input_values['hingeLength_input_id']
        self._spaceBetween = input_values['springSpace_input_id']
        self._springCoilThickness = input_values['springCoilThickness_input_id']
        self._materialThickness = input_values['materialThickness_input_id']
        all_selections = input_values.get('selection_input_id', None)
        self._plane = all_selections[0]
        #self._slotWidthOffset = input_values['hingeOffset_input_id']
        self._width = input_values['width_input_id']
        self._height = input_values['height_input_id']
        self._offsetSidesSpring = input_values['springOffset_input_id']
        #self._angle = input_values['angle_input_id']
        self._xOffset = xOffset 
        self._yOffset = yOffset 
        self._springWidth = self._springWidth - (self._offsetSidesSpring *2)
        #self._x = 0
        self._x = self._springCoilThickness*1.5 
        self._y = self._springCoilThickness*1.5 
        self._position = position
        #self._y = -self._springWidth/2 + (self._springCoilThickness*1.5) +xOffset 
        #self._x = -self._springWidth -( self._materialThickness*2)
        #self._y = yOffset - (self._springCoilThickness *2)+(self._slotHeight /2)
        #print(self._slotHeight)

        self._comp = comp
                 
    def createSpring(self):
        ao = AppObjects()
        mainBodyComponent = self._comp
        sketches = mainBodyComponent.sketches
        sketch = sketches.addWithoutEdges(self._plane)
        sketchRatchet = sketches.addWithoutEdges(self._plane)
        linesRatchet = sketchRatchet.sketchCurves.sketchLines
        
        offsetX = (self._hingeHeight ) /4 

        
        rectAroundSpringOffset = 0.01
        points = []
        points2 = []
        points3 = []
        points4 = []
        arcs = sketch.sketchCurves.sketchArcs
        spaceDivider = self._springCoilThickness * 3
   
        lines = sketch.sketchCurves.sketchLines
        
        for i in range(self._springCoils * 4):
            points.append(adsk.core.Point3D.create(self._y+ i * self._springCoilThickness /2, self._x + 0,  0))
            points2.append(adsk.core.Point3D.create( self._y+ i * self._springCoilThickness /2, self._x+ self._springWidth /2 -(self._spaceBetween /2) -spaceDivider,0))
            
        for i in range(self._springCoils * 4):
            points3.append(adsk.core.Point3D.create( self._y+ i * self._springCoilThickness /2, self._x+ self._springWidth/2 +(self._spaceBetween /2),0))
            points4.append(adsk.core.Point3D.create(self._y+ i * self._springCoilThickness /2, self._x+ self._springWidth -(self._springCoilThickness*3) , 0))
        
        leftArcsArray = self.pointsToSpring(sketch, points,points2)
        rightArcArray = self.pointsToSpring(sketch, points4,points3)
        
        #close inner structure
        lines.addByTwoPoints(rightArcArray[0][0][1].endSketchPoint, leftArcsArray[0][0][1].startSketchPoint)  
        lines.addByTwoPoints(leftArcsArray[0][-1][1].endSketchPoint, rightArcArray[0][-1][1].startSketchPoint)  
        #sideWall left spring
        offsetVec = adsk.core.Vector3D.create( 0, -self._springCoilThickness*1.5   , 0)
        offsetVec2 = adsk.core.Vector3D.create(0, -self._springCoilThickness*1.5+rectAroundSpringOffset , 0)
        sidwallLeftStartPoint = adsk.core.Point3D.cast(leftArcsArray[1][0][1].startSketchPoint.geometry.copy())
        sidwallLeftStartPoint.translateBy(offsetVec2)
        sidwallLeftEndPoint = adsk.core.Point3D.cast(leftArcsArray[1][-1][1].endSketchPoint.geometry.copy())
        sidwallLeftEndPoint.translateBy(offsetVec)
        bottomLeftSmall = lines.addByTwoPoints(sidwallLeftStartPoint, leftArcsArray[1][0][1].startSketchPoint) 
        topLeftSmall = lines.addByTwoPoints(leftArcsArray[1][-1][1].endSketchPoint, sidwallLeftEndPoint)  
        #sideWall right spring
        offsetVec = adsk.core.Vector3D.create(0 , self._springCoilThickness * 1.5  , 0)
        offsetVec2 = adsk.core.Vector3D.create(0 , self._springCoilThickness * 1.5 -rectAroundSpringOffset, 0)
        sidwallRightStartPoint = adsk.core.Point3D.cast(rightArcArray[1][0][1].endSketchPoint.geometry.copy())
        sidwallRightStartPoint.translateBy(offsetVec2)
        sidwallRightEndPoint = adsk.core.Point3D.cast(rightArcArray[1][-1][1].startSketchPoint.geometry.copy())
        sidwallRightEndPoint.translateBy(offsetVec)
        #connected to arc top goes to right
        bottomRightSmall= lines.addByTwoPoints(sidwallRightStartPoint, rightArcArray[1][0][1].endSketchPoint) 
        topRightSmall = lines.addByTwoPoints(rightArcArray[1][-1][1].startSketchPoint, sidwallRightEndPoint)  
        #sliding guide right
        offsetVec = adsk.core.Vector3D.create(self._springCoilThickness, 0, 0)
        guideRightEndPoint = adsk.core.Point3D.cast(sidwallRightEndPoint.copy())
        guideRightEndPoint.translateBy(offsetVec)
        sideWallRighTop = adsk.core.Line3D.create(sidwallRightEndPoint, guideRightEndPoint)
        sideWallRightBottom = adsk.core.Point3D.create(-offsetX, sidwallRightEndPoint.y,0)
        lines.addByTwoPoints(sideWallRightBottom, sidwallRightEndPoint)
        guideLeftEndPoint = adsk.core.Point3D.cast(sidwallLeftEndPoint.copy())
        guideLeftEndPoint.translateBy(offsetVec)

        sideWallLeftTop = adsk.core.Line3D.create(sidwallLeftEndPoint, guideLeftEndPoint)
        sideWallLeftBottom = adsk.core.Point3D.create( -offsetX,sidwallLeftEndPoint.y,0)
        sideLineLeft = lines.addByTwoPoints(sideWallLeftBottom, sidwallLeftEndPoint)
        #bottom
        offsetVec = adsk.core.Vector3D.create(0,-self._springCoilThickness*2 , 0)
        bottomLeftStartPoint = sidwallLeftStartPoint
        bottomLeftEndPoint = adsk.core.Point3D.create(-offsetX, bottomLeftStartPoint.y ,0)
        lines.addByTwoPoints(bottomLeftStartPoint, bottomLeftEndPoint)
        bottomRightStartPoint = sidwallRightStartPoint
        bottomRightEndPoint = adsk.core.Point3D.create( -offsetX,bottomRightStartPoint.y,0)
        lines.addByTwoPoints(bottomRightStartPoint, bottomRightEndPoint)
        
        lineTop = lines.addByTwoPoints(sideWallLeftBottom, sideWallRightBottom)
        
        centerPointX =  -(sideLineLeft.startSketchPoint.geometry.x -sideLineLeft.endSketchPoint.geometry.x)/2- offsetX
        centerPointY =  (lineTop.endSketchPoint.geometry.y - lineTop.startSketchPoint.geometry.y) /2
        sketch.sketchPoints.add(adsk.core.Point3D.create(centerPointX, centerPointY, 0))

        extraOffset = 0
        if self._position == 'Bottom':
            angle = math.radians(180)
            extraOffset = self._hingeHeight - sideLineLeft.length
            ratchetPointA = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x, centerPointY +self._materialThickness, 0)
            ratchetPointB = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x -0.15, centerPointY +self._materialThickness, 0)
           
            ratchetPointC = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x, centerPointY , 0)
            
            ratchetPointD = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x -0.15, centerPointY , 0)
            ratchetPointE = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x , centerPointY -self._materialThickness , 0)
            ratchetPointF = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x -0.15, centerPointY -self._materialThickness , 0)
            
            linesRatchet.addByTwoPoints(ratchetPointC, ratchetPointD)
            linesRatchet.addByTwoPoints(ratchetPointD, ratchetPointA)
            linesRatchet.addByTwoPoints(ratchetPointA, ratchetPointC)
            
            linesRatchet.addByTwoPoints(ratchetPointE, ratchetPointF)  
            linesRatchet.addByTwoPoints(ratchetPointF, ratchetPointC)
            linesRatchet.addByTwoPoints(ratchetPointE, ratchetPointC)
            
        elif self._position =='Top':
            angle = 0
            ratchetPointA = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x, centerPointY +self._materialThickness, 0)
            ratchetPointB = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x -0.15, centerPointY +self._materialThickness, 0)
            ratchetPointC = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x, centerPointY , 0)
            ratchetPointD = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x -0.15, centerPointY , 0)
            ratchetPointE = adsk.core.Point3D.create(lineTop.endSketchPoint.geometry.x , centerPointY -self._materialThickness , 0)

            linesRatchet.addByTwoPoints(ratchetPointA, ratchetPointB)
            linesRatchet.addByTwoPoints(ratchetPointC, ratchetPointB)
            linesRatchet.addByTwoPoints(ratchetPointC, ratchetPointA)

            linesRatchet.addByTwoPoints(ratchetPointC, ratchetPointD)
            linesRatchet.addByTwoPoints(ratchetPointD, ratchetPointE)
            linesRatchet.addByTwoPoints(ratchetPointC, ratchetPointE)
        else:
            angle = 0
        allCurvesA = adsk.core.ObjectCollection.create()
        allCurvesB = adsk.core.ObjectCollection.create()
        for c in sketch.sketchCurves:
            allCurvesA.add(c)
        for curves in sketchRatchet.sketchCurves:
            allCurvesB.add(curves)
        for p in sketch.sketchPoints:
            allCurvesA.add(p)          
               
        normal = sketch.xDirection.crossProduct(sketch.yDirection)
        normal.transformBy(sketch.transform)
        origin = adsk.core.Point3D.create(centerPointX, centerPointY, 0)
        if self._position == 'Bottom' or self._position == 'Top':
            matA = adsk.core.Matrix3D.create()
            matA.setToRotation(angle, normal, origin)
            sketch.move(allCurvesA, matA)
            sketchRatchet.move(allCurvesB, matA)
            
            matB = adsk.core.Matrix3D.create()
            offsetVec = adsk.core.Vector3D.create(offsetX+ self._xOffset +extraOffset, -self._springWidth-self._yOffset, 0)
            matB.translation = offsetVec
            sketch.move(allCurvesA, matB)
            sketchRatchet.move(allCurvesB, matB)
            

        
        if True:
            for profile in sketch.profiles:
                extrudes = mainBodyComponent.features.extrudeFeatures
                extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
                extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
                start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(self._materialThickness))
                extrudeInput.startExtent = start_from
                extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
            
            for profile in sketchRatchet.profiles:
                extrudes = mainBodyComponent.features.extrudeFeatures
                extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(self._materialThickness))
                extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
                start_from = adsk.fusion.FromEntityStartDefinition.create(self._plane, adsk.core.ValueInput.createByReal(self._materialThickness))
                extrudeInput.startExtent = start_from
                extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
            
            if sketchRatchet.profiles.count > 0:
                extrudes = mainBodyComponent.features.extrudeFeatures
                extrudeInput = extrudes.createInput(sketchRatchet.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
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