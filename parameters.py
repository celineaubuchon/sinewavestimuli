import math
## This file contains display information and experimental paramters that are used
    # to generate the stimuli in the demo 'window.py'
    # These parameters match those that were used in Jovan's experiment

    # to change display distance, edit the value of 'focal_distance' here
    # to improve the quality of the texture stimulus, increase 'subdivs' (around 300 is fine)

## SCREEN PARAMETERS ###########################################
display_width = 700 # pixel width of the window
display_height = 700 # pixel height of the window
display_wide_size = 154 # mm width of the window (depends on display)
display_height_size = 154 # mm height of the window (depends on display)

## VIEWING PARAMETERS ##########################################
focal_distance = -400 # in mm, -400 and -800 used in experiment
IOD = 64 # inter-ocular distance (differs by observer)

## STIMULUS PARAMETERS #########################################
stimulus_visang = 8 # in degrees, size of the stimulus
dot_visang = 0.1 # in degrees, size of a dot in the rds sinewave
polka_visang = 0.45 # in degrees, size of a polka dot in the textured sinewave
period_visang = 4.5 # in degrees, length of a period in the sinewave

stimulus_width = abs(2 * focal_distance*math.tan(math.radians(0.5*stimulus_visang))) # in mm, stimulus width
polka_width = math.tan(math.radians(polka_visang/2)) * 2*(abs(focal_distance)) # in mm, polka dot width
period = 1/(math.tan(math.radians(period_visang)) * abs(focal_distance)) * (2*math.pi) 
polka_density = 4.5
depths = [2.5, 5, 10, 15] # in mm, depths used in experiment
num_dots = 400 # number of dots in the rds sinewave

subdivs = 150 # number of subdivisions in the textured sinewave mesh (increase this for better quality polka dots)

## LIGHTING PARAMETERS #########################################
LightAmbient = [0.15, 0.0, 0.0, 1.0] 
LightDiffuse = [0.2, 0.0, 0.0, 1.0]
LightSpecular = [0.3, 0.0, 0.0, 0.0]
LightPosition = [20.0, 150.0, 0.0, 1.0]
LightPosition = [0.0, 0.0, 0.0, 1.0]
specularMaterial = [0.25, 0.0, 0.0, 1.0]
shininessMaterial = 16.0