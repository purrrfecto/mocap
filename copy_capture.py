bl_info = {
    "name": "Copy Mocap to Armature",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

capture_to_mmd = {
"Head": "head", 
"Neck": "neck",
"Shoulder": "shoulder",
"Arm": "arm",
"Forearm": "elbow",
"Hand": "wrist",
"Torso": "master", # copy rotation and copy location
        # "Hip": "leg",
        # "Hip_R": "leg_R",
"Thigh": "leg",
"Leg": "knee",
"Foot": "ankle",
}
mmd_to_capture = {v: k for k, v in capture_to_mmd.items()}

class OBJECT_OT_CopyMocapToArm(bpy.types.Operator):
    """Copy mocap to armature"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.copy_mocap"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Copy Mocap"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    def execute(self, context):        # execute() is called when running the operator.

        # The original script start
        #context & scene for testing
        context = bpy.context
        scene = context.scene


        # other armature other bone
        armature_src = scene.objects.get("Capture Rig")
        armature_dst = scene.objects.get("Type3_Arm")
        
        if not armature_src or not armature_dst:
            print("armature does not exist")
            exit()
        if context.object.mode != 'POSE':
            print("swtich to pose mode first")
            bpy.ops.object.mode_set(mode='POSE')
            
        if armature_dst is not None:
            for bone in armature_dst.pose.bones:
#                bone.select=True
                target_bonename = ""
                if (bone.name == "master"):
                    print(bone.name)
                    target_bonename = mmd_to_capture[bone.name]
                    # copy rotation and location
                    crc = bone.constraints.new('COPY_LOCATION')
                    crc.target = armature_src
                    crc.subtarget = target_bonename     # note subtarget uses name not object.
                    crc = bone.constraints.new('COPY_ROTATION')
                    crc.target = armature_src
                    crc.subtarget = target_bonename     # note subtarget uses name not object.
                else: # copy rot only
                    if (bone.name.endswith("_L") or bone.name.endswith("_R")):
                        prefix = bone.name[:-2]
                        if (mmd_to_capture.get(prefix) == None):
                            continue
                        prefix = mmd_to_capture[prefix]
                        suffix = bone.name[-2:]
                        target_bonename = prefix + suffix
                    else:
                        if (mmd_to_capture.get(bone.name) == None):
                            continue
                        target_bonename = mmd_to_capture[bone.name]
                    crc = bone.constraints.new('COPY_ROTATION')
                    crc.target = armature_src
                    crc.subtarget = target_bonename
            
        # remove all constraint targeted to capture rig    
        #All copy loc constraints on pose bone bone will be [c for c in bone.constraints if c.type=='COPY_LOCATION']

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
        # The original script ends
        

class OBJECT_OT_RemoveMocapCopy(bpy.types.Operator):
    """remove mocap copy rot"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.remove_copy_mocap"        # Unique identifier for buttons and menu items to reference.
    bl_label = "remove Mocap"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    def execute(self, context):        # execute() is called when running the operator.
        # The original script start
        #context & scene for testing
        context = bpy.context
        scene = context.scene
        
        # other armature other bone
        armature_src = scene.objects.get("Capture Rig")
        armature_dst = scene.objects.get("Type3_Arm")
        
        if not armature_src or not armature_dst:
            print("armature does not exist")
            exit()
        if context.object.mode != 'POSE':
            print("swtich to pose mode first")
            bpy.ops.object.mode_set(mode='POSE')
            
        if armature_dst is not None:
            for bone in armature_dst.pose.bones:
                for crc in bone.constraints:
                    if crc.target == armature_src:
                        bone.constraints.remove(crc)
            
        # remove all constraint targeted to capture rig    
        #All copy loc constraints on pose bone bone will be [c for c in bone.constraints if c.type=='COPY_LOCATION']

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
        # The original script ends
        

classes = (OBJECT_OT_CopyMocapToArm,OBJECT_OT_RemoveMocapCopy,)
register, unregister = bpy.utils.register_classes_factory(classes)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
