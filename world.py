from Gen import Perlin_Noise
import numpy as np
from Render_Settings import *
import random, pygame, math

class World:
    def __init__(self):
        self.size = [0, 0]
        self.NoiseMap = []
        self.world = []

    # Generates a World using perlin_noise given the inputs and creates it into a world
    def Generate_world(self, Size=(100,100), Seed="random"):
        self.size = Size
        if Seed == "random": Seed = random.seed()
        xpix, ypix = Size
        self.NoiseMap = Perlin_Noise()


        # Turn Map into World
        arr = np.array(self.NoiseMap)
        Mean = arr.mean()

        self.world = np.where(arr > Mean, True, False)


# Recursive Function For Getting A Angle Into a range from 0 to 360
def SimplifyAngle(Angle):
    if Angle > 360:
        return SimplifyAngle(Angle - 360)
    if Angle < 0:
        return SimplifyAngle(Angle + 360)
    if Angle == 360:
        return 0
    return Angle


class Ray:
    def __init__(self, x, z, Rotation, Column_Number=None):
        self.Column_Number = Column_Number
        self.Distance_Traveled = 0

        self.x = x
        self.z = z

        # Simplify The Calcs For Less Accurate Results (Faster Still)
        self.x_vel = round(RayTrace_JumpSize * math.cos(math.radians(Rotation)), 5)
        self.z_vel = round(RayTrace_JumpSize * math.sin(math.radians(Rotation)), 5)

        if 270 > Rotation > 90:
            self.x_vel *= -1
        if 360 > Rotation > 180:
            self.z_vel *= -1





    def March(self):
        self.Distance_Traveled += 1
        self.x += self.x_vel
        self.z += self.z_vel



class Player_Camera:
    def __init__(self, World, xz=(0,0), Rotation=1):
        self.Rotation = Rotation
        self.x = xz[0]
        self.z = xz[1]

        # Take world data from 'World' Class, Should be a 2d array of Bools
        self.World_Data = World.world

        self.Debug_Map = True

    def Check_For_Collision(self, x, z):
        x //= RayTrace_TileSize
        z //= RayTrace_TileSize

        if (x < 0) or (z < 0):
            return None


        if self.World_Data[int(x)][int(z)] == True:
            return True
        return False

    def Render(self, PygameDisplay, UpdateScreen=True):
        # Generate Rays
        # Run Some Calculations and get values we need to generate the rays

        # We Add Some Big Multiple of 360 here to bodge a bug :)
        Rotation = SimplifyAngle(self.Rotation)
        FOV = RayTrace_FOV // 2
        StartingRotation = Rotation - FOV

        Angle_Differance_Between_Rays = RayTrace_FOV / RayTrace_NumberOfRays

        self.Column_Width = PygameDisplay.get_size()[0] / RayTrace_NumberOfRays
        Screen_Hight = PygameDisplay.get_size()[1]

        # Make The Rays
        self.Debug_rays = []
        self.Rays = [Ray(self.x, self.z, StartingRotation + (i * Angle_Differance_Between_Rays), self.Column_Width * i) for i in range(RayTrace_NumberOfRays)]

        if RayTrace_Debug == False or not RayTrace_DebugFast:
            PygameDisplay.fill((0,0,0))
        for Tick in range(RayTrace_Cycle_TimeOut):
            for ray in self.Rays:
                # March Ray
                ray.March()
                Result = self.Check_For_Collision(ray.x, ray.z)
                if Result == True:
                    if RayTrace_Debug == True:
                        self.Debug_rays.append(ray)

                    if RayTrace_Debug == False:
                        # Render Pixel / Column
                        pygame.draw.rect(PygameDisplay, (255 / (ray.Distance_Traveled * 2) + 10, 255 / (ray.Distance_Traveled * 2)+ 10, 255 / (ray.Distance_Traveled * 2) + 10), pygame.Rect(ray.Column_Number, 0, self.Column_Width, Screen_Hight))

                    # Remove Ray To Save Processing Power
                    self.Rays.remove(ray)


        if RayTrace_Debug == True: # Screen size is set to 100x100 for testing
            if self.Debug_Map:
                if RayTrace_DebugFast:
                    self.Debug_Map = False
                # Show Map
                x = 0
                for row in self.World_Data:
                    y = 0
                    for OBJECT in row:
                        if OBJECT == True:
                            PygameDisplay.set_at((x, y), (255, 255, 255))
                        y += 1
                    x += 1

            # Show Rays
            for ray in self.Rays:
                pygame.draw.line(PygameDisplay, (0, 0, 255), (ray.x, ray.z), (self.x, self.z))
            for ray in self.Debug_rays:
                pygame.draw.line(PygameDisplay, (0, 0, 255), (ray.x, ray.z), (self.x, self.z))

        if UpdateScreen:
            pygame.display.flip()

    def Move_Forward(self, Amount):
        x_change = Amount * math.cos(math.radians(self.Rotation))
        z_change = Amount * math.sin(math.radians(self.Rotation))

        if 270 > self.Rotation > 90:
            x_change *= -1
        if 360 > self.Rotation > 180:
            z_change *= -1


        self.x += x_change
        self.z += z_change

        print(self.x, self.z)
