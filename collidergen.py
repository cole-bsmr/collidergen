# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ColliderGen",
    "author" : "Cole Biesemeyer", 
    "description" : "Creates collision geometry and simple shapes for use in robotics simulators.",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location" : "Editors -> ColliderGen",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import mathutils
import math
import bmesh
import numpy as np
from bpy.app.handlers import persistent
import blf
import os
from mathutils import Vector


addon_keymaps = {}
_icons = None
collider = {'sna_ray_origin_global': None, 'sna_cylindercapobj': None, 'sna_activeobject': None, 'sna_selection': None, 'sna_collidername': None, 'sna_activeobjectcollider': None, 'sna_userscollection': None, 'sna_moveoutcollection': None, 'sna_collidercollectionexists': False, 'sna_minbb': None, 'sna_joinedobj': None, 'sna_minboxname': '', 'sna_isincolliders': False, }
cylinder = {'sna_actobjcylgen': '', 'sna_cylsource': None, 'sna_cylusercollection': None, 'sna_colliderscollectionexists': False, }
export_colliders = {'sna_location_x': '', 'sna_selobjforexp': None, }
genface = {'sna_genfaceactobj': None, 'sna_rayfail': False, }
genmesh = {'sna_collidercollection': None, 'sna_incolliderscollection': False, 'sna_colliderscollectionexist': False, }
visual_scripting_editor = {'sna_collidercollection': None, }


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class SNA_OT_Box_9D9E4(bpy.types.Operator):
    bl_idname = "sna.box_9d9e4"
    bl_label = "Box"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_perobj:
            collider['sna_selection'] = bpy.context.selected_objects
            for i_5C24E in range(len(collider['sna_selection'])-1,-1,-1):
                exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
                bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
                bpy.ops.mesh.primitive_cube_add('INVOKE_DEFAULT', location=collider['sna_selection'][i_5C24E].location, rotation=collider['sna_selection'][i_5C24E].rotation_euler, scale=tuple(mathutils.Vector(collider['sna_selection'][i_5C24E].dimensions) / 2.0))
                bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
        else:
            exec('bpy.ops.object.duplicate()')
            exec('bpy.ops.object.join()')
            print(str(bpy.context.view_layer.objects.active))
            collider['sna_joinedobj'] = bpy.context.view_layer.objects.active
            for i_0C6CA in range(len(bpy.context.view_layer.objects.selected)):
                exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
                bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
                print(bpy.context.view_layer.objects.active.name)
                bpy.ops.mesh.primitive_cube_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.selected[i_0C6CA].location, rotation=bpy.context.view_layer.objects.selected[i_0C6CA].rotation_euler, scale=tuple(mathutils.Vector(bpy.context.view_layer.objects.selected[i_0C6CA].dimensions) / 2.0))
                bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
                bpy.data.objects.remove(object=collider['sna_joinedobj'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_CREATE_D9148(bpy.types.Panel):
    bl_label = 'Create'
    bl_idname = 'SNA_PT_CREATE_D9148'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Collider Gen'
    bl_order = 2
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_700F2 = layout.column(heading='', align=False)
        col_700F2.alert = False
        col_700F2.enabled = True
        col_700F2.active = True
        col_700F2.use_property_split = False
        col_700F2.use_property_decorate = False
        col_700F2.scale_x = 1.0
        col_700F2.scale_y = 1.0
        col_700F2.alignment = 'Expand'.upper()
        col_700F2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if bpy.context.scene.sna_minbox:
            op = col_700F2.operator('sna.minbox_0936b', text='Box', icon_value=0, emboss=True, depress=False)
        else:
            op = col_700F2.operator('sna.box_9d9e4', text='Box', icon_value=0, emboss=True, depress=False)
        op = col_700F2.operator('sna.cylinder_050b8', text='Cylinder', icon_value=0, emboss=True, depress=False)
        op = col_700F2.operator('sna.sphere_f5cd9', text='Sphere', icon_value=0, emboss=True, depress=False)
        row_90E90 = layout.row(heading='', align=False)
        row_90E90.alert = False
        row_90E90.enabled = True
        row_90E90.active = True
        row_90E90.use_property_split = False
        row_90E90.use_property_decorate = False
        row_90E90.scale_x = 1.0
        row_90E90.scale_y = 1.0
        row_90E90.alignment = 'Expand'.upper()
        row_90E90.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = layout.operator('sna.selectflatfaces_0bf7c', text='Generate by Face', icon_value=0, emboss=True, depress=False)
        row_F586A = layout.row(heading='', align=False)
        row_F586A.alert = False
        row_F586A.enabled = True
        row_F586A.active = True
        row_F586A.use_property_split = False
        row_F586A.use_property_decorate = False
        row_F586A.scale_x = 1.0
        row_F586A.scale_y = 1.0
        row_F586A.alignment = 'Expand'.upper()
        row_F586A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = layout.operator('sna.mesh_85d40', text='Mesh Collider', icon_value=0, emboss=True, depress=False)
        box_55536 = layout.box()
        box_55536.alert = False
        box_55536.enabled = True
        box_55536.active = True
        box_55536.use_property_split = False
        box_55536.use_property_decorate = False
        box_55536.alignment = 'Expand'.upper()
        box_55536.scale_x = 1.0
        box_55536.scale_y = 1.0
        if not True: box_55536.operator_context = "EXEC_DEFAULT"
        row_6C90F = box_55536.row(heading='', align=False)
        row_6C90F.alert = False
        row_6C90F.enabled = True
        row_6C90F.active = True
        row_6C90F.use_property_split = False
        row_6C90F.use_property_decorate = False
        row_6C90F.scale_x = 1.0
        row_6C90F.scale_y = 1.0
        row_6C90F.alignment = 'Expand'.upper()
        row_6C90F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'Decimate' in bpy.context.view_layer.objects.active.modifiers):
            row_6C90F.prop(bpy.context.view_layer.objects.active.modifiers['Decimate'], 'ratio', text='Simplify', icon_value=0, emboss=True)
        row_40A46 = box_55536.row(heading='', align=False)
        row_40A46.alert = False
        row_40A46.enabled = True
        row_40A46.active = True
        row_40A46.use_property_split = False
        row_40A46.use_property_decorate = False
        row_40A46.scale_x = 1.0
        row_40A46.scale_y = 1.0
        row_40A46.alignment = 'Expand'.upper()
        row_40A46.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (property_exists("bpy.context.view_layer.objects.active.modifiers", globals(), locals()) and 'Solidify' in bpy.context.view_layer.objects.active.modifiers):
            row_40A46.prop(bpy.context.view_layer.objects.active.modifiers['Solidify'], 'thickness', text='Inflate', icon_value=0, emboss=True)


class SNA_PT_TRANSFORM_30201(bpy.types.Panel):
    bl_label = 'Transform'
    bl_idname = 'SNA_PT_TRANSFORM_30201'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Collider Gen'
    bl_order = 3
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        split_61591 = layout.split(factor=0.7988929748535156, align=False)
        split_61591.alert = False
        split_61591.enabled = True
        split_61591.active = True
        split_61591.use_property_split = False
        split_61591.use_property_decorate = False
        split_61591.scale_x = 1.0
        split_61591.scale_y = 1.0
        split_61591.alignment = 'Expand'.upper()
        if not True: split_61591.operator_context = "EXEC_DEFAULT"
        op = split_61591.operator('sna.scale_cage_4e08e', text='Scale Cage', icon_value=0, emboss=True, depress=False)
        split_61591.prop(bpy.data.scenes['Scene'].tool_settings, 'use_snap', text='', icon_value=577, emboss=True, toggle=bpy.data.scenes['Scene'].tool_settings.use_snap)
        if (bpy.context.view_layer.objects.active == None):
            pass
        else:
            if 'Cylinder' in bpy.context.view_layer.objects.active.name:
                op = layout.operator('sna.scalecylradius_e1610', text='Scale Radius', icon_value=0, emboss=True, depress=False)
        if (bpy.context.view_layer.objects.active == None):
            pass
        else:
            if 'Sphere' in bpy.context.view_layer.objects.active.name:
                op = layout.operator('sna.scalesphereradius_bd79d', text='Scale Radius', icon_value=0, emboss=True, depress=False)


class SNA_OT_Scale_Cage_4E08E(bpy.types.Operator):
    bl_idname = "sna.scale_cage_4e08e"
    bl_label = "Scale Cage"
    bl_description = "Sets the current tool to Select Cage"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        exec("bpy.context.scene.tool_settings.snap_elements_base = {'FACE'}")
        bpy.data.scenes['Scene'].tool_settings.use_snap_scale = True
        bpy.data.scenes['Scene'].tool_settings.use_snap_translate = True
        bpy.data.scenes['Scene'].transform_orientation_slots[0].type = 'LOCAL'
        bpy.ops.wm.tool_set_by_id('INVOKE_DEFAULT', name='builtin.scale_cage')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_EXPORT_420D3(bpy.types.Panel):
    bl_label = 'Export'
    bl_idname = 'SNA_PT_EXPORT_420D3'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Collider Gen'
    bl_order = 4
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene, 'sna_filepath', text='', icon_value=0, emboss=True)
        op = layout.operator('sna.export_selected_9f890', text='Export Selected', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.export_all_451dc', text='Export All', icon_value=0, emboss=True, depress=False)


class SNA_OT_Scalecylradius_E1610(bpy.types.Operator):
    bl_idname = "sna.scalecylradius_e1610"
    bl_label = "ScaleCylRadius"
    bl_description = "Increases the radius of the cylinder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.transform.resize('INVOKE_DEFAULT', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(True, True, False))
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Scalesphereradius_Bd79D(bpy.types.Operator):
    bl_idname = "sna.scalesphereradius_bd79d"
    bl_label = "ScaleSphereRadius"
    bl_description = "Increases the radius of the sphere"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.transform.resize('INVOKE_DEFAULT', orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(True, True, True))
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_CREATE_OPTIONS_F211B(bpy.types.Panel):
    bl_label = 'Create Options'
    bl_idname = 'SNA_PT_CREATE_OPTIONS_F211B'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Collider Gen'
    bl_order = 1
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        split_90272 = layout.split(factor=0.5, align=False)
        split_90272.alert = False
        split_90272.enabled = True
        split_90272.active = True
        split_90272.use_property_split = False
        split_90272.use_property_decorate = False
        split_90272.scale_x = 1.0
        split_90272.scale_y = 1.0
        split_90272.alignment = 'Expand'.upper()
        if not True: split_90272.operator_context = "EXEC_DEFAULT"
        split_90272.prop(bpy.context.scene, 'sna_perobj', text='Per Object', icon_value=0, emboss=True, toggle=bpy.context.scene.sna_perobj)
        split_90272.prop(bpy.context.scene, 'sna_minbox', text='Minimal Box', icon_value=0, emboss=True, toggle=bpy.context.scene.sna_minbox)


class SNA_MT_5CC5F(bpy.types.Menu):
    bl_idname = "SNA_MT_5CC5F"
    bl_label = "Menu"

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        layout = self.layout.column_flow(columns=1)
        layout.operator_context = "INVOKE_DEFAULT"
        layout.label(text='My Label', icon_value=0)


class SNA_MT_4968B(bpy.types.Menu):
    bl_idname = "SNA_MT_4968B"
    bl_label = "Create"

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        layout = self.layout.menu_pie()
        box_961B2 = layout.box()
        box_961B2.alert = False
        box_961B2.enabled = True
        box_961B2.active = True
        box_961B2.use_property_split = False
        box_961B2.use_property_decorate = False
        box_961B2.alignment = 'Expand'.upper()
        box_961B2.scale_x = 1.0
        box_961B2.scale_y = 1.0
        if not True: box_961B2.operator_context = "EXEC_DEFAULT"
        box_961B2.label(text='Generate by Face', icon_value=0)
        op = box_961B2.operator('sna.cylindercap_0f9d8', text='Cylinder', icon_value=0, emboss=True, depress=False)
        op = box_961B2.operator('sna.boxcap_7899e', text='Box', icon_value=0, emboss=True, depress=False)
        box_1BCEE = layout.box()
        box_1BCEE.alert = False
        box_1BCEE.enabled = True
        box_1BCEE.active = True
        box_1BCEE.use_property_split = False
        box_1BCEE.use_property_decorate = False
        box_1BCEE.alignment = 'Expand'.upper()
        box_1BCEE.scale_x = 1.0
        box_1BCEE.scale_y = 1.0
        if not True: box_1BCEE.operator_context = "EXEC_DEFAULT"
        op = box_1BCEE.operator('sna.scale_cage_4e08e', text='Scale Cage', icon_value=0, emboss=True, depress=False)
        box_1BCEE.prop(bpy.data.scenes['Scene'].tool_settings, 'use_snap', text='', icon_value=577, emboss=True, toggle=bpy.data.scenes['Scene'].tool_settings.use_snap)
        split_A7304 = layout.split(factor=0.5, align=False)
        split_A7304.alert = False
        split_A7304.enabled = True
        split_A7304.active = True
        split_A7304.use_property_split = False
        split_A7304.use_property_decorate = False
        split_A7304.scale_x = 1.0
        split_A7304.scale_y = 1.0
        split_A7304.alignment = 'Expand'.upper()
        if not True: split_A7304.operator_context = "EXEC_DEFAULT"
        split_A7304.prop(bpy.context.scene, 'sna_perobj', text='Per Object', icon_value=0, emboss=True, toggle=bpy.context.scene.sna_perobj)
        split_A7304.prop(bpy.context.scene, 'sna_minbox', text='Minimal Box', icon_value=0, emboss=True, toggle=bpy.context.scene.sna_minbox)
        box_E3D95 = layout.box()
        box_E3D95.alert = False
        box_E3D95.enabled = True
        box_E3D95.active = True
        box_E3D95.use_property_split = False
        box_E3D95.use_property_decorate = False
        box_E3D95.alignment = 'Expand'.upper()
        box_E3D95.scale_x = 1.0
        box_E3D95.scale_y = 1.0
        if not True: box_E3D95.operator_context = "EXEC_DEFAULT"
        box_E3D95.label(text='Create', icon_value=0)
        row_E1C20 = box_E3D95.row(heading='', align=False)
        row_E1C20.alert = False
        row_E1C20.enabled = True
        row_E1C20.active = True
        row_E1C20.use_property_split = False
        row_E1C20.use_property_decorate = False
        row_E1C20.scale_x = 1.0
        row_E1C20.scale_y = 1.0
        row_E1C20.alignment = 'Expand'.upper()
        row_E1C20.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_E1C20.operator('sna.box_9d9e4', text='Box', icon_value=0, emboss=True, depress=False)
        op = row_E1C20.operator('sna.cylinder_050b8', text='Cylinder', icon_value=0, emboss=True, depress=False)
        op = row_E1C20.operator('sna.sphere_f5cd9', text='Sphere', icon_value=0, emboss=True, depress=False)


class SNA_OT_Select_Cylinder_Face_8A190(bpy.types.Operator):
    bl_idname = "sna.select_cylinder_face_8a190"
    bl_label = "Select cylinder face"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        bpy.ops.mesh.select_mode('INVOKE_DEFAULT', type='FACE')
        bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='DESELECT')
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        bpy.context.view_layer.objects.active.data.polygons[33].select = True
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        bpy.ops.wm.tool_set_by_id('INVOKE_DEFAULT', name='builtin.move')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Minbox_0936B(bpy.types.Operator):
    bl_idname = "sna.minbox_0936b"
    bl_label = "MinBox"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        collider['sna_minboxname'] = bpy.context.view_layer.objects.active.name
        if bpy.context.scene.sna_perobj:
            for i_88F10 in range(len(bpy.context.view_layer.objects.selected)):
                MinBB = bpy.context.view_layer.objects.selected[i_88F10]
                from timeit import default_timer as timer
                #import bpy
                from mathutils import Matrix
                DEBUG = False
                CUBE_FACE_INDICES = (
                    (0, 1, 3, 2),
                    (2, 3, 7, 6),
                    (6, 7, 5, 4),
                    (4, 5, 1, 0),
                    (2, 6, 4, 0),
                    (7, 3, 1, 5),
                )

                def gen_cube_verts():
                    for x in range(-1, 2, 2):
                        for y in range(-1, 2, 2):
                            for z in range(-1, 2, 2):
                                yield x, y, z

                def rotating_calipers(hull_points: np.ndarray, bases):
                    min_bb_basis = None
                    min_bb_min = None
                    min_bb_max = None
                    min_vol = math.inf
                    for basis in bases:
                        rot_points = hull_points.dot(np.linalg.inv(basis))
                        # Equivalent to: rot_points = hull_points.dot(np.linalg.inv(np.transpose(basis)).T)
                        bb_min = rot_points.min(axis=0)
                        bb_max = rot_points.max(axis=0)
                        volume = (bb_max - bb_min).prod()
                        if volume < min_vol:
                            min_bb_basis = basis
                            min_vol = volume
                            min_bb_min = bb_min
                            min_bb_max = bb_max
                    return np.array(min_bb_basis), min_bb_max, min_bb_min

                def obj_rotating_calipers(obj):
                    bm = bmesh.new()
                    dg = bpy.context.evaluated_depsgraph_get()
                    bm.from_object(obj, dg)
                    t0 = timer()
                    chull_out = bmesh.ops.convex_hull(bm, input=bm.verts, use_existing_faces=False)
                    t1 = timer()
                    print(f"Convex-Hull calculated in {t1-t0} sec")
                    chull_geom = chull_out["geom"]
                    chull_points = np.array([bmelem.co for bmelem in chull_geom if isinstance(bmelem, bmesh.types.BMVert)])
                    # Create object from Convex-Hull (for debugging)
                    if DEBUG:
                        t0 = timer()
                        for face in set(bm.faces) - set(chull_geom):
                            bm.faces.remove(face)
                        for edge in set(bm.edges) - set(chull_geom):
                            bm.edges.remove(edge)
                        t1 = timer()
                        print(f"Deleted non Convex-Hull edges and faces in {t1 - t0} sec")
                        chull_mesh = bpy.data.meshes.new(obj.name + "_convex_hull")
                        chull_mesh.validate()
                        bm.to_mesh(chull_mesh)
                        chull_obj = bpy.data.objects.new(chull_mesh.name, chull_mesh)
                        chull_obj.matrix_world = obj.matrix_world
                        bpy.context.scene.collection.objects.link(chull_obj)
                    bases = []
                    t0 = timer()
                    for elem in chull_geom:
                        if not isinstance(elem, bmesh.types.BMFace):
                            continue
                        if len(elem.verts) != 3:
                            continue
                        face_normal = elem.normal
                        if np.allclose(face_normal, 0, atol=0.00001):
                            continue
                        for e in elem.edges:
                            v0, v1 = e.verts
                            edge_vec = (v0.co - v1.co).normalized()
                            co_tangent = face_normal.cross(edge_vec)
                            basis = (edge_vec, co_tangent, face_normal)
                            bases.append(basis)
                    t1 = timer()
                    print(f"List of bases built in {t1-t0} sec")
                    t0 = timer()
                    bb_basis, bb_max, bb_min = rotating_calipers(chull_points, bases)
                    t1 = timer()
                    print(f"Rotating Calipers finished in {t1-t0} sec")
                    bm.free()
                    bb_basis_mat = bb_basis.T
                    bb_dim = bb_max - bb_min
                    bb_center = (bb_max + bb_min) / 2
                    mat = Matrix.Translation(bb_center.dot(bb_basis)) @ Matrix(bb_basis_mat).to_4x4() @ Matrix(np.identity(3) * bb_dim / 2).to_4x4()
                    bb_mesh = bpy.data.meshes.new(obj.name + "_minimum_bounding_box")
                    bb_mesh.from_pydata(vertices=list(gen_cube_verts()), edges=[], faces=CUBE_FACE_INDICES)
                    bb_mesh.validate()
                    #bb_mesh.transform(mat)
                    bb_mesh.update()
                    bb_obj = bpy.data.objects.new(bb_mesh.name, bb_mesh)
                    bb_obj.matrix_world = obj.matrix_world @ mat
                    bpy.context.scene.collection.objects.link(bb_obj)
                    bpy.context.view_layer.objects.active = bb_obj
                    #bb_obj.select_set(True)
                    #MinBB.select_set(False)
                #MinBB = bpy.context.object
                obj_rotating_calipers(MinBB)
                #print(str(bb_obj))
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
                bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
                collider['sna_moveoutcollection'] = bpy.context.collection
                collider['sna_activeobjectcollider'] = bpy.context.view_layer.objects.active
                bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
                bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
                bpy.context.active_object.select_set(state=True, )
                bpy.context.view_layer.objects.active.name = collider['sna_minboxname'] + '_Cube'
        else:
            bpy.ops.object.duplicate('INVOKE_DEFAULT', )
            bpy.ops.object.join('INVOKE_DEFAULT', )
            collider['sna_joinedobj'] = bpy.context.view_layer.objects.active
            MinBB = bpy.context.view_layer.objects.active
            from timeit import default_timer as timer
            #import bpy
            from mathutils import Matrix
            DEBUG = False
            CUBE_FACE_INDICES = (
                (0, 1, 3, 2),
                (2, 3, 7, 6),
                (6, 7, 5, 4),
                (4, 5, 1, 0),
                (2, 6, 4, 0),
                (7, 3, 1, 5),
            )

            def gen_cube_verts():
                for x in range(-1, 2, 2):
                    for y in range(-1, 2, 2):
                        for z in range(-1, 2, 2):
                            yield x, y, z

            def rotating_calipers(hull_points: np.ndarray, bases):
                min_bb_basis = None
                min_bb_min = None
                min_bb_max = None
                min_vol = math.inf
                for basis in bases:
                    rot_points = hull_points.dot(np.linalg.inv(basis))
                    # Equivalent to: rot_points = hull_points.dot(np.linalg.inv(np.transpose(basis)).T)
                    bb_min = rot_points.min(axis=0)
                    bb_max = rot_points.max(axis=0)
                    volume = (bb_max - bb_min).prod()
                    if volume < min_vol:
                        min_bb_basis = basis
                        min_vol = volume
                        min_bb_min = bb_min
                        min_bb_max = bb_max
                return np.array(min_bb_basis), min_bb_max, min_bb_min

            def obj_rotating_calipers(obj):
                bm = bmesh.new()
                dg = bpy.context.evaluated_depsgraph_get()
                bm.from_object(obj, dg)
                t0 = timer()
                chull_out = bmesh.ops.convex_hull(bm, input=bm.verts, use_existing_faces=False)
                t1 = timer()
                print(f"Convex-Hull calculated in {t1-t0} sec")
                chull_geom = chull_out["geom"]
                chull_points = np.array([bmelem.co for bmelem in chull_geom if isinstance(bmelem, bmesh.types.BMVert)])
                # Create object from Convex-Hull (for debugging)
                if DEBUG:
                    t0 = timer()
                    for face in set(bm.faces) - set(chull_geom):
                        bm.faces.remove(face)
                    for edge in set(bm.edges) - set(chull_geom):
                        bm.edges.remove(edge)
                    t1 = timer()
                    print(f"Deleted non Convex-Hull edges and faces in {t1 - t0} sec")
                    chull_mesh = bpy.data.meshes.new(obj.name + "_convex_hull")
                    chull_mesh.validate()
                    bm.to_mesh(chull_mesh)
                    chull_obj = bpy.data.objects.new(chull_mesh.name, chull_mesh)
                    chull_obj.matrix_world = obj.matrix_world
                    bpy.context.scene.collection.objects.link(chull_obj)
                bases = []
                t0 = timer()
                for elem in chull_geom:
                    if not isinstance(elem, bmesh.types.BMFace):
                        continue
                    if len(elem.verts) != 3:
                        continue
                    face_normal = elem.normal
                    if np.allclose(face_normal, 0, atol=0.00001):
                        continue
                    for e in elem.edges:
                        v0, v1 = e.verts
                        edge_vec = (v0.co - v1.co).normalized()
                        co_tangent = face_normal.cross(edge_vec)
                        basis = (edge_vec, co_tangent, face_normal)
                        bases.append(basis)
                t1 = timer()
                print(f"List of bases built in {t1-t0} sec")
                t0 = timer()
                bb_basis, bb_max, bb_min = rotating_calipers(chull_points, bases)
                t1 = timer()
                print(f"Rotating Calipers finished in {t1-t0} sec")
                bm.free()
                bb_basis_mat = bb_basis.T
                bb_dim = bb_max - bb_min
                bb_center = (bb_max + bb_min) / 2
                mat = Matrix.Translation(bb_center.dot(bb_basis)) @ Matrix(bb_basis_mat).to_4x4() @ Matrix(np.identity(3) * bb_dim / 2).to_4x4()
                bb_mesh = bpy.data.meshes.new(obj.name + "_minimum_bounding_box")
                bb_mesh.from_pydata(vertices=list(gen_cube_verts()), edges=[], faces=CUBE_FACE_INDICES)
                bb_mesh.validate()
                #bb_mesh.transform(mat)
                bb_mesh.update()
                bb_obj = bpy.data.objects.new(bb_mesh.name, bb_mesh)
                bb_obj.matrix_world = obj.matrix_world @ mat
                bpy.context.scene.collection.objects.link(bb_obj)
                bpy.context.view_layer.objects.active = bb_obj
                #bb_obj.select_set(True)
                #MinBB.select_set(False)
            #MinBB = bpy.context.object
            obj_rotating_calipers(MinBB)
            #print(str(bb_obj))
            bpy.data.objects.remove(object=collider['sna_joinedobj'], )
            bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
            bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
            collider['sna_moveoutcollection'] = bpy.context.collection
            collider['sna_activeobjectcollider'] = bpy.context.view_layer.objects.active
            bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
            bpy.context.active_object.select_set(state=True, )
            bpy.context.view_layer.objects.active.name = collider['sna_minboxname'] + '_Cube'
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


