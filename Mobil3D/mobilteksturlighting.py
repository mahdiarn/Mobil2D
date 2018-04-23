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
"""
    initialPosition = (0,0,3) # set initial camera position, tutorial does the re-positioning
    def OnInit( self ):
        """Load the image on initial load of the application"""
        self.imageIDs = self.loadImages()
        self.currentFilter = 0 # index into imageIDs
        self.lightsOn = 1 # boolean
        self.currentZOffset = -6
        self.rotationCycle = 8.0
	self.lightIntensity = 1
        self.addEventHandler(
            'keypress', name = 'f', function = self.OnFilter
        )
        self.addEventHandler(
            'keypress', name = 'l', function = self.OnLighterToggle
        )
	self.addEventHandler(
            'keypress', name = 'k', function = self.OnDarkerToggle
        )
       
        print self.usage
        glLightfv( GL_LIGHT1, GL_AMBIENT, GLfloat_4(0.2, .2, .2, 1) );
        glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_3(self.lightIntensity,self.lightIntensity,self.lightIntensity));
        glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(0,0,3,1) );
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
        glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_3(self.lightIntensity,self.lightIntensity,self.lightIntensity));
        glTranslatef(1.5,0.0,self.currentZOffset);
        glEnable(GL_TEXTURE_2D)
        # re-select our texture, could use other generated textures
        # if we had generated them earlier...
        glBindTexture(GL_TEXTURE_2D, self.imageIDs[self.currentFilter])
        
        self.drawCube()
        self.drawRoad()
        self.drawHouse()
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
    def OnLighterToggle( self, event ):
        """Handles the key event telling us to toggle the lighting"""
        self.lightIntensity = self.lightIntensity + 0.1
        print "Lights now %d"% (self.lightIntensity)
    def OnDarkerToggle( self, event ):
        """Handles the key event telling us to toggle the lighting"""
        self.lightIntensity = self.lightIntensity - 0.1
        print "Lights now %d"% (self.lightIntensity)
    def drawCube( self ):
        "Draw a cube with both normals and texture coordinates"
        glBegin(GL_TRIANGLES);
        #Bagian atas
        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  0);
        glTexCoord2f(0.25, 0.0); glVertex3f(1.0, -1.0,  0);

        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.0, 0.25); glVertex3f(-3.0, 1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  0);
        #Samping kanan (besar)
        glTexCoord2f(0.0, 0.25); glVertex3f(-3.0, -1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  -2.0);
        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, -1.0,  0);

        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, -1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0,  -2.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(1.0, -1.0,  -2.0);
        #Samping kanan (kecil)
        glTexCoord2f(0.0, 0.25); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0,  -2.0);
        glTexCoord2f(0.25, 0.25); glVertex3f(2.0, -1.0,  -1.0);

        glTexCoord2f(0.25, 0.25); glVertex3f(2.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0,  -2.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(2.0, -1.0,  -2.0);
        #Samping kiri (Besar)
        glTexCoord2f(0.0, 0.25); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.25, 0.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.25, 0.25); glVertex3f(-3.0, 1.0,  0);

        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, 1.0,  -2.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(1.0, 1.0,  0);
        #Samping kiri (Kecil)
        glTexCoord2f(0.0, 0.25); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(1.0, 1.0,  -2.0);
        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, 1.0,  -1.0);

        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, 1.0,  -2.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(1.0, 1.0,  -2.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(2.0, 1.0,  -1.0);
        #pantat mobil
        glTexCoord2f(0.5, 0.5); glVertex3f(-3.0, -1.0,  0);
        glTexCoord2f(0.25, 0.25); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.5, 0.25); glVertex3f(-3.0, -1.0,  -2.0);
        
        glTexCoord2f(0.25, 0.5); glVertex3f(-3.0, 1.0,  0);
        glTexCoord2f(0.25, 0.25); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.5, 0.5); glVertex3f(-3.0, -1.0,  0);
        #kaca depan
        glTexCoord2f(0.0, 0.25); glVertex3f(1.0, -1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, 1.0,  0);

        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, 1.0,  0);
        glTexCoord2f(0.0, 0.0); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(1.0, 1.0,  -1.0);
        #hood
        glTexCoord2f(0.25, 0.0); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.25, 0.25); glVertex3f(1.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(1.0, -1.0,  -1.0);

        glTexCoord2f(0.25, 0.0); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(1.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, -1.0,  -1.0);
        #moncong
        glTexCoord2f(0.25, 0.25); glVertex3f(2.0, 1.0,  -1.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(2.0, -1.0,  -1.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(2.0, 1.0,  -2.0);

        glTexCoord2f(0.0, 0.25); glVertex3f(2.0, -1.0,  -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(2.0, -1.0,  -2.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(2.0, 1.0,  -2.0);
        #alas
        glTexCoord2f(0.25, 0.25); glVertex3f(2.0, -1.0,  -2.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(-3.0, -1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.0,  -2.0);
        
        glTexCoord2f(0.25, 0.25); glVertex3f(2.0, -1.0,  -2.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.0,  -2.0);
        glTexCoord2f(0.25, 0.0); glVertex3f(2.0, 1.0,  -2.0);
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
        glTexCoord2f(0.5, 0.25)
        glVertex3f(0, 0, h/2.0)
        for (x, y) in circle_pts:
            z = h/2.0
            glTexCoord2f(0.25, 0.0)
            glVertex3f(x, y, z)
        glEnd()
        
        
        glBegin(GL_TRIANGLE_FAN)#drawing the front circle
        glTexCoord2f(0.25, 0.0)
        glVertex3f(0, 0, h/2.0)
        for (y, x) in circle_pts:
            z = -h/2.0
            glTexCoord2f(0.5, 0.25)
            glVertex3f(x, y, z)
        glEnd()
        
        glBegin(GL_TRIANGLE_STRIP)#draw the tube        
        for (x, y) in circle_pts:
            z = h/2.0
            glTexCoord2f(0.5, 0.25)
            glVertex3f(x, y, z)
            glTexCoord2f(0.25, 0.0)
            glVertex3f(x, y, -z)
        glEnd()

    def drawRoad( self ):
        glBegin(GL_TRIANGLES);
        glTexCoord2f(0.25, 0.5); glVertex3f(20.0, 3.0,  -3.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(-20.0, -3.0,  -3.0);
        glTexCoord2f(0.25, 0.25); glVertex3f(20.0, -3.0,  -3.0);

        glTexCoord2f(0.25, 0.5); glVertex3f(20.0, 3.0,  -3.0);
        glTexCoord2f(0.0, 0.5); glVertex3f(-20.0, 3.0,  -3.0);
        glTexCoord2f(0.0, 0.25); glVertex3f(-20.0, -3.0,  -3.0);
        glEnd();
    def drawHouse( self ):
        
        glBegin(GL_TRIANGLES)
        x=[0,1,2,4,5,6,0,2,4,6,0,1,2,3,4,5,6,1,2,3,4,5,2,3,4,3]
        y=[0,0,0,0,0,0,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,4,4,4,5]
        
        #tembok depan
        for n in range(len(x)):
            glTexCoord2f(0.5, 0.25); glVertex3f(x[n]+(-3.0), 3.0, y[n]+(-2.0));
            glTexCoord2f(0.5, 0.0); glVertex3f(x[n]+(-3.0), 3.0, y[n]+(-3.0));
            glTexCoord2f(0.75, 0.25); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-2.0));

            glTexCoord2f(0.75, 0.25); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-2.0));
            glTexCoord2f(0.5, 0.0); glVertex3f(x[n]+(-3.0), 3.0,  y[n]+(-3.0));
            glTexCoord2f(0.75, 0.0); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-3.0));
        #tembok segtiga kiri
        x=[0,1,2]
        y=[3,4,5] 
        for n in range(len(x)):
            glTexCoord2f(0.75, 0.25); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-2.0));
            glTexCoord2f(0.5, 0.0); glVertex3f(x[n]+(-3.0), 3.0,  y[n]+(-3.0));
            glTexCoord2f(0.75, 0.0); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-3.0));       
        #tembok segtiga kanan
        x=[4,5,6]
        y=[5,4,3]
        for n in range(len(x)):
            glTexCoord2f(0.75, 0.25); glVertex3f(x[n]+(-3.0), 3.0,  y[n]+(-2.0));
            glTexCoord2f(0.5, 0.0); glVertex3f(x[n]+(-3.0), 3.0,  y[n]+(-3.0));
            glTexCoord2f(0.75, 0.0); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-3.0));       
        #jendela
        x=[1,5]
        y=[1,1]
        for n in range(len(x)):
            glTexCoord2f(0.75, 0.25); glVertex3f(x[n]+(-3.0), 3.0, y[n]+(-2.0));
            glTexCoord2f(0.75, 0.0); glVertex3f(x[n]+(-3.0), 3.0, y[n]+(-3.0));
            glTexCoord2f(1.0, 0.25); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-2.0));

            glTexCoord2f(1.0, 0.25); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-2.0));
            glTexCoord2f(0.75, 0.0); glVertex3f(x[n]+(-3.0), 3.0,  y[n]+(-3.0));
            glTexCoord2f(1.0, 0.0); glVertex3f(x[n]+(-2.0), 3.0,  y[n]+(-3.0));
        
        #pintu bawah
        x=3
        y=0

        glTexCoord2f(0.0, 0.75); glVertex3f(x+(-3.0), 3.0, y+(-2.0));
        glTexCoord2f(0.0, 0.5); glVertex3f(x+(-3.0), 3.0, y+(-3.0));
        glTexCoord2f(0.25, 0.75); glVertex3f(x+(-2.0), 3.0,  y+(-2.0));

        glTexCoord2f(0.25, 0.75); glVertex3f(x+(-2.0), 3.0,  y+(-2.0));
        glTexCoord2f(0.0, 0.5); glVertex3f(x+(-3.0), 3.0,  y+(-3.0));
        glTexCoord2f(0.25, 0.5); glVertex3f(x+(-2.0), 3.0,  y+(-3.0));

        #pintu atas
        y=1

        glTexCoord2f(0.0, 1.0); glVertex3f(x+(-3.0), 3.0, y+(-2.0));
        glTexCoord2f(0.0, 0.75); glVertex3f(x+(-3.0), 3.0, y+(-3.0));
        glTexCoord2f(0.25, 1.0); glVertex3f(x+(-2.0), 3.0,  y+(-2.0));

        glTexCoord2f(0.25, 1.0); glVertex3f(x+(-2.0), 3.0,  y+(-2.0));
        glTexCoord2f(0.0, 0.75); glVertex3f(x+(-3.0), 3.0,  y+(-3.0));
        glTexCoord2f(0.25, 0.75); glVertex3f(x+(-2.0), 3.0,  y+(-3.0));

        #tembok kiri
        x=[0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
        y=[0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]

        for n in range(len(x)):
            glTexCoord2f(0.75, 0.25); glVertex3f(-3.0, 3.0+x[n], -2.0+y[n]);
            glTexCoord2f(0.5, 0.0); glVertex3f(-3.0, 4.0+x[n], -3.0+y[n]);
            glTexCoord2f(0.75, 0.0); glVertex3f(-3.0, 3.0+x[n], -3.0+y[n]);

            glTexCoord2f(0.5, 0.25); glVertex3f(-3.0, 4.0+x[n], -2.0+y[n]);
            glTexCoord2f(0.5, 0.0); glVertex3f(-3.0, 4.0+x[n], -3.0+y[n]);
            glTexCoord2f(0.75, 0.25); glVertex3f(-3.0, 3.0+x[n], -2.0+y[n]);

        #tembok kanan

        x=[0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
        y=[0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]

        for n in range(len(x)):
            glTexCoord2f(0.75, 0.25); glVertex3f(4.0, 4.0+x[n], -2.0+y[n]);
            glTexCoord2f(0.5, 0.25); glVertex3f(4.0, 3.0+x[n], -2.0+y[n]);
            glTexCoord2f(0.75, 0.0); glVertex3f(4.0, 4.0+x[n], -3.0+y[n]);

            glTexCoord2f(0.5, 0.25); glVertex3f(4.0, 3.0+x[n], -2.0+y[n]);
            glTexCoord2f(0.5, 0.0); glVertex3f(4.0, 3.0+x[n], -3.0+y[n]);
            glTexCoord2f(0.75, 0.0); glVertex3f(4.0, 4.0+x[n], -3.0+y[n]);
        
        #genteng kanan

        x=[0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
        y=[-1,-1,-1,-1,-1,0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]

        for n in range(len(x)):
            glTexCoord2f(0.75, 0.5); glVertex3f(3.0-y[n], 4.0+x[n], 1.0+y[n]);
            glTexCoord2f(0.5, 0.5); glVertex3f(3.0-y[n], 3.0+x[n], 1.0+y[n]);
            glTexCoord2f(0.75, 0.25); glVertex3f(4.0-y[n], 4.0+x[n], 0.0+y[n]);

            glTexCoord2f(0.5, 0.5); glVertex3f(3.0-y[n], 3.0+x[n], 1.0+y[n]);
            glTexCoord2f(0.5, 0.25); glVertex3f(4.0-y[n], 3.0+x[n], 0.0+y[n]);
            glTexCoord2f(0.75, 0.25); glVertex3f(4.0-y[n], 4.0+x[n], 0.0+y[n]);

        #genteng kiri
        x=[0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
        y=[-1,-1,-1,-1,-1,0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]

        for n in range(len(x)):
            glTexCoord2f(0.75, 0.5); glVertex3f(-2.0+y[n], 3.0+x[n], 1.0+y[n]);
            glTexCoord2f(0.5, 0.25); glVertex3f(-3.0+y[n], 4.0+x[n], 0.0+y[n]);
            glTexCoord2f(0.75, 0.25); glVertex3f(-3.0+y[n], 3.0+x[n], 0.0+y[n]);

            glTexCoord2f(0.5, 0.5); glVertex3f(-2.0+y[n], 4.0+x[n], 1.0+y[n]);
            glTexCoord2f(0.5, 0.25); glVertex3f(-3.0+y[n], 4.0+x[n], 0.0+y[n]);
            glTexCoord2f(0.75, 0.5); glVertex3f(-2.0+y[n], 3.0+x[n], 1.0+y[n]);

        #genteng atas

        y = [0,1,2,3,4]
        for n in range(len(y)):
            glTexCoord2f(0.75, 0.5); glVertex3f(1.0, 4.0+y[n],  3.0);
            glTexCoord2f(0.5, 0.25); glVertex3f(0.0, 3.0+y[n],  3.0);
            glTexCoord2f(0.75, 0.25); glVertex3f(1.0, 3.0+y[n],  3.0);

            glTexCoord2f(0.75, 0.5); glVertex3f(1.0, 4.0+y[n],  3.0);
            glTexCoord2f(0.5, 0.5); glVertex3f(0.0, 4.0+y[n],  3.0);
            glTexCoord2f(0.5, 0.25); glVertex3f(0.0, 3.0+y[n],  3.0);

        #tembok belakang
        x=[0,1,2,3,4,5,6,0,1,2,3,4,5,6,0,1,2,3,4,5,6,1,2,3,4,5,2,3,4,3]
        y=[0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,4,4,4,5]

        for n in range(len(x)):
            glTexCoord2f(0.5, 0.25); glVertex3f(-2.0+x[n], 8.0,  -2.0+y[n]);
            glTexCoord2f(0.75, 0.0); glVertex3f(-3.0+x[n], 8.0,  -3.0+y[n]);
            glTexCoord2f(0.75, 0.25); glVertex3f(-3.0+x[n], 8.0,  -2.0+y[n]);

            glTexCoord2f(0.5, 0.0); glVertex3f(-2.0+x[n], 8.0,  -3.0+y[n]);
            glTexCoord2f(0.75, 0.0); glVertex3f(-3.0+x[n], 8.0,  -3.0+y[n]);
            glTexCoord2f(0.5, 0.25); glVertex3f(-2.0+x[n], 8.0,  -2.0+y[n]);

        #tembok segtiga kiri
        x=[0,1,2]
        y=[3,4,5] 
        for n in range(len(x)):
            glTexCoord2f(0.5, 0.0); glVertex3f(-2.0+x[n], 8.0,  -3.0+y[n]);
            glTexCoord2f(0.75, 0.0); glVertex3f(-3.0+x[n], 8.0,  -3.0+y[n]);
            glTexCoord2f(0.5, 0.25); glVertex3f(-2.0+x[n], 8.0,  -2.0+y[n]);    

        #tembok segtiga kanan
        x=[4,5,6]
        y=[5,4,3]
        for n in range(len(x)):
            glTexCoord2f(0.5, 0.0); glVertex3f(-2.0+x[n], 8.0,  -3.0+y[n]);
            glTexCoord2f(0.75, 0.0); glVertex3f(-3.0+x[n], 8.0,  -3.0+y[n]);
            glTexCoord2f(0.5, 0.25); glVertex3f(-3.0+x[n], 8.0,  -2.0+y[n]);    

        glEnd();

        

if __name__ == "__main__":
    TestContext.ContextMainLoop()
