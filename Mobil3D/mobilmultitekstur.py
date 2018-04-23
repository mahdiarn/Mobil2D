from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGLContext import texture
from OpenGL.GL import *
from OpenGL.GL.ARB.multitexture import *
from OpenGLContext.arrays import array
import sys
from OpenGLContext.events.timer import Timer
from OpenGL.extensions import alternate
glMultiTexCoord2f = alternate(
    glMultiTexCoord2f,
    glMultiTexCoord2fARB
)
glActiveTexture = alternate(
    glActiveTexture,
    glActiveTextureARB,
)
class TestContext( BaseContext ):
    """Multi-texturing demo
    """
    initialPosition = (0,0,0)
    rotation =  0
    def OnInit( self ):
        """Do all of our setup functions..."""
        if not glMultiTexCoord2f:
            print 'Multitexture not supported!'
            sys.exit(1)
        self.addEventHandler( "keypress", name="r", function = self.OnReverse)
        self.addEventHandler( "keypress", name="s", function = self.OnSlower)
        self.addEventHandler( "keypress", name="f", function = self.OnFaster)
        print 'r -- reverse time\ns -- slow time\nf -- speed time'
        self.time = Timer( duration = 8.0, repeating = 1 )
        self.time.addEventHandler( "fraction", self.OnTimerFraction )
        self.time.register (self)
        self.time.start ()
        self.Load()
    ### Timer callback
    def OnTimerFraction( self, event ):
        self.rotation = event.fraction()* -360
    def OnReverse( self, event ):
        self.time.internal.multiplier = -self.time.internal.multiplier
        print "reverse",self.time.internal.multiplier
    def OnSlower( self, event ):
        self.time.internal.multiplier = self.time.internal.multiplier /2.0
        print "slower",self.time.internal.multiplier
    def OnFaster( self, event ):
        self.time.internal.multiplier = self.time.internal.multiplier * 2.0
        print "faster",self.time.internal.multiplier
    def Load( self ):
        self.image = self.loadImage ("nehe_wall.bmp")
        self.lightmap = self.loadLightMap( "bigtext.bmp" )
    def Render( self, mode):
        """Render scene geometry"""
        BaseContext.Render( self, mode )
        if mode.visible:
            glDisable( GL_LIGHTING) # context lights by default
            glTranslatef(1.5,0.0,-6.0);
            glRotated( self.rotation, 1,0,0)
            glRotated( self.rotation, 0,1,0)
            glRotated( self.rotation, 0,0,1)

            glActiveTexture(GL_TEXTURE0);
            glTexParameterf(
                GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST
            )
            glTexParameterf(
                GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST
            )
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            self.image()
            glActiveTexture(GL_TEXTURE1);
            glTexParameterf(
                GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST
            )
            glTexParameterf(
                GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST
            )
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            self.lightmap()
            self.drawCube()
    def loadImage( self, imageName = "nehe_wall.bmp" ):
        """Load an image from a file using PIL."""
        try:
            from PIL.Image import open
        except ImportError, err:
            from Image import open
        glActiveTexture(GL_TEXTURE0_ARB);
        return texture.Texture( open(imageName) )
    def loadLightMap( self, imageName = "lightmap1.jpg" ):
        """Load an image from a file using PIL as a lightmap (greyscale)
        """
        try:
            from PIL.Image import open
        except ImportError, err:
            from Image import open
        glActiveTextureARB(GL_TEXTURE1);
        return texture.Texture( open(imageName) )
    def drawCube( self ):
        """Draw a cube with texture coordinates"""
        glBegin(GL_QUADS);
        mTexture(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        mTexture(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        mTexture(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
        mTexture(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
        mTexture(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        mTexture(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        mTexture(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        mTexture(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
        mTexture(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        mTexture(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
        mTexture(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
        mTexture(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        mTexture(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
        mTexture(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
        mTexture(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        mTexture(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        mTexture(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
        mTexture(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        mTexture(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
        mTexture(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        mTexture(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        mTexture(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        mTexture(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
        mTexture(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        glEnd()
    def OnIdle( self, ):
        """Request refresh of the context whenever idle"""
        self.triggerRedraw(1)
        return 1            
def mTexture( a,b ):
    glMultiTexCoord2f(GL_TEXTURE0, a,b)
    glMultiTexCoord2f(GL_TEXTURE1, a,b)
if __name__ == "__main__":
    TestContext.ContextMainLoop()

