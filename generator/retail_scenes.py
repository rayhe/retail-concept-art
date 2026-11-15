# Procedural retail wall-art pieces for Blender Cycles. Each seed picks a palette and a layout, so every render is new.
#   blender -b --factory-startup --python-exit-code 3 -P retail_scenes.py -- --piece arches --seed 7 --out C:\x\a.png
# Pieces: arches, podiums, ribbons, monoliths, spheres, waves. --device cpu with --scale 0.15 is a quick smoke test.
# --loop-frames N renders a seamless loop instead: N PNG frames into the --out directory (f_0001.png ...), sized so
# the short side is --video-short pixels. Frame 1 is the still; frame N+1 would be frame 1 again. Existing frames
# are kept, so an interrupted loop resumes where it stopped.
import argparse
import math
import os
import random
import sys
import time

import bpy
from mathutils import Vector

TAU = 2 * math.pi
ANIMS = []                # loop mode: callables fn(theta), theta = TAU * (frame - 1) / frames
ARNG = random.Random(0)   # motion parameters; separate from the scene RNG so stills stay reproducible


def animate(fn):
    ANIMS.append(fn)
    return fn


def wobble(amp, phase, th, mult=1):
    # A sinusoid that is exactly 0 at theta = 0 (frame 1 matches the still) and closes after one loop.
    return amp * (math.sin(mult * th + phase) - math.sin(phase))


def parse_args():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument('--piece', required=True)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', required=True)
    ap.add_argument('--samples', type=int, default=384)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--device', choices=['gpu', 'cpu'], default='gpu')
    ap.add_argument('--loop-frames', type=int, default=0)
    ap.add_argument('--fps', type=int, default=30)
    ap.add_argument('--video-short', type=int, default=1080)
    return ap.parse_args(argv)


# ---------- colour ----------

def lin(h, a=1.0):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (a,)


PALETTES = {
    'sand':   dict(bg='#E8DCCB', a='#C2643F', b='#8F9C7A', c='#F5EFE6', d='#3E3A36'),
    'blush':  dict(bg='#F2D7D2', a='#C97C7C', b='#E8B36B', c='#FBF6F2', d='#5A3B3B'),
    'ocean':  dict(bg='#CFE3E8', a='#1F5466', b='#F07F68', c='#F7FAFA', d='#0F2A33'),
    'noir':   dict(bg='#2A2A2E', a='#C9A15B', b='#2F6B5A', c='#EDE6DA', d='#0B0B0C'),
    'citrus': dict(bg='#FBEFD3', a='#F2913D', b='#5C8A4A', c='#FFFDF7', d='#3A3226'),
    'lilac':  dict(bg='#E3DDF0', a='#7A62B3', b='#F2C14E', c='#FAF8FD', d='#2E2640'),
}
GOLD = (1.0, 0.766, 0.336, 1.0)


# ---------- materials ----------

ALIASES = {
    'base': ['Base Color'], 'metal': ['Metallic'], 'rough': ['Roughness'], 'ior': ['IOR'],
    'transmission': ['Transmission Weight', 'Transmission'], 'coat': ['Coat Weight', 'Clearcoat'],
    'sheen': ['Sheen Weight', 'Sheen'], 'film': ['Thin Film Thickness'], 'film_ior': ['Thin Film IOR'],
    'dispersion': ['Dispersion'], 'emit': ['Emission Color', 'Emission'], 'emit_strength': ['Emission Strength'],
}


def setin(node, key, value):
    for name in ALIASES.get(key, [key]):
        sock = node.inputs.get(name)
        if sock is not None:
            sock.default_value = value
            return True
    return False


def principled(name, **inputs):
    m = bpy.data.materials.new(name)
    if m.node_tree is None:
        m.use_nodes = True
    nt = m.node_tree
    out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'), None) or nt.nodes.new('ShaderNodeOutputMaterial')
    p = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if p is None:
        p = nt.nodes.new('ShaderNodeBsdfPrincipled')
        nt.links.new(p.outputs[0], out.inputs['Surface'])
    for k, v in inputs.items():
        setin(p, k, v)
    return m, p


def matte(c, rough=0.8):
    return principled('matte', base=c, rough=rough)[0]


