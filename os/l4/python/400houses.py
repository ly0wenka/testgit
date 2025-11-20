import bpy
from random import uniform
import time  # для діагностики

def generate_house_verts(width, length, height, roof_height, offset_x, offset_y):
    floor_verts = [
        (0 + offset_x, 0 + offset_y, 0),
        (width + offset_x, 0 + offset_y, 0),
        (width + offset_x, length + offset_y, 0),
        (0 + offset_x, length + offset_y, 0)
    ]
    floor_faces = [(0, 1, 2, 3)]
    
    walls = []
    def wall(x1, y1, x2, y2):
        verts = [
            (x1 + offset_x, y1 + offset_y, 0),
            (x2 + offset_x, y2 + offset_y, 0),
            (x2 + offset_x, y2 + offset_y, height),
            (x1 + offset_x, y1 + offset_y, height),
        ]
        faces = [(0,1,2,3)]
        return (verts, faces)
    
    walls.append(wall(0,0,width,0))
    walls.append(wall(width,0,width,length))
    walls.append(wall(width,length,0,length))
    walls.append(wall(0,length,0,0))
    
    roof_verts = [
        (0 + offset_x, 0 + offset_y, height),
        (width + offset_x, 0 + offset_y, height),
        (width + offset_x, length + offset_y, height),
        (0 + offset_x, length + offset_y, height),
        (width/2 + offset_x, length/2 + offset_y, height + roof_height)
    ]
    roof_faces = [
        (0,1,4),
        (1,2,4),
        (2,3,4),
        (3,0,4)
    ]
    
    meshes = []
    meshes.append(('Floor', floor_verts, floor_faces))
    for idx, (verts, faces) in enumerate(walls):
        meshes.append((f'Wall_{idx}', verts, faces))
    meshes.append(('Roof', roof_verts, roof_faces))
    
    return meshes

def create_mesh(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# -------------------------------
# Generate 400 houses in 20x20 grid
# -------------------------------
rows = 20
cols = 20
spacing_x = 12
spacing_y = 12

start_time = time.time()  # старт таймера

for row in range(rows):
    for col in range(cols):
        w = uniform(3,6)
        l = uniform(4,8)
        h = uniform(2.5,4)
        rh = uniform(1.5,3)
        ox = col * spacing_x
        oy = row * spacing_y
        
        meshes = generate_house_verts(w,l,h,rh, ox, oy)
        
        # Start timer for individual house
        house_start = time.time()
        
        # Create meshes in Blender
        objects = []
        for name, verts, faces in meshes:
            obj = create_mesh(name, verts, faces)
            objects.append(obj)
        
        # Join one house into single object
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objects[0]
        bpy.ops.object.join()
        
        house_end = time.time()
        print(f"House at row {row}, col {col} generated in {house_end - house_start:.3f} seconds")

end_time = time.time()  # кінець таймера
print(f"\nTotal time to generate {rows*cols} houses: {end_time - start_time:.3f} seconds")
