import adsk.core
import adsk.fusion
import adsk.cam
import math
import apper

from apper import AppObjects


class FabricateCommand(apper.Fusion360CommandBase):

    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        ao = AppObjects()
        
        kerf = input_values['kerf_input_id']
        borderSize = input_values['borderSize_input_id']
        text_box_input = inputs.itemById('text_box_input_id')
        sizeText_box_input = inputs.itemById('sizeText_box_input_id')
        rigidGroups = self.checkForRigidGroup()
        
        
        
        state, lowestBodies, exportOcc, lowestBodiesOcc = self.detectLowestBody(input_values)
        if lowestBodies:
            layerCounter = 0
            state, numberOfLayers = self.findConnectedBodies(input_values, lowestBodies, exportOcc, layerCounter, rigidGroups, lowestBodiesOcc)
        
            sizeText_box_input.text = self.getSheetSize(input_values) + "/ " + str(numberOfLayers)+ " sheets"
            text_box_input.text = str(state)
        else: 
            text_box_input.text = "Something went wrong, no lowest body found"
        args.isValidResult = True

    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        pass

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):

        pass


    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
         pass
     

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        ao = AppObjects()
        
        default_borderSize = adsk.core.ValueInput.createByString('15 mm')
        default_kerf = adsk.core.ValueInput.createByString('0.1 mm')
        default_width = adsk.core.ValueInput.createByString('1220 mm')
        default_height = adsk.core.ValueInput.createByString('850 mm')
        # Get teh user's current units
        default_units = ao.units_manager.defaultLengthUnits

        inputs.addValueInput('kerf_input_id', 'Laser Kerf',default_units ,  default_kerf)
        inputs.addValueInput('borderSize_input_id', 'Border Size', default_units, default_borderSize)
        inputs.addValueInput('sheetWidth_input_id', 'Stock sheet width',default_units ,  default_width)
        inputs.addValueInput('borderheight_input_id', 'Stock sheet height', default_units, default_height)
        inputs.addBoolValueInput('modelCheckbox_input_id', 'Export Model Profiles', True, '', True)
        inputs.addBoolValueInput('glueCheckbox_input_id', 'Export Glue Stencil', True, '', True)
        inputs.addTextBoxCommandInput('sizeText_box_input_id', 'Sheet size: ', '', 1, True)
        inputs.addTextBoxCommandInput('text_box_input_id', 'Info: ', '', 1, True)

    def getSheetSize(self, input_values):
        ao = AppObjects()
        occ = ao.root_comp
        borderSize = input_values['borderSize_input_id']
        L  = (occ.boundingBox.maxPoint.x - occ.boundingBox.minPoint.x) + (borderSize*2) 
        W = (occ.boundingBox.maxPoint.y - occ.boundingBox.minPoint.y)+ (borderSize*2) 
        return  str(math.ceil(L)) +"cm x "+ str(math.ceil(W)) + "cm"
        
    def drawGlueSheet(self, input_values, plane, maxPointZ, exportOcc):
        ao = AppObjects()
        
        occ = ao.root_comp
        L  = occ.boundingBox.maxPoint.x - occ.boundingBox.minPoint.x
        W = occ.boundingBox.maxPoint.y - occ.boundingBox.minPoint.y
        H  = occ.boundingBox.maxPoint.z - occ.boundingBox.minPoint.z
        borderSize = input_values['borderSize_input_id']

        sketches = exportOcc.component.sketches
        glueSketch = sketches.addWithoutEdges(plane)  
        #glueSketch = sketches.add(planeOne)
        glueSketch.name = "Glue sheet"
        
        glueSheetLines = glueSketch.sketchCurves.sketchLines
        p1 = adsk.core.Point3D.create(occ.boundingBox.minPoint.x -borderSize, occ.boundingBox.minPoint.y -borderSize, 0)
        p2 = adsk.core.Point3D.create(occ.boundingBox.maxPoint.x +borderSize, occ.boundingBox.maxPoint.y +borderSize, 0)
        glueSheetLines.addTwoPointRectangle(p1, p2)
        extrudeFeat = apper.extrude_all_profiles(glueSketch,0.05, exportOcc.component,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        targetBody = extrudeFeat.bodies.item(0)
        return targetBody

  
    def combine(self, component, tool, target):
        combine_features = component.features.combineFeatures
        combine_tools = adsk.core.ObjectCollection.create()
        combine_tools.add(tool)

        combine_input = combine_features.createInput(target, combine_tools)
        combine_input.isKeepToolBodies = False
        combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation 
        combineFeat = combine_features.add(combine_input)
             
    def combineCut(self, component, tools, target):
        combine_features = component.features.combineFeatures
  
        combine_input = combine_features.createInput(target, tools)
        combine_input.isKeepToolBodies = False
        combine_input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation #cut bodies
        combine_features.add(combine_input)
    
    def detectLowestBody(self, input_values):
        ao = AppObjects()
        
        occ = ao.root_comp
        L  = occ.boundingBox.maxPoint.x - occ.boundingBox.minPoint.x
        W = occ.boundingBox.maxPoint.y - occ.boundingBox.minPoint.y
        H  = occ.boundingBox.maxPoint.z - occ.boundingBox.minPoint.z
        #lowestBodiesTemp = adsk.core.ObjectCollection.create()
        lowestBodies = adsk.core.ObjectCollection.create()
        exportOcc = apper.create_component(ao.root_comp, "Export")
        attribs = ao.design.findAttributes('', 'Thickness')
        state = "Nothing done"
        thickness = None
        lowestBodiesOcc = adsk.core.ObjectCollection.create()
        
        for attr in attribs: 
            thickness = float(attr.value)
        if not thickness:
            succes = False
            for allOcc in ao.root_comp.allOccurrences:
                for body in allOcc.bRepBodies:
                    if body:
                        thickness = body.boundingBox.maxPoint.z - body.boundingBox.minPoint.z
                        succes = True
                        break
                    
            if not succes:                
                state =  "could not find thickness" 
                return state, None, None
        
        if thickness:
            for compareOcc in ao.root_comp.allOccurrences:
                a = compareOcc.boundingBox.minPoint.z
                b = occ.boundingBox.minPoint.z
                if math.isclose(a, b, abs_tol=0.01):
                    compareH = compareOcc.boundingBox.maxPoint.z - compareOcc.boundingBox.minPoint.z
                    # print("first: " +compareOcc.name + " height: " +str(compareH))
                    if math.isclose(thickness,compareH, abs_tol=0.01): 
                        lowestBodiesOcc.add(compareOcc)
                        #print("Lowest component: " + compareOcc.name)
                        for body in compareOcc.bRepBodies:
                            lowestBodies.add(body)
                else:
                    state = "No component found that low"
                            
            for rootBody in ao.root_comp.bRepBodies:
                a = rootBody.boundingBox.minPoint.z
                b = occ.boundingBox.minPoint.z
                #print("max a: " + str(a))
                #print("max b:" + str(b))
                if math.isclose(a, b, abs_tol=0.01):
                    compareH = rootBody.boundingBox.maxPoint.z - rootBody.boundingBox.minPoint.z
                    #print(rootBody.name + " height " + str(compareH))
                    if math.isclose(thickness,compareH, abs_tol=0.01):     
                        print("Lowest body: " + rootBody.name)
                        lowestBodies.add(rootBody)
                        lowestBodiesOcc.add(ao.root_comp)
                else:
                    state = "No root Body found that low"
                    
            # for num, body in enumerate(lowestBodiesTemp):
            #     copyBody = body.copyToComponent(exportOcc)
            #     copyBody.name = "Layer 0 - Body " + str(num)
            #     lowestBodies.add(copyBody)
                
            if  lowestBodies.count > 0:
                state = "All good"
                
            return state, lowestBodies, exportOcc, lowestBodiesOcc
    
    def findConnectedBodies(self, input_values, lowestBodies, exportOcc, layerCounter, rigidGroups, lowestBodiesOcc):
        ao = AppObjects()
        layerCounter = layerCounter +1
        #find top face
        plane = self.findTopFace(input_values, lowestBodies,exportOcc )
        sketches = exportOcc.component.sketches
        interferenceSketch = sketches.addWithoutEdges(plane)              
        normal = plane.geometry.normal
        inputBodies = adsk.core.ObjectCollection.create()
        openInputBodies = adsk.core.ObjectCollection.create()
        cutInputBodies = adsk.core.ObjectCollection.create()
        compareOccColl = adsk.core.ObjectCollection.create()

            
        H  = lowestBodies.item(0).boundingBox.maxPoint.z - lowestBodies.item(0).boundingBox.minPoint.z
        maxPointZ = lowestBodies.item(0).boundingBox.maxPoint.z

        for compareOcc in ao.root_comp.allOccurrences:
            a = compareOcc.boundingBox.minPoint.z
            if math.isclose(a, maxPointZ, abs_tol=0.01):
                compareH = compareOcc.boundingBox.maxPoint.z - compareOcc.boundingBox.minPoint.z
                print("first: " +compareOcc.name + " height: " +str(compareH))
                
                if math.isclose(compareH, H, abs_tol=0.01):
                    compareOccColl.add(compareOcc)
                    for body in compareOcc.bRepBodies:
                        if body.isLightBulbOn:
                            inputBodies.add(body)
                        
            for rootBodies in ao.root_comp.bRepBodies:
                a = rootBodies.boundingBox.minPoint.z
                # print("max a: " + str(a))
                # print("max b:" + str(b))
                if math.isclose(a, maxPointZ, abs_tol=0.01):
                    compareH = rootBodies.boundingBox.maxPoint.z - rootBodies.boundingBox.minPoint.z
                    if math.isclose(compareH, H, abs_tol=0.01):  
                        print("Next body: " + compareOcc.name)   
                        inputBodies.add(rootBodies)
                        compareOccColl.add(ao.root_comp)
                        
        if inputBodies.count > 0:                
             targetBody = self.drawGlueSheet(input_values, plane, maxPointZ, exportOcc)   
             targetBody.name = "Glue layer: " + str(layerCounter)
             
        interferenceInputBodies = adsk.core.ObjectCollection.create()     

        for occ in compareOccColl:
            print("Compare: "+occ.name)
            interferenceInputBodies.add(occ)
        for lowBodyOcc in lowestBodiesOcc:
            print("Lower: " + lowBodyOcc.name)
            interferenceInputBodies.add(lowBodyOcc)

        if interferenceInputBodies.count >= 2:
            interferenceInput = ao.design.createInterferenceInput(interferenceInputBodies)
            interferenceInput.areCoincidentFacesIncluded = True
            results = ao.design.analyzeInterference(interferenceInput)  
            if results.count > 0:
      
                intResult = adsk.fusion.InterferenceResult.cast(None)
                for intResult in results:
                    for face in intResult.interferenceBody.faces:
                        if face.geometry.objectType == adsk.core.Plane.classType():
                            if not face.geometry.isPerpendicularToPlane(plane.geometry):
                                if not intResult.interferenceBody.isSolid:
                                    occList1 = ao.root_comp.allOccurrencesByComponent(intResult.entityOne.parentComponent)
                                    occList2 = ao.root_comp.allOccurrencesByComponent(intResult.entityTwo.parentComponent)
                                    for rigidGroup in ao.root_comp.allRigidGroups:
                                        group = adsk.core.ObjectCollection.create()
                                        for rigidOcc in rigidGroup.occurrences:
                                            print("Rigid Occ: "+ rigidOcc.name)
                                            for occA in occList1:
                                                print('Occlist1: ' + occA.name)
                                                if occA == rigidOcc:
                                                    group.add(occA)
                                                    print("Add --> " + occA.name)
                                            for occB in occList2:
                                                print('Occlist2: ' + occB.name)
                                                if occB == rigidOcc:
                                                    group.add(occB)
                                                    print("Add -->" + occB.name)
            
                                        if group.count >= 2:
                                            baseFeat =  exportOcc.component.features.baseFeatures.add()
                                            baseFeat.startEdit()
                                            print("in group: "+intResult.entityTwo.parentComponent.name + ' and ' + intResult.entityOne.parentComponent.name)
                                            body =  exportOcc.component.bRepBodies.add(intResult.interferenceBody, baseFeat)
                                            interferenceSketch.project(body)
                                            body.deleteMe() 
                                            baseFeat.finishEdit()
                                            baseFeat.name = 'Inteference Results'
                                            
                                        #else:
                                         #   print("Not in Group " + intResult.entityTwo.parentComponent.name + ' and ' + intResult.entityOne.parentComponent.name)
                                                    
                    if interferenceSketch.profiles.count > 0:
                        extrudeFeat = apper.extrude_all_profiles(interferenceSketch,0.05, exportOcc.component,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                        for body in extrudeFeat.bodies:
                            cutInputBodies.add(body)
                        self.combineCut( exportOcc.component,cutInputBodies , targetBody)
            if inputBodies.count > 0:    
                self.addKeepOut(exportOcc, plane, maxPointZ, layerCounter, targetBody)   
        else:
            #print("no next layer") 
            return "All glue stencils done - no errors" , layerCounter
        if inputBodies.count == 0:
            return "All glue stencils done no input bodies - no errors" , layerCounter
             
        return  self.findConnectedBodies(input_values, inputBodies, exportOcc, layerCounter, rigidGroups, compareOccColl)
    
    def checkForRigidGroup(self):
        ao = AppObjects()
        rigidGroups = adsk.core.ObjectCollection.create()
        for rigidGroup in ao.root_comp.allRigidGroups:
            rigidGroups.add(rigidGroup)
        return rigidGroups
    
    def addKeepOut(self, exportOcc, plane, maxPointZ, layerCounter, targetBody):
        ao = AppObjects()
        
        keepOutBodies = []
        attribs = ao.design.findAttributes('KeepOut', '')
        
        for attr in attribs:
            if math.isclose(attr.parent.boundingBox.maxPoint.z,maxPointZ, abs_tol=0.1) or math.isclose(attr.parent.boundingBox.minPoint.z,maxPointZ, abs_tol=0.1):
                if attr.parent.parentComponent != exportOcc.component:
                    sketches = exportOcc.component.sketches
                    keepOutSketch = sketches.add(plane)
                    keepOutSketch.name = "keep out - layer: " + str(layerCounter)
                    
                    body = attr.parent.copyToComponent(exportOcc) 
                    body.name =  attr.parent.name + " layer " +str(layerCounter)
                    body.isLightBulbOn = False
                    keepOutSketch.project(body) 
                    print('sketchprofilecount : ' + str(keepOutSketch.profiles.count))
                    if (keepOutSketch.profiles.count > 0):
                        extrudes = exportOcc.component.features.extrudeFeatures
                        extrudeInput = extrudes.createInput(keepOutSketch.profiles.item(1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
                        extentDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(0.1))
                        extrudeInput.setOneSideExtent(extentDistance, adsk.fusion.ExtentDirections.NegativeExtentDirection)  
                        extrude = adsk.fusion.ExtrudeFeature.cast(extrudes.add(extrudeInput))
                        self.combine(ao.root_comp, extrude.bodies.item(0), targetBody)
                        
            # features = exportOcc.component.features
            # removeFeatures = features.removeFeatures
            # for body in keepOutBodies:
            #     removeFeatures.add(body)
        
    def findTopFace(self, input_values, lowestBodies,exportOcc ):
        ao = AppObjects()
                
        upDir = adsk.core.Vector3D.create(0,0,1)
        
        if lowestBodies.count > 0:
            body = lowestBodies.item(0)
        else:
            print("no lowest body")
            return None    
        component = body.parentComponent
       
        L  = body.boundingBox.maxPoint.x - body.boundingBox.minPoint.x
        W = body.boundingBox.maxPoint.y - body.boundingBox.minPoint.y
        H  = body.boundingBox.maxPoint.z - body.boundingBox.minPoint.z
        maxPointZ = body.boundingBox.maxPoint.z
       # print(maxPointZ)
        
        for face in body.faces:
        # Check to see if the face is a plane.
            if face.geometry.objectType == adsk.core.Plane.classType():
                # Get the normal of the face.  This will always point out of the solid.
                faceEval = face.evaluator
                (retVal, normal) = faceEval.getNormalAtPoint(face.pointOnFace)

                # Check that the normal is pointing up.
                if normal.angleTo(upDir) < 0.001:
                     # Get construction planes
        
                    xyPlane = exportOcc.component.xYConstructionPlane
                    planes = exportOcc.component.constructionPlanes
                    planeInput = planes.createInput()
                                
                    # Add construction plane by offset
                    offsetValue = adsk.core.ValueInput.createByReal(maxPointZ)
                    planeInput.setByOffset(xyPlane, offsetValue)
                    planeOne = planes.add(planeInput)
                    
        return planeOne
   
        return "Length: " + str(L)+ " Width: " + str(W) + " Height: " + str(H)

    
