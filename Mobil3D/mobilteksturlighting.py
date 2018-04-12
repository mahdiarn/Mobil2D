from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *
import time
import math
try:
    from PIL.Image import open
except ImportError, err:
    from Image import open
from OpenGL.GLU import *
from OpenGL.constants import GLfloat_3,GLfloat_4
class TestContext( BaseContext ):
    """Texture Filters, Lighting, Keyboard Control"""
    usage ="""Demonstrates filter functions:
    press 'f' to toggle filter functions
    press 'l' to toggle lighting
    press '<pageup>' to speed up rotation
    press '<pagedown>' to slow down rotation
"""
    initialPosition = (0,0,0) # set initial camera position, tutorial does the re-positioning
    def OnInit( self ):
        """Load the image on initial load of the application"""
        self.imageIDs = self.loadImages()
        self.currentFilter = 0 # index into imageIDs
        self.lightsOn = 1 # boolean
        self.currentZOffset = -6
        self.rotationCycle = 8.0
        self.addEventHandler(
            'keypress', name = 'f', function = self.OnFilter
        )
        self.addEventHandler(
            'keypress', name = 'l', function = self.OnLightToggle
        )
       
        print self.usage
        glLightfv( GL_LIGHT1, GL_AMBIENT, GLfloat_4(0.2, .2, .2, 1.0) );
        glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_3(.8,.8,.8));
        glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(-2,0,3,1) );
    def loadImages( self, imageName = "nehe_wall.bmp" ):
        """Load an image from a file using PIL,
        produces 3 textures to demo filter types.
        Converts the paletted image to RGB format.
        """
        im = open(imageName)
        try:
            ## Note the conversion to RGB the crate bitmap is paletted!
            im = im.convert( 'RGB')
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
        assert ix*iy*4 == len(image), """Image size != expected array size"""
        IDs = []
        # a Nearest-filtered texture...
        ID = glGenTextures(1)
        IDs.append( ID )
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        # linear-filtered
        ID = glGenTextures(1)
        IDs.append( ID )
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        # linear + mip-mapping
        ID = glGenTextures(1)
        IDs.append( ID )
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        print 'doing mip-maps, fails on RedHat Linux'
        gluBuild2DMipmaps(
            GL_TEXTURE_2D,
            GL_RGBA, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, image
        )
        print 'finished mip-mapped'
        return IDs
    def Render( self, mode = 0):
        BaseContext.Render( self, mode )
        if self.lightsOn:
            glEnable( GL_LIGHTING )
            glEnable(GL_LIGHT1);
            glDisable(GL_LIGHT0);
        else:
            glDisable( GL_LIGHTING )
            glDisable(GL_LIGHT1);
            glDisable(GL_LIGHT0);
        glTranslatef(1.5,0.0,self.currentZOffset);
        glEnable(GL_TEXTURE_2D)
        # re-select our texture, could use other generated textures
        # if we had generated them earlier...
        glBindTexture(GL_TEXTURE_2D, self.imageIDs[self.currentFilter])
        
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
    ### Callback-handlers
    def OnIdle( self, ):
        self.triggerRedraw(1)
        return 1
    def OnFilter( self, event):
        """Handles the key event telling us to change the filter"""
        self.currentFilter = (self.currentFilter + 1 ) % 3
        print 'Drawing filter now %s'% (
            ["Nearest","Linear","Linear Mip-Mapped"][ self.currentFilter]
        )
    def OnLightToggle( self, event ):
        """Handles the key event telling us to toggle the lighting"""
        self.lightsOn = not self.lightsOn
        print "Lights now %s"% (["off", "on"][self.lightsOn])
    def drawCube( self ):
        "Draw a cube with both normals and texture coordinates"
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

if __name__ == "__main__":
    TestContext.ContextMainLoop()