@persistent
def load_post_handler_A55A1(dummy):
    pass


class SNA_OT_Set_Active_Collection_50942(bpy.types.Operator):
    bl_idname = "sna.set_active_collection_50942"
    bl_label = "Set Active Collection"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.scene.collection.children", globals(), locals()) and 'Colliders' in bpy.context.scene.collection.children):
            pass
        else:
            bpy.ops.collection.create('INVOKE_DEFAULT', name='Colliders')
            bpy.data.scenes['Scene'].collection.children.link(child=bpy.data.collections['Colliders'], )
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                # Access the 3D Viewport's shading settings
                space_3d = area.spaces.active
                if space_3d:
                    # Set the viewport shading color type to 'OBJECT'
                    space_3d.shading.color_type = 'OBJECT'
                    print("Viewport shading color type set to 'OBJECT'")
        print("Script could not find an active 3D Viewport.")
        bpy.data.collections['Colliders'].objects.link(object=bpy.context.view_layer.objects.active, )
        for i_BC317 in range(len(bpy.data.collections)):
            if False:
                None.objects.unlink(object=bpy.context.view_layer.objects.active, )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Set_Collider_Material_33Bff(bpy.types.Operator):
    bl_idname = "sna.set_collider_material_33bff"
    bl_label = "Set Collider Material"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.show_wire = True
        bpy.context.view_layer.objects.active.color = (1.0, 0.0, 1.0, 0.5)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Move_To_Colllder_Collection_1Fa60(bpy.types.Operator):
    bl_idname = "sna.move_to_colllder_collection_1fa60"
    bl_label = "Move to Colllder collection"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.scene.collection.children", globals(), locals()) and 'Colliders' in bpy.context.scene.collection.children):
            pass
        else:
            bpy.ops.collection.create('INVOKE_DEFAULT', name='Colliders')
            bpy.data.scenes['Scene'].collection.children.link(child=bpy.data.collections['Colliders'], )
        collider['sna_isincolliders'] = False
        if False:
            pass
        collider['sna_userscollection'] = bpy.context.view_layer.objects.active.users_collection
        for i_CC8AD in range(len(collider['sna_userscollection'])):
            if 'Colliders' in collider['sna_userscollection'][i_CC8AD].name:
                collider['sna_isincolliders'] = True
        if collider['sna_isincolliders']:
            pass
        else:
            bpy.data.collections['Colliders'].objects.link(object=bpy.context.view_layer.objects.active, )
        for i_0A612 in range(len(collider['sna_userscollection'])):
            if (collider['sna_userscollection'][i_0A612].name == 'Colliders'):
                pass
            else:
                collider['sna_userscollection'][i_0A612].objects.unlink(object=bpy.context.view_layer.objects.active, )
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        # Access the 3D Viewport's shading settings
                        space_3d = area.spaces.active
                        if space_3d:
                            # Set the viewport shading color type to 'OBJECT'
                            space_3d.shading.color_type = 'OBJECT'
                            print("Viewport shading color type set to 'OBJECT'")
                print("Script could not find an active 3D Viewport.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Cylinder_Z_83F4C(bpy.types.Operator):
    bl_idname = "sna.cylinder_z_83f4c"
    bl_label = "Cylinder Z"
    bl_description = "Cylinder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.scene.collection.children", globals(), locals()) and 'Colliders' in bpy.context.scene.collection.children):
            cylinder['sna_colliderscollectionexists'] = True
        else:
            cylinder['sna_colliderscollectionexists'] = False
        cylinder['sna_cylusercollection'] = bpy.context.view_layer.objects.active.users_collection
        cylinder['sna_cylsource'] = bpy.context.view_layer.objects.active
        for i_6E2BC in range(len(bpy.context.view_layer.objects.selected)):
            exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
            bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
            if (tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]):
                bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2]))
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
            else:
                bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2]))
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Cylinder_X_3A040(bpy.types.Operator):
    bl_idname = "sna.cylinder_x_3a040"
    bl_label = "Cylinder X"
    bl_description = "Cylinder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.scene.collection.children", globals(), locals()) and 'Colliders' in bpy.context.scene.collection.children):
            cylinder['sna_colliderscollectionexists'] = True
        else:
            cylinder['sna_colliderscollectionexists'] = False
        cylinder['sna_cylsource'] = bpy.context.view_layer.objects.active
        for i_315C7 in range(len(bpy.context.view_layer.objects.selected)):
            exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
            bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
            if (tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]):
                bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0]))
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
                exec("bpy.ops.transform.rotate(value=1.57, orient_axis='Y', orient_type='LOCAL')")
            else:
                bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0]))
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
                exec("bpy.ops.transform.rotate(value=1.57, orient_axis='Y', orient_type='LOCAL')")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Cylinder_Y_F23B4(bpy.types.Operator):
    bl_idname = "sna.cylinder_y_f23b4"
    bl_label = "Cylinder Y"
    bl_description = "Cylinder"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if (property_exists("bpy.context.scene.collection.children", globals(), locals()) and 'Colliders' in bpy.context.scene.collection.children):
            cylinder['sna_colliderscollectionexists'] = True
        else:
            cylinder['sna_colliderscollectionexists'] = False
        cylinder['sna_cylsource'] = bpy.context.view_layer.objects.active
        for i_4D876 in range(len(bpy.context.view_layer.objects.selected)):
            exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
            bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
            if (tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]):
                bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]))
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
                exec("bpy.ops.transform.rotate(value=1.57, orient_axis='X', orient_type='LOCAL')")
            else:
                bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]))
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
                exec("bpy.ops.transform.rotate(value=1.57, orient_axis='X', orient_type='LOCAL')")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


