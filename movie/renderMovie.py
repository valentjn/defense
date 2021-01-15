#!/usr/bin/python3
# use with Blender 2.79, not compatible with Blender 2.80

import platform

import numpy as np

import blender
import part1
import part2
import part3

import bpy
import mathutils



def main():
  rad = blender.rad
  doRender = (platform.node() != "lapsgs12")
  
  # clear everything
  blender.select(bpy.data.objects)
  bpy.ops.object.delete()
  
  # scene
  scene = bpy.context.scene
  
  # camera
  camLoc, camRot = (0, -11, 2), rad(79.8, 0, 0)
  bpy.ops.object.camera_add(location=camLoc, rotation=camRot)
  cam = bpy.context.object
  scene.camera = cam
  
  # light
  bpy.ops.object.lamp_add(type="SUN", radius=1, location=(0, -11, 10),
                          rotation=rad(30, 0, 30))
  #bpy.ops.object.light_add(type="SUN", radius=1, location=(0, 0, 10),
  #                         rotation=rad(30, 0, 0))
  
  # animation
  ani = blender.Animation(24)
  objLogo = blender.addLogo((0, 0, 0), n=9)
  circles = objLogo.children
  circleLocs = [np.array(obj.location) for obj in circles]
  for obj in circles: ani.setAlpha(obj, 0)
  ani.rotate(objLogo, 0, rad(0, 0, 30))
  
  ani.rotate(objLogo, 7, rad(0, 0, 0))
  
  ani.wait(0.5)
  
  for obj in circles[:7]: ani.fadeIn(obj, 1)
  ani.wait(1)
  ani.wait(5)
  
  for q in range(3):
    I = [[0], [4, 3, 5], [1, 6, 2]][q]
    if q > 0:
      ani.rotate(objLogo, 2, rad(0, 0, [None, 30, -30][q]))
    for i in range(7):
      if i not in I: ani.fade(circles[i], 1, 0.3, wait=1)
    ani.wait(1)
    ani.wait(2)
    
    ani.move(cam, 2, circles[I[0]].location)
    ani.rotate(cam, 2, rad(90, 0, 0))
    for obj in circles[:7]: ani.fadeOut(obj, 1.8)
    ani.wait(2)
    
    part = [part1, part2, part3][q]
    part.animate(ani)
    ani.wait(1)
    
    for obj, loc in zip(circles[7:], circleLocs[7:]):
      newLoc = loc + loc / np.linalg.norm(loc, ord=2)
      ani.move(obj, 0, newLoc)
    
    ani.move(cam, 2, camLoc)
    ani.rotate(cam, 2, camRot)
    for obj in circles[:7]: ani.fadeIn(obj, 1.8, wait=0.2)
    ani.wait(2)
    ani.wait(1)
  
  ani.move(cam, 7, [1.35*x for x in camLoc])
  
  for i, obj in enumerate(circles):
    if i >= 7:
      ani.move(obj, 0.5, circleLocs[i])
      ani.fade(obj, 0.5, 0.3)
      ani.wait((2/i**0.9 if i < len(circles) - 1 else 0.5))
  
  ani.wait(-3)
  
  objMessage = blender.addLaTeX((2.9, -2, 1.6), rad(90, 0, -30), r"""%
\bfseries%
``B-splines on sparse grids\\
\hspace{0.45em}can be used to efficiently\\
\hspace{0.45em}solve high-dimensional\\
\hspace{0.45em}optimization problems with\\
\hspace{0.45em}gradient-based methods.''%
""", scale=1.2)
  ani.fadeOut(objMessage, 0)
  
  ani.rotate(cam, 1, camRot[:2] + [-13/180*np.pi])
  ani.fadeIn(objMessage, 1)
  ani.wait(1)
  
  ani.wait(5)
  
  ani.finish()
  
  # render settings
  scene.render.alpha_mode = "SKY"
  scene.world.horizon_color = mathutils.Color((1, 1, 1))
  #scene.world.color = mathutils.Color((1, 1, 1))
  scene.render.resolution_percentage = 100
  scene.render.resolution_x = 1920
  scene.render.resolution_y = 1080
  if not doRender:
    scene.render.resolution_x /= 4
    scene.render.resolution_y /= 4
  
  # 3D render settings
  scene.render.use_multiview = doRender
  scene.render.views_format = "STEREO_3D"
  scene.render.image_settings.views_format = "STEREO_3D"
  scene.camera.data.stereo.pivot = "CENTER"
  scene.camera.data.stereo.convergence_distance = 11
  scene.camera.data.stereo.interocular_distance = (
      scene.camera.data.stereo.convergence_distance / 30)
  
  # render still from last frame
  scene.frame_set(ani.frame())
  scene.render.image_settings.file_format = "PNG"
  scene.render.filepath = blender.getOutPath("image.png")
  bpy.ops.render.render(write_still=True)
  
  # render movie
  if doRender:
    scene.frame_set(1)
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.filepath = blender.getOutPath("movie.mkv")
    bpy.ops.render.render(animation=True)
  
  # UI settings
  # select camera
  blender.select([cam], active=cam)
  
  for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
      for space in area.spaces:
        if space.type == "VIEW_3D":
          # use material shading in viewport
          space.viewport_shade = "MATERIAL"
          # set 3D viewport settings
          space.show_stereo_3d_cameras = True
          space.show_stereo_3d_volume  = True
          space.stereo_3d_volume_alpha = 0
  
  blender.deleteUnusedTmpFiles()



if __name__ == "__main__":
  main()
