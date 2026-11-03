"""Run in Blender. Reconstruct a lightweight chair using room_Chair.spz as reference.
This is a visual reconstruction, not a dimensionally calibrated scan conversion.
"""
import bpy
import math
from mathutils import Vector
from pathlib import Path

ROOT = Path(r'C:/Users/rnsgu/Immersive_Physical_Computing')
scene = bpy.data.scenes.new('Chair Digital Twin')
bpy.context.window.scene = scene

def material(name, color, roughness=.6, metallic=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    return m

ivory = material('Warm ivory frame', (.67, .70, .68), .38)
fabric = material('Graphite blue fabric', (.105, .14, .18), .86)
meshmat = material('Woven mesh', (.22, .27, .29), .8)
black = material('Charcoal fittings', (.027, .035, .043), .65)
steel = material('Satin gas lift', (.38, .43, .46), .27, .75)

def empty(name, parent=None):
    o = bpy.data.objects.new(name, None)
    scene.collection.objects.link(o)
    o.parent = parent
    return o

root = empty('Chair')
base = empty('Base', root)
upper = empty('Swivel', root)

def finish(o, name, mat, parent):
    o.name = name
    o.data.materials.append(mat)
    o.parent = parent
    if hasattr(o.data, 'polygons'):
        for p in o.data.polygons: p.use_smooth = True
    return o

def box(name, loc, size, mat, parent, radius=.02):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = o.modifiers.new('Soft edges', 'BEVEL')
    bevel.width = radius
    bevel.segments = 5
    o.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    return finish(o, name, mat, parent)

def rod(name, a, b, radius, mat, parent, vertices=16):
    a, b = Vector(a), Vector(b)
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=(b-a).length, location=(a+b)/2)
    o = bpy.context.object
    o.rotation_euler = (b-a).to_track_quat('Z', 'Y').to_euler()
    bevel=o.modifiers.new('Edge rounding','BEVEL');bevel.width=.003;bevel.segments=2
    return finish(o, name, mat, parent)

def tube(name, points, radius, mat, parent, cyclic=False):
    c = bpy.data.curves.new(name, 'CURVE'); c.dimensions='3D'; c.resolution_u=2
    c.bevel_depth=radius; c.bevel_resolution=2
    s=c.splines.new('POLY');s.points.add(len(points)-1)
    for p,xyz in zip(s.points,points):p.co=(*xyz,1)
    s.use_cyclic_u=cyclic
    o=bpy.data.objects.new(name,c);scene.collection.objects.link(o)
    return finish(o,name,mat,parent)

# Five radial feet and paired caster wheels stay still when the seat swivels.
for i in range(5):
    a=2*math.pi*i/5+.3
    x,y=.305*math.cos(a),.305*math.sin(a)
    rod('Foot %d'%i,(0,0,.18),(x,y,.105),.025,ivory,base)
    rod('Caster fork %d'%i,(x,y,.11),(x,y,.065),.016,black,base)
    tangent=Vector((-math.sin(a),math.cos(a),0))
    for side in [-1,1]:
        center=Vector((x,y,.045))+tangent*side*.022
        rod('Wheel %d %d'%(i,side),center-tangent*.011,center+tangent*.011,.043,black,base,24)
rod('Gas lift casing',(0,0,.135),(0,0,.30),.038,black,base,32)
rod('Gas lift piston',(0,0,.28),(0,0,.425),.022,steel,base,32)
box('Seat mechanism',(0,0,.424),(.23,.23,.045),black,upper,.015)
box('Seat shell',(0,-.035,.46),(.48,.455,.057),ivory,upper,.026)
box('Seat cushion',(0,-.054,.50),(.485,.46,.08),fabric,upper,.037)
rod('Adjustment stalk',(.09,0,.428),(.26,-.035,.405),.009,black,upper)
box('Height paddle',(.27,-.04,.405),(.075,.037,.018),black,upper,.008)