_050B8_running = False
class SNA_OT_Cylinder_050B8(bpy.types.Operator):
    bl_idname = "sna.cylinder_050b8"
    bl_label = "Cylinder"
    bl_description = "Creates a cylinder collider that fits selected cylindrical shaped objects. Choose your alignment axis in the subsequent menu"
    bl_options = {"REGISTER", "UNDO"}
    cursor = "CROSSHAIR"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        if not True or context.area.spaces[0].bl_rna.identifier == 'SpaceView3D':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_F73DC, y_F73DC = (100.0, 600.0)
                    blf.position(font_id, x_F73DC, y_F73DC, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 5000:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 5000)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[X] Cylinder along X axis')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_0ADD1, y_0ADD1 = tuple(mathutils.Vector((100.0, 600.0)) - mathutils.Vector((0.0, 80.0)))
                    blf.position(font_id, x_0ADD1, y_0ADD1, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 5000:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 5000)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[Y] Cylinder along Y axis')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_0CD0E, y_0CD0E = tuple(mathutils.Vector(tuple(mathutils.Vector((100.0, 600.0)) - mathutils.Vector((0.0, 80.0)))) - mathutils.Vector((0.0, 80.0)))
                    blf.position(font_id, x_0CD0E, y_0CD0E, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 5000:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 5000)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[Z] Cylinder along Z axis')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_E459D, y_E459D = tuple(mathutils.Vector(tuple(mathutils.Vector(tuple(mathutils.Vector((100.0, 600.0)) - mathutils.Vector((0.0, 80.0)))) - mathutils.Vector((0.0, 80.0)))) - mathutils.Vector((0.0, 80.0)))
                    blf.position(font_id, x_E459D, y_E459D, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 5000:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 5000)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[ESC] Cancel')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_BD0B8, y_BD0B8 = tuple(mathutils.Vector(tuple(mathutils.Vector(tuple(mathutils.Vector(tuple(mathutils.Vector((100.0, 600.0)) - mathutils.Vector((0.0, 80.0)))) - mathutils.Vector((0.0, 80.0)))) - mathutils.Vector((0.0, 80.0)))) - mathutils.Vector((0.0, 80.0)))
                    blf.position(font_id, x_BD0B8, y_BD0B8, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 5000:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 5000)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[Space] Confirm')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
            except Exception as error:
                print(error)

    def execute(self, context):
        global _050B8_running
        _050B8_running = False
        context.window.cursor_set("DEFAULT")
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _050B8_running
        if not context.area or not _050B8_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.area.tag_redraw()
        context.window.cursor_set('CROSSHAIR')
        try:
            if (event.type == 'X' and event.value == 'PRESS' and event.alt == False and event.shift == False and event.ctrl == False):
                print('1')
                if (bpy.context.view_layer.objects.active.name == cylinder['sna_actobjcylgen']):
                    print('1')
                    bpy.ops.sna.cylinder_x_3a040('INVOKE_DEFAULT', )
                else:
                    bpy.ops.object.delete('INVOKE_DEFAULT', confirm=False)
                    bpy.data.objects[cylinder['sna_actobjcylgen']].select_set(state=True, )
                    bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.selected[cylinder['sna_actobjcylgen']]
                    bpy.ops.sna.cylinder_x_3a040('INVOKE_DEFAULT', )
            else:
                print('2')
                if (event.type == 'Y' and event.value == 'PRESS' and event.alt == False and event.shift == False and event.ctrl == False):
                    if (bpy.context.view_layer.objects.active.name == cylinder['sna_actobjcylgen']):
                        bpy.ops.sna.cylinder_x_3a040('INVOKE_DEFAULT', )
                    else:
                        bpy.ops.object.delete('INVOKE_DEFAULT', confirm=False)
                        bpy.data.objects[cylinder['sna_actobjcylgen']].select_set(state=True, )
                        bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.selected[cylinder['sna_actobjcylgen']]
                        bpy.ops.sna.cylinder_y_f23b4('INVOKE_DEFAULT', )
                if (event.type == 'Z' and event.value == 'PRESS' and event.alt == False and event.shift == False and event.ctrl == False):
                    if (bpy.context.view_layer.objects.active.name == cylinder['sna_actobjcylgen']):
                        bpy.ops.sna.cylinder_z_83f4c('INVOKE_DEFAULT', )
                    else:
                        bpy.ops.object.delete('INVOKE_DEFAULT', confirm=False)
                        bpy.data.objects[cylinder['sna_actobjcylgen']].select_set(state=True, )
                        bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.selected[cylinder['sna_actobjcylgen']]
                        bpy.ops.sna.cylinder_z_83f4c('INVOKE_DEFAULT', )
                if (event.type == 'ESC' and event.value == 'PRESS' and event.alt == False and event.shift == False and event.ctrl == False):
                    if (bpy.context.view_layer.objects.active.name != cylinder['sna_actobjcylgen']):
                        bpy.ops.object.delete('INVOKE_DEFAULT', confirm=False)
                    else:
                        if event.type in ['RIGHTMOUSE', 'ESC']:
                            self.execute(context)
                            return {'CANCELLED'}
                        self.execute(context)
                        return {"FINISHED"}
                if (event.type == 'SPACE' and event.value == 'PRESS' and event.alt == False and event.shift == False and event.ctrl == False):
                    if event.type in ['RIGHTMOUSE', 'ESC']:
                        self.execute(context)
                        return {'CANCELLED'}
                    self.execute(context)
                    return {"FINISHED"}
        except Exception as error:
            print(error)
        if event.type in ['RIGHTMOUSE', 'ESC']:
            self.execute(context)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        global _050B8_running
        if _050B8_running:
            _050B8_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            cylinder['sna_actobjcylgen'] = bpy.context.view_layer.objects.active.name
            args = (context,)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            _050B8_running = True
            return {'RUNNING_MODAL'}


