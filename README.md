# collidergen
A robotics focused addon for Blender that creates collision geometry and SDF files.

## Installation
 - Download the addon: **[ColliderGen addon](https://github.com/cole-bsmr/collidergen/blob/main/collidergen.py)**
 - Go to Edit > Preferences > Addons then click the “Install” button in the upper right. Select the collidergen.py file that you downloaded. Collider Gen will now appear in your list of addons and you can activate by checking the box next to it.

## How to use

## Import
The import interface allows you to quickly access importers for commonly used file types as well as prepare the imported meshes for applying collision objects
#### STL/FBX/OBJ/DAE Importers
 - These simply give you access to importers for commonly used mesh file types. These are the same import tools used in default Blender.
#### Clear Hierarchy/Reset Scale
 - This tool performs some basic functions to clean up the imported meshes and ensures they work correctly with the rest of the collision generation tools. It first removes objects from any imported hierarchy and deletes the empty objects. It then resets all scale values which is important when Collider Gen is fitting objects to the imported geometry. It is highly recommended that this tool be used on all imported geometry.
#### Separate Parts
 - This tool identifies continuous geometry and separates those into separate meshes. This allows the user to have finer control over what collisions are placed where. If your imported geometry is already split into parts it’s not necessary to run this tool.
![](https://i.imgur.com/m6bmgMc.png)

## Create Options
The create options panel contains settings you can adjust to change the way the tools in the “Create” panel behave.
#### Per Object
 - This option determines whether an operation is applied to the selected objects as a whole or to each object individually. When toggled on the tool will loop through each object and apply a collision to each object in that selection. When toggled off the tool will create one collider that fits the entire selection of objects. This option only applies to the “Box” and “Sphere” tools in the “Create” interface.
![](https://i.imgur.com/xhE0KGM.png)
#### Minimal Box
 - This option determines whether a created collider box is aligned to the object’s local rotation or whether it is fit to the object in a way that creates the tightest fitting collision. When toggled off the box collider will use the object’s local rotation to align itself. When toggled on the box collider will be fit to the object in the way that creates the tightest fitting box.
![](https://i.imgur.com/vTnr4ON.png)

 - This tool is mainly used for when an object is box-like and at an angle but its rotational information has been reset so that instead of creating a box that aligns to the geometry it is being aligned to the world. The “Minimal Box” setting will allow the correct alignment of box collisions to these types of geometries.

## Create
#### Box
 - This tool creates a box shape that fits around the selected geometry.
#### Cylinder
 - This tool creates a cylinder shape that fits around the selected geometry. After selected this tool you’ll be required to select an axis. Pressing the the X, Y, or Z keys will create a cylinder object that aligns with that objects local X, Y, or Z axis. After choosing the axis that looks appropriate you can confirm your selection with the ENTER key or his ESC to cancel the operation. 
#### Sphere
 - This tool creates a sphere shape that fits around the selected geometry
#### Generate by Face
 - This tool is a more advanced option for creating collision shapes that allows you to create box and cylinder collision shapes around cylindrical and boxy features even if they aren’t separate parts.
 - To use this tool select an object and then press the “Generate by Face” button. You can then select a flat surface of the object. This surface will be the “end cap” of your collision shape. After confirming your surface the collision object will be extruded from that surface. The length of this extruded shape is determined automatically but may need to be adjusted after the shape is generated.
#### Mesh Collider
 - This tool creates a collision mesh as opposed to a simple shape. It creates a convex hull mesh that can then be simplified. Simply select an object and press the button to create the mesh. You will then see two new tools appear under the button.
![](https://i.imgur.com/IJpDfwR.png)
 - The Simplify and Inflate tools will appear any time a mesh collider is selected and these values can be adjusted at any time as long as the modifiers have not been applied.
#### - Simplify
 - This tool allows you to dynamically adjust the triangle count of the generated mesh.
#### - Inflate
 - As you lower the triangle count and the coarseness of the mesh increases you will notice that parts of the mesh will begin to extend outside the geometry of the collider. Use this tool to inflate the collision mesh until it fully encompasses the object.

## Transform
After generating colliders it is not uncommon for these colliders to need adjustment. This interface contains transformation tools to make those adjustments.

#### Scale Cage
 - This tool simply selects Blender’s built-in “Scale Cage” tool which is ideal for transforming collider shapes.
#### Snap
 - This tool turns on snapping and sets the snapping settings to snap to face. These settings are ideal when using “Scale Cage” to move collision geometry to the surfaces of its associated object.
#### Scale Radius
 - This tool will only be visible on when a “Cylinder” or “Sphere” collision shape is selected. It allows you to adjust the radius of the collision shape. Press the button and then move your mouse left and right to increase or decrease the radius of the collision shape.

## Export
This interface contains the tools needed to export your colliders. An SDF file will be created that contains the information for all collision shapes and will point to any mesh colliders as well. The geometry for these mesh colliders will be exported to STL format in the selected file directory.
#### File directory
 - Here you can select the folder in which to save the SDF files as well as the mesh files for any mesh colliders that were generated.
#### Export selected
 - This tool will export all selected colliders.
#### Export All
 - This tool will export all colliders contained in the “Colliders” collection regardless of what is selected.