def plaster(c, rough=0.85, bump=0.12):
    m, p = principled('plaster', base=c, rough=rough)
    nt = m.node_tree
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 45.0
    noise.inputs['Detail'].default_value = 8.0
    b = nt.nodes.new('ShaderNodeBump')
    b.inputs['Strength'].default_value = bump
    nt.links.new(noise.outputs['Fac'], b.inputs['Height'])
    nt.links.new(b.outputs['Normal'], p.inputs['Normal'])
    return m


def marble(c1, c2, scale=1.6):
    m, p = principled('marble', rough=0.22, coat=0.4)
    nt = m.node_tree
    tc = nt.nodes.new('ShaderNodeTexCoord')
    wave = nt.nodes.new('ShaderNodeTexWave')
    wave.inputs['Scale'].default_value = scale
    wave.inputs['Distortion'].default_value = 12.0
    wave.inputs['Detail'].default_value = 8.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    els = ramp.color_ramp.elements
    vein = tuple(0.45 * a + 0.55 * b for a, b in zip(c1, c2))   # soft grey-ish veins, not stripes
    els[0].position, els[0].color = 0.0, vein
    els[1].position, els[1].color = 0.05, c1
    nt.links.new(tc.outputs['Object'], wave.inputs['Vector'])
    nt.links.new(wave.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], p.inputs['Base Color'])
    return m


def metal(c=GOLD, rough=0.25):
    return principled('metal', base=c, metal=1.0, rough=rough)[0]


def glass(c=(1, 1, 1, 1), rough=0.02, ior=1.5):
    m, p = principled('glass', base=c, transmission=1.0, rough=rough, ior=ior)
    setin(p, 'dispersion', 0.35)
    return m


def satin(c):
    return principled('satin', base=c, rough=0.32, sheen=0.7, coat=0.25)[0]


def iridescent(rng):
    m, p = principled('irid', base=(0.92, 0.92, 0.95, 1), metal=1.0, rough=rng.uniform(0.12, 0.25))
    setin(p, 'film', rng.uniform(280, 720))
    setin(p, 'film_ior', 1.45)
    return m


# ---------- scene helpers ----------

def clear_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def mesh_obj(name, verts, faces, mat=None, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if smooth:
        for poly in me.polygons:
            poly.use_smooth = True
    if mat:
        me.materials.append(mat)
    return link(bpy.data.objects.new(name, me))


def add(kind, mat=None, smooth=True, bevel=0.0, **kw):
    getattr(bpy.ops.mesh, f'primitive_{kind}_add')(**kw)
    ob = bpy.context.active_object
    if mat:
        ob.data.materials.append(mat)
    if smooth:
        for poly in ob.data.polygons:
            poly.use_smooth = True
    if bevel:
        bv = ob.modifiers.new('bevel', 'BEVEL')
        bv.width, bv.segments, bv.limit_method = bevel, 4, 'ANGLE'
    if smooth and kind in ('cube', 'cylinder', 'cone'):
        es = ob.modifiers.new('split', 'EDGE_SPLIT')
        es.split_angle = math.radians(30)
    return ob


def look_at(ob, target):
    ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()


def camera(loc, target, lens=50, fstop=None):
    cd = bpy.data.cameras.new('cam')
    cd.lens = lens
    cam = link(bpy.data.objects.new('cam', cd))
    cam.location = loc
    look_at(cam, target)
    if fstop:
        cd.dof.use_dof = True
        cd.dof.focus_distance = (Vector(target) - Vector(loc)).length
        cd.dof.aperture_fstop = fstop
    bpy.context.scene.camera = cam
    return cam


def light(kind, loc, target=None, energy=1000.0, color=(1, 1, 1), size=2.0, angle=None):
    ld = bpy.data.lights.new(kind, kind)
    ld.energy, ld.color = energy, color
    if kind == 'AREA':
        ld.size = size
    if kind == 'SUN' and angle is not None:
        ld.angle = angle
    ob = link(bpy.data.objects.new(kind.lower(), ld))
    ob.location = loc
    if kind == 'AREA':
        ob.visible_camera = False   # light the set without showing a glowing panel in frame
    if target is not None:
        look_at(ob, target)
    return ob


def world(c, strength):
    w = bpy.data.worlds.new('world')
    bpy.context.scene.world = w
    if w.node_tree is None:
        w.use_nodes = True
    nt = w.node_tree
    out = next((n for n in nt.nodes if n.type == 'OUTPUT_WORLD'), None) or nt.nodes.new('ShaderNodeOutputWorld')
    bg = next((n for n in nt.nodes if n.type == 'BACKGROUND'), None)
    if bg is None:
        bg = nt.nodes.new('ShaderNodeBackground')
        nt.links.new(bg.outputs[0], out.inputs['Surface'])
    bg.inputs['Color'].default_value = c
    bg.inputs['Strength'].default_value = strength


def cyclorama(mat, width=30.0, depth=20.0, height=14.0, radius=2.5, y_wall=6.0):
    # Seamless floor-to-wall sweep, the photo-studio backdrop.
    prof = [(-depth, 0.0)]
    cy, cz = y_wall - radius, radius
    for i in range(17):
        a = -math.pi / 2 + (math.pi / 2) * i / 16
        prof.append((cy + radius * math.cos(a), cz + radius * math.sin(a)))
    prof.append((y_wall, height))
    verts = [(x, y, z) for y, z in prof for x in (-width / 2, width / 2)]
    faces = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(len(prof) - 1)]
    return mesh_obj('cyc', verts, faces, mat)


