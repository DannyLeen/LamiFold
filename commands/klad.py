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
        ao = AppObjects()
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id']
        
        springCoils = input_values['springCoils_input_id']
        widthSpring = input_values['widthSpring_input_id']
        springSpace = input_values['springSpace_input_id']
        springCoilThickness = input_values['springCoilThickness_input_id']
        springLockValue = input_values['springLockCheckBox_input_id']
        springUnlockValue = input_values['springUnlockCheckBox_input_id']
        

        
        all_selections = input_values.get('selection_input_id', None)
        
        
        if len(all_selections) > 0:
            
            mainBodyOcc = ao.root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            mainBodyComponent = mainBodyOcc.component
            mainBodyOcc.component.name = 'Hinge'
            
            the_first_selection = all_selections[0]
            diagonal = math.sqrt(2*materialThickness*materialThickness)
            
            offsetThickness = diagonal - materialThickness 
            
            allValues = {
            "comp": mainBodyComponent,
            "amountOfHinges" : amountOfHinges,
            "width": width, 
            "height": height, 
            "materialThickness":materialThickness,
            "hingeLength":hingeLength, 
            "hingePenLength": hingePenLength,
            "springCoils": springCoils,
            "widthSpring":widthSpring, 
            "springSpace":springSpace, 
            "springCoilThickness":springCoilThickness,
            "springLockValue":springLockValue,
            "springUnlockValue":springUnlockValue,
            "offsetThickness":offsetThickness, 
            "the_first_selection":the_first_selection
            }
     
            state1 = self.drawHingeBase(allValues, 0)
            state = self.drawHingeBase(allValues,1)
            state3 = self.drawHingeBase(allValues, 2)
            #state = "Layer 1: " + state1 + " Layer 2: " state2 + " Layer 3: " + state3 
            text_box_input = inputs.itemById('text_box_input_id')
            text_box_input.text = state
           

    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass


    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        pass

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = AppObjects()
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        materialThickness = input_values['materialThickness_input_id']
        amountOfHinges= input_values['amountOfHinges_input_id']
        hingeLength = input_values['hingeLength_input_id']
        hingePenLength = input_values['hingePenLength_input_id'] 
        
        springCoils = input_values['springCoils_input_id']
        widthSpring = input_values['widthSpring_input_id']
        springSpace = input_values['springSpace_input_id']
        springCoilThickness = input_values['springCoilThickness_input_id']
        springLockValue = input_values['springLockCheckBox_input_id']
        springUnlockValue = input_values['springUnlockCheckBox_input_id']
        
        all_selections = input_values.get('selection_input_id', None)
        
        
        if len(all_selections) > 0:
            
            mainBodyOcc = ao.root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            mainBodyComponent = mainBodyOcc.component
            mainBodyOcc.component.name = 'Hinge'
            
            the_first_selection = all_selections[0]
            diagonal = math.sqrt(2*materialThickness*materialThickness)
            
            offsetThickness = diagonal - materialThickness 
            
            allValues = {
            "comp": mainBodyComponent,
            "amountOfHinges" : amountOfHinges,
            "width": width, 
            "height": height, 
            "materialThickness":materialThickness,
            "hingeLength":hingeLength, 
            "hingePenLength": hingePenLength,
            "springCoils": springCoils,
            "widthSpring":widthSpring, 
            "springSpace":springSpace, 
            "springCoilThickness":springCoilThickness,
            "springLockValue":springLockValue,
            "springUnlockValue":springUnlockValue,
            "offsetThickness":offsetThickness, 
            "the_first_selection":the_first_selection
            }
           # state = ''
           # self.drawHingeBase(allValues, 0)
            state = self.drawHingeBase(allValues,1)
            #state = self.drawHingeBase(allValues, 2)
            
            text_box_input = inputs.itemById('text_box_input_id')
            text_box_input.text = state
           
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
        
        default_springLength = adsk.core.ValueInput.createByString('15 mm')
        default_springCoilThickness = adsk.core.ValueInput.createByString('0.9 mm')
        default_springSpace = adsk.core.ValueInput.createByString('0.5 mm')
        # Get teh user's current units
        default_units = ao.units_manager.defaultLengthUnits

        tab1ChildInputs.addSelectionInput('selection_input_id', 'Select a plane', 'Select Something')
           
        # Create a value input.  This will respect units and user defined equation input.
        tab1ChildInputs.addValueInput('width_input_id', 'Width', default_units, default_valueX)
        tab1ChildInputs.addValueInput('height_input_id', 'Height', default_units, default_valueY)
        
        tab1ChildInputs.addValueInput('materialThickness_input_id', 'Thickness',default_units , default_materialThickness)
        tab1ChildInputs.addIntegerSpinnerCommandInput('amountOfHinges_input_id', 'Amount of Hinges', 1, 10, 1, 2)
        tab1ChildInputs.addValueInput('hingeLength_input_id', 'Hinge length', default_units, default_hingeLength)
        tab1ChildInputs.addValueInput('hingePenLength_input_id', 'Hinge pen length', default_units, default_penLength)


        # Other Input types
        tab1ChildInputs.addBoolValueInput('springLockCheckBox_input_id', 'Add Lock', True, '', True)
        tab1ChildInputs.addBoolValueInput('springUnlockCheckBox_input_id', 'Add Unlock', True)
        tab1ChildInputs.addBoolValueInput('bool_input_id', 'Add Bottom', True)
        tab1ChildInputs.addTextBoxCommandInput('text_box_input_id', 'State: ', '', 1, True)
        
        
        # Tab 2
        tab2ChildInputs.addValueInput('widthSpring_input_id', 'Spring Width', default_units, default_springLength)
        tab2ChildInputs.addValueInput('springCoilThickness_input_id', 'Spring Coil Thickness', default_units, default_springCoilThickness)
        tab2ChildInputs.addIntegerSpinnerCommandInput('springCoils_input_id', 'Spring Coils', 1, 10, 2, 3)
        tab2ChildInputs.addValueInput('springSpace_input_id', 'Spring space between', default_units, default_springSpace)
        
    def drawHingeBase(self, allValues, layerNumber):
            mainBodyComponent = allValues["comp"]
            amountOfHinges = allValues["amountOfHinges"]
            plane = allValues["the_first_selection"]
            width = allValues["width"]
            height = allValues["height"]
            materialThickness = allValues["materialThickness"]
            hingeLength = allValues["hingeLength"]
            hingePenLength = allValues["hingePenLength"]
            springCoils = allValues["springCoils"]
            widthSpring = allValues["widthSpring"]
            springSpace = allValues["springSpace"]
            springCoilThickness = allValues["springCoilThickness"]
            lockCheckBoxValue = allValues["springLockValue"]
            springUnlockValue = allValues["springUnlockValue"]
            offsetThickness = allValues["offsetThickness"]
            
            if layerNumber == 0: extrudeOffset = 0
            if layerNumber == 1: 
                extrudeOffset = materialThickness

            if layerNumber == 2: extrudeOffset = materialThickness*2
        
            
            start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(extrudeOffset))
        
            sketches = mainBodyComponent.sketches
            sketch = sketches.addWithoutEdges(plane)
            lines = sketch.sketchCurves.sketchLines
            rectPoint = adsk.core.Point3D.create(height, width, 0)
            offset = 1 # offset from top and bottom = 1 cm 
            
            #Left Side
            sketchCutOut = sketches.addWithoutEdges(plane)
            lastSketchCutOut = sketches.addWithoutEdges(plane)
            lastLineCutOut = lastSketchCutOut.sketchCurves.sketchLines
            linesCutOut = sketchCutOut.sketchCurves.sketchLines
            
            lastSketchFold  = sketches.addWithoutEdges(plane)
            lastLineFold = lastSketchFold.sketchCurves.sketchLines
            #Draw baseplate
            lines.addTwoPointRectangle(adsk.core.Point3D.create(0,0,0), rectPoint)
            self.extrudeProfile(mainBodyComponent, sketch.profiles.item(0), materialThickness, start_from)
            
            #Fold = Right side
            rectPointFold = adsk.core.Point3D.create(height, -(width + materialThickness), 0)
            sketchFold = sketches.addWithoutEdges(plane)
            sketchFold.name = "fold"
            linesFold = sketchFold.sketchCurves.sketchLines
            linesFold.addTwoPointRectangle(adsk.core.Point3D.create(0,- materialThickness,0), rectPointFold)
            
            
            hingeLengthSmall = hingeLength - (hingePenLength*2)
            
            if amountOfHinges > 1:
                # if  layerNumber < 2:
                #     topRect = linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(offset,materialThickness - offsetThickness,0), adsk.core.Point3D.create(hingeLength+offset, materialThickness*2 , 0))
                #     topRectSmall = linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(offset + hingePenLength,0,0), adsk.core.Point3D.create(hingeLengthSmall+offset+hingePenLength, materialThickness*2, 0))
                    
                #     bottomRect = linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(height-offset,materialThickness -offsetThickness,0), adsk.core.Point3D.create(height - (hingeLength+offset), materialThickness*2 , 0))
                #     bottomRectSmall = linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(height-offset-hingePenLength ,0,0), adsk.core.Point3D.create(height - (hingeLengthSmall+offset+hingePenLength), materialThickness*2, 0))
                #     if layerNumber == 0:
                       
                      #  topRectSmallFold = linesFold.addTwoPointRectangle(adsk.core.Point3D.create(offset + hingePenLength,-materialThickness,0), adsk.core.Point3D.create(hingeLengthSmall+offset+hingePenLength, materialThickness*2, 0))
                       # bottomRectSmallFold = linesFold.addTwoPointRectangle(adsk.core.Point3D.create(height-offset-hingePenLength ,-materialThickness ,0), adsk.core.Point3D.create(height - (hingeLengthSmall+offset+hingePenLength), materialThickness*2, 0))
                    
                    if layerNumber == 1 and lockCheckBoxValue:
                        
                        
                        topRectSmallFoldPin = lastLineFold.addTwoPointRectangle(adsk.core.Point3D.create(offset,materialThickness,0), adsk.core.Point3D.create(hingeLength+offset, materialThickness*2 , 0))
                        bottomRectSmallFoldPin = lastLineFold.addTwoPointRectangle(adsk.core.Point3D.create(height-offset,materialThickness,0), adsk.core.Point3D.create(height - (hingeLength+offset), materialThickness*2 , 0))
                        
                     
                        topRectSmallCut = lastLineCutOut.addTwoPointRectangle(adsk.core.Point3D.create(offset + hingePenLength,-materialThickness -4,0), adsk.core.Point3D.create(hingeLengthSmall+offset+hingePenLength, materialThickness*2, 0))
                        bottomRectSmallCut = lastLineCutOut.addTwoPointRectangle(adsk.core.Point3D.create(height-offset-hingePenLength ,-materialThickness -4,0), adsk.core.Point3D.create(height - (hingeLengthSmall+offset+hingePenLength), materialThickness*2, 0))
                        
                        topRectGuidCut = lastLineCutOut.addTwoPointRectangle(adsk.core.Point3D.create(offset,materialThickness-width,0), adsk.core.Point3D.create(hingeLength+offset, materialThickness*4-width , 0))
                        bottomRectGuideCut = lastLineCutOut.addTwoPointRectangle(adsk.core.Point3D.create(height-offset,materialThickness-width,0), adsk.core.Point3D.create(height - (hingeLength+offset), materialThickness*4-width , 0))
                        
                        topRectGuidPiece = lastLineFold.addTwoPointRectangle(adsk.core.Point3D.create(offset,-width +materialThickness*4 ,0), adsk.core.Point3D.create(hingeLength+offset, materialThickness*2-width , 0))
                        bottomRectGuidePiece = lastLineFold.addTwoPointRectangle(adsk.core.Point3D.create(height-offset,-width +materialThickness*4,0), adsk.core.Point3D.create(height - (hingeLength+offset), materialThickness*2-width , 0))
                        
                        topRectSmallFoldPiece = lastLineFold.addTwoPointRectangle(adsk.core.Point3D.create(offset + hingePenLength,materialThickness*4 -width,0), adsk.core.Point3D.create(hingeLengthSmall+offset+hingePenLength, materialThickness*2, 0))
                        bottomRectSmallFoldPiece = lastLineFold.addTwoPointRectangle(adsk.core.Point3D.create(height-offset-hingePenLength ,materialThickness*4 -width,0), adsk.core.Point3D.create(height - (hingeLengthSmall+offset+hingePenLength), materialThickness*2, 0))
                        

                    if layerNumber == 1 and not lockCheckBoxValue:
                        topRectSmallFoldPin = linesFold.addTwoPointRectangle(adsk.core.Point3D.create(offset,materialThickness,0), adsk.core.Point3D.create(hingeLength+offset, materialThickness*2 , 0))
                        bottomRectSmallFoldPin = linesFold.addTwoPointRectangle(adsk.core.Point3D.create(height-offset,materialThickness,0), adsk.core.Point3D.create(height - (hingeLength+offset), materialThickness*2 , 0))
                        topRectSmallFoldPiece = linesFold.addTwoPointRectangle(adsk.core.Point3D.create(offset + hingePenLength,-materialThickness*2 ,0), adsk.core.Point3D.create(hingeLengthSmall+offset+hingePenLength, materialThickness, 0))
                        bottomRectSmallFoldPiece = linesFold.addTwoPointRectangle(adsk.core.Point3D.create(height-offset-hingePenLength ,-materialThickness*2,0), adsk.core.Point3D.create(height - (hingeLengthSmall+offset+hingePenLength), materialThickness, 0))
   
                    
                else: 
                    topRectSmall = linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(offset + hingePenLength,0,0), adsk.core.Point3D.create(hingeLengthSmall+offset+hingePenLength, materialThickness*2, 0))
                    bottomRectSmall = linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(height-offset-hingePenLength ,0,0), adsk.core.Point3D.create(height - (hingeLengthSmall+offset+hingePenLength), materialThickness*2, 0))
                   
                   # bottomRectSmallFold = linesFold.addTwoPointRectangle(adsk.core.Point3D.create(height-offset-hingePenLength ,-materialThickness,0), adsk.core.Point3D.create(height - (hingeLengthSmall+offset+hingePenLength), materialThickness*2, 0))

                brutLength = height - ((offset + hingeLength)*2)
                
                netLength = brutLength - (hingeLength*(amountOfHinges-2))
                rectOffset = netLength/(amountOfHinges -1) # for e.g. 4 hinges = 5 spaces - 2 hinges on top of bottom
                startPos = hingeLength + offset
                startPosSmall = hingeLengthSmall+offset
                countDistance= 0
                inbetweenRect = []
                
                if rectOffset > 0:
                    state = "All good"
                    for i in range(amountOfHinges -2):
                        if layerNumber < 2 :
                            inbetweenRect.append(linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(startPos+rectOffset + countDistance,materialThickness-offsetThickness,0), adsk.core.Point3D.create(startPos+hingeLength+rectOffset  +countDistance, materialThickness*2 , 0)))
                            inbetweenRect.append(linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(startPos+rectOffset + countDistance+hingePenLength,0,0), adsk.core.Point3D.create(startPos+hingeLength+rectOffset  +countDistance-hingePenLength, materialThickness, 0)))
                            inbetweenRect.append(linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(startPos+rectOffset + countDistance+hingePenLength,0,0), adsk.core.Point3D.create(startPos+hingeLength+rectOffset  +countDistance-hingePenLength, materialThickness*2, 0)))
                            inbetweenRect.append(linesFold.addTwoPointRectangle(adsk.core.Point3D.create(startPos+rectOffset + countDistance+hingePenLength,-materialThickness,0), adsk.core.Point3D.create(startPos+hingeLength+rectOffset  +countDistance-hingePenLength, materialThickness*2, 0)))

                            if layerNumber == 1:
                                inbetweenRect.append(linesFold.addTwoPointRectangle(adsk.core.Point3D.create(startPos+rectOffset + countDistance,materialThickness,0), adsk.core.Point3D.create(startPos+hingeLength+rectOffset  +countDistance, materialThickness*2, 0)))

                        else:
                            inbetweenRect.append(linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create(startPos+rectOffset + countDistance+hingePenLength,0,0), adsk.core.Point3D.create(startPos+hingeLength+rectOffset  +countDistance-hingePenLength, materialThickness*2, 0)))

                        countDistance = countDistance + rectOffset + hingeLength
                else:
                    state = "Can't fit that many hinges"
                    print(state)
            else:
            
                linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create((height/2)-(hingeLength/2),materialThickness-offsetThickness,0), adsk.core.Point3D.create((height/2)+(hingeLength/2), materialThickness*2 , 0))
                linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create((height/2)-(hingeLengthSmall/2),0,0), adsk.core.Point3D.create((height/2)+(hingeLengthSmall/2), materialThickness, 0))
                linesCutOut.addTwoPointRectangle(adsk.core.Point3D.create((height/2)-(hingeLengthSmall/2),0,0), adsk.core.Point3D.create((height/2)+(hingeLengthSmall/2), materialThickness *2, 0))
                if layerNumber == 1:
                    linesFold.addTwoPointRectangle(adsk.core.Point3D.create((height/2)-(hingeLength/2),materialThickness,0), adsk.core.Point3D.create((height/2)+(hingeLength/2), materialThickness*2 , 0))
                    linesFold.addTwoPointRectangle(adsk.core.Point3D.create((height/2)-(hingeLengthSmall/2),-materialThickness,0), adsk.core.Point3D.create((height/2)+(hingeLengthSmall/2), materialThickness, 0))
                    linesFold.addTwoPointRectangle(adsk.core.Point3D.create((height/2)-(hingeLengthSmall/2),0,0), adsk.core.Point3D.create((height/2)+(hingeLengthSmall/2), materialThickness *2, 0))
                if layerNumber == 0:
                    linesFold.addTwoPointRectangle(adsk.core.Point3D.create((height/2)-(hingeLengthSmall/2),-materialThickness,0), adsk.core.Point3D.create((height/2)+(hingeLengthSmall/2), materialThickness *2, 0))

                
            profs = adsk.core.ObjectCollection.create()
            profsLast = adsk.core.ObjectCollection.create()
            profsFold = adsk.core.ObjectCollection.create()
            profsFoldLast = adsk.core.ObjectCollection.create()
            # Add all of the profiles to the collection.
            for prof in sketchCutOut.profiles:
                profs.add(prof)
                
            self.cutProfile(mainBodyComponent, profs, materialThickness,start_from)
            
            for profFold in sketchFold.profiles:
                profsFold.add(profFold)
            
            self.extrudeProfile(mainBodyComponent, profsFold, materialThickness, start_from)
            
            for profLast in lastSketchCutOut.profiles:
                profsLast.add(profLast)
            if len(profsLast) > 0:
                self.cutProfile(mainBodyComponent, profsLast, materialThickness,start_from)

            for profLast in lastSketchFold.profiles:
                profsFoldLast.add(profLast)
                
            if len(profsLast) > 0:
                self.extrudeProfile(mainBodyComponent, profsFoldLast, materialThickness,start_from)
                
          #  if layerNumber == 1:
                #pass
             #   Spring(plane, springCoils, widthSpring, springSpace, springCoilThickness, materialThickness, materialThickness)

            return state
                 
    def extrudeProfile(self, comp, profiles, materialThickness, start_from):
        
        extrudes = comp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = start_from 

        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
    
    def cutProfile(self, comp, profiles, materialThickness, start_from):
        
        extrudes = comp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = start_from 

        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput)) 
        
  