class SNA_OT_Export_Selected_9F890(bpy.types.Operator):
    bl_idname = "sna.export_selected_9f890"
    bl_label = "Export Selected"
    bl_description = "Creates an SDF of the currently selected colliders"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        export_colliders['sna_selobjforexp'] = bpy.context.selected_objects
        bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.sna.print_param_835e7('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Export_All_451Dc(bpy.types.Operator):
    bl_idname = "sna.export_all_451dc"
    bl_label = "Export All"
    bl_description = "Creates an SDF of all objects in the 'Collider' collection"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        export_colliders['sna_selobjforexp'] = bpy.data.collections['Colliders'].all_objects
        bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.sna.print_param_835e7('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Print_Param_835E7(bpy.types.Operator):
    bl_idname = "sna.print_param_835e7"
    bl_label = "Print Param"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        with open(os.path.join(bpy.context.scene.sna_filepath,'model.sdf'), mode='w') as file_C0D8E:
            file_C0D8E.seek(0)
            file_C0D8E.write('')
            file_C0D8E.truncate()
        for i_9E654 in range(len(export_colliders['sna_selobjforexp'])):
            if 'Cube' in export_colliders['sna_selobjforexp'][i_9E654].name:
                with open(os.path.join(bpy.context.scene.sna_filepath,'model.sdf'), mode='a') as file_CE19C:
                    file_CE19C.write('\n<collision name ="' + export_colliders['sna_selobjforexp'][i_9E654].name + '">\n' + '  <pose>' + str(export_colliders['sna_selobjforexp'][i_9E654].location[0]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].location[1]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].location[2]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[0]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[1]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[2]) + '</pose>\n' + '  <geometry>\n' + '    <box>\n' + '      <size>' + str(export_colliders['sna_selobjforexp'][i_9E654].dimensions[0]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].dimensions[1]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].dimensions[2]) + '</size>\n' + '    </box>\n' + '  </geometry>\n' + '</collision>')
            else:
                if 'Cylinder' in export_colliders['sna_selobjforexp'][i_9E654].name:
                    with open(os.path.join(bpy.context.scene.sna_filepath,'model.sdf'), mode='a') as file_BA18C:
                        file_BA18C.write('\n<collision name ="' + export_colliders['sna_selobjforexp'][i_9E654].name + '">\n' + '  <pose>' + str(export_colliders['sna_selobjforexp'][i_9E654].location[0]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].location[1]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].location[2]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[0]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[1]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[2]) + '</pose>\n' + '  <geometry>\n' + '    <cylinder>\n' + '      <length>' + str(export_colliders['sna_selobjforexp'][i_9E654].dimensions[2]) + '</length>\n' + '      <radius>' + str(float(export_colliders['sna_selobjforexp'][i_9E654].dimensions[0] / 2.0)) + '</radius>\n' + '    </cylinder>\n' + '  </geometry>\n' + '</collision>')
                else:
                    if 'Sphere' in export_colliders['sna_selobjforexp'][i_9E654].name:
                        with open(os.path.join(bpy.context.scene.sna_filepath,'model.sdf'), mode='a') as file_5E037:
                            file_5E037.write('\n<collision name ="' + export_colliders['sna_selobjforexp'][i_9E654].name + '">\n' + '  <pose>' + str(export_colliders['sna_selobjforexp'][i_9E654].location[0]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].location[1]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].location[2]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[0]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[1]) + ' ' + str(export_colliders['sna_selobjforexp'][i_9E654].rotation_euler[2]) + '</pose>\n' + '  <geometry>\n' + '    <sphere>\n' + '      <radius>' + str(float(export_colliders['sna_selobjforexp'][i_9E654].dimensions[2] / 2.0)) + '</radius>\n' + '    </sphere>\n' + '  </geometry>\n' + '</collision>\n')
                    else:
                        if '_meshcollider' in export_colliders['sna_selobjforexp'][i_9E654].name:
                            bpy.context.scene.sna_filepathtype = export_colliders['sna_selobjforexp'][i_9E654].name + '.stl'
                            bpy.ops.export_mesh.stl(filepath=os.path.join(bpy.path.abspath(bpy.context.scene.sna_filepath),bpy.context.scene.sna_filepathtype), check_existing=False, use_selection=True)
                            with open(os.path.join(bpy.path.abspath(bpy.context.scene.sna_filepath),'model.sdf'), mode='a') as file_FC99B:
                                file_FC99B.write('\n<collision name ="' + export_colliders['sna_selobjforexp'][i_9E654].name + '">\n' + '  <geometry>\n' + '    <mesh>\n' + '      <uri>' + export_colliders['sna_selobjforexp'][i_9E654].name + '.stl</uri>\n' + '    </mesh>\n' + '  </geometry>\n' + '</collision>')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Cylindercap_0F9D8(bpy.types.Operator):
    bl_idname = "sna.cylindercap_0f9d8"
    bl_label = "CylinderCap"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        collider['sna_activeobject'] = bpy.context.view_layer.objects.active.name
        bpy.ops.object.duplicate('INVOKE_DEFAULT', )
        print(collider['sna_activeobject'])
        bpy.context.scene.sna_duplicate_to_delete = bpy.context.view_layer.objects.active
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        exec("bpy.ops.mesh.select_all(action='INVERT')")
        bpy.ops.mesh.delete('INVOKE_DEFAULT', type='FACE')
        exec("bpy.ops.mesh.select_all(action='SELECT')")
        area_type = 'VIEW_3D'
        areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]
        bpy.context.scene.tool_settings.use_transform_data_origin = True
        with bpy.context.temp_override(area=areas[0]):
            bpy.ops.transform.create_orientation(use=True)
            bpy.ops.object.editmode_toggle()
            transform_type = bpy.context.scene.transform_orientation_slots[0].type
            bpy.ops.transform.transform(mode='ALIGN', orient_type='Face', orient_matrix_type=transform_type, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='ACTIVE', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
            bpy.ops.transform.delete_orientation()
        exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
        bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
        exec('')
        exec('from mathutils import Vector')
        exec('bpy.context.active_object.location += 1.0 * bpy.context.active_object.matrix_world.to_quaternion() @ Vector((0, 0, -100))')
        euler_angles = bpy.context.view_layer.objects.active.rotation_euler
        normal_direction = None
        from mathutils import Euler
        # Convert Euler angles to a rotation matrix
        rotation_matrix = euler_angles.to_matrix()
        # Extract the normal direction from the rotation matrix
        normal_direction = rotation_matrix.to_3x3() @ mathutils.Vector((0, 0, 1))
        print(collider['sna_activeobject'], str(normal_direction), str(bpy.context.view_layer.objects.active.location))
        print(str(normal_direction), str(bpy.context.view_layer.objects.active.location), collider['sna_activeobject'])
        ray_direction_global_vec = normal_direction
        ray_origin_global_vec = bpy.context.view_layer.objects.active.location
        specified_object_name = collider['sna_activeobject']
        hit_location_global = None
        #import bpy
        from mathutils import Euler
        #ray_origin_global_vec = (1, 1, 1)
        #ray_direction_global_vec = (1, 1, 1)
        # Set the starting point for the ray (origin) in global coordinates
        ray_origin_global = mathutils.Vector(ray_origin_global_vec)
        # Set the direction of the ray (upwards along the positive Z-axis) in global coordinates
        ray_direction_global = mathutils.Vector(ray_direction_global_vec)
        # Set the maximum distance for the ray
        max_distance = 1000.0  # Adjust as needed
        # Specify the object name you want to cast rys against
        #specified_object_name = "Link4"
        # Ensure the scene is in OBJECT mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # Get the current dependency graph
        depsgraph = bpy.context.evaluated_depsgraph_get()
        hit_object_name = None
        hit_location_global = None
        # Iterate through all visible objects in the scene
        for obj in bpy.context.visible_objects:
            # Check if the current object is the specified object
            if obj.name == specified_object_name:
                # Convert the ray origin and direction to object local coordinates
                ray_origin_local = obj.matrix_world.inverted() @ ray_origin_global
                ray_direction_local = obj.matrix_world.inverted().to_3x3() @ ray_direction_global
                # Cast the ray for the specified object
                success, location, normal, index = obj.ray_cast(ray_origin_local, ray_direction_local)
                if success:
                    # Convert the hit location back to global coordinates
                    hit_location_global = obj.matrix_world @ location
                    print("Ray Hit Location (Global):", hit_location_global)
                    print("Hit Normal:", normal)
                    print("Face Index:", index)
                    hit_object_name = obj.name
                    break  # Exit the loop after the first hit
        # Check if any hits occurred
        if hit_object_name:
            print("Object Hit:", hit_object_name)
        #    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=hit_location_global)
        else:
            print("Ray did not hit anything within the specified distance on the specified object.")
        if (hit_location_global == None):
            genface['sna_rayfail'] = True
        exec('')
        exec('from mathutils import Vector')
        exec('bpy.context.active_object.location += 1.0 * bpy.context.active_object.matrix_world.to_quaternion() @ Vector((0, 0, 100))')
        if (tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]):
            bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], 0.0))
            collider['sna_moveoutcollection'] = bpy.context.collection
            collider['sna_activeobjectcollider'] = bpy.context.view_layer.objects.active
            bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
            bpy.data.scenes['Scene'].tool_settings.use_transform_data_origin = False
            bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
            bpy.data.objects.remove(object=bpy.context.scene.sna_duplicate_to_delete, )
            bpy.ops.sna.select_cylinder_face_8a190('INVOKE_DEFAULT', )
            print('1')
            if genface['sna_rayfail']:
                prev_context = bpy.context.area.type
                bpy.context.area.type = 'VIEW_3D'
                bpy.ops.transform.translate(value=(0.0, 0.0, float(float(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0] * 3.0) * -1.0)), orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(False, False, True))
                bpy.context.area.type = prev_context
            else:
                target_global_position = hit_location_global
                object_name = bpy.context.view_layer.objects.active.name
                import bmesh
                # Replace 'Cube' with the name of your object
                #object_name = 'Cylinder.013'
                # Replace these coordinates with your desired global position
                #target_global_position = Vector((7.05492, -15.1448, -2.33593))
                # Get the active object
                obj = bpy.data.objects.get(object_name)
                # Check if the object exists and is in Edit Mode
                if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
                    # Get the mesh data
                    mesh = bmesh.from_edit_mesh(obj.data)
                    # Check if there is at least one selected face
                    selected_faces = [f for f in mesh.faces if f.select]
                    if selected_faces:
                        # Calculate the translation vector to the target position
                        target_local_position = obj.matrix_world.inverted() @ target_global_position
                        translation_vector = target_local_position - selected_faces[0].calc_center_median()
                        # Move the selected face(s) to the target global position
                        for face in selected_faces:
                            for vert in face.verts:
                                vert.co += translation_vector
                        # Update the mesh
                        bmesh.update_edit_mesh(obj.data)
                        # Print the new location of the face after the update
                        updated_center = selected_faces[0].calc_center_median()
                        print("Updated Location of Selected Face(s):", obj.matrix_world @ updated_center)
                    else:
                        print("No faces selected.")
                else:
                    print("Object not found or not in Edit Mode.")
        else:
            bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=bpy.context.view_layer.objects.active.rotation_euler, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], 0.0))
            bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
            bpy.data.scenes['Scene'].tool_settings.use_transform_data_origin = False
            bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
            bpy.data.objects.remove(object=bpy.context.scene.sna_duplicate_to_delete, )
            print('')
            if genface['sna_rayfail']:
                prev_context = bpy.context.area.type
                bpy.context.area.type = 'VIEW_3D'
                bpy.ops.transform.translate(value=(0.0, 0.0, float(float(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1] * 3.0) * -1.0)), orient_type='LOCAL', orient_matrix_type='LOCAL', constraint_axis=(False, False, True))
                bpy.context.area.type = prev_context
            else:
                target_global_position = hit_location_global
                object_name = bpy.context.view_layer.objects.active.name
                import bmesh
                # Replace 'Cube' with the name of your object
                #object_name = 'Cylinder.013'
                # Replace these coordinates with your desired global position
                #target_global_position = Vector((7.05492, -15.1448, -2.33593))
                # Get the active object
                obj = bpy.data.objects.get(object_name)
                # Check if the object exists and is in Edit Mode
                if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
                    # Get the mesh data
                    mesh = bmesh.from_edit_mesh(obj.data)
                    # Check if there is at least one selected face
                    selected_faces = [f for f in mesh.faces if f.select]
                    if selected_faces:
                        # Calculate the translation vector to the target position
                        target_local_position = obj.matrix_world.inverted() @ target_global_position
                        translation_vector = target_local_position - selected_faces[0].calc_center_median()
                        # Move the selected face(s) to the target global position
                        for face in selected_faces:
                            for vert in face.verts:
                                vert.co += translation_vector
                        # Update the mesh
                        bmesh.update_edit_mesh(obj.data)
                        # Print the new location of the face after the update
                        updated_center = selected_faces[0].calc_center_median()
                        print("Updated Location of Selected Face(s):", obj.matrix_world @ updated_center)
                    else:
                        print("No faces selected.")
                else:
                    print("Object not found or not in Edit Mode.")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Boxcap_7899E(bpy.types.Operator):
    bl_idname = "sna.boxcap_7899e"
    bl_label = "BoxCap"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        collider['sna_activeobject'] = bpy.context.view_layer.objects.active.name
        bpy.ops.mesh.faces_select_linked_flat('INVOKE_DEFAULT', )
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        bpy.ops.object.duplicate('INVOKE_DEFAULT', )
        bpy.context.scene.sna_duplicate_to_delete = bpy.context.view_layer.objects.active
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        exec("bpy.ops.mesh.select_all(action='INVERT')")
        bpy.ops.mesh.delete('INVOKE_DEFAULT', type='FACE')
        exec("bpy.ops.mesh.select_all(action='SELECT')")
        Variable = None
        area_type = 'VIEW_3D'
        areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]
        bpy.context.scene.tool_settings.use_transform_data_origin = True
        with bpy.context.temp_override(area=areas[0]):
            bpy.ops.transform.create_orientation(use=True)
            bpy.ops.object.editmode_toggle()
            transform_type = bpy.context.scene.transform_orientation_slots[0].type
            bpy.ops.transform.transform(mode='ALIGN', orient_type='Face', orient_matrix_type=transform_type, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='ACTIVE', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
            bpy.ops.transform.delete_orientation()
        exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
        bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
        exec('')
        exec('from mathutils import Vector')
        exec('bpy.context.active_object.location += 1.0 * bpy.context.active_object.matrix_world.to_quaternion() @ Vector((0, 0, -100))')
        euler_angles = bpy.context.view_layer.objects.active.rotation_euler
        normal_direction = None
        from mathutils import Euler
        # Convert Euler angles to a rotation matrix
        rotation_matrix = euler_angles.to_matrix()
        # Extract the normal direction from the rotation matrix
        normal_direction = rotation_matrix.to_3x3() @ mathutils.Vector((0, 0, 1))
        print(collider['sna_activeobject'])
        ray_direction_global_vec = normal_direction
        ray_origin_global_vec = bpy.context.view_layer.objects.active.location
        specified_object_name = collider['sna_activeobject']
        hit_location_global = None
        #import bpy
        from mathutils import Euler
        #ray_origin_global_vec = (1, 1, 1)
        #ray_direction_global_vec = (1, 1, 1)
        # Set the starting point for the ray (origin) in global coordinates
        ray_origin_global = mathutils.Vector(ray_origin_global_vec)
        # Set the direction of the ray (upwards along the positive Z-axis) in global coordinates
        ray_direction_global = mathutils.Vector(ray_direction_global_vec)
        # Set the maximum distance for the ray
        max_distance = 1000.0  # Adjust as needed
        # Specify the object name you want to cast rys against
        #specified_object_name = "Link4"
        # Ensure the scene is in OBJECT mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # Get the current dependency graph
        depsgraph = bpy.context.evaluated_depsgraph_get()
        hit_object_name = None
        hit_location_global = None
        # Iterate through all visible objects in the scene
        for obj in bpy.context.visible_objects:
            # Check if the current object is the specified object
            if obj.name == specified_object_name:
                # Convert the ray origin and direction to object local coordinates
                ray_origin_local = obj.matrix_world.inverted() @ ray_origin_global
                ray_direction_local = obj.matrix_world.inverted().to_3x3() @ ray_direction_global
                # Cast the ray for the specified object
                success, location, normal, index = obj.ray_cast(ray_origin_local, ray_direction_local)
                if success:
                    # Convert the hit location back to global coordinates
                    hit_location_global = obj.matrix_world @ location
                    print("Ray Hit Location (Global):", hit_location_global)
                    print("Hit Normal:", normal)
                    print("Face Index:", index)
                    hit_object_name = obj.name
                    break  # Exit the loop after the first hit
        # Check if any hits occurred
        if hit_object_name:
            print("Object Hit:", hit_object_name)
        #    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=hit_location_global)
        else:
            print("Ray did not hit anything within the specified distance on the specified object.")
        exec('')
        exec('from mathutils import Vector')
        exec('bpy.context.active_object.location += 1.0 * bpy.context.active_object.matrix_world.to_quaternion() @ Vector((0, 0, 100))')
        bpy.ops.mesh.primitive_cube_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, rotation=(bpy.context.view_layer.objects.active.rotation_euler[0], bpy.context.view_layer.objects.active.rotation_euler[1], bpy.context.view_layer.objects.active.rotation_euler[2]), scale=tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0))
        bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
        bpy.data.scenes['Scene'].tool_settings.use_transform_data_origin = False
        bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
        bpy.data.objects.remove(object=bpy.context.scene.sna_duplicate_to_delete, )
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        bpy.ops.mesh.select_mode('INVOKE_DEFAULT', type='FACE')
        bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='DESELECT')
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        bpy.context.view_layer.objects.active.data.polygons[4].select = True
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        bpy.ops.wm.tool_set_by_id('INVOKE_DEFAULT', name='builtin.move')
        target_global_position = hit_location_global
        object_name = bpy.context.view_layer.objects.active.name
        import bmesh
        # Replace 'Cube' with the name of your object
        #object_name = 'Cylinder.013'
        # Replace these coordinates with your desired global position
        #target_global_position = Vector((7.05492, -15.1448, -2.33593))
        # Get the active object
        obj = bpy.data.objects.get(object_name)
        # Check if the object exists and is in Edit Mode
        if obj and obj.type == 'MESH' and obj.mode == 'EDIT':
            # Get the mesh data
            mesh = bmesh.from_edit_mesh(obj.data)
            # Check if there is at least one selected face
            selected_faces = [f for f in mesh.faces if f.select]
            if selected_faces:
                # Calculate the translation vector to the target position
                target_local_position = obj.matrix_world.inverted() @ target_global_position
                translation_vector = target_local_position - selected_faces[0].calc_center_median()
                # Move the selected face(s) to the target global position
                for face in selected_faces:
                    for vert in face.verts:
                        vert.co += translation_vector
                # Update the mesh
                bmesh.update_edit_mesh(obj.data)
                # Print the new location of the face after the update
                updated_center = selected_faces[0].calc_center_median()
                print("Updated Location of Selected Face(s):", obj.matrix_world @ updated_center)
            else:
                print("No faces selected.")
        else:
            print("Object not found or not in Edit Mode.")
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