def arch(W, H, w, h, depth, mat, loc, rot_z=0.0):
    # A wall slab with a round-topped opening down to the floor, built as one filled 2D outline.
    cu = bpy.data.curves.new('arch', 'CURVE')
    cu.dimensions, cu.fill_mode, cu.extrude = '2D', 'BOTH', depth / 2
    r = w / 2
    pts = [(-W / 2, 0), (-r, 0), (-r, h - r)]
    pts += [(r * math.cos(a), h - r + r * math.sin(a)) for a in [math.pi - math.pi * i / 24 for i in range(1, 24)]]
    pts += [(r, h - r), (r, 0), (W / 2, 0), (W / 2, H), (-W / 2, H)]
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, (x, y) in zip(sp.points, pts):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    cu.materials.append(mat)
    ob = link(bpy.data.objects.new('arch', cu))
    ob.location = loc
    ob.rotation_euler = (math.pi / 2, 0, rot_z)
    return ob


# ---------- pieces ----------
# Each returns (resolution, sample multiplier).

def piece_arches(rng, P):
    world(lin(P['bg']), 0.35)
    cyclorama(plaster(lin(P['bg'])), y_wall=9.0, height=16.0)
    arch_mat = plaster(lin(rng.choice([P['c'], P['bg'], P['a']])))
    n = rng.choice([3, 4, 5])
    if rng.random() < 0.5:   # a colonnade across the frame
        span, H = rng.uniform(2.6, 3.4), rng.uniform(4.5, 6.0)
        for i in range(n):
            arch(span, H, span * 0.62, H * 0.72, 0.6, arch_mat, ((i - (n - 1) / 2) * span, 3.0, 0))
    else:                    # a corridor receding into the set
        for i in range(n):
            arch(6.5, 6.0, 3.2, 4.6, 0.5, arch_mat, (0, -1.0 + i * 2.4, 0))
    add('uv_sphere', matte(lin(P['a']), 0.6), radius=rng.uniform(0.5, 0.8), segments=96, ring_count=48,
        location=(rng.uniform(-2.0, 2.0), -3.0, 0.65))
    pot = add('cylinder', matte(lin(P['b']), 0.7), bevel=0.03, radius=0.55, depth=1.1, vertices=96,
              location=(rng.uniform(-3, 3), -2.0, 0.55))
    add('cone', matte(lin(P['b']), 0.7), radius1=0.45, depth=2.6, vertices=96,
        location=(pot.location.x, pot.location.y, 2.4))
    sun = light('SUN', (0, 0, 10), energy=rng.uniform(3.5, 5.0), color=(1.0, 0.9, 0.78), angle=math.radians(0.6))
    sun.rotation_euler = (math.radians(rng.uniform(52, 66)), 0, math.radians(rng.choice([-1, 1]) * rng.uniform(25, 55)))
    camera((rng.uniform(-3, 3), -15, rng.uniform(2.0, 3.5)), (0, 3, 2.6), lens=50)
    # Loop: the sun swings back and forth, sliding the shadows through the arches.
    rx0, rz0 = sun.rotation_euler.x, sun.rotation_euler.z
    az, el, ph = math.radians(ARNG.uniform(8, 12)), math.radians(ARNG.uniform(2, 4)), ARNG.uniform(0, TAU)
    animate(lambda th: setattr(sun, 'rotation_euler', (rx0 + wobble(el, ph, th, 2), 0, rz0 + wobble(az, 0, th))))
    return (2400, 3000), 1.0


