import pygame
from pygame.locals import *
from rt import RayTracer
from figures import *
from lights import *
from materials import *
from math import*

width = 1500
height = 650
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("cielo.png")
raytracer.rtClearColor(0.25, 0.25, 0.25)

brick = Material(diffuse=(0, 0, 1), spec=8, Ks=0.01, matType=TRANSPARENT)

grass = Material(diffuse=(0.4, 1, 0.4), spec=32, Ks=0.1,matType=REFLECTIVE)
piel = Material(diffuse=(157/255, 126/255, 61/255), spec=256, Ks=0.2, matType=OPAQUE)

white_opaque = Material(diffuse=(1, 1, 1), spec=256, Ks=0.2, matType=OPAQUE)
boxTexture=pygame.image.load("ros.jpg")
box=Material(texture=boxTexture)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, Ks=0.2, matType=OPAQUE)
glass = Material(diffuse=(0.9, 0.9, 0.9), spec=64, Ks=0.15, ior=1.5, matType=TRANSPARENT)
diamond = Material(diffuse=(0.5, 0.9, 1), spec=128, Ks=0.2, ior=2.417, matType=TRANSPARENT)
regalo = Material(diffuse=(0.5, 0.9, 1), spec=128, Ks=0.2, ior=2.417, matType=REFLECTIVE)

floor_material = Material(diffuse=(1, 0.4, 0.4), spec=8, Ks=0.01, matType=REFLECTIVE)  # Rojo
ceiling_material = Material(diffuse=(0.4, 1, 0.4), spec=32, Ks=0.1, matType=REFLECTIVE) # Verde
front_wall_material = Material(diffuse=(0.4, 0.4, 1), spec=256, Ks=0.2, matType=OPAQUE) # Azul
left_wall_material = Material(diffuse=(1, 1, 0), spec=64, Ks=0.2, matType=OPAQUE)       # Amarillo
right_wall_material = Material(diffuse=(1, 0, 1), spec=64, Ks=0.15, matType=TRANSPARENT) # Morado

boca = Material(diffuse=(197/255, 178/255, 137/255), spec=256, Ks=0.2, matType=OPAQUE)

ojos = Material(diffuse=(0, 0, 0), spec=256, Ks=0.2, matType=REFLECTIVE)



raytracer.camPosition=[0, 0.5, 0.75]
def rotation_y_matrix(angle):
    """ Devuelve una matriz de rotación alrededor del eje Y. """
    c = cos(angle)
    s = sin(angle)

    return [
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ]



horizontal_body_position = (0, 1, -4)  
horizontal_body_radii = (0.65, 0.57, 0.7) 
horizontal_body_material = brick
raytracer.scene.append(Ellipsoid(position=horizontal_body_position, radii=horizontal_body_radii, material=piel))
horizontal_body_position1 = (0, 2, -3)  
horizontal_body_radii1 = (0.256, 0.185, 0.5) 
horizontal_body_material1 = brick
raytracer.scene.append(Ellipsoid(position=horizontal_body_position1, radii=horizontal_body_radii1, material=boca))

left_ear_position = (-0.7, 1.37, -4.1)
right_ear_position = (0.7, 1.37, -4.1)
ear_radii = (0.2, 0.2, 0.2)

raytracer.scene.append(Sphere(position=left_ear_position, radius=0.3, material=boca))
raytracer.scene.append(Sphere(position=right_ear_position, radius=0.3, material=boca))
left_eye_position = (-0.18, 0.55, -1.8)
right_eye_position = (0.18, 0.55, -1.8)

raytracer.scene.append(Sphere(position=left_eye_position, radius=0.1/2, material=ojos))
raytracer.scene.append(Sphere(position=right_eye_position, radius=0.1/2, material=ojos))

nariz = Material(diffuse=(0, 0, 0), spec=256, Ks=0.2, matType=REFLECTIVE)

# Posición de la nariz
nose_position = (0, 0.4, -1.7)  
raytracer.scene.append(Sphere(position=nose_position, radius=0.05, material=nariz))

# Cuerpo del osito
body_position = (0, -0.75, -4)  
body_radii = (0.75, 0.8, 1)  
body_material = brick
raytracer.scene.append(Ellipsoid(position=body_position, radii=body_radii, material=piel))
white_belly = Material(diffuse=(1, 1, 1), spec=256, Ks=0.2, matType=OPAQUE)
belly_position = (0, 0, -3.8)  


# Brazo izquierdo
left_arm_position = (1.8, 7.5, -3.9)  
left_arm_radii = (0.5/5, 0.25/5, 0.25/5) 
left_arm_material = brick
raytracer.scene.append(Ellipsoid(position=left_arm_position, radii=left_arm_radii, material=piel))

