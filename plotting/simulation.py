#-*- coding: utf-8 -*-
"""
Simple 2D simulation to test dual window support
@author Jesse Hinrichsen <jesse@j-apps.com>
"""
from OpenGL.GL import *
from mygl.glfw import *

from opencl.cl_handler import BaseCalculator

import numpy
import os
from sys import exc_info
from traceback import print_exc

from mygl import util
from mygl.app import BasicGl
import math

VERTEX_SHADER = """
    #version 410
    in vec2 simple_data;
    out vec3 color;
    void main() {
        color = vec3(0.6, 0.2, 0.2);
        gl_Position = vec4 (simple_data.xy, 0.0, 1.0);;
    }
"""

FRAGMENT_SHADER = """
    #version 410
    out vec4 frag_colour;
    in vec2 points;
    in vec3 p_color;

    void main() {
        if (points.x*points.x + points.y*points.y > 1.0) {
            discard;
        }
        
        frag_colour = vec4(p_color.xyz, 1.0);
    }
"""

GEOMETRY_SHADER = """
    #version 410
    layout (points) in;
    layout (triangle_strip) out;
    layout (max_vertices = 4) out;

    in vec3 color[1];
    out vec3 p_color;

    out vec2 points;
    void main(void)
    {
        p_color = color[0];
        float size = 0.05;
        points = vec2(-1,-1);
        gl_Position = gl_in[0].gl_Position + vec4(-size,-size, 0, 0) ;
        EmitVertex();

        points = vec2(-1,1);
        gl_Position = gl_in[0].gl_Position + vec4(-size,size, 0,0) ;
        EmitVertex();

        points = vec2(1,-1);
        gl_Position = gl_in[0].gl_Position + vec4(size,-size, 0,0) ;
        EmitVertex();

        points = vec2(1,1);
        gl_Position = gl_in[0].gl_Position + vec4(size,size, 0,0) ;
        EmitVertex();

        EndPrimitive();
    }
"""

CL_KERNEL = """__kernel void f(int comp_count, __global float *velocity, __global float *position, __global int *time, __global float *plt_buffer)
{
    int vertex_id = get_global_id(0);
    int x = vertex_id*comp_count;

    float dt = 0.004f;

    float acc = 5.0f/(pown(position[x], 2)+pown(position[x+1], 2));

    velocity[x] -= position[x]*acc*dt;
    velocity[x+1] -= position[x+1]*acc*dt;

    position[x] += velocity[x]*dt;
    position[x+1] += velocity[x+1]*dt;


    if(vertex_id == 1) {
        plt_buffer[2*time[0]] = float(time[1]*dt);
        plt_buffer[2*time[0]+1] = sqrt(velocity[x]*velocity[x] + velocity[x+1]*velocity[x+1]);
        time[0] += 1;
        time[1] += 1;
        if(time[0] > time[2]) {
            time[0] = 0;
        }
    }
    
}
"""

class SimulationFrame():
    def __init__(self, plt_window, creation_callback, params):
        self.plt_window = plt_window
        self.sim_window = creation_callback(*params)

    def __enter__(self):
        glfwMakeContextCurrent(self.sim_window)
        return self

    def __exit__(self, type, value, traceback):
        glfwMakeContextCurrent(self.plt_window)



class Simulation():
    """
    class to add simulation window
    """
    def __init__(self, plotterWindow):
        if not isinstance(plotterWindow.app, BasicGl):
            raise RuntimeError("PlotterWindow class not compatible")

        self.domain = None
        self.plotter = plotterWindow
        size = (300, 300)
        self.sim_frame = SimulationFrame(self.plotter.app.window, self.plotter.app.createAdditionalWindow, ("Simulation", size))



        with self.sim_frame as frame:
            glfwSetKeyCallback(frame.sim_window, self.onKeyboard)

            self.shader = util.Shader(vertex=VERTEX_SHADER, geometry=GEOMETRY_SHADER, fragment=FRAGMENT_SHADER, link=True)
            self.vbo = glGenBuffers(1)
            self.data = numpy.array([0.3, 0.0, 0.0, 0.5], dtype=numpy.float32)
            self.velocity = numpy.array([0.0, 0.5, 3, 0.0], dtype=numpy.float32)
            #self.external = numpy.array([0,0,0,0], dtype=numpy.float32)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.data), self.data, GL_STATIC_DRAW)
            
            self.vao = glGenVertexArrays(1)
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(0)

            glViewport(0, 0, 300, 300)
            glEnable(GL_DEPTH_TEST)
            glClearColor(0.5, 0.5, 0.5,1.0)

        self.calculator = BaseCalculator(sharedGlContext=True)
        self.gl_buffer = self.calculator.getOpenGLBufferFromId(self.vbo)
        self.vel_buffer = self.calculator.createArrayBufferWrite(self.velocity)
        self.program = self.calculator._buildKernel(CL_KERNEL)

    # z: faster 89
    # u: slower 85
    def onKeyboard(self, win, key, scancode, action, mods):
        if key == 89:
            self.velocity = self.calculator.arrayFromBuffer(self.velocity, self.vel_buffer)
            self.velocity[2] += 0.1*self.velocity[2]
            self.velocity[3] += 0.1*self.velocity[3]
            self.vel_buffer = self.calculator.createArrayBufferWrite(self.velocity)

        if key == 85:
            self.velocity = self.calculator.arrayFromBuffer(self.velocity, self.vel_buffer)
            self.velocity[2] -= 0.1*self.velocity[2]
            self.velocity[3] -= 0.1*self.velocity[3]
            self.vel_buffer = self.calculator.createArrayBufferWrite(self.velocity)

    def applyPhysics(self):

        buffers = (numpy.int32(2), self.vel_buffer, self.gl_buffer, self.time_buffer, self.domain.buffer)
        self.program.f(self.calculator.queue, (2,), None, *buffers)
        self.calculator.queue.finish()
        self.calculator.releaseGlObjects([self.gl_buffer, self.domain.buffer])

    def setExternal(self, particle_id, velocity=(0,0)):
        self.external[2*particle_id] = velocity[0]
        self.external[2*particle_id + 1] = velocity[1]

        self.external[2*particle_id] = 0
        self.external[2*particle_id + 1] = 0



    def run(self):
        if not self.domain:
            raise RuntimeError("No Domain available")
        self.time_buffer = self.calculator.createArrayBufferWrite(numpy.array([0, 0, self.domain.length], dtype=numpy.int32))
        #self.ext_buffer = self.calculator.createArrayBufferWrite(self.external)

        self.plotter.initRun()
        while self.plotter.app.active():
            with self.sim_frame as frame:
                if not glfwWindowShouldClose(frame.sim_window):
                    try:
                        self.applyPhysics()

                        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                        self.shader.useProgram()
                        glEnable(GL_BLEND);
                        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

                        glBindVertexArray(self.vao)
                        glDrawArrays(GL_POINTS, 0, len(self.data))
                        glUseProgram(0)
                        glBindVertexArray(0)
                    
                        glfwSwapBuffers(frame.sim_window)

                    except:
                        print_exc(exc_info()[0])
                        print "try to shutdown...","yellow"
                        self.plotter.app.exit = True
                        print "program terminated due an unkown error!"
                        break;


            # Super dirty to enable live render
            self.plotter.plotter.gl_plot.render_graphs = True

            self.plotter.runCycle()