def piece_podiums(rng, P):
    world(lin(P['bg']), 0.4)
    cyclorama(matte(lin(P['bg']), 0.9), y_wall=4.0)
    mats = [marble(lin(P['c']), lin(P['d'])), matte(lin(P['a']), 0.6), matte(lin(P['b']), 0.6), metal(GOLD, 0.3)]
    placed = []
    for _ in range(rng.choice([3, 4, 5])):
        for _ in range(200):
            r = rng.uniform(0.35, 0.9)
            x, y = rng.uniform(-1.8, 1.8), rng.uniform(-1.2, 1.2)
            if all(math.hypot(x - px, y - py) > r + pr + 0.08 for px, py, pr, _ in placed):
                break
        h = rng.uniform(0.25, 1.6)
        add('cylinder', rng.choice(mats), bevel=0.02, radius=r, depth=h, vertices=128, location=(x, y, h / 2))
        placed.append((x, y, r, h))
    toppers = [
        lambda x, y, z, s: add('uv_sphere', glass(lin(P['c'])), radius=s, segments=96, ring_count=48, location=(x, y, z + s)),
        lambda x, y, z, s: add('torus', metal(GOLD, 0.2), major_radius=s, minor_radius=s * 0.22,
                               major_segments=128, minor_segments=48, location=(x, y, z + s * 1.22), rotation=(math.pi / 2, 0, 0)),
        lambda x, y, z, s: add('cube', matte(lin(P['a']), 0.5), bevel=0.02, size=s * 1.3,
                               location=(x, y, z + s * 0.92), rotation=(0, 0, math.radians(rng.uniform(15, 45)))),
    ]
    spinners = []
    for (x, y, r, h) in rng.sample(placed, k=min(len(placed), rng.choice([1, 2, 3]))):
        top = rng.choice(toppers)(x, y, h, min(r * 0.7, 0.45))
        # Loop: rings turn half a turn and cubes a quarter turn, which brings each back onto itself.
        turn = {'Torus': math.pi, 'Cube': math.pi / 2}.get(top.name.split('.')[0])
        if turn:
            spinners.append((top, top.rotation_euler.copy(), turn * ARNG.choice([-1, 1])))
    light('AREA', (-4, -5, 6), (0, 0, 0.8), energy=1600, size=3.5, color=(1.0, 0.95, 0.9))
    light('AREA', (5, 3, 4), (0, 0, 0.8), energy=700, size=2.0, color=(0.9, 0.95, 1.0))
    cam = camera((rng.uniform(-1.5, 1.5), -9.5, rng.uniform(1.6, 2.6)), (0, 0, 0.9), lens=70, fstop=4.0)
    # Loop: the camera sways around the display and back.
    tgt, rel, yaw = Vector((0, 0, 0.9)), cam.location - Vector((0, 0, 0.9)), math.radians(ARNG.uniform(5, 7))

    def podium_frame(th):
        a = wobble(yaw, 0, th)
        c, s = math.cos(a), math.sin(a)
        cam.location = tgt + Vector((rel.x * c - rel.y * s, rel.x * s + rel.y * c, rel.z))
        look_at(cam, tgt)
        for ob, rot0, turn in spinners:
            ob.rotation_euler = (rot0.x, rot0.y, rot0.z + turn * th / TAU)
    animate(podium_frame)
    return (2400, 3000), 1.0