_0BF7C_running = False
class SNA_OT_Selectflatfaces_0Bf7C(bpy.types.Operator):
    bl_idname = "sna.selectflatfaces_0bf7c"
    bl_label = "SelectFlatFaces"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    cursor = "CROSSHAIR"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        if not True or context.area.spaces[0].bl_rna.identifier == 'SpaceView3D':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_4590E, y_4590E = (410.0, 1000.0)
                    blf.position(font_id, x_4590E, y_4590E, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 0.06046402454376221, 0.032939016819000244, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 0:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 0)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, 'Choose a flat surface')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_3F7BB, y_3F7BB = (400.0, 930.0)
                    blf.position(font_id, x_3F7BB, y_3F7BB, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 1493:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 1493)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[Ctrl + Shift + C] Generate Cylinder')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_C45A9, y_C45A9 = (400.0, 860.0)
                    blf.position(font_id, x_C45A9, y_C45A9, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 1493:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 1493)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[Ctrl + Shift + B] Generate Box')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
                font_id = 0
                if r'' and os.path.exists(r''):
                    font_id = blf.load(r'')
                if font_id == -1:
                    print("Couldn't load font!")
                else:
                    x_5FB65, y_5FB65 = (400.0, 790.0)
                    blf.position(font_id, x_5FB65, y_5FB65, 0)
                    if bpy.app.version >= (3, 4, 0):
                        blf.size(font_id, 50.0)
                    else:
                        blf.size(font_id, 50.0, 72)
                    clr = (1.0, 1.0, 1.0, 1.0)
                    blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                    if 1493:
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.word_wrap(font_id, 1493)
                    if 0.0:
                        blf.enable(font_id, blf.ROTATION)
                        blf.rotation(font_id, 0.0)
                    blf.enable(font_id, blf.WORD_WRAP)
                    blf.draw(font_id, '[ESC] Cancel')
                    blf.disable(font_id, blf.ROTATION)
                    blf.disable(font_id, blf.WORD_WRAP)
            except Exception as error:
                print(error)

    def execute(self, context):
        global _0BF7C_running
        _0BF7C_running = False
        context.window.cursor_set("DEFAULT")
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _0BF7C_running
        if not context.area or not _0BF7C_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.area.tag_redraw()
        context.window.cursor_set('CROSSHAIR')
        try:
            if 'RELEASE' in event.value_prev:
                bpy.ops.mesh.faces_select_linked_flat('INVOKE_DEFAULT', sharpness=0.10000000149011612)
            else:
                if (event.type == 'C' and event.value == 'PRESS' and event.alt == False and event.shift == True and event.ctrl == True):
                    bpy.ops.sna.cylindercap_0f9d8('INVOKE_DEFAULT', )
                    print('1')
                    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
                    if event.type in ['RIGHTMOUSE', 'ESC']:
                        self.execute(context)
                        return {'CANCELLED'}
                    self.execute(context)
                    return {"FINISHED"}
                else:
                    if (event.type == 'B' and event.value == 'PRESS' and event.alt == False and event.shift == True and event.ctrl == True):
                        bpy.ops.sna.boxcap_7899e('INVOKE_DEFAULT', )
                        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
                        if event.type in ['RIGHTMOUSE', 'ESC']:
                            self.execute(context)
                            return {'CANCELLED'}
                        self.execute(context)
                        return {"FINISHED"}
        except Exception as error:
            print(error)
        if event.type in ['RIGHTMOUSE', 'ESC']:
            self.execute(context)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        global _0BF7C_running
        if _0BF7C_running:
            _0BF7C_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
            bpy.ops.mesh.select_mode('INVOKE_DEFAULT', type='FACE', action='ENABLE')
            bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='DESELECT')
            args = (context,)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            _0BF7C_running = True
            return {'RUNNING_MODAL'}


