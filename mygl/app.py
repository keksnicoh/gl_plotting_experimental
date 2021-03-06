"""
   @author Nicolas 'keksnicoh' Heimann <nicolas.heimann@gmail.com>
   """

from OpenGL.GL import *
from glfw import *
from sys import exc_info
from traceback import print_exc
from termcolor import colored
from math import pi
from termcolor import colored
import numpy


class BasicGl():
	def __init__(self, width=600, height=600, window_title="no title"):
		"""general window configuration"""
		self.window_title = window_title
		self.width        = width
		self.height       = height
		self.exit         = False
		self.destruct     = lambda w : None
		self.scene        = lambda w : None
		"""keyboard_stack [I,...] stack of pressed keys"""
		self.keyboardStack = []
		"""keyboard_active [I,...] contains all currently active keys"""
		self.keyboardActive = []
		self.scrolled = 0.0
		self.origin = [1.0, 1.0]
		self.glwh = [2.0, 2.0]
		BasicGl._dbg("init GLFW", '...')
		self.initGlfw()
		BasicGl._dbg("load {}".format(colored('OPENGL_CORE_PROFILE 4.10', 'red')), '...')
		self.initGlCoreProfile()
		self.initGlfwWindow()
		self.mouse = [None, None]
		self.mouse_active = False
		self.mouse_relative = [0,0]
		self.mouse_button = None
		BasicGl._dbg('  + Vendor             {}'.format(colored(glGetString(GL_VENDOR), 'cyan')))
		BasicGl._dbg('  + Opengl version     {}'.format(colored(glGetString(GL_VERSION), 'cyan')))
		BasicGl._dbg('  + GLSL Version       {}'.format(colored(glGetString(GL_SHADING_LANGUAGE_VERSION), 'cyan')))
		BasicGl._dbg('  + Renderer           {}'.format(colored(glGetString(GL_RENDERER), 'cyan')))
		BasicGl._dbg('  + GLFW3              {}'.format(colored(glfwGetVersion(), 'cyan')))
		BasicGl._dbg('GL_VIEWPORT         {}'.format(colored(glGetIntegerv(GL_VIEWPORT), 'blue')))
		BasicGl._dbg('GL_MAX_TEXTURE_SIZE {}'.format(colored(glGetIntegerv(GL_MAX_TEXTURE_SIZE), 'blue')))

		BasicGl._dbg("init keyboard and mouse", '...')
		glfwSetKeyCallback(self.window, self.onKeyboard)
		BasicGl._dbg("application is ready to use.", 'OK')

	@classmethod
	def _dbg(cls, text, state=None):
		if state is not None:
			if state == 'OK': state = colored(state, 'green')
			if state == 'FAIL': state = colored(state, 'red')
			if state == '...': state = colored(state, 'yellow')
			text = '[{}] {}'.format(state, text)
		print(text)

	def initGlCoreProfile(self):
		"""setup opengl 4.1"""
		#glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, 1)
		#glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
		#glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1)
		#glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

		# all profiles since 3.2 are compatible
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	def createAdditionalWindow(self, title, size=(200,200), position=(100,100)):
		win = glfwCreateWindow(size[0], size[1], title, None, self.window)
		glfwSetWindowPos(win, position[0], position[1]);
		self.windows.append(win)

		return win

	def onKeyboard(self, win, key, scancode, action, mods):
		if action == 0:
			self.keyboardActive.remove(key)
		elif action == 1:
			self.keyboardStack.append(key)
			self.keyboardActive.append(key)
		elif action == 2:
			self.keyboardStack.append(key)

	def initGlfw(self):
		"""initialize glfw"""
		if not glfwInit():
			raise RuntimeError('glfw.Init() error')
	def scroll_callback(self, win, bla, scrolled):
		self.scrolled = scrolled

	def mouse_callback(self, win, button, action, mod):
		if action == 1:
			self.mouse[button] = self.getCursorRelative()
		if action == 0:
			self.mouse[button] = None

		if button == 0 and action == 1:
			self.mouse_active = True
			self.mouse_relative = self.getCursorRelative()
		else:
			self.mouse_active = False
			self.mouse_relative = [0,0]

	def get_mouse_drag(self, button=0):
		if self.mouse[button] is not None:
			current_drag = self.getCursorRelative()
			old_drag = self.mouse[button]
			self.mouse[button] = current_drag
			drag = (float(old_drag[0]-current_drag[0]), float(current_drag[1]-old_drag[1]))
			return drag
	def getCursorRelative(self):
		"""returns cursor position relative to window"""
		wx,wy = glfwGetCursorPos(self.window)
		cx,cy = glfwGetWindowPos(self.window)
		return cx-wx,cy-wy

	def get_cursor_absolute(self):
		return glfwGetCursorPos(self.window)
	def get_cursor_absolute_normalized(self):
		(cx, cy) = self.get_cursor_absolute()
		return float(cx)/self.width, float(cy)/self.height

	def normalize(self, data):
		if data is None: return None
		return data[0]/self.width, data[1]/self.height
	def initGlfwWindow(self):
		"""initialize glwf window and attach callbacks"""
		self.window = glfwCreateWindow(self.width,self.height,self.window_title)
		if not self.window:
			raise RuntimeError('glfw.CreateWindow() error')
		self.windows = [self.window]
		glfwMakeContextCurrent(self.window)
		glfwSetScrollCallback(self.window, self.scroll_callback)
		glfwSetMouseButtonCallback(self.window, self.mouse_callback)
		#glfw.SetKeyCallback(self.window, self.onKeyboard)
	def active(self):
		return not self.exit and not glfwWindowShouldClose(self.window)

	def run(self):
		print "fpp"
		exit(3)
		while not self.exit and not glfwWindowShouldClose(self.window):
			"""todo move to a better place..."""
			try:
				glfw.PollEvents()
				self.scene(self)

				#Also update the other window
				glfwMakeContextCurrent(self.windows[1])
				glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

				#glUseProgram(self.shader.program)
				glEnable(GL_BLEND);
				glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

				#glBindVertexArray(self.vaos[i])
				#glDrawArrays(GL_POINTS, 0, 1)
				#glUseProgram(0)
				#glBindVertexArray(0)
			
				glfwSwapBuffers(window);

				glfwMakeContextCurrent(self.window)

			except:
				print_exc(exc_info()[0])
				BasicGl._dbg(colored("try to shutdown...","yellow"))
				self.terminate()
				BasicGl._dbg(colored("program terminated due an unkown error!","red"))
				break;
			#try:
			#	self.keyboard(self)
			#	self.mouseDrag(self)
			#except:
			#	print_exc(exc_info()[0])
			#	BasicGl._dbg(colored("IO interrupted...","red", attrs=['reverse', 'blink']))
		self.terminate()
	def glwf_cycle(self):
		glfwPollEvents()
	def init_cycle(self):
		self.scrolled = 0.0
		self.glwf_cycle()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glBindTexture(GL_TEXTURE_2D, 0)
	def swap(self):
		glfwSwapBuffers(self.window)
	def terminate(self):
		self.destruct(self)
		BasicGl._dbg("shutdown opengl application with following settings")
		glfwDestroyWindow(self.window)
		glfwTerminate()
