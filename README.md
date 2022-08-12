# sinewavestimuli
 This is a simple example of how to generate the stimuli in Jovan's experiment using PyOpenGL and GLUT.
# Install necessary libraries
This code was developed using:
- Python 3.9
- Numpy
- PyOpenGL with GLUT 
  - IMPORTANT: in order to install the correct version of GLUT, download the PyOpenGL binaries from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl
  - download both PyOpenGL and PyOpenGL_accelerate (make sure you get the correct binaries based on your Python version, you can watch this video for a walkthrough https://www.youtube.com/watch?v=a4NVQC_2S2U)
  - install the .whl files with 'pip install <filename.whl>'
  - if you get errors at glutInit(), this could be because you don't have compatible version of PyOpenGL and GLUT

# Run the demo
The demo can be run with 'python window.py'. See 'window.py for commented instructions on how to interact with the demo.

# Files
- window.py
  - generates the GLUT window and the stimuli based on parameters in 'parameters.py'

- parameters.py
  - contains experimental parameters used to set up the correct display and generate the stimuli
  - the parameters match Jovan's experiment
  - edit the value for 'focal_length' to change the viewing distance
  - increase 'subdivs' to improve the quality of the texture stimuli

- rds.py
  - contains functions used to generate and draw a random-dot-stereogram sinewave

- texturedSinewave.py
  - a class that manages the generation and drawing of a textured sinewave
