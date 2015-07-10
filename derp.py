# -- coding: utf-8 --
import glfw
import OpenGL.GL as PyGL
import sys, os , site
## set the path of your PyCEGUI* modules
for _path in [os.path.join(s,'cegui-0.8') for s in site.getsitepackages()]:
   print _path
   sys.path.insert(0, _path)
sys.path.insert(0, "/media/sdb5/python-ogre-cegui/cegui-0.8/lib")
## set the path to our resource files
CEGUI_PATH = "/media/sdb5/Libraries/OGRE/sdk/v1-9/share/cegui-0/"
## import our PyCEGUI and out glfw3 to cegui key mappings
import PyCEGUI
import PyCEGUIOpenGLRenderer
from keymappings_glfw3 import *
def ConvertMouseButton(button):
   ### Convert Mouse Buttons to CEGUI
   if (button == glfw.GLFW_MOUSE_BUTTON_RIGHT):
       return PyCEGUI.RightButton
   elif (button == glfw.GLFW_MOUSE_BUTTON_LEFT):
       return PyCEGUI.LeftButton
   elif (button == glfw.GLFW_MOUSE_BUTTON_MIDDLE):
       return PyCEGUI.MiddleButton
   else:
       return PyCEGUI.LeftButton
class Application(object):
   def __init__(self):
       # Initialize glfw
       if not glfw.glfwInit():
           print (" Error : glfw failed to initialize")
           sys.exit (glfw.EXIT_FAILURE)
       ceguiGL3Renderer = True
       if ceguiGL3Renderer:
           glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MAJOR, 3)
           glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MINOR, 2)
           glfw.glfwWindowHint(glfw.GLFW_OPENGL_FORWARD_COMPAT, PyGL.GL_TRUE)
           glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE, glfw.GLFW_OPENGL_CORE_PROFILE)
       else:
           glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MAJOR, 2)
           glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MINOR, 1)
           glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE, glfw.GLFW_OPENGL_ANY_PROFILE)
       # our window hints
       ## http://www.glfw.org/docs/latest/window.html
       ## set our framebuffer related hints
       glfw.glfwWindowHint(glfw.GLFW_DEPTH_BITS, 24)
       glfw.glfwWindowHint(glfw.GLFW_STENCIL_BITS, 8)
       glfw.glfwWindowHint(glfw.GLFW_FOCUSED, True)
       fullScreen = False
       # create window
       if (not fullScreen):
           glfw_window = glfw.glfwCreateWindow(1024, 768, "PyCEGUI glfw3 Demo", None, None)
       else:
           glfw_window = glfw.glfwCreateWindow(1024, 768, "PyCEGUI glfw3 Demo", glfw.glfwGetPrimaryMonitor(), None)
       # check window created
       if not glfw_window:
           print (" Error : glfw failed to create a window")
           glfw.glfwTerminate()
           sys.exit()
       self.glfw_window = glfw_window
       glfw.glfwMakeContextCurrent(glfw_window)
       self.showglfwInfo()
       ## this does nothing on linux
       glfw.glfwSwapInterval(0)
       glfw.glfwSetInputMode(glfw_window, glfw.GLFW_CURSOR, glfw.GLFW_CURSOR_HIDDEN)
       # call backs
       glfw.glfwSetKeyCallback(             glfw_window,  self.on_key)
       glfw.glfwSetMouseButtonCallback(     glfw_window,  self.on_mouse)
       glfw.glfwSetCursorPosCallback(       glfw_window,  self.on_move)
       glfw.glfwSetWindowSizeCallback(      glfw_window,  self.on_resize)
       glfw.glfwSetCharCallback(            glfw_window,  self.on_char_callback)
       glfw.glfwSetFramebufferSizeCallback( glfw_window,  self.on_framebuffer_size_callback)
       # initialise our CEGUI renderer
       ctx_major      = glfw.glfwGetWindowAttrib(glfw_window, glfw.GLFW_CONTEXT_VERSION_MAJOR)
       ctx_minor      = glfw.glfwGetWindowAttrib(glfw_window, glfw.GLFW_CONTEXT_VERSION_MINOR)
       forward_compat = glfw.glfwGetWindowAttrib(glfw_window, glfw.GLFW_OPENGL_FORWARD_COMPAT)
       if (not ceguiGL3Renderer):
           PyCEGUIOpenGLRenderer.OpenGLRenderer.bootstrapSystem()
       else :
           PyCEGUIOpenGLRenderer.OpenGL3Renderer.bootstrapSystem()
       # initialise PyCEGUI and resources
       rp = PyCEGUI.System.getSingleton().getResourceProvider()
       rp.setResourceGroupDirectory("schemes",    CEGUI_PATH + "schemes")
       rp.setResourceGroupDirectory("imagesets",  CEGUI_PATH + "imagesets")
       rp.setResourceGroupDirectory("fonts",      CEGUI_PATH + "fonts")
       rp.setResourceGroupDirectory("layouts",    CEGUI_PATH + "layouts")
       rp.setResourceGroupDirectory("looknfeels", CEGUI_PATH + "looknfeel")
       rp.setResourceGroupDirectory("schemas",    CEGUI_PATH + "xml_schemas")
       PyCEGUI.ImageManager.setImagesetDefaultResourceGroup("imagesets")
       PyCEGUI.Font.setDefaultResourceGroup("fonts")
       PyCEGUI.Scheme.setDefaultResourceGroup("schemes")
       PyCEGUI.WidgetLookManager.setDefaultResourceGroup("looknfeels")
       PyCEGUI.WindowManager.setDefaultResourceGroup("layouts")
       parser = PyCEGUI.System.getSingleton().getXMLParser()
       if parser.isPropertyPresent("SchemaDefaultResourceGroup"):
           parser.setProperty("SchemaDefaultResourceGroup", "schemas")
       # Load schemes
       PyCEGUI.SchemeManager.getSingleton().createFromFile("TaharezLook.scheme")
       PyCEGUI.SchemeManager.getSingleton().createFromFile("WindowsLook.scheme")
       PyCEGUI.System.getSingleton().getDefaultGUIContext().getMouseCursor().setDefaultImage("TaharezLook/MouseArrow")
       # set root window
       root = PyCEGUI.WindowManager.getSingleton().createWindow("DefaultWindow", "background_wnd");
       root.setArea( PyCEGUI.UVector2(PyCEGUI.UDim(0.0, 0),PyCEGUI.UDim(0.0, 0)) ,PyCEGUI.USize(PyCEGUI.UDim(1.0, 0),PyCEGUI.UDim(1.0, 0)))
       PyCEGUI.System.getSingleton().getDefaultGUIContext().setRootWindow(root)
       # load a layout
       layout = PyCEGUI.WindowManager.getSingleton().loadLayoutFromFile("TextDemo.layout")
       root.addChild(layout.getChild('TextDemo'))
       self.edit = root.getChild('TextDemo/MultiLineGroup/editMulti')
       # create label for our FPS
       self.labelFPS = PyCEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Label", "FPSLabel")
       root.addChild(self.labelFPS)
       # create hello button
       button = PyCEGUI.WindowManager.getSingleton().createWindow("TaharezLook/Button", "HelloButton")
       button.setArea( PyCEGUI.UVector2(PyCEGUI.UDim(.50, 0),PyCEGUI.UDim(.92, 0)) ,PyCEGUI.USize(PyCEGUI.UDim(0.3, 0),PyCEGUI.UDim(0.05, 0)))
       button.setText("Hello")
       root.addChild(button)
       button.subscribeEvent(PyCEGUI.PushButton.EventClicked, self.OnbuttonClicked)
       # init simple timing
       self.previous_time = glfw.glfwGetTime()
       self.current_time  = self.previous_time
   def showglfwInfo(self):
       ctx_major      = glfw.glfwGetWindowAttrib(self.glfw_window, glfw.GLFW_CONTEXT_VERSION_MAJOR)
       ctx_minor      = glfw.glfwGetWindowAttrib(self.glfw_window, glfw.GLFW_CONTEXT_VERSION_MINOR)
       forward_compat = glfw.glfwGetWindowAttrib(self.glfw_window, glfw.GLFW_OPENGL_FORWARD_COMPAT)
       print "Created Window for OpenGL version %d.%d " % ( ctx_major, ctx_major )
       if ( ctx_major >=3 and forward_compat):
           print "Context is forward compatible, you can't use OpenGL 2.x commands"
       fwidth,fheight = glfw.glfwGetFramebufferSize(self.glfw_window)
       width, height =  glfw.glfwGetWindowSize(self.glfw_window)
       print "Framebuffer size %dx%d Window size %dx%d " % (fwidth,fheight, width,height)
   def OnbuttonClicked(self, args):
       self.edit.setText(self.edit.getText() + "You Clicked")
       return
   def cleanUp(self):
       ### shutdown glfw and CEGUI
       PyCEGUIOpenGLRenderer.OpenGLRenderer.destroySystem()
       glfw.glfwTerminate()
   def updateGL(self):
       ### glfw GL updates
       pass
   def updateCEGUI(self, elapsed):
       ### CEGUI updates
       #focused = glfw.glfwGetWindowAttrib(glfw_window, glfw.GLFW_CONTEXT_VERSION_MAJOR)
       if (PyCEGUI.System.getSingleton()):
           PyCEGUI.System.getSingleton().injectTimePulse(elapsed)
           PyCEGUI.System.getSingleton().renderAllGUIContexts()
           self.labelFPS.setText("FPS : %s" %(str(int(1.0/elapsed))))
   def mainLoop(self):
       ### Loop until glfw window is closed
       while not glfw.glfwWindowShouldClose(self.glfw_window):
           PyGL.glClear(PyGL.GL_COLOR_BUFFER_BIT)
           # update timing
           self.current_time = glfw.glfwGetTime()
           elapsed = self.current_time - self.previous_time
           self.previous_time = self.current_time
           # update GL/CEGUI
           self.updateGL()
           self.updateCEGUI(elapsed)
           # Swap front and back buffers
           glfw.glfwSwapBuffers(self.glfw_window)
           # Handle glfw events
           glfw.glfwPollEvents()
   def on_framebuffer_size_callback(self,window,width,height):
       PyGL.glViewport(0, 0, width, height)
       if ( PyCEGUI.System.getSingleton()):
           PyCEGUI.System.getSingleton().notifyDisplaySizeChanged(PyCEGUI.Sizef(float(width), float(height) ))
   def on_move(self, window, x,y):
       ### pass glfw mouse moves to CEGUI
       if ( PyCEGUI.System.getSingleton()):
           PyCEGUI.System.getSingleton().getDefaultGUIContext().injectMousePosition(x, y)
   def on_resize(self, window, width,height):
       ### resize glfw viewport and CEGUI display
       PyGL.glViewport(0, 0, width, height)
       if ( PyCEGUI.System.getSingleton()):
           PyCEGUI.System.getSingleton().notifyDisplaySizeChanged(PyCEGUI.Sizef(float(width), float(height) ))
   def on_mouse(self, window, button, action, mods):
       ### pass glfw mouse press events to CEGUI
       if ( PyCEGUI.System.getSingleton()):
           context = PyCEGUI.System.getSingleton().getDefaultGUIContext()
           if (action == glfw.GLFW_PRESS):
               context.injectMouseButtonDown( ConvertMouseButton(button) )
           if (action == glfw.GLFW_RELEASE):
               context.injectMouseButtonUp( ConvertMouseButton(button) )
   def on_char_callback(self, window, code):
       ### Unicode character callback function to CEGUI
       PyCEGUI.System.getSingleton().getDefaultGUIContext().injectChar(code)
   def on_key(self, window, key, scancode, action, mods):
       ### pass keypress events to CEGUI
       if PyCEGUI.System.getSingleton():
           cegui_key = KEYMAPPINGS[key]
           if (not cegui_key==PyCEGUI.Key.Unknown):
               if (action == glfw.GLFW_PRESS):
                  PyCEGUI.System.getSingleton().getDefaultGUIContext().injectKeyDown(PyCEGUI.Key.Scan(cegui_key))
               if (action == glfw.GLFW_RELEASE):
                   PyCEGUI.System.getSingleton().getDefaultGUIContext().injectKeyUp(PyCEGUI.Key.Scan(cegui_key))
       ## exit
       if key == glfw.GLFW_KEY_ESCAPE and action == glfw.GLFW_PRESS:
           glfw.glfwSetWindowShouldClose(window,1)
if __name__ == '__main__':
   app = Application()
   app.mainLoop()
   app.cleanUp()
   del app
