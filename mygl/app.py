"""
   @author Nicolas 'keksnicoh' Heimann <nicolas.heimann@gmail.com>
   """

from OpenGL.GL import *
import cyglfw3 as glfw
from sys import exc_info
from traceback import print_exc
from termcolor import colored
from math import pi

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

		print "* initialize application"
		self.initGlfw()
		print "- try to load OpenGL 4.1 core profile"
		self.initGlCoreProfile()
		self.initGlfwWindow()

		print 'Vendor: %s' %         glGetString(GL_VENDOR)
		print 'Opengl version: %s' % glGetString(GL_VERSION)
		print 'GLSL Version: %s' %   glGetString(GL_SHADING_LANGUAGE_VERSION)
		print 'Renderer: %s' %       glGetString(GL_RENDERER)
		print 'GLFW3: %s' %          glfw.GetVersionString()

		glfw.SetKeyCallback(self.window, self.onKeyboard)
		print "[OK] application is ready."

	def initGlCoreProfile(self):
		"""setup opengl 4.1"""
		glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, 1)
		glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 4)
		glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 1)
		glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

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
		if not glfw.Init():
			raise RuntimeError('glfw.Init() error')

	def initGlfwWindow(self):
		"""initialize glwf window and attach callbacks"""
		self.window = glfw.CreateWindow(self.width,self.height,self.window_title)
		if not self.window:
			raise RuntimeError('glfw.CreateWindow() error')
		glfw.MakeContextCurrent(self.window)
		#glfw.SetMouseButtonCallback(self.window, self.onMouse)
		#glfw.SetKeyCallback(self.window, self.onKeyboard)

	def active(self):
		return not self.exit and not glfw.WindowShouldClose(self.window)
	def run(self):
		while not self.exit and not glfw.WindowShouldClose(self.window):
			"""todo move to a better place..."""
			try:
				glfw.PollEvents()
				self.scene(self)

			except:
				print_exc(exc_info()[0])
				print colored("try to shutdown...","yellow")
				self.terminate()
				print colored("program terminated due an unkown error!","red")
				break;
			#try:
			#	self.keyboard(self)
			#	self.mouseDrag(self)
			#except:
			#	print_exc(exc_info()[0])
			#	print colored("IO interrupted...","red", attrs=['reverse', 'blink'])
		self.terminate()
	def glwf_cycle(self):
		glfw.PollEvents()
	def init_cycle(self):
		self.glwf_cycle()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	def swap(self):
		glfw.SwapBuffers(self.window)
	def terminate(self):
		self.destruct(self)
		print "shutdown opengl application with following settings"
		glfw.DestroyWindow(self.window)
		glfw.Terminate()