def piece_ribbons(rng, P):
    world(lin(P['bg']), 0.3)
    cyclorama(matte(lin(P['bg']), 0.85), y_wall=5.0)
    cols = [P['a'], P['b'], P['c'], P['d']]
    for k in range(rng.choice([3, 4, 5, 6])):
        cu = bpy.data.curves.new('ribbon', 'CURVE')
        # 256 points per span: at 48 the edges show saw teeth wherever a ribbon twists
        cu.dimensions, cu.resolution_u, cu.extrude = '3D', 256, rng.uniform(0.18, 0.42)
        sp = cu.splines.new('BEZIER')
        sp.use_smooth = True
        n = rng.choice([6, 7, 8])
        sp.bezier_points.add(n - 1)
        z, y = rng.uniform(1.0, 4.4), rng.uniform(-1.5, 1.5)
        for i, bp in enumerate(sp.bezier_points):
            z = min(4.6, max(0.6, z + rng.uniform(-1.1, 1.1)))
            y = min(1.8, max(-1.8, y + rng.uniform(-0.8, 0.8)))
            bp.co = (-6.5 + 13.0 * i / (n - 1), y, z)
            bp.handle_left_type = bp.handle_right_type = 'AUTO'
            bp.tilt = rng.uniform(-math.pi, math.pi)
        cu.materials.append(metal(GOLD, 0.25) if k == 0 and rng.random() < 0.4 else satin(lin(rng.choice(cols))))
        link(bpy.data.objects.new('ribbon', cu))
        # Loop: a slow wave travels along each ribbon, lifting, drifting and twisting it.
        pts = [(bp, bp.co.copy(), bp.tilt) for bp in sp.bezier_points]
        az, ay, at = ARNG.uniform(0.15, 0.3), ARNG.uniform(0.08, 0.18), ARNG.uniform(0.25, 0.5)
        p0, step, d = ARNG.uniform(0, TAU), ARNG.uniform(0.6, 1.2), ARNG.choice([-1, 1])

        def ribbon_frame(th, pts=pts, az=az, ay=ay, at=at, p0=p0, step=step, d=d):
            for i, (bp, co0, t0) in enumerate(pts):
                ph = p0 + step * i
                bp.co = (co0.x, co0.y + wobble(ay, ph + 1.3, d * th), co0.z + wobble(az, ph, d * th))
                bp.tilt = t0 + wobble(at, ph + 0.7, d * th)
        animate(ribbon_frame)
    light('AREA', (-6, -6, 5), (0, 0, 2.5), energy=2200, size=5.0, color=(1.0, 0.86, 0.72))
    light('AREA', (6, -5, 4), (0, 0, 2.5), energy=1600, size=5.0, color=(0.74, 0.84, 1.0))
    light('AREA', (0, 4, 7), (0, 0, 2.5), energy=600, size=3.0)
    camera((0, -14, 2.8), (0, 0, 2.6), lens=60)
    return (3840, 2160), 1.0


def piece_monoliths(rng, P):
    # A light wall washed with two coloured pools; the glass slabs refract and split those colours.
    bgc = lin(P['c'] if rng.random() < 0.5 else P['bg'])
    world(bgc, 0.3)
    cyclorama(principled('floor', base=bgc, rough=0.3)[0], y_wall=4.0, height=12.0)
    n = rng.choice([4, 5, 6, 7])
    for i in range(n):
        ang = math.radians(-50 + 100 * i / (n - 1) + rng.uniform(-6, 6))
        w, h = rng.uniform(0.5, 1.0), rng.uniform(1.2, 2.8)
        tint = lin(rng.choice([P['c'], P['a'], P['b']]))
        tint = tuple(0.65 + 0.35 * t for t in tint[:3]) + (1.0,)
        ob = add('cube', glass(tint, rough=rng.choice([0.0, 0.0, 0.08])), bevel=0.01, size=1.0,
                 location=(3.0 * math.sin(ang), 3.0 * math.cos(ang) - 2.2, h / 2))
        ob.scale = (w, 0.06, h)
        ob.rotation_euler = (0, 0, -ang + math.radians(rng.uniform(-20, 20)))
        # Loop: each slab turns a few degrees and back, so the refracted colours shift.
        rz0, amp, ph = ob.rotation_euler.z, math.radians(ARNG.uniform(5, 9)), ARNG.uniform(0, TAU)
        animate(lambda th, ob=ob, rz0=rz0, amp=amp, ph=ph: setattr(ob.rotation_euler, 'z', rz0 + wobble(amp, ph, th)))
    for col, x in ((P['a'], -2.2), (P['b'], 2.2)):
        c = lin(col)
        lt = light('AREA', (x * 1.6, 0.5, 0.6), (x, 4.0, 2.5), energy=rng.uniform(1500, 2500), size=1.0, color=c[:3])
        # Loop: the two coloured pools wander across the wall and back.
        ax, azz, px, pz = ARNG.uniform(1.0, 1.6), ARNG.uniform(0.4, 0.8), ARNG.uniform(0, TAU), ARNG.uniform(0, TAU)
        animate(lambda th, lt=lt, x=x, ax=ax, azz=azz, px=px, pz=pz:
                look_at(lt, (x + wobble(ax, px, th), 4.0, 2.5 + wobble(azz, pz, th, 2))))
    light('AREA', (0, -6, 6), (0, 0, 1), energy=500, size=4.0)
    sc = bpy.context.scene
    sc.cycles.caustics_refractive = sc.cycles.caustics_reflective = True
    camera((rng.uniform(-1, 1), -8.5, 1.7), (0, 0, 1.1), lens=50)
    return (2400, 3000), 1.6


