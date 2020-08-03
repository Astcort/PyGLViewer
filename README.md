
# PyGLViewer

Framework developed for the course [Numerical mechanics: From Lagrangian mechanics to simulation tools for computer graphics](https://team.inria.fr/elan/classes/) given with Florence Bertails-Descoubes & Mélina Skouras.

This is a simple OpenGL viewer designed to have a quick visualization of the results of the simulations. The goal is *not* to do efficient/marvelous renderings, although you can tune a bit the viewer if you want.

## Author 

* [Mickaël LY](https://github.com/Astcort/)

## How to use

### Dependancies 

* Python3
* GLFW3
* Assimp
* OpenGL

To install them (on Ubuntu) :
```
sudo apt-get install freeglut3 freeglut3-dev mesa-utils python3 python3-setuptools libglfw3-dev libassimp-dev python3-pip
pip3 install numpy Pillow pyassimp==4.1.3 PyOpenGL PyOpenGL-accelerate glfw scipy
```
**Warning:** Be careful with the version of PyAssimp, the latest version (4.1.4) crashes...
If there is some problem with the Python installation, try :
```
python3 -m pip install numpy Pillow pyassimp==4.1.3 PyOpenGL PyOpenGL-accelerate glfw scipy
```


### Test

Running
```
python3 main.py
```
should play one of the default base scenarios.

### Making your own scenarios

The examples of the file `scene.py` are quite self explanatory. 