class SNA_OT_Mesh_85D40(bpy.types.Operator):
    bl_idname = "sna.mesh_85d40"
    bl_label = "Mesh"
    bl_description = "Generates a convex hull mesh collider"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if 'OBJECT'==bpy.context.mode:
            exec('bpy.ops.object.duplicate()')
            exec('bpy.ops.object.join()')
            collider['sna_joinedobj'] = bpy.context.view_layer.objects.active
            bpy.context.view_layer.objects.active.name = bpy.context.view_layer.objects.active.name + '_meshcollider'
            bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
            exec('bpy.ops.mesh.select_mode(type="VERT")')
            exec("bpy.ops.mesh.select_all(action='SELECT')")
            exec('bpy.ops.mesh.convex_hull()')
            bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='DECIMATE')
            exec('bpy.ops.object.editmode_toggle()')
            bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='SOLIDIFY')
            exec('bpy.context.object.modifiers["Solidify"].use_rim_only = True')
            exec('bpy.context.object.modifiers["Solidify"].offset = 1')
            bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
            bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
        else:
            if 'EDIT_MESH'==bpy.context.mode:
                bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
                exec('bpy.ops.object.duplicate()')
                bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
                exec("bpy.ops.mesh.select_all(action='INVERT')")
                bpy.ops.mesh.delete('INVOKE_DEFAULT', type='FACE')
                exec('bpy.ops.mesh.convex_hull()')
                bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
                bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='DECIMATE')
                bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='SOLIDIFY')
                exec('bpy.context.object.modifiers["Solidify"].use_rim_only = True')
                exec('bpy.context.object.modifiers["Solidify"].offset = 1')
                bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_IMPORT_FC836(bpy.types.Panel):
    bl_label = 'Import'
    bl_idname = 'SNA_PT_IMPORT_FC836'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Collider Gen'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        row_5533A = layout.row(heading='Import', align=False)
        row_5533A.alert = False
        row_5533A.enabled = True
        row_5533A.active = True
        row_5533A.use_property_split = False
        row_5533A.use_property_decorate = False
        row_5533A.scale_x = 1.0
        row_5533A.scale_y = 1.0
        row_5533A.alignment = 'Expand'.upper()
        row_5533A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_5533A.operator('sna.import_stl_90582', text='STL', icon_value=0, emboss=True, depress=False)
        op = row_5533A.operator('sna.import_fbx_644d9', text='FBX', icon_value=0, emboss=True, depress=False)
        op = row_5533A.operator('sna.import_obj_befeb', text='OBJ', icon_value=0, emboss=True, depress=False)
        op = row_5533A.operator('sna.import_dae_a17ee', text='DAE', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.clear_hierarchy_9ff17', text='Clear Hierarchy/Reset Scale', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.separate_parts_17bd5', text='Separate Parts', icon_value=0, emboss=True, depress=False)


