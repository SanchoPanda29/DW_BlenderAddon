import bpy
from bpy.props import StringProperty, FloatProperty, PointerProperty, IntProperty
from bpy.types import Operator, Panel, PropertyGroup
from bpy_extras.io_utils import ImportHelper

bl_info = {
    "name": "DrawningsMashine",
    "author": "AlexMelnyk",
    "description": "DrawningMashine addon",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}

# Define a Property Group to hold custom properties for the image
class ImageProperties(PropertyGroup):
    position_x: FloatProperty(
        name="Position X",
        description="Position X",
        default=0.0,
    )
    position_y: FloatProperty(
        name="Position Y",
        description="Position Y",
        default=0.0,
    )
    position_z: FloatProperty(
        name="Position Z",
        description="Position Z",
        default=0.0,
    )
    scale: FloatProperty(
        name="Scale",
        description="Scale of the image",
        default=1.0,
    )
    rotation: FloatProperty(
        name="Rotation",
        description="Rotation angle around Z axis in degrees",
        default=0.0,
    )
    width: IntProperty(
        name="Width",
        description="Width of the image",
        default=100,
        min=1
    )
    height: IntProperty(
        name="Height",
        description="Height of the image",
        default=100,
        min=1
    )

class LoadImage(bpy.types.Operator, ImportHelper):
    bl_idname = "object.load_image"
    bl_label = "Load Image"
    bl_description = "Load an image into the 3D Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".jpg;.jpeg;.png;.tga;.tiff;.bmp"

    filter_glob: StringProperty(
        default="*.jpg;*.jpeg;*.png;*.tga;*.tiff;.bmp",
        options={'HIDDEN'},
    )

    def execute(self, context):
        filepath = self.filepath
        self.load_image_to_viewport(context, filepath)
        return {'FINISHED'}

    def load_image_to_viewport(self, context, filepath):
        scene = context.scene
        image_props = scene.image_props

        # Load the image
        image = bpy.data.images.load(filepath)

        # Create an empty object with image
        bpy.ops.object.add(type='EMPTY', location=(image_props.position_x, image_props.position_y, image_props.position_z))
        empty = bpy.context.object
        empty.empty_display_type = 'IMAGE'
        empty.data = image

        # Apply rotation directly
        empty.rotation_euler[2] = image_props.rotation * (3.14159265 / 180.0)

        # Adjust the size of the empty object
        aspect_ratio = image.size[0] / image.size[1]
        empty.scale = (image_props.scale * aspect_ratio, image_props.scale, 1)

        # Adjust the image size using the width and height properties
        empty.scale = (image_props.width / 100, image_props.height / 100, 1)

class ResetImageProps(bpy.types.Operator):
    bl_idname = "object.reset_image_props"
    bl_label = "Reset Image Properties"
    bl_description = "Reset image properties to default values"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        image_props = scene.image_props

        # Reset properties to default values
        image_props.position_x = 0.0
        image_props.position_y = 0.0
        image_props.position_z = 0.0
        image_props.scale = 1.0
        image_props.rotation = 0.0
        image_props.width = 100
        image_props.height = 100

        return {'FINISHED'}
    
class RotateImageY(bpy.types.Operator):
    bl_idname = "object.rotate_image_y"
    bl_label = "Rotate Image"
    bl_description = "Rotate the active image"
    bl_options = {'REGISTER', 'UNDO'}

    rotation_angle: FloatProperty(
        name="Rotation Angle",
        description="Rotation angle in degrees",
        default=0.0,
    )

    def execute(self, context):
        image_props = context.scene.image_props
        image_props.rotation += self.rotation_angle
        if context.object:
            context.object.rotation_euler[2] = image_props.rotation * (3.14159265 / 180.0)
        elif context.object:
            context.object.rotation_euler[0] = image_props.rotation * (3.14159265 / 180.0)
        return {'FINISHED'}
    
class RotateImageX(bpy.types.Operator):
    bl_idname = "object.rotate_image_x"
    bl_label = "Rotate Image"
    bl_description = "Rotate the active image"
    bl_options = {'REGISTER', 'UNDO'}

    rotation_angle: FloatProperty(
        name="Rotation Angle",
        description="Rotation angle in degrees",
        default=0.0,
    )

    def execute(self, context):
        image_props = context.scene.image_props
        image_props.rotation += self.rotation_angle
        if context.object:
            context.object.rotation_euler[0] = image_props.rotation * (3.14159265 / 180.0)
        return {'FINISHED'}

class ImageViewportPanel(bpy.types.Panel):
    bl_label = "DrawHELPER_v1.0"
    bl_idname = "VIEW3D_PT_image_viewport_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DrawningsMashine'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        image_props = scene.image_props

        col = layout.column(align=True)
        row = col.row(align=True)
        
        
        
        
        row.scale_y = 2.0
        row.operator("object.load_image", text="Load Image")
        row.operator("object.reset_image_props", text="Reset Properties")
        
        row = col.row(align=True)
        row.label(text="Add drawings") 

        col.separator()
        col.label(text="Image Properties:")
        col.prop(image_props, "position_x", text="Position X")
        col.prop(image_props, "position_y", text="Position Y")
        col.prop(image_props, "position_z", text="Position Z")
        col.prop(image_props, "scale", text="Scale")
        
        col.separator()
        col.label(text="Rotations")
        row = col.row(align=True)
        row.operator("object.rotate_image_y", text="Rotate -90° Y").rotation_angle = -90
        row.operator("object.rotate_image_y", text="Rotate 90° Y").rotation_angle = 90
        row = col.row(align=True)
        row.operator("object.rotate_image_x", text="Rotate -90° X").rotation_angle = -90
        row.operator("object.rotate_image_x", text="Rotate 90° X").rotation_angle = 90

def register():
    bpy.utils.register_class(ImageProperties)
    bpy.utils.register_class(LoadImage)
    bpy.utils.register_class(ResetImageProps)
    bpy.utils.register_class(RotateImageX)
    bpy.utils.register_class(RotateImageY)
    bpy.utils.register_class(ImageViewportPanel)
    bpy.types.Scene.image_props = PointerProperty(type=ImageProperties)

def unregister():
    bpy.utils.unregister_class(ImageProperties)
    bpy.utils.unregister_class(LoadImage)
    bpy.utils.unregister_class(ResetImageProps)
    bpy.utils.register_class(RotateImageY)
    bpy.utils.register_class(RotateImageX)
    bpy.utils.unregister_class(ImageViewportPanel)
    del bpy.types.Scene.image_props

if __name__ == "__main__":
    register()