# Brazo derecho
right_arm_position = (-1.8, 7.5, -4.1) 
right_arm_radii = (0.5/5, 0.25/5, 0.25/5) 
right_arm_material = brick
raytracer.scene.append(Ellipsoid(position=right_arm_position, radii=right_arm_radii, material=piel))

raytracer.scene.append(Ellipsoid(position=(-1.8, 2.5, -4.1), radii=(0.4/5, 0.25/5, 0.25/5), material=piel))
raytracer.scene.append(Ellipsoid(position=(1.8, 2.5, -4.1), radii=(0.4/5, 0.25/5, 0.25/5), material=piel))
# Parámetros para el OBB
obb_position = [0, 0.006, 0]  
obb_size = [0.25, 0.25, 0.25]   
obb_rotation_matrix = [ 
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]
obb_material = brick 

#raytracer.scene.append(OBB(position=obb_position, size=obb_size, rotation_matrix=obb_rotation_matrix, material=obb_material))


raytracer.scene.append(Ellipsoid(position=(4, 1, -5), radii=(0.7, 1, 1), material=Material(diffuse=(226/255, 187/255, 192/255), spec=64, Ks=0.2, matType=OPAQUE)))
raytracer.scene.append(Ellipsoid(position=(6.2, 1, -5), radii=(0.7, 1, 1.1), material=Material(diffuse=(170/255, 209/255, 210/255), spec=64, Ks=0.2, matType=OPAQUE)))
raytracer.scene.append(Ellipsoid(position=(5, 1.9, -7), radii=(1.7, 2.2, 1.7), material=Material(diffuse=(226/255, 187/255, 192/255), spec=64, Ks=0.2, matType=REFLECTIVE)))
raytracer.scene.append(Ellipsoid(position=(4, 2.5, -8), radii=(1.8, 2.4, 1.7), material=Material(diffuse=(226/255, 187/255, 192/255), spec=64, Ks=0.2, matType=OPAQUE)))
raytracer.scene.append(Ellipsoid(position=(2.2, 2, -7), radii=(1.7, 2.2, 1.7), material=Material(diffuse=(170/255, 209/255, 210/255), spec=64, Ks=0.2, matType=REFLECTIVE)))
#raytracer.scene.append(Ellipsoid(position=(7.5, 1.75, -2), radii=(0.15, 0.9, 0.9), material=Material(diffuse=(170/255, 209/255, 210/255), spec=64, Ks=0.2, matType=OPAQUE)))
raytracer.scene.append(Ellipsoid(position=(9.5, 1.8, -7), 
                                 radii=(1.3, 2.3, 1.7), 
                                 material=Material(diffuse=(158/255, 104/255, 39/255), 
                                                  spec=64, 
                                                  Ks=0.2, 
       
                                           matType=OPAQUE)))
cilindro_position = (9, 0, -8)  
cilindro_radius = 0.5/10  
cilindro_height = 8  
cilindro_material = brick  



raytracer.scene.append(ThinCylinder(position=(9, 0, -8.5), radius=0.5/10, height=8, material=white_opaque))
raytracer.scene.append(ThinCylinder(position=(9, 0, -11.5), radius=0.5/10, height=8, material=white_opaque))
raytracer.scene.append(ThinCylinder(position=(9, -1, -13), radius=0.5/10, height=8, material=white_opaque))
raytracer.scene.append(ThinCylinder(position=(9, -3, -15.5), radius=0.5/10, height=8, material=white_opaque))
raytracer.scene.append(ThinCylinder(position=(9, -4, -17.5), radius=0.5/10, height=8, material=white_opaque))
raytracer.scene.append(ThinCylinder(position=(9, 0.4, -28.75
                                              ), radius=0.5/10, height=8, material=white_opaque))
v0 = [-2.5/4, -2.5/4, 0]
v1 = [2.5/4, -2.5/4, 0]
v2 = [0, 2.5/4, 0]

#triangulo = Triangle(v0, v1, v2, brick)
#raytracer.scene.append(triangulo)


raytracer.scene.append(OBB(position=[-2, -1.25, -4], size=[2, 2, 2], rotation_matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], material=box))
raytracer.scene.append(OBB(position=[1.5, -1.25, -4], size=[2, 2, 2], rotation_matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]], material=box))

raytracer.scene.append(AABB(position=(-2.5, -2.8, -7), size=(1,1,1), material=diamond))
#raytracer.scene.append(AABB(position=(-6.5, -1.2, -7), size=(1.2,1.5,1), material=regalo))
raytracer.scene.append(AABB(position=(3.5, -2.8, -7), size=(1,1,1), material=diamond))



raytracer.lights.append(AmbientLight(intensity=0.6))
raytracer.lights.append(DirectionalLight(direction=(0, -1, 0), intensity=0.9))



raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:", pygame.time.get_ticks() / 1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

pygame.quit()
