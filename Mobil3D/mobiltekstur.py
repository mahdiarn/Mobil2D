from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
import time
import math
try:
    from PIL.Image import open
except ImportError, err:
    from Image import open
class TestContext( BaseContext ):
    """NeHe 6 Demo"""
    initialPosition = (0,0,0) # set initial camera position, tutorial does the re-positioning
    def OnInit( self ):
        """Load the image on initial load of the application"""
        self.imageID = self.loadImage ()
    def loadImage( self, imageName = "nehe_wall.bmp" ):
        """Load an image file as a 2D texture using PIL"""
        im = open(imageName)
        try:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        return ID
    def Render( self, mode):
        """Render scene geometry"""
        BaseContext.Render( self, mode )
        #glDisable( GL_LIGHTING) # context lights by default
        glTranslatef(1.5,0.0,-6.0);
        
        self.setupTexture()
        self.drawCube()
        glTranslatef(0,-1.0,-2.0);
        glRotated(90,1,0,0)
        self.draw_cylinder()
        glTranslatef(-2.5,0.0,0);
        self.draw_cylinder()
        glTranslatef(0,0.0,-2.0);
        glRotated(180,1,0,0)
        self.draw_cylinder()
        glTranslatef(2.5,0.0,0);
        self.draw_cylinder()
    def setupTexture( self ):
        """Render-time texture environment setup"""
        glEnable(GL_TEXTURE_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, self.imageID)
    def drawCube( self ):
        """Draw a cube with texture coordinates"""
        glBegin(GL_TRIANGLES);
        #Bagian atas
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  0);
        glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0,  0);

        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  0);
        #Samping kanan (besar)
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, -1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  -2.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, -1.0,  0);

        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, -1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  -2.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(1.0, -1.0,  -2.0);
        #Samping kanan (kecil)
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0,  -2.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, -1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0,  -2.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(2.0, -1.0,  -2.0);
        #Samping kiri (Besar)
        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.0,  0);

        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, 1.0,  0);
        #Samping kiri (Kecil)
        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, 1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, 1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, 1.0,  0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  -2.0);
        
        glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, 1.0,  0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  0);

        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, -1.0,  0);
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, 1.0,  0);

        glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, 1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, -1.0,  -1.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(2.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, 1.0,  -2.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(2.0, -1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, 1.0,  -2.0);

        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, -1.0,  -2.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, -1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.0,  -2.0);
        
        glTexCoord2f(1.0, 1.0); glVertex3f(2.0, -1.0,  -2.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, 1.0,  -2.0);
        glEnd()

    def draw_cylinder(self):
        r = 1
        h = 1
        n = float(20)

        circle_pts = []
        for i in range(int(n) + 1):
            angle = 2 * math.pi * (i/n)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            pt = (x, y)
            circle_pts.append(pt)
        
        glBegin(GL_TRIANGLE_FAN)#drawing the back circle
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0, 0, h/2.0)
        for (x, y) in circle_pts:
            z = h/2.0
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x, y, z)
        glEnd()
        
        
        glBegin(GL_TRIANGLE_FAN)#drawing the front circle
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0, 0, h/2.0)
        for (y, x) in circle_pts:
            z = -h/2.0
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x, y, z)
        glEnd()
        
        glBegin(GL_TRIANGLE_STRIP)#draw the tube        
        for (x, y) in circle_pts:
            z = h/2.0
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x, y, z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x, y, -z)
        glEnd()

        

        

    def OnIdle( self, ):
        """Request refresh of the context whenever idle"""
        self.triggerRedraw(1)
        return 1
if __name__ == "__main__":
    TestContext.ContextMainLoop()