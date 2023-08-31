import adsk.core
import adsk.fusion
import adsk.cam

# Import the entire apper package
import apper

# Alternatively you can import a specific function or class
from apper import AppObjects



class PlanarCommand(apper.Fusion360CommandBase):

    # Run whenever a user makes any change to a value or selection in the addin UI
    # Commands in here will be run through the Fusion processor and changes will be reflected in  Fusion graphics area
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        
        width = input_values['width_input_id']
        height = input_values['height_input_id']
        slotWidth = input_values['slotWidth_input_id']
        materialThickness = input_values['materialThickness_input_id']
        
        all_selections = input_values.get('selection_input_id', None)
        if len(all_selections) > 0:
            
            the_first_selection = all_selections[0]
            self.drawRectangle(the_first_selection, width, height, slotWidth, materialThickness)
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

        width = input_values['width_input_id']
        height = input_values['height_input_id']
        slotWidth = input_values['slotWidth_input_id']
        materialThickness = input_values['materialThickness_input_id']
        
        all_selections = input_values.get('selection_input_id', None)
        if len(all_selections) > 0:
        
            the_first_selection = all_selections[0]
            self.drawRectangle(the_first_selection, width, height, slotWidth, materialThickness)

    # Run when the user selects your command icon from the Fusion 360 UI
    # Typically used to create and display a command dialog box
    # The following is a basic sample of a dialog UI

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        ao = AppObjects()
        inputs.addSelectionInput('selection_input_id', 'Select a plane', 'Select Something')
 
        # Create a default value using a string
        default_valueX = adsk.core.ValueInput.createByString('50 mm')
        default_valueY = adsk.core.ValueInput.createByString('100 mm')
        
       # default_offsetX = adsk.core.ValueInput.createByString('20 mm')
        #default_offsetY = adsk.core.ValueInput.createByString('10 mm')
        default_slotWidth = adsk.core.ValueInput.createByString('10 mm')
        default_materialThickness = adsk.core.ValueInput.createByString('4 mm')
        # Get teh user's current units
        default_units = ao.units_manager.defaultLengthUnits

        # Create a value input.  This will respect units and user defined equation input.
        inputs.addValueInput('width_input_id', 'Width', default_units, default_valueX)
        inputs.addValueInput('height_input_id', 'Height', default_units, default_valueY)
        
        inputs.addValueInput('slotWidth_input_id', 'Slot width',default_units , default_slotWidth)
        inputs.addValueInput('materialThickness_input_id', 'Thickness',default_units , default_materialThickness)


    def drawRectangle(self, plane, width, height, slotWidth, materialThickness):
        ao = AppObjects()
        
        mainBodyOcc = ao.root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        mainBodyComponent = mainBodyOcc.component
        mainBodyOcc.component.name = 'Slider'
            
        offsetY= 2
        offsetX = (width -slotWidth) 
        extrudes = mainBodyComponent.features.extrudeFeatures
        
        sketches = mainBodyComponent.sketches
        sketch = sketches.addWithoutEdges(plane)
        lines = sketch.sketchCurves.sketchLines
        rectPoint = adsk.core.Point3D.create(height, width, 0)

        rectangle = lines.addTwoPointRectangle(adsk.core.Point3D.create(0,0,0), rectPoint)
        lines.addTwoPointRectangle(adsk.core.Point3D.create(offsetY/2,offsetX/2,0),  adsk.core.Point3D.create(height -offsetY/2, width -offsetX/2, 0))
        
        profiles = sketch.profiles.item(0)
        extrudeInput = extrudes.createInput(profiles, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))    
           
        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)       
        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput))
        
        sketchInternal = sketches.addWithoutEdges(plane)
        linesInternal = sketchInternal.sketchCurves.sketchLines
        
        linesInternal.addTwoPointRectangle(adsk.core.Point3D.create(height/2 -slotWidth/2,offsetX/2,0),  adsk.core.Point3D.create(height/2 + slotWidth/2, width -offsetX/2, 0))
        
        profilesInternal = sketchInternal.profiles.item(0)
        extrudeInputInternal = extrudes.createInput(profilesInternal, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)   
           
        extrudeInputInternal.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)       
        extrudeInternal = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInputInternal))
        extrudeInternal.parentComponent.name = 'Slider Internal'
       
        
        
        sketchBottom = sketches.addWithoutEdges(plane)
        linesBottom= sketchBottom.sketchCurves.sketchLines
        knobOffset = 1
        linesBottom.addTwoPointRectangle(adsk.core.Point3D.create(height/2 -slotWidth -(knobOffset/2),offsetX/2 - knobOffset,0),  adsk.core.Point3D.create(height/2 + slotWidth +(knobOffset/2), width -offsetX/2 +knobOffset, 0))
        
        profilesBottom = sketchBottom.profiles.item(0)
        extrudeInputBottom = extrudes.createInput(profilesBottom, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)   
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))  
        extrudeInputBottom.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.NegativeExtentDirection)       
        extrudeBottom = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInputBottom))
        extrudeBottom.parentComponent.name = 'Slider Bottom'
        
        sketchTop = sketches.addWithoutEdges(plane)
        start_from = adsk.fusion.FromEntityStartDefinition.create(plane, adsk.core.ValueInput.createByReal(materialThickness))
        linesTop= sketchTop.sketchCurves.sketchLines
        linesTop.addTwoPointRectangle(adsk.core.Point3D.create(height/2 -slotWidth -(knobOffset/2),offsetX/2 - knobOffset,0),  adsk.core.Point3D.create(height/2 + slotWidth +(knobOffset/2), width -offsetX/2 +knobOffset, 0))
        
        profilesTop = sketchTop.profiles.item(0)
        extrudeInputTop = extrudes.createInput(profilesTop, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)   
  
        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(materialThickness))  
        
        extrudeInputTop.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)     
        extrudeInputTop.startExtent = start_from 
        extrudeTop = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInputTop))
        extrudeTop.parentComponent.name = 'Slider Top'
        
        


        
        
        


        
        
        
        
        