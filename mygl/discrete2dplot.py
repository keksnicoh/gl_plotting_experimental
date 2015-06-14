"""
pretty rough plotting class experiment
@author Nicolas 'keksnicoh' Heimann <keksnicoh@googlemail.com>
"""
import app
import util
from OpenGL.GL import *
import numpy
from OpenGL.arrays import vbo
import math
from itertools import groupby
from time import sleep
VERTEX_SHADER = """
#version 410
in vec2 position;
uniform vec3 color_encoding;
uniform mat4 translation;
void main() {
	gl_Position = translation* vec4(position, 0.0, 1.0);
}
"""
FRAGMENT_SHADER = """
#version 410

uniform vec3 dot_color;
in vec2 tex_coord;
uniform float dot_alpha;
uniform float width;
out vec4 outputColor;
void main()
{
	if (tex_coord.x > width && tex_coord.y > width) {
		discard;
	}

	if (tex_coord.x < -width && tex_coord.y > width) {
		discard;
	}

	if (tex_coord.x > width && tex_coord.y < -width) {
		discard;
	}

	if (tex_coord.x < -width && tex_coord.y < -width) {
		discard;
	}

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
uniform mat4 dot_rot;
void main(void)
{
	tex_coord = vec2(-1,-1);
	gl_Position = gl_in[0].gl_Position + dot_rot*vec4(-dot_size,-dot_size, 0, 0) ;
	EmitVertex();

	tex_coord = vec2(-1,1);
	gl_Position = gl_in[0].gl_Position + dot_rot*vec4(-dot_size,dot_size, 0,0) ;
	EmitVertex();

	tex_coord = vec2(1,-1);
	gl_Position = gl_in[0].gl_Position + dot_rot*vec4(dot_size,-dot_size, 0,0) ;
	EmitVertex();

	tex_coord = vec2(1,1);
	gl_Position = gl_in[0].gl_Position + dot_rot*vec4(dot_size,dot_size, 0,0) ;
	EmitVertex();

	EndPrimitive();
}
"""

class Plotter():
	def __init__(self, app):
		self.force_render = False
		self.translation = [0,0]
		self.app = app
		self.data = []
		self.dot_size = 0.005*10
		self.dot_alpha = 1.0
		self.width = 0.1
		self.dot_color = numpy.array([0.7, 0.9, 0.7], dtype=numpy.float32)
		self.rot = math.pi / 4
		self.shader = util.Shader()
		self.shader.attachShader(GL_VERTEX_SHADER, VERTEX_SHADER)
		self.shader.attachShader(GL_FRAGMENT_SHADER, FRAGMENT_SHADER)
		self.shader.attachShader(GL_GEOMETRY_SHADER, GEOMETRY_SHADER)
		self.shader.linkProgram()

		self.vao_id = glGenVertexArrays(1)
		self.vbo_id = glGenBuffers(2)

		self._data_updated = True

	def set_data(self, data):
		self._data_updated = True
		amax = max(numpy.amax(data), 1.0) # todo make me nicer ...
		self.data = [i/amax for i in data]

	def calculate(self):
		coords = []
		x_l = 2.0 / len(self.data)
		current_x = -1.0 + x_l/2
		for point in self.data:
			coords.append(current_x)
			coords.append((point-0.5)*2)
			current_x += x_l
		self.vertices = numpy.array(coords, dtype=numpy.float32)
		glBindVertexArray(self.vao_id)
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo_id[0])
		glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.vertices), self.vertices, GL_STATIC_DRAW)
		glVertexAttribPointer(self.shader.attributeLocation('position'), 2, GL_FLOAT, GL_FALSE, 0, None)
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)


	def render(self):
		# only render if neccessary
			# init render cycle
		self.app.init_cycle()
		if self._data_updated or self.force_render:
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.shader.useProgram()

			(tx, ty) = self.translation
			translation = numpy.array([
				1.0, 0.0, 0.0, 0.0,
				0.0, 1.0, 0.0, 0.0,
				0.0, 0.0, 1.0, 0.0,
				tx,  ty,  0.0, 1.0], dtype=numpy.float32)

			dot_rot = numpy.array([
				math.cos(self.rot), -math.sin(self.rot), 0.0, 0.0,
				math.sin(self.rot), math.cos(self.rot),  0.0, 0.0,
				0.0,                0.0,                 0.0, 0.0,
				0.0,                0.0,                 0.0, 0.0], dtype=numpy.float32)

			glUniform3f(self.shader.uniformLocation('dot_color'), *self.dot_color)
			glUniform1f(self.shader.uniformLocation('dot_alpha'), self.dot_alpha)
			glUniform1f(self.shader.uniformLocation('dot_size'), self.dot_size)
			glUniform1f(self.shader.uniformLocation('width'), self.width)
			glUniformMatrix4fv(self.shader.uniformLocation('dot_rot'), 1, GL_FALSE, dot_rot)
			glUniformMatrix4fv(self.shader.uniformLocation('translation'), 1, GL_FALSE, translation)
			# render
			glEnable(GL_BLEND);
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

			self.calculate()

			glBindVertexArray(self.vao_id)
			glDrawArrays(0,0,len(self.data))
			glBindVertexArray(0)

			# cleanup
			self.shader.unuseProgram()
			self.app.swap()
			self.force_render = False
