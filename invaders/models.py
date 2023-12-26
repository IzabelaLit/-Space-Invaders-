"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Izabela L. & Luca G.
12/04/2023
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """

    # GETTERS AND SETTERS
    def getX(self):
        """
        Returns the x-coordinate of the center of the ship.
        """
        return self.x

    def setX(self, pos):
        """
        Sets the x-coordinate of the ship to pos.

        Parameter pos: the x-coordinate of the ship
        Precondition: pos is a float >= 0 and <= GAME_WIDTH
        """
        assert isinstance(pos, float)
        self.x = pos

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,w,h=SHIP_BOTTOM):
        """
        Creates a ship centered at (w,h).

        The ship has a width of SHIP_WIDTH, a height of SHIP_HEIGHT, and the
        image SHIP_IMAGE.

        Parameter w: the x-coordinate of the ship
        Precondition: w is a float >= 0 and <= GAME_WIDTH

        Parameter h: the y-coordinate of the ship
        Precondition: h is a float > 0 and < DEFENSE_LINE
        """
        assert isinstance(w,float)
        super().__init__(x=w,y=h,width=SHIP_WIDTH,height=SHIP_HEIGHT,\
        source=SHIP_IMAGE)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveShip(self,input,dt):
        """
        Moves the ship left if the 'a' key is pressed and right if the 'd' key
        is pressed.

        Parameter input: the keyboard input
        Precondition: input is a touched key on the keyboard.

        Parameter dt: the time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if input.is_key_down('a') and self.x >= SHIP_WIDTH/2: #Left
            self.setX(self.x - SHIP_MOVEMENT)
        if input.is_key_down('d') and self.x <= GAME_WIDTH - (SHIP_WIDTH /2): #Right
            self.setX(self.x + SHIP_MOVEMENT)

    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.getPlayer() == False: #Could only be hit if the alien shoots.
            w = self.contains((bolt.getX() - BOLT_WIDTH/2, bolt.getY() - \
            BOLT_HEIGHT/2))
            x = self.contains((bolt.getX() - BOLT_WIDTH/2, bolt.getY() + \
            BOLT_HEIGHT/2))
            y = self.contains((bolt.getX() + BOLT_WIDTH/2, bolt.getY() - \
            BOLT_HEIGHT/2))
            z = self.contains((bolt.getX() + BOLT_WIDTH/2, bolt.getY() + \
            BOLT_HEIGHT/2))
            return w or x or y or z
        else:
            return False


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """

    # GETTERS AND SETTERS
    def getX(self):
        """
        Returns the x-coordinate of the center of the alien.
        """
        return self.x

    def getY(self):
        """
        Returns the y-coordinate of the center of the alien.
        """
        return self.y

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,w,z,row):
        """
        Creates an alien centered at (w,z) with an image based off the row it's
        in.

        The alien image cycles between 3 different images every 2 rows.

        Parameter w: the x-coordinate of the alien
        Precondition: w is a float >= 0 and <= GAME_WIDTH

        Parameter z: the y-coordinate of the alien
        Precondition: z is a float > DEFENSE_LINE

        Parameter row: the row of the alien
        Precondition: row is an int >= 0 and < ALIEN_ROWS
        """
        super().__init__(x = w,y = z,width = ALIEN_WIDTH,height = \
        ALIEN_HEIGHT,source = ALIEN_IMAGES[(row % 6) // 2])

    # METHOD TO CHECK FOR COLLISION
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.getPlayer() == True:
            w = self.contains((bolt.getX() - BOLT_WIDTH/2, bolt.getY() - \
            BOLT_HEIGHT/2))
            x = self.contains((bolt.getX() - BOLT_WIDTH/2, bolt.getY() + \
            BOLT_HEIGHT/2))
            y = self.contains((bolt.getX() + BOLT_WIDTH/2, bolt.getY() - \
            BOLT_HEIGHT/2))
            z = self.contains((bolt.getX() + BOLT_WIDTH/2, bolt.getY() + \
            BOLT_HEIGHT/2))
            return w or x or y or z
        else:
            return False

    # METHODS
    def moveAlienRight(self):
        """
        Moves the aliens right by ALIEN_H_WALK.
        """
        self.x = self.x + ALIEN_H_WALK

    def moveAlienDown(self):
        """
        Moves the aliens down by ALIEN_V_WALK.
        """
        self.y = self.y - ALIEN_V_WALK

    def moveAlienLeft(self):
        """
        Moves the aliens left by ALIEN_H_WALK.
        """
        self.x = self.x - ALIEN_H_WALK


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _player: determines whether the bolt is from a player or alien
    # Invariant: _player is a bool; True is player, False is alien

    # GETTERS AND SETTERS
    def getX(self):
        """
        Returns the x-coordinate centered at the bolt.
        """
        return self.x

    def getY(self):
        """
        Returns the y-coordinate centered at the bolt.
        """
        return self.y

    def getPlayer(self):
        """
        Returns True if the bolt is shot by the ship and False if the bolt is
        shot by an alien.
        """
        return self._player

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,xpos,choseny,velocity,pl):
        """
        Creates a bolt centered at (xpos, choseny) with a velocity of velocity.

        The bolt has a height of BOLT_HEIGHT and a width of BOLT_WIDTH. The bolt
        fillcolor is 'blue' if it's shot by the player and 'red' if it's shot by
        the alien.

        Parameter xpos: the x-coordinate of the bolt
        Precondition: xpos is a float >= 0 and <= GAME_WIDTH

        Parameter choseny: the y-coordinate of the bolt
        Precondition: choseny is a float >= 0 and <= GAME_HEIGHT

        Parameter velocity: the velocity of the bolt
        Precondition: velocity is a float

        Parameter pl: pl is whether the bolt is shot by a ship or an alien
        Precondition: pl is a bool that's True if the bolt is from the ship and
        False if it's from the alien
        """
        if pl == True:
            super().__init__(x=xpos, y=choseny, width=BOLT_WIDTH, \
        height=BOLT_HEIGHT, fillcolor='blue')
        else:
            super().__init__(x=xpos, y=choseny, width=BOLT_WIDTH, \
        height=BOLT_HEIGHT, fillcolor='red')
        self._velocity = velocity
        self._player = pl

    # METHODS
    def moveBolt(self):
        """
        Moves the bolt vertically by self._velocity.
        """
        self.y = self.y + self._velocity


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class DefenseLine(GPath):
    """
    A class representing a defense line.
    """

    def __init__(self,p=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],lw=3):
        """
        Creates a defense line across the coordinates (0,DEFENSE_LINE) and
        (GAME_WIDTH,DEFENSE_LINE) with thickness lw and a linecolor of 'black'.

        Parameter p: p is a list of coordinates [x1,y1,x2,y2], where those two
        points are (x1,y1) and (x2,y2).
        Precondition: p's x-coordinates must be >= 0 and <= GAME_WIDTH. p's
        y-coordinates must be >= 0 and <= GAME_HEIGHT.

        Parameter lw: the width of the defense line
        Precondition: lw is a float > 0
        """
        super().__init__(points=p,linewidth=lw,linecolor='black')