_319F9_running = False
class SNA_OT_Modal_Operator_319F9(bpy.types.Operator):
    bl_idname = "sna.modal_operator_319f9"
    bl_label = "Modal Operator"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    cursor = "CROSSHAIR"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        if not False or context.area.spaces[0].bl_rna.identifier == 'SpaceNodeEditor':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                pass
            except Exception as error:
                print(error)

    def execute(self, context):
        global _319F9_running
        _319F9_running = False
        context.window.cursor_set("DEFAULT")
        print('Import')
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _319F9_running
        if not context.area or not _319F9_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.window.cursor_set('CROSSHAIR')
        try:
            bpy.app.handlers.load_post()
        except Exception as error:
            print(error)
        if event.type in ['RIGHTMOUSE', 'ESC']:
            self.execute(context)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        global _319F9_running
        if _319F9_running:
            _319F9_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            context.window_manager.modal_handler_add(self)
            _319F9_running = True
            return {'RUNNING_MODAL'}


class SNA_OT_Import_Stl_90582(bpy.types.Operator):
    bl_idname = "sna.import_stl_90582"
    bl_label = "Import STL"
    bl_description = "Import STL file"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.import_mesh.stl('INVOKE_DEFAULT', axis_up='Z')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Import_Fbx_644D9(bpy.types.Operator):
    bl_idname = "sna.import_fbx_644d9"
    bl_label = "Import FBX"
    bl_description = "Import FBX file"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        prev_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.import_scene.fbx('INVOKE_DEFAULT', axis_up='Z')
        bpy.context.area.type = prev_context
        for i_C745B in range(len(bpy.context.selected_objects)):
            print('Done')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Import_Obj_Befeb(bpy.types.Operator):
    bl_idname = "sna.import_obj_befeb"
    bl_label = "Import OBJ"
    bl_description = "Import OBJ file"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.wm.obj_import('INVOKE_DEFAULT', up_axis='Z')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Import_Dae_A17Ee(bpy.types.Operator):
    bl_idname = "sna.import_dae_a17ee"
    bl_label = "Import DAE"
    bl_description = "Import DAE file"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.wm.collada_import('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Clear_Hierarchy_9Ff17(bpy.types.Operator):
    bl_idname = "sna.clear_hierarchy_9ff17"
    bl_label = "Clear Hierarchy"
    bl_description = "Removes all hierarchys and empty objects as well as resetting scale values. This ensures collision objects fit correctly to the scene objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        prev_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.object.parent_clear('INVOKE_DEFAULT', type='CLEAR_KEEP_TRANSFORM')
        bpy.context.area.type = prev_context
        prev_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.object.parent_clear('INVOKE_DEFAULT', type='CLEAR_KEEP_TRANSFORM')
        bpy.context.area.type = prev_context
        prev_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.object.parent_clear('INVOKE_DEFAULT', type='CLEAR_KEEP_TRANSFORM')
        bpy.context.area.type = prev_context
        prev_context = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.object.parent_clear('INVOKE_DEFAULT', type='CLEAR_KEEP_TRANSFORM')
        bpy.context.area.type = prev_context
        bpy.ops.object.transform_apply('INVOKE_DEFAULT', scale=True)
        for i_85522 in range(len(bpy.context.view_layer.objects.selected)):
            if (bpy.context.view_layer.objects.selected[i_85522].type == 'EMPTY'):
                bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.selected[i_85522]
                bpy.data.objects.remove(object=bpy.context.view_layer.objects.active, )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Separate_Parts_17Bd5(bpy.types.Operator):
    bl_idname = "sna.separate_parts_17bd5"
    bl_label = "Separate Parts"
    bl_description = "Separates objects into individual parts when able. This allows the user to apply colliders to individual parts. Note that continuous geometry will not be separated however this can be done manually"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        exec("bpy.ops.mesh.select_all(action='SELECT')")
        bpy.ops.mesh.customdata_custom_splitnormals_clear('INVOKE_DEFAULT', )
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
        bpy.ops.mesh.separate('INVOKE_DEFAULT', type='LOOSE')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Sphere_F5Cd9(bpy.types.Operator):
    bl_idname = "sna.sphere_f5cd9"
    bl_label = "Sphere"
    bl_description = "Creates a sphere collider that fits the selected object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_perobj:
            bpy.ops.sna.sphereop_6d8a0('INVOKE_DEFAULT', )
        else:
            exec('bpy.ops.object.duplicate()')
            exec('bpy.ops.object.join()')
            collider['sna_joinedobj'] = bpy.context.view_layer.objects.active
            bpy.ops.sna.sphereop_6d8a0('INVOKE_DEFAULT', )
            bpy.data.objects.remove(object=collider['sna_joinedobj'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Sphereop_6D8A0(bpy.types.Operator):
    bl_idname = "sna.sphereop_6d8a0"
    bl_label = "SphereOp"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        collider['sna_selection'] = bpy.context.selected_objects
        for i_6F8AA in range(len(collider['sna_selection'])-1,-1,-1):
            bpy.context.view_layer.objects.active = collider['sna_selection'][i_6F8AA]
            exec("bpy.data.scenes['Scene'].tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'")
            bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
            print(bpy.context.view_layer.objects.active.name)
            if ((tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]) and (tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2])):
                bpy.ops.mesh.primitive_uv_sphere_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0]))
                bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
                bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
            else:
                if ((tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2]) and (tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0])):
                    bpy.ops.mesh.primitive_uv_sphere_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]))
                    bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
                    bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
                else:
                    if ((tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[1]) and (tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2] >= tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[0])):
                        bpy.ops.mesh.primitive_uv_sphere_add('INVOKE_DEFAULT', location=bpy.context.view_layer.objects.active.location, scale=(tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2], tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) / 2.0)[2]))
                        bpy.ops.sna.move_to_colllder_collection_1fa60('INVOKE_DEFAULT', )
                        bpy.ops.sna.set_collider_material_33bff('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_GROUP_sna_property_group(bpy.types.PropertyGroup):
    string: bpy.props.StringProperty(name='String', description='', default='', subtype='NONE', maxlen=0)


class SNA_GROUP_sna_sog(bpy.types.PropertyGroup):
    new_property: bpy.props.StringProperty(name='New Property', description='', default='', subtype='NONE', maxlen=0)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_GROUP_sna_property_group)
    bpy.utils.register_class(SNA_GROUP_sna_sog)
    bpy.types.Scene.sna_source_collection = bpy.props.CollectionProperty(name='Source Collection', description='', type=SNA_GROUP_sna_property_group)
    bpy.types.Scene.sna_duplicate_to_delete = bpy.props.PointerProperty(name='Duplicate to delete', description='', type=bpy.types.Object)
    bpy.types.Scene.sna_cylcaplocation = bpy.props.FloatProperty(name='CylCapLocation', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    bpy.types.Scene.sna_selectedobjsforexp = bpy.props.PointerProperty(name='SelectedObjsForExp', description='', type=bpy.types.Collection)
    bpy.types.Object.sna_radius = bpy.props.FloatProperty(name='Radius', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    bpy.types.Scene.sna_radiuscylinderx = bpy.props.FloatProperty(name='RadiusCylinderX', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    bpy.types.Scene.sna_radiuscylindery = bpy.props.FloatProperty(name='RadiusCylinderY', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    bpy.types.Scene.sna_perobj = bpy.props.BoolProperty(name='PerObj', description='', default=False)
    bpy.types.Object.sna_actobjcollider = bpy.props.PointerProperty(name='ActObjCollider', description='', type=bpy.types.Scene)
    bpy.types.Scene.sna_minbox = bpy.props.BoolProperty(name='MinBox', description='', default=False)
    bpy.types.Scene.sna_filepath = bpy.props.StringProperty(name='FilePath', description='', default='C:/', subtype='DIR_PATH', maxlen=0)
    bpy.types.Scene.sna_filepathtype = bpy.props.StringProperty(name='FilePathType', description='', default='', subtype='FILE_PATH', maxlen=0)
    bpy.utils.register_class(SNA_OT_Box_9D9E4)
    bpy.utils.register_class(SNA_PT_CREATE_D9148)
    bpy.utils.register_class(SNA_PT_TRANSFORM_30201)
    bpy.utils.register_class(SNA_OT_Scale_Cage_4E08E)
    bpy.utils.register_class(SNA_PT_EXPORT_420D3)
    bpy.utils.register_class(SNA_OT_Scalecylradius_E1610)
    bpy.utils.register_class(SNA_OT_Scalesphereradius_Bd79D)
    bpy.utils.register_class(SNA_PT_CREATE_OPTIONS_F211B)
    bpy.utils.register_class(SNA_MT_5CC5F)
    bpy.utils.register_class(SNA_MT_4968B)
    bpy.utils.register_class(SNA_OT_Select_Cylinder_Face_8A190)
    bpy.utils.register_class(SNA_OT_Minbox_0936B)
    bpy.app.handlers.load_post.append(load_post_handler_A55A1)
    bpy.utils.register_class(SNA_OT_Set_Active_Collection_50942)
    bpy.utils.register_class(SNA_OT_Set_Collider_Material_33Bff)
    bpy.utils.register_class(SNA_OT_Move_To_Colllder_Collection_1Fa60)
    bpy.utils.register_class(SNA_OT_Cylinder_Z_83F4C)
    bpy.utils.register_class(SNA_OT_Cylinder_X_3A040)
    bpy.utils.register_class(SNA_OT_Cylinder_Y_F23B4)
    bpy.utils.register_class(SNA_OT_Cylinder_050B8)
    bpy.utils.register_class(SNA_OT_Export_Selected_9F890)
    bpy.utils.register_class(SNA_OT_Export_All_451Dc)
    bpy.utils.register_class(SNA_OT_Print_Param_835E7)
    bpy.utils.register_class(SNA_OT_Cylindercap_0F9D8)
    bpy.utils.register_class(SNA_OT_Boxcap_7899E)
    bpy.utils.register_class(SNA_OT_Selectflatfaces_0Bf7C)
    bpy.utils.register_class(SNA_OT_Mesh_85D40)
    bpy.utils.register_class(SNA_PT_IMPORT_FC836)
    bpy.utils.register_class(SNA_OT_Modal_Operator_319F9)
    bpy.utils.register_class(SNA_OT_Import_Stl_90582)
    bpy.utils.register_class(SNA_OT_Import_Fbx_644D9)
    bpy.utils.register_class(SNA_OT_Import_Obj_Befeb)
    bpy.utils.register_class(SNA_OT_Import_Dae_A17Ee)
    bpy.utils.register_class(SNA_OT_Clear_Hierarchy_9Ff17)
    bpy.utils.register_class(SNA_OT_Separate_Parts_17Bd5)
    bpy.utils.register_class(SNA_OT_Sphere_F5Cd9)
    bpy.utils.register_class(SNA_OT_Sphereop_6D8A0)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_filepathtype
    del bpy.types.Scene.sna_filepath
    del bpy.types.Scene.sna_minbox
    del bpy.types.Object.sna_actobjcollider
    del bpy.types.Scene.sna_perobj
    del bpy.types.Scene.sna_radiuscylindery
    del bpy.types.Scene.sna_radiuscylinderx
    del bpy.types.Object.sna_radius
    del bpy.types.Scene.sna_selectedobjsforexp
    del bpy.types.Scene.sna_cylcaplocation
    del bpy.types.Scene.sna_duplicate_to_delete
    del bpy.types.Scene.sna_source_collection
    bpy.utils.unregister_class(SNA_GROUP_sna_sog)
    bpy.utils.unregister_class(SNA_GROUP_sna_property_group)
    bpy.utils.unregister_class(SNA_OT_Box_9D9E4)
    bpy.utils.unregister_class(SNA_PT_CREATE_D9148)
    bpy.utils.unregister_class(SNA_PT_TRANSFORM_30201)
    bpy.utils.unregister_class(SNA_OT_Scale_Cage_4E08E)
    bpy.utils.unregister_class(SNA_PT_EXPORT_420D3)
    bpy.utils.unregister_class(SNA_OT_Scalecylradius_E1610)
    bpy.utils.unregister_class(SNA_OT_Scalesphereradius_Bd79D)
    bpy.utils.unregister_class(SNA_PT_CREATE_OPTIONS_F211B)
    bpy.utils.unregister_class(SNA_MT_5CC5F)
    bpy.utils.unregister_class(SNA_MT_4968B)
    bpy.utils.unregister_class(SNA_OT_Select_Cylinder_Face_8A190)
    bpy.utils.unregister_class(SNA_OT_Minbox_0936B)
    bpy.app.handlers.load_post.remove(load_post_handler_A55A1)
    bpy.utils.unregister_class(SNA_OT_Set_Active_Collection_50942)
    bpy.utils.unregister_class(SNA_OT_Set_Collider_Material_33Bff)
    bpy.utils.unregister_class(SNA_OT_Move_To_Colllder_Collection_1Fa60)
    bpy.utils.unregister_class(SNA_OT_Cylinder_Z_83F4C)
    bpy.utils.unregister_class(SNA_OT_Cylinder_X_3A040)
    bpy.utils.unregister_class(SNA_OT_Cylinder_Y_F23B4)
    bpy.utils.unregister_class(SNA_OT_Cylinder_050B8)
    bpy.utils.unregister_class(SNA_OT_Export_Selected_9F890)
    bpy.utils.unregister_class(SNA_OT_Export_All_451Dc)
    bpy.utils.unregister_class(SNA_OT_Print_Param_835E7)
    bpy.utils.unregister_class(SNA_OT_Cylindercap_0F9D8)
    bpy.utils.unregister_class(SNA_OT_Boxcap_7899E)
    bpy.utils.unregister_class(SNA_OT_Selectflatfaces_0Bf7C)
    bpy.utils.unregister_class(SNA_OT_Mesh_85D40)
    bpy.utils.unregister_class(SNA_PT_IMPORT_FC836)
    bpy.utils.unregister_class(SNA_OT_Modal_Operator_319F9)
    bpy.utils.unregister_class(SNA_OT_Import_Stl_90582)
    bpy.utils.unregister_class(SNA_OT_Import_Fbx_644D9)
    bpy.utils.unregister_class(SNA_OT_Import_Obj_Befeb)
    bpy.utils.unregister_class(SNA_OT_Import_Dae_A17Ee)
    bpy.utils.unregister_class(SNA_OT_Clear_Hierarchy_9Ff17)
    bpy.utils.unregister_class(SNA_OT_Separate_Parts_17Bd5)
    bpy.utils.unregister_class(SNA_OT_Sphere_F5Cd9)
    bpy.utils.unregister_class(SNA_OT_Sphereop_6D8A0)
