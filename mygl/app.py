"""
   @author Nicolas 'keksnicoh' Heimann <nicolas.heimann@gmail.com>
   """

from OpenGL.GL import *
import cyglfw3 as glfw
from sys import exc_info
from traceback import print_exc
from termcolor import colored
from math import pi
from termcolor import colored
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

		BasicGl._dbg("init GLFW", '...')
		self.initGlfw()
		BasicGl._dbg("load {}".format(colored('OPENGL_CORE_PROFILE 4.10', 'red')), '...')
		self.initGlCoreProfile()
		self.initGlfwWindow()

		BasicGl._dbg('  + Vendor             {}'.format(colored(glGetString(GL_VENDOR), 'cyan')))
		BasicGl._dbg('  + Opengl version     {}'.format(colored(glGetString(GL_VERSION), 'cyan')))
		BasicGl._dbg('  + GLSL Version       {}'.format(colored(glGetString(GL_SHADING_LANGUAGE_VERSION), 'cyan')))
		BasicGl._dbg('  + Renderer           {}'.format(colored(glGetString(GL_RENDERER), 'cyan')))
		BasicGl._dbg('  + GLFW3              {}'.format(colored(glfw.GetVersionString(), 'cyan')))
		BasicGl._dbg('GL_VIEWPORT         {}'.format(colored(glGetIntegerv(GL_VIEWPORT), 'blue')))
		BasicGl._dbg('GL_MAX_TEXTURE_SIZE {}'.format(colored(glGetIntegerv(GL_MAX_TEXTURE_SIZE), 'blue')))

		BasicGl._dbg("init keyboard and mouse", '...')
		glfw.SetKeyCallback(self.window, self.onKeyboard)
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
		glfw.PollEvents()
	def init_cycle(self):
		self.glwf_cycle()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glBindTexture(GL_TEXTURE_2D, 0)
	def swap(self):
		glfw.SwapBuffers(self.window)
	def terminate(self):
		self.destruct(self)
		BasicGl._dbg("shutdown opengl application with following settings")
		glfw.DestroyWindow(self.window)
		glfw.Terminate()
