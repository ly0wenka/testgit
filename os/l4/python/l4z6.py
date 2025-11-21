# Barber shop simulation animation (Blender bpy)
# Paste into Blender Scripting editor and Run
import bpy, math
from mathutils import Vector, Euler
import random

# --------------------
# Parameters (from your C code)
NUM_CHAIRS = 3
NUM_CLIENTS = 10
ARRIVAL_INTERVAL_SEC = 1.0      # clients arrive every 1 second
HAIRCUT_DURATION_SEC = 3.0      # haircut takes 3 seconds
FPS = 30

# Time -> frames
ARRIVAL_INTERVAL = int(ARRIVAL_INTERVAL_SEC * FPS)
HAIRCUT_DURATION = int(HAIRCUT_DURATION_SEC * FPS)

# Scene setup
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end = max( (NUM_CLIENTS * ARRIVAL_INTERVAL) + HAIRCUT_DURATION*3, 2000 )
scene.render.fps = FPS

# Clear scene (optional — careful)
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # remove collections except Scenes collection
    for block in bpy.data.meshes:
        pass

clear_scene()

# Create ground plane
bpy.ops.mesh.primitive_plane_add(size=12, location=(0,0,0))
floor = bpy.context.active_object
floor.name = "Floor"
floor_mat = bpy.data.materials.new("FloorMat")
floor_mat.diffuse_color = (0.9,0.9,0.95,1)
floor.data.materials.append(floor_mat)

# Create barber chair (center)
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, 0, 0.4))
barber_chair = bpy.context.active_object
barber_chair.scale = (0.6, 0.6, 0.4)
barber_chair.name = "BarberSeat"
mat = bpy.data.materials.new("BarberMat")
mat.diffuse_color = (0.2,0.2,0.6,1)
barber_chair.data.materials.append(mat)

# Barber object (simple cube as barber body + a rotating "scissors" as child)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=(0, -0.8, 0.65))
barber_body = bpy.context.active_object
barber_body.name = "Barber"
barber_mat = bpy.data.materials.new("BarberMatBody")
barber_mat.diffuse_color = (0.8,0.5,0.2,1)
barber_body.data.materials.append(barber_mat)

# Create a scissors-like object (thin plane) to animate cutting
bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0.4, -0.8, 0.9))
scissors = bpy.context.active_object
scissors.scale = (0.8, 0.05, 0.02)
scissors.name = "Scissors"
sc_mat = bpy.data.materials.new("ScMat")
sc_mat.diffuse_color = (0.1, 0.1, 0.1, 1)
scissors.data.materials.append(sc_mat)
scissors.parent = barber_body

# Waiting chairs (line on the right)
waiting_chairs = []
start_x = 2.5
start_y = 1.5
gap = 1.2
for i in range(NUM_CHAIRS):
    x = start_x
    y = start_y - i * gap
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(x, y, 0.3))
    ch = bpy.context.active_object
    ch.scale = (0.4, 0.4, 0.2)
    ch.name = f"WaitingChair_{i+1}"
    matc = bpy.data.materials.new(f"ChairMat_{i+1}")
    matc.diffuse_color = (0.6,0.3,0.3,1)
    ch.data.materials.append(matc)
    waiting_chairs.append(ch)

# Exit point (left)
exit_point = Vector((-4.0, 0.0, 0.0))

# Function to create a client object (colored sphere)
def create_client(i):
    color = (random.uniform(0.2,0.9), random.uniform(0.2,0.9), random.uniform(0.2,0.9), 1)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(6.0, 3.0, 0.25))
    obj = bpy.context.active_object
    obj.name = f"Client_{i+1}"
    m = bpy.data.materials.new(f"ClientMat_{i+1}")
    m.diffuse_color = color
    obj.data.materials.append(m)
    return obj

# Helper: insert location keyframe for object
def key_location(obj, frame, loc):
    obj.location = loc
    obj.keyframe_insert(data_path="location", frame=frame)

# Helper: insert rotation keyframe (for scissors animation)
def key_rotation(obj, frame, rot_euler):
    obj.rotation_euler = Euler(rot_euler, 'XYZ')
    obj.keyframe_insert(data_path="rotation_euler", frame=frame)

# Simulation logic (deterministic scheduler)
clients = []
waiting_queue = []  # indices of clients on waiting chairs
chair_positions = [Vector((start_x, start_y - i*gap, 0.35)) for i in range(NUM_CHAIRS)]
barber_position = Vector((0,0.0,0.45))
arrival_frame = 10  # the frame first client arrives (small offset)
current_frame = arrival_frame
barber_free_at = 0
next_waiting_index = 0

# Create clients and schedule their animations
for i in range(NUM_CLIENTS):
    c = create_client(i)
    clients.append(c)