# Curved backrest follows the visible lumbar bulge in the user's scan.
def back(t,u):
    width=.202 + .018*t - .012*math.sin(math.pi*t)
    return (u*width, .18+.08*t-.04*math.sin(math.pi*t)+.016*u*u, .55+.49*t)
outline=[back(i/40,-1) for i in range(41)]
outline += [back(1,-1+2*i/24) for i in range(1,25)]
outline += [back(1-i/40,1) for i in range(1,41)]
outline += [back(0,1-2*i/24) for i in range(1,25)]
tube('Backrest ivory perimeter',outline,.022,ivory,upper,True)
for i in range(1,39):
    u=-1+2*i/39
    tube('Back mesh vertical %02d'%i,[back(t/20,u) for t in range(21)],.0015,meshmat,upper)
for i in range(1,49):
    t=i/49
    tube('Back mesh horizontal %02d'%i,[back(t,-1+2*j/12) for j in range(13)],.0012,meshmat,upper)
tube('Back spine',[(0,.17,.45),(0,.23,.57),(0,.255,.7),(0,.32,.89)],.023,ivory,upper)
box('Lumbar support',(0,.215,.68),(.31,.045,.075),ivory,upper,.021)

for side in [-1,1]:
    x=side*.285
    tube('Arm support %d'%side,[(side*.19,.04,.447),(x,.04,.45),(x,.045,.68)],.019,ivory,upper)
    box('Armrest %d'%side,(x,-.045,.695),(.065,.27,.035),ivory,upper,.017)
    box('Arm pad %d'%side,(x,-.045,.715),(.068,.275,.018),fabric,upper,.009)

rod('Headrest neck',(0,.29,1.0),(0,.31,1.115),.021,ivory,upper)
# Rounded rectangular headrest with open mesh center.
hp=[]
for cx,cz,start in [(.115,1.19,0),(-.115,1.19,90),(-.115,1.105,180),(.115,1.105,270)]:
    for i in range(9):
        a=math.radians(start+i*90/8)
        hp.append((cx+.038*math.cos(a),.295,cz+.038*math.sin(a)))
tube('Headrest frame',hp,.016,ivory,upper,True)
for i in range(21):
    x=-.13+i*.013
    tube('Headrest mesh %02d'%i,[(x,.29,1.09),(x,.275,1.15),(x,.29,1.205)],.002,meshmat,upper)
for i in range(13):
    z=1.095+i*.009
    tube('Headrest cross mesh %02d'%i,[(-.134,.283,z),(.134,.283,z)],.0015,meshmat,upper)

root['reference']='Visual reconstruction from user room_Chair.spz; approximate dimensions'
upper['purpose']='MQTT rotation around vertical axis; fixed base remains stationary'
scene.unit_settings.system='METRIC'
scene.world=bpy.data.worlds.new('Chair studio world');scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.19,.22,.27,1)
scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.5

def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
for name,loc,power,size in [('Key',(2,-3,4),450,4),('Fill',(-3,-1,2),270,3),('Rim',(1,3,3),500,2)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc;aim(o,(0,0,.6))
d=bpy.data.cameras.new('Chair camera');cam=bpy.data.objects.new('Chair camera',d)
scene.collection.objects.link(cam);cam.location=(1.8,-2.7,1.75);aim(cam,(0,0,.61));d.type='ORTHO';d.ortho_scale=1.65;scene.camera=cam
try:scene.render.engine='CYCLES'
except TypeError:pass
scene.cycles.samples=24
scene.render.resolution_x=900;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.film_transparent=True
# Export only the model; preserve the user's original scene in the .blend.
bpy.ops.object.select_all(action='DESELECT')
for obj in [root,*root.children_recursive]:obj.select_set(True)
bpy.context.view_layer.objects.active=root
(ROOT/'assets').mkdir(exist_ok=True);(ROOT/'source').mkdir(exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'assets'/'posture-chair.glb'),export_format='GLB',use_selection=True,export_extras=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'source'/'posture-chair.blend'))
print('Chair export complete:',ROOT/'assets'/'posture-chair.glb')
