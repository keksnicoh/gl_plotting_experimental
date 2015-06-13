import mygl.app
import mygl.util
from OpenGL.GL import *
import numpy
from OpenGL.arrays import vbo
import math
from itertools import groupby
from time import sleep
VERTEX_SHADER = """
#version 410
in vec3 position;
uniform vec3 color_encoding;
void main() {
	gl_Position = vec4(position, 1.0f);
}
"""
FRAGMENT_SHADER = """
#version 410

uniform vec3 dot_color;
in vec2 tex_coord;
uniform float dot_alpha;
out vec4 outputColor;
void main()
{
	if (tex_coord == vec2(0.0f, 0.0f)) {}
    outputColor = vec4(dot_color, dot_alpha);
}
"""
GEOMETRY_SHADER = """
#version 410
layout (points) in;
layout (triangle_strip) out;
layout (max_vertices = 4) out;
uniform float dot_size;
out vec2 tex_coord;
void main(void)
{
	tex_coord = vec2(-1,-1);
	gl_Position = gl_in[0].gl_Position +vec4(-dot_size,-dot_size,0,0) ;
	EmitVertex();

	tex_coord = vec2(-1,1);
	gl_Position = gl_in[0].gl_Position + vec4(-dot_size,dot_size, 0,0) ;
	EmitVertex();

	tex_coord = vec2(1,-1);
	gl_Position = gl_in[0].gl_Position + vec4( dot_size,-dot_size, 0,0) ;
	EmitVertex();

	tex_coord = vec2(1,1);
	gl_Position = gl_in[0].gl_Position + vec4( dot_size,dot_size, 0,0) ;
	EmitVertex();

	EndPrimitive();
}
"""
SHADER_PROGRAM = None
APP = None
def dreieck_list(a, x_0, n=1000):
	x = range(0, n)
	x[0] = x_0
	for i in range(1, n):
		x[i] = 2*a*x[i-1] if x[i-1] < 0.5 else 2*a*(1-x[i-1])
	return x

class Blurp():

	def __init__(self):
		self.a = 0.5
		self.dot_size = 0.005
		self.dot_alpha = 1.0
		self.n = 2500
		self.dot_color = numpy.array([0.7, 0.9, 0.7], dtype=numpy.float32)
		self.render = True

		self.shader = mygl.util.Shader()
		self.shader.attachShader(GL_VERTEX_SHADER, VERTEX_SHADER)
		self.shader.attachShader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
		self.shader.attachShader(GL_GEOMETRY_SHADER, GEOMETRY_SHADER)
		self.shader.linkProgram()

		self.vao_id = glGenVertexArrays(1)
		self.vbo_id = glGenBuffers(2)

		self.calculate()

	def calculate(self):
		coords = []
		x_l = 2.0 / self.n
		current_x = -1.0 + x_l/2
		for point in dreieck_list(self.a, 0.8, n=self.n):
			coords.append(current_x)
			coords.append((point-0.5)*2)
			coords.append(0)
			current_x += x_l
		self.vertices = numpy.array(coords, dtype=numpy.float32)

		glBindVertexArray(self.vao_id)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo_id[0])
		glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.vertices), self.vertices, GL_STATIC_DRAW)
		glVertexAttribPointer(self.shader.attributeLocation('position'), 3, GL_FLOAT, GL_FALSE, 0, None)
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)

	def keyboard_control(self, active):
		KEY_65 = 0.01
		KEY_78 = int(math.ceil(float(self.n) / 100))
		KEY_83 = 0.0005
		KEY_68 = 0.01
		delta = lambda o, a: (1 if o else -1) * a

		if 93 in active: o = True
		elif 47 in active: o = False
		else: return

		if 65 in active: self.a = max(.0, min(1., self.a + delta(o, KEY_65)))
		elif 78 in active: self.n = max(.0, self.n + delta(o, KEY_78))
		elif 83 in active: self.dot_size = max(.0, self.dot_size + delta(o, KEY_83))
		elif 68 in active: self.dot_alpha = max(.0, min(1., self.dot_alpha + delta(o, KEY_68)))
		else: return

		print("a={}, n={}, dot_size={}, dot_alpha={}".format(self.a, self.n, self.dot_size, self.dot_alpha))
		self.render = True

	def scene(self, app):
		# only render if neccessary
		if not self.render:
			self.keyboard_control(app.keyboardActive)
			sleep(0.05)

		else:
			# init render cycle
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.shader.useProgram()

			glUniform3f(self.shader.uniformLocation('dot_color'), *self.dot_color)
			glUniform1f(self.shader.uniformLocation('dot_alpha'), self.dot_alpha)
			glUniform1f(self.shader.uniformLocation('dot_size'), self.dot_size)

			# render
			glEnable(GL_BLEND);
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

			self.calculate()

			glBindVertexArray(self.vao_id)
			glDrawArrays(0,0,self.n)
			glBindVertexArray(0)

			# cleanup
			self.shader.unuseProgram()
			self.render = False
			app.swap()

def main():
	APP = mygl.app.BasicGl()
	blurp = Blurp()
	APP.scene = blurp.scene
	APP.run()

if __name__ == '__main__': main()