# We'll simulate arrival by iterating clients and setting keyframes
frame = arrival_frame
for idx, client_obj in enumerate(clients):
    # client arrives from far right to entry point
    entry_pos = Vector((4.5, 3.0 - idx*0.05, 0.25))
    key_location(client_obj, frame-5, entry_pos + Vector((1.0,0,0)))  # before arrival
    key_location(client_obj, frame, entry_pos)
    
    # Check waiting room availability
    if len(waiting_queue) < NUM_CHAIRS and frame >= barber_free_at:
        # If barber is free AND no one waiting, client goes straight to barber
        # But we still check logically: if waiting_queue empty and barber_free_at <= frame, go to barber.
        if len(waiting_queue) == 0 and frame >= barber_free_at:
            # go to barber immediately
            to_barber_frame = frame + 5
            key_location(client_obj, to_barber_frame, barber_position)
            # start haircut
            cut_start = to_barber_frame + 1
            cut_end = cut_start + HAIRCUT_DURATION
            # animate scissors during haircut
            # add small up/down rotation for scissor
            key_rotation(scissors, cut_start, (0,0,math.radians(-20)))
            key_rotation(scissors, cut_start + HAIRCUT_DURATION//3, (0,0,math.radians(20)))
            key_rotation(scissors, cut_start + 2*HAIRCUT_DURATION//3, (0,0,math.radians(-20)))
            key_rotation(scissors, cut_end, (0,0,0))
            # after haircut client leaves to exit
            leave_frame = cut_end + 5
            key_location(client_obj, leave_frame, exit_point)
            # mark barber busy until cut_end
            barber_free_at = cut_end + 1
        else:
            # sit in next waiting chair
            idx_chair = len(waiting_queue)
            target = chair_positions[idx_chair]
            approach_frame = frame + 10
            key_location(client_obj, approach_frame, target)
            waiting_queue.append(client_obj)
            # they will wait until their turn
    else:
        # waiting room full -> client leaves
        leave_frame = frame + 10
        key_location(client_obj, leave_frame, exit_point)
        # color the client slightly greyed to indicate turned-away
        mat = client_obj.data.materials[0]
        mat.diffuse_color = (0.4,0.4,0.4,1)
    
    # After each arrival, try to process waiting queue if barber is free
    # If barber is free and someone is waiting, move first waiting to barber
    # We schedule processing as soon as barber_free_at allows
    while len(waiting_queue) > 0 and barber_free_at <= frame:
        waiter = waiting_queue.pop(0)
        # animate waiter moving to barber
        move_frame = barber_free_at + 5
        key_location(waiter, move_frame, barber_position)
        # haircut period
        cut_start = move_frame + 1
        cut_end = cut_start + HAIRCUT_DURATION
        # animate scissors
        key_rotation(scissors, cut_start, (0,0,math.radians(-20)))
        key_rotation(scissors, cut_start + HAIRCUT_DURATION//3, (0,0,math.radians(20)))
        key_rotation(scissors, cut_start + 2*HAIRCUT_DURATION//3, (0,0,math.radians(-20)))
        key_rotation(scissors, cut_end, (0,0,0))
        # leave
        leave_frame = cut_end + 5
        key_location(waiter, leave_frame, exit_point)
        barber_free_at = cut_end + 1
        # shift remaining waiting clients forward to fill seats (animate them moving forward)
        for j, remaining in enumerate(waiting_queue):
            newpos = chair_positions[j]
            shift_frame = move_frame + 2
            key_location(remaining, shift_frame, newpos)
    # increment frame for next client arrival
    frame += ARRIVAL_INTERVAL

# If barber is still idle and there are waiting clients after loop, process them
while len(waiting_queue) > 0:
    waiter = waiting_queue.pop(0)
    move_frame = barber_free_at + 5
    key_location(waiter, move_frame, barber_position)
    cut_start = move_frame + 1
    cut_end = cut_start + HAIRCUT_DURATION
    key_rotation(scissors, cut_start, (0,0,math.radians(-20)))
    key_rotation(scissors, cut_start + HAIRCUT_DURATION//3, (0,0,math.radians(20)))
    key_rotation(scissors, cut_start + 2*HAIRCUT_DURATION//3, (0,0,math.radians(-20)))
    key_rotation(scissors, cut_end, (0,0,0))
    leave_frame = cut_end + 5
    key_location(waiter, leave_frame, exit_point)
    barber_free_at = cut_end + 1

# Add labels (Text objects) for barber and waiting room
def add_text(name, string, loc):
    bpy.ops.object.text_add(location=loc)
    txt = bpy.context.active_object
    txt.data.body = string
    txt.name = name
    txt.rotation_euler = Euler((math.radians(90), 0, 0), 'XYZ')
    txt.scale = (0.2,0.2,0.2)
    return txt

add_text("Label_Barber", "Barber", (0, -1.6, 0.05))
add_text("Label_Wait", "Waiting chairs", (start_x - 0.6, start_y + 0.4, 0.05))

# Camera
bpy.ops.object.camera_add(location=(8, -2, 5), rotation=(math.radians(60), 0, math.radians(110)))
cam = bpy.context.active_object
scene.camera = cam

# Light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))
sun = bpy.context.active_object
sun.data.energy = 2.0

# Set interpolation to linear for more mechanical movement
def set_linear_fcurves(obj):
    if not obj.animation_data:
        return
    action = obj.animation_data.action
    if not action:
        return
    if not hasattr(action, "fcurves"):
        return
    if action.fcurves is None:
        return
    if len(action.fcurves) == 0:
        return

    for fcu in action.fcurves:
        if not hasattr(fcu, "keyframe_points"):
            continue
        for kf in fcu.keyframe_points:
            kf.interpolation = 'LINEAR'



for ob in bpy.data.objects:
    set_linear_fcurves(ob)


print("Barbershop animation created. Timeline frames: {} to {}.".format(scene.frame_start, scene.frame_end))