def piece_spheres(rng, P):
    world(lin(P['bg']), 0.45)
    cyclorama(matte(lin(P['bg']), 0.9), y_wall=10.0, height=20.0)
    mats = [metal(GOLD, 0.22), matte(lin(P['a']), 0.55), matte(lin(P['b']), 0.55), matte(lin(P['c']), 0.6),
            glass(lin(P['c']), rough=0.25), iridescent(rng)]
    weights = [2, 3, 3, 2, 1, 1]
    N = rng.randint(45, 90)
    base, c = rng.uniform(0.32, 0.45), rng.uniform(0.42, 0.55)
    golden = math.radians(137.508)
    for i in range(1, N + 1):
        s = base * (1.0 - 0.65 * i / N)
        r = c * math.sqrt(i)
        add('uv_sphere', rng.choices(mats, weights)[0], radius=s, segments=64, ring_count=32,
            location=(r * math.cos(i * golden), r * math.sin(i * golden), s))
    sun = light('SUN', (0, 0, 10), energy=rng.uniform(3.0, 4.5), color=(1.0, 0.94, 0.86), angle=math.radians(4))
    sun.rotation_euler = (math.radians(rng.uniform(30, 45)), 0, math.radians(rng.uniform(-60, 60)))
    # Loop: the sun swings round, so the shadows sweep across the garden and back.
    rx0, rz0 = sun.rotation_euler.x, sun.rotation_euler.z
    az, el = math.radians(ARNG.uniform(30, 40)), math.radians(ARNG.uniform(3, 5))
    animate(lambda th: setattr(sun, 'rotation_euler', (rx0 + wobble(el, math.pi / 2, th), 0, rz0 + wobble(az, 0, th))))
    if rng.random() < 0.5:
        camera((0, -0.01, 13.0), (0, 0, 0), lens=50)
        return (3000, 3000), 1.0
    camera((0, -9.5, 6.5), (0, 0, 0), lens=50)
    return (2400, 3000), 1.0


def piece_waves(rng, P):
    # Dark silk: a deep set with coloured light grazing the folds.
    world(lin(P['d']), 0.2)
    nx, ny = 300, 300
    x0, x1, y0, y1 = -9.0, 9.0, -4.0, 14.0
    terms = [(rng.uniform(0.08, 0.3), rng.uniform(0.5, 1.8), rng.uniform(-0.7, 0.7), rng.uniform(0, 6.3)) for _ in range(5)]

    def height(x, y):
        return sum(a * math.sin(k * (x * math.cos(t) + y * math.sin(t)) + ph) for a, k, t, ph in terms)

    verts = []
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        for i in range(nx + 1):
            x = x0 + (x1 - x0) * i / nx
            verts.append((x, y, height(x, y)))
    faces = [(j * (nx + 1) + i, j * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i)
             for j in range(ny) for i in range(nx)]
    mat = iridescent(rng) if rng.random() < 0.3 else satin(lin(rng.choice([P['c'], P['bg']])))
    ob = mesh_obj('waves', verts, faces, mat)
    # Loop: every fold travels a whole number of wavelengths, so the silk rolls and returns to where it began.
    import numpy as np
    X, Y = np.meshgrid(np.linspace(x0, x1, nx + 1), np.linspace(y0, y1, ny + 1))
    speeds = [ARNG.choice([-1, 1]) * (2 if k > 1.3 else 1) for _, k, _, _ in terms]
    me = ob.data

    def wave_frame(th):
        Z = sum(a * np.sin(k * (X * math.cos(t) + Y * math.sin(t)) + ph + m * th) for (a, k, t, ph), m in zip(terms, speeds))
        me.vertices.foreach_set('co', np.stack([X, Y, Z], axis=-1).astype(np.float32).ravel())
        me.update()
    animate(wave_frame)
    sub = ob.modifiers.new('subd', 'SUBSURF')
    sub.levels, sub.render_levels = 0, 1
    a, b = lin(P['a']), lin(P['b'])
    light('AREA', (-8, 2, 2.0), (0, 4, 0), energy=rng.uniform(3000, 4500), size=4.0, color=a[:3])
    light('AREA', (8, 7, 2.5), (0, 4, 0), energy=rng.uniform(2500, 4000), size=4.0, color=b[:3])
    light('AREA', (0, 10, 6), (0, 3, 0), energy=900, size=8.0, color=(1.0, 0.97, 0.94))
    camera((rng.uniform(-1.5, 1.5), -7.5, rng.uniform(2.4, 3.4)), (0, 4, 0.0), lens=45)
    return (3840, 2160), 1.0


