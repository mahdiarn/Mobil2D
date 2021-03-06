import time
from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OpenGLContext.arrays import *
from OpenGL.GL import shaders
class TestContext( BaseContext ):
    """This shader just passes gl_Color from an input array to
    the fragment shader, which interpolates the values across the
    face (via a "varying" data type).
    """
    def OnInit( self ):
        """Initialize the context once we have a valid OpenGL environ"""
        try:
            shaders.compileShader( """ void main() { """, GL_VERTEX_SHADER )
        except (GLError, RuntimeError) as err:
            print 'Example of shader compile error', err
        else:
            raise RuntimeError( """Didn't catch compilation error!""" )
    	vertex = shaders.compileShader(
            """
            varying vec4 vertex_color;
            void main() {
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                vertex_color = gl_Color;
            }""",GL_VERTEX_SHADER)
    	fragment = shaders.compileShader("""
            varying vec4 vertex_color;
            void main() {
                gl_FragColor = vertex_color;
            }""",GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vertex,fragment)
        self.vbo = vbo.VBO(
            array( [
                [  1, 1, 0,  1,1,1 ],
                [ -3,-1, 0,  1,1,1 ],
                [  1,-1, 0,  1,1,1 ],

                [  1,1, 0,  1,1,1 ],
                [  -3,1, 0,  1,1,1 ],
                [  -3,-1, 0,  1,1,1 ],

                [  -3,-1, 0,  1,1,0 ],
                [  -3,-1, -2,  1,1,0 ],
                [  1,-1, 0,  1,1,0 ],

                [  1,-1, 0,  1,1,0 ],
                [  -3,-1, -2,  1,1,0 ],
                [  1,-1, -2,  1,1,0 ],

                [  1,-1, -1,  1,1,0 ],
                [  1,-1, -2,  1,1,0 ],
                [  2,-1, -1,  1,1,0 ],

                [  2,-1, -1,  1,1,0 ],
                [  1,-1, -2,  1,1,0 ],
                [  2,-1, -2,  1,1,0 ],

                [  1,1, 0,  1,1,0 ],
                [  -3,1, -2,  1,1,0 ],
                [  -3,1, 0,  1,1,0 ],

                [  1,1, -2,  1,1,0 ],
                [  -3,1, -2,  1,1,0 ],
                [  1,1, 0,  1,1,0 ],

                [  2,1, -1,  1,1,0 ],
                [  1,1, -2,  1,1,0 ],
                [  1,1, -1,  1,1,0 ],

                [  2,1, -2,  1,1,0 ],
                [  1,1, -2,  1,1,0 ],
                [  2,1, -1,  1,1,0 ],


                [  -3,-1, 0,  0,1,0 ],
                [  -3,1, -2,  0,1,0 ],
                [  -3,-1, -2,  0,1,0 ],

                [  -3,1, 0,  0,1,0 ],
                [  -3,1, -2,  0,1,0 ],
                [  -3,-1, 0,  0,1,0 ],

                [  -1,1, -1,  0,1,1 ],
                [  -3,1, -1,  0,1,1 ],
                [  -1,-1, -1,  0,1,1 ],

                [  -3,1, -1,  0,1,1 ],
                [  -3,-1, -1,  0,1,1 ],
                [  -1,-1, -1,  0,1,1 ],

                [  1,-1, 0,  0,1,0 ],
                [  1,-1, -1,  0,1,0 ],
                [  1,1, 0,  0,1,0 ],

                [  1,1, 0,  0,1,0 ],
                [  1,-1, -1,  0,1,0 ],
                [  1,1, -1,  0,1,0 ],

                [  2,1, -1,  1,1,1 ],
                [  1,1, -1,  1,1,1 ],
                [  1,-1, -1,  1,1,1 ],

                [  2,1, -1,  1,1,1 ],
                [  1,-1, -1,  1,1,1 ],
                [  2,-1, -1,  1,1,1 ],

                [  2,1, -1,  1,0,1 ],
                [  2,-1, -1,  1,0,1 ],
                [  2,1, -2,  1,0,1 ],

                [  2,-1, -1,  1,0,1 ],
                [  2,-1, -2,  1,0,1 ],
                [  2,1, -2,  1,0,1 ],

                #alas

                [  2,-1, -2,  1,0,0 ],
                [  -3,-1, -2,  1,0,0 ],
                [  -3,1, -2,  1,0,0 ],

                [  2,-1, -2,  1,0,0 ],
                [  -3,1, -2,  1,0,0 ],
                [  2,1, -2,  1,0,0 ],

                #kaca jendela depan

                [  1.1,0.9, -0.1,  0,1,1 ],
                [  1.1,-0.9, -0.1,  0,1,1 ],
                [  1.1,0.9, -0.9,  0,1,1 ],

                [  1.1,-0.9, -0.1,  0,1,1 ],
                [  1.1,-0.9, -0.9,  0,1,1 ],
                [  1.1,0.9, -0.9,  0,1,1 ],

                #Kaca jendela samping 1

                [  -2.8,-1.1, -0.1,  0,1,1 ],
                [  -2.8,-1.1, -0.9,  0,1,1 ],
                [  -0.8,-1.1, -0.1,  0,1,1 ],

                [  -0.8,-1.1, -0.1,  0,1,1 ],
                [  -2.8,-1.1, -0.9,  0,1,1 ],
                [  -0.8,-1.1, -0.9,  0,1,1 ],

                [  -0.1,-1.1, -0.1,  0,1,1 ],
                [  -0.1,-1.1, -0.9,  0,1,1 ],
                [  0.9,-1.1, -0.1,  0,1,1 ],

                [  0.9,-1.1, -0.1,  0,1,1 ],
                [  -0.1,-1.1, -0.9,  0,1,1 ],
                [  0.9,-1.1, -0.9,  0,1,1 ],

                #Kaca jendela samping 2



                [  -0.8,1.1, -0.1,  0,1,1 ],
                [  -2.8,1.1, -0.9,  0,1,1 ],
                [  -2.8,1.1, -0.1,  0,1,1 ],

                [  -0.8,1.1, -0.9,  0,1,1 ],
                [  -2.8,1.1, -0.9,  0,1,1 ],
                [  -0.8,1.1, -0.1,  0,1,1 ],

                [  0.9,1.1, -0.1,  0,1,1 ],
                [  -0.1,1.1, -0.9,  0,1,1 ],
                [  -0.1,1.1, -0.1,  0,1,1 ],

                [  0.9,1.1, -0.9,  0,1,1 ],
                [  -0.1,1.1, -0.9,  0,1,1 ],
                [  0.9,1.1, -0.1,  0,1,1 ],
            ],'f')
        )
    def Render( self, mode):
        """Render the geometry for the scene."""
        BaseContext.Render( self, mode )
        glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try:
            	glEnableClientState(GL_VERTEX_ARRAY);
                glEnableClientState(GL_COLOR_ARRAY);
                glVertexPointer(3, GL_FLOAT, 24, self.vbo )
                glColorPointer(3, GL_FLOAT, 24, self.vbo+12 )
                glRotated(-75,1,0,0)
                glDrawArrays(GL_TRIANGLES, 0, 120)
                base = 0.5
                height = 0.3
                g = gluNewQuadric()
                glRotated(90, 1, 0, 0)
                
                glTranslate(1, -1.85, -1.25)
                gluCylinder(g, base, base, height, 30, 30)
                glRotated(-180, 1, 0, 0) 
                gluDisk(g, 0, base, 30, 30)
                glRotated(-180, 1, 0, 0) 
                glTranslate(0, 0, height)
                gluDisk(g, 0, base, 30, 30)
                
                glTranslate(0, 0, -1*height)
                glTranslate(-3, 0, 0)
                gluCylinder(g, base, base, height, 30, 30)
                glRotated(-180, 1, 0, 0) 
                gluDisk(g, 0, base, 30, 30)
                glRotated(-180, 1, 0, 0) 
                glTranslate(0, 0, height)
                gluDisk(g, 0, base, 30, 30)
                
                glTranslate(0, 0, -1*height)
                glTranslate(0, 0, 2.2)
                gluCylinder(g, base, base, height, 30, 30)
                glRotated(-180, 1, 0, 0) 
                gluDisk(g, 0, base, 30, 30)
                glRotated(-180, 1, 0, 0) 
                glTranslate(0, 0, height)
                gluDisk(g, 0, base, 30, 30)
                
                glTranslate(0, 0, -1*height)
                glTranslate(3, 0, 0)
                gluCylinder(g, base, base, height, 30, 30)
                glRotated(-180, 1, 0, 0) 
                gluDisk(g, 0, base, 30, 30)
                glRotated(-180, 1, 0, 0) 
                glTranslate(0, 0, height)
                gluDisk(g, 0, base, 30, 30)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY);
                glDisableClientState(GL_COLOR_ARRAY);
        finally:
            glUseProgram( 0 )
if __name__ == "__main__":
    print "test"
    TestContext.ContextMainLoop()
