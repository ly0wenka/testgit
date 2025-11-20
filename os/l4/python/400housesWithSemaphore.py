import bpy
import threading
from queue import Queue
from random import uniform
import time

# -------------------------------
# Черга для передачі даних від потоків до головного потоку
mesh_queue = Queue()

# Семафор для обмеження одночасних потоків
sema = threading.Semaphore(8)  # максимум 8 потоків одночасно

def generate_house_verts(width, length, height, roof_height, offset_x, offset_y):
    floor_verts = [
        (0 + offset_x, 0 + offset_y, 0),
        (width + offset_x, 0 + offset_y, 0),
        (width + offset_x, length + offset_y, 0),
        (0 + offset_x, length + offset_y, 0)
    ]
    floor_faces = [(0,1,2,3)]
    
    walls = []
    def wall(x1,y1,x2,y2):
        verts = [
            (x1+offset_x, y1+offset_y, 0),
            (x2+offset_x, y2+offset_y, 0),
            (x2+offset_x, y2+offset_y, height),
            (x1+offset_x, y1+offset_y, height),
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
    roof_faces = [(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
    
    meshes = []
    meshes.append(('Floor', floor_verts, floor_faces))
    for idx,(verts,faces) in enumerate(walls):
        meshes.append((f'Wall_{idx}', verts, faces))
    meshes.append(('Roof', roof_verts, roof_faces))
    
    return meshes

def worker(row, col, spacing_x, spacing_y):
    with sema:  # обмежуємо кількість потоків
        w = uniform(3,6)
        l = uniform(4,8)
        h = uniform(2.5,4)
        rh = uniform(1.5,3)
        ox = col * spacing_x
        oy = row * spacing_y
        meshes = generate_house_verts(w,l,h,rh, ox, oy)
        mesh_queue.put((row, col, meshes))

def create_mesh(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj

# -------------------------------
# Параметри сітки
rows = 20
cols = 20
spacing_x = 12
spacing_y = 12

threads = []

start_time = time.time()

# -------------------------------
# Запуск потоків для генерації вершин
for row in range(rows):
    for col in range(cols):
        t = threading.Thread(target=worker, args=(row, col, spacing_x, spacing_y))
        t.start()
        threads.append(t)

# Чекаємо завершення потоків
for t in threads:
    t.join()

# -------------------------------
# Створення всіх об'єктів у головному потоці
house_counter = 0
while not mesh_queue.empty():
    row, col, meshes = mesh_queue.get()
    objects = []
    for name, verts, faces in meshes:
        obj = create_mesh(name, verts, faces)
        objects.append(obj)
    # Об'єднуємо елементи одного будинку
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    house_counter += 1
    print(f"House {house_counter} at row {row}, col {col} created")

end_time = time.time()
print(f"\nTotal time to generate {rows*cols} houses: {end_time - start_time:.3f} seconds")