PIECES = {f.__name__.removeprefix('piece_'): f for f in
          (piece_arches, piece_podiums, piece_ribbons, piece_monoliths, piece_spheres, piece_waves)}


# ---------- render ----------

def use_gpu():
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for kind in ('OPTIX', 'CUDA'):
        try:
            prefs.compute_device_type = kind
        except TypeError:
            continue
        (prefs.refresh_devices if hasattr(prefs, 'refresh_devices') else prefs.get_devices)()
        gpus = [d for d in prefs.devices if d.type == kind]
        if gpus:
            for d in prefs.devices:
                d.use = d.type == kind
            print('DEVICES', kind, [(d.name, d.id) for d in gpus], flush=True)
            return
    raise SystemExit('no CUDA/OptiX device visible to Cycles')


def setup_render(res, samples, scale, device):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'GPU' if device == 'gpu' else 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.01
    sc.cycles.use_denoising = True
    for attr, val in (('denoiser', 'OPENIMAGEDENOISE'), ('denoising_use_gpu', device == 'gpu')):
        if hasattr(sc.cycles, attr):
            setattr(sc.cycles, attr, val)
    sc.render.resolution_x, sc.render.resolution_y = max(64, int(res[0] * scale)), max(64, int(res[1] * scale))
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'
    try:
        sc.view_settings.view_transform = 'AgX'
        for look in ('AgX - Medium High Contrast', 'Medium High Contrast'):
            try:
                sc.view_settings.look = look
                break
            except TypeError:
                pass
    except TypeError:
        pass


def setup_loop(sc, frames, fps, out):
    os.makedirs(out, exist_ok=True)
    sc.render.filepath = os.path.join(out, 'f_####')
    sc.frame_start, sc.frame_end = 1, frames
    sc.render.fps = fps
    sc.render.use_overwrite = False     # resume: frames already on disk are skipped
    sc.render.use_placeholder = False   # a crash must not leave an empty file that later counts as done
    sc.render.use_persistent_data = True
    sc.render.use_lock_interface = True
    sc.render.image_settings.compression = 15

    def on_frame(scene, *_):
        th = TAU * (scene.frame_current - 1) / frames
        for fn in ANIMS:
            fn(th)
    bpy.app.handlers.frame_change_pre.append(on_frame)


def main():
    global ARNG
    a = parse_args()
    rng = random.Random(a.seed)
    ARNG = random.Random(f'loop-{a.seed}')
    clear_scene()
    pal = rng.choice(sorted(PALETTES))
    if a.device == 'gpu':
        use_gpu()
    res, mult = PIECES[a.piece](rng, PALETTES[pal])
    setup_render(res, int(a.samples * mult), a.scale, a.device)
    sc = bpy.context.scene
    if a.loop_frames:
        s = a.video_short / min(res)
        sc.render.resolution_x, sc.render.resolution_y = (round(v * s) // 2 * 2 for v in res)   # even, for H.264
        setup_loop(sc, a.loop_frames, a.fps, a.out)
    else:
        sc.render.filepath = a.out
    print('PIECE', a.piece, 'seed', a.seed, 'palette', pal, 'res', sc.render.resolution_x, sc.render.resolution_y,
          'samples', sc.cycles.samples, flush=True)
    t = time.time()
    if a.loop_frames:
        print('LOOP', a.loop_frames, 'frames at', a.fps, 'fps', flush=True)
        bpy.ops.render.render(animation=True)
    else:
        bpy.ops.render.render(write_still=True)
    print('RENDER_SECONDS', round(time.time() - t, 1), flush=True)


main()
