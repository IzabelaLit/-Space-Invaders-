"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Izabela L. & Luca G.
12/04/2023
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _savedx: the ship position when a life is lost
    # Invariant: _savedx is a float >= 0 and <= GAME_WIDTH

    # Attribute _num: the first attribute that helps keep track of alien movement
    # Invariant: _num is an int >= 0

    # Attribute _down: the second attribute that helps keep track of alien movement
    # Invariant: _down is an int >= 0

    # Attribute _walkies: the number of steps each alien takes per _fire interval
    # Invariant: _walkies is an int >= 0 that resets to 0 each time it's >= _fire

    # Attribute _fire: the step number at which an alien fires a bolt
    # Invariant: _fire is an int >= 1 and <= BOLT_RATE

    # Attribute _destroyed: whether all the aliens are destroyed or not
    # Invariant: _destroyed is a bool that is True when there are no aliens left
    # in self._aliens

    # Attribute _passed: whether the botom row of aliens has passed the _dline
    # Invariant: _passed is a bool that is True if the aliens have passed the
    # _dline and is False if they haven't

    # GETTERS AND SETTERS
    def getShip(self):
        """
        Returns the player ship to control.
        """
        return self._ship

    def setShip(self, value):
        """
        Creates a new ship centered at a specific x and y coordinate.

        Parameter value: the new ship being created
        Precondition: value is a Ship object
        """
        assert isinstance(value, Ship)
        self._ship = value

    def getAlien(self,row,col):
        """
        Returns an alien from the 2D list of aliens in the wave.

        Parameter row: the row of the alien
        Precondition: row is an int >= 0 and an int < ALIEN_ROWS

        Parameter col: the col of the alien
        Precondition: col is an int >= 0 and an int < ALIENS_IN_ROW
        """
        if self._aliens[row][col] != None:
            return self._aliens[row][col]

    def getBolts(self):
        """
        Returns the list of bolt objects.
        """
        return self._bolts

    def getLives(self):
        """
        Returns the number of lives left.
        """
        return self._lives

    def getPassed(self):
        """
        Returns a bool specifying whether the aliens have passed the _dline.
        """
        return self._passed

    def getDestroyed(self):
        """
        Returns a bool specifying whether the array self._aliens is empty.
        """
        return self._destroyed

    def getSavedX(self):
        """
        Returns the position of x at which the player ship lost a life.
        """
        return self._savedx

    # INITIALIZER TO CREATE SHIP AND ALIENS
    def __init__(self,height=GAME_HEIGHT,width=GAME_WIDTH):
        """
        Initializes a wave of aliens, bolts, and the ship inside a game window.

        The wave of aliens is a nested list of ALIEN_ROWS by ALIENS_IN_ROW. The
        ship spawns at (width/2, SHIP_HEIGHT). Additionally creates an array of
        bolts that will store all of the on-screen bolts and a _dline that
        the player must prevent the aliens from passing.

        DEFAULT: The game window has a height of GAME_HEIGHT and a width
        of GAME_WIDTH.

        Parameter height: is window height
        Precondition: height is an int > 0

        Parameter width: is window width
        Precondition: width is an int > 0
        """
        #Creates the 2D nested list of aliens.
        self._aliens = []
        for row in range(ALIEN_ROWS):
            r = []
            for col in range(ALIENS_IN_ROW):
                r.append(0)
            self._aliens.append(r)
        for row in range(ALIEN_ROWS):
            for col in range (ALIENS_IN_ROW):
                x = ALIEN_H_SEP + (ALIEN_WIDTH / 2) + col * (ALIEN_H_SEP + \
                ALIEN_WIDTH)
                y = height - ALIEN_CEILING - ALIEN_HEIGHT / 2 - ((ALIEN_ROWS - \
                (row + 1)) * (ALIEN_V_SEP + ALIEN_HEIGHT))
                self._aliens[row][col] = Alien(x,y,row)
        self._ship = Ship(width/2)
        self._savedx = width/2
        self._dline = DefenseLine()
        self._time = 0
        self._num = 0
        self._down = 0
        self._bolts = []
        self._walkies = 0
        self._fire = random.randint(1,BOLT_RATE)
        self._lives = SHIP_LIVES
        self._destroyed = False
        self._passed = False

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Moves and removes the ship, bolts, and aliens.

        Aliens move every time self._time reaches ALIEN_SPEED. If the aliens go
        across the _dline, then self._passed is True. If all of the aliens are
        destroyed, then self._destroyed is True.

        Parameter input: The keyboard input
        Precondition: input is a touched key on the keyboard.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self.getShip().moveShip(input,dt)
        q = []
        for x in range(len(self._bolts)):
            self._bolts[x].moveBolt()
            if(self._bolts[x].getY() - BOLT_HEIGHT / 2 <= GAME_HEIGHT and \
            self._bolts[x].getY() + BOLT_HEIGHT / 2 > 0):
                q.append(self._bolts[x])
        self._bolts = q[:]
        for y in range(len(q)):
            self.delEntity(q[y])
        if self.aliensDead() == True:
            self._destroyed = True
        elif self.bottomRowY() - ALIEN_HEIGHT / 2 < DEFENSE_LINE:
            self._passed = True
        elif(self._time <= ALIEN_SPEED): #Keeps track of the time.
            self._time = self._time + dt
        else: #Resets the time and makes the aliens move.
            self.alienMarch()
            self._walkies = self._walkies + 1
            if(self._walkies >= self._fire): #Makes the aliens fire.
                self._walkies = 0
                self.makeAlienBolt()
                self._fire = random.randint(1,BOLT_RATE)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the aliens, bolts, and ship into view.

        Parameter view: the view window
        Precondition: view is a GView.
        """
        for row in self._aliens: #Draws the aliens.
            for alien in row:
                if alien != None:
                    alien.draw(view)
        self._ship.draw(view) #Draws the ship.
        self._dline.draw(view)
        for x in range(len(self._bolts)):
            self._bolts[x].draw(view)

    #HELPER METHODS
    def firstColX(self):
        """
        Returns the x-coordinate of the left-most column of aliens.
        """
        for x in range(ALIEN_ROWS):
            if self._aliens[x][self.firstCol()] != None:
                alien = self._aliens[x][self.firstCol()]
                return alien.getX()

    def lastColX(self):
        """
        Returns the x-coordinate of the right-most column of aliens.
        """
        for x in range(ALIEN_ROWS):
            if self._aliens[x][self.lastCol()] != None:
                alien = self._aliens[x][self.lastCol()]
                return alien.getX()

    def firstCol(self):
        """
        Returns the number of the left-most non-empty column.
        """
        for x in range(ALIENS_IN_ROW):
            count = 0
            for y in range(len(self._aliens)):
                if self._aliens[y][x] != None:
                    count = count + 1
            if count > 0:
                return x
        return len(self._aliens)

    def lastCol(self):
        """
        Returns the number of the right-most non-empty column.
        """
        for x in range(ALIENS_IN_ROW):
            count = 0
            for y in range(len(self._aliens)):
                if self._aliens[y][ALIENS_IN_ROW - 1 - x] != None:
                    count = count + 1
            if count > 0:
                return ALIENS_IN_ROW - 1 - x

    def bottomRow(self):
        """
        Returns the bottom non-empty row number of aliens.
        """
        for x in range(len(self._aliens)):
            count = 0
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] != None:
                    count = count + 1
                if count > 0:
                    return x
        return None

    def bottomRowY(self):
        """
        Returns the y-coordinate of the bottom row of aliens.
        """
        for x in range(len(self._aliens[self.bottomRow()])):
            if self._aliens[self.bottomRow()][x] != None:
                alien = self._aliens[self.bottomRow()][x]
                return alien.getY()

    def alienMarch(self):
        """
        Coordinates the movement of aliens across the screen.

        First, the aliens step right until they're ALIEN_H_SEP away from the right
        side of the screen. Then, they move down a step and go left until they're
        ALIEN_H_SEP away from the left side of the screen. Lastly, they move a
        step down and repeat the process.
        """
        if self._down % 2 == 1:
            for row in range(ALIEN_ROWS):
                for col in range (ALIENS_IN_ROW):
                    if self._aliens[row][col] != None:
                        if self._num % 2 == 1:
                            self.getAlien(row,col).moveAlienLeft()
                        else:
                            self.getAlien(row,col).moveAlienRight()
            self._down = self._down + 1
        elif((self.lastColX() + (ALIEN_WIDTH / 2) > \
        GAME_WIDTH - ALIEN_H_SEP) or (self.firstColX() - \
        (ALIEN_WIDTH / 2) < ALIEN_H_SEP)):
            for row in range(ALIEN_ROWS):
                for col in range (ALIENS_IN_ROW):
                    if self._aliens[row][col] != None:
                        self.getAlien(row,col).moveAlienDown()
            self._num = self._num + 1
            self._down = self._down + 1
        elif self._num % 2 == 0:
            for row in range(ALIEN_ROWS):
                for col in range (ALIENS_IN_ROW):
                    if self._aliens[row][col] != None:
                        self.getAlien(row,col).moveAlienRight()
        elif self._num % 2 == 1:
            for row in range(ALIEN_ROWS):
                for col in range (ALIENS_IN_ROW):
                    if self._aliens[row][col] != None:
                        self.getAlien(row,col).moveAlienLeft()
        self._time = 0

    def makeBolt(self):
        """
        Creates a player ship bolt.
        """
        count = 0
        for x in range(len(self._bolts)):
            if self._bolts[x].getPlayer():
                count = count + 1
        if count == 0:
            ypos = (SHIP_BOTTOM + SHIP_HEIGHT + (BOLT_HEIGHT/2))
            self._bolts.append(Bolt(self._ship.getX(),ypos,BOLT_SPEED,True))

    def makeAlienBolt(self):
        """
        Creates an alien bolt.
        """
        list = []
        for x in range(ALIENS_IN_ROW):
            empty = True
            for y in range(ALIEN_ROWS):
                if(self._aliens[y][x] != None):
                    empty = False
            if(empty == False):
                list.append(x)
        call = random.randint(0,len(list) - 1)
        column = list[call]
        for x in range(ALIEN_ROWS):
            if(self._aliens[ALIEN_ROWS - 1 - x][column] != None):
                high = ALIEN_ROWS - 1 - x
        chosen = self._aliens[high][column]
        self._bolts.append(Bolt(chosen.getX(),chosen.getY() - \
        ALIEN_HEIGHT / 2,-1 * BOLT_SPEED,False))

    def delEntity(self, bolt):
        """
        Removes aliens and ship from screen and decreases player lives.

        Once an alien is shot, it's set to None. Once the ship is shot, it's set
        to None and self._lives is decreased by 1.

        Parameter bolt: the laser bolt to check
        Precondition: bolt of the class Bolt
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] != None:
                    if self._aliens[row][col].collides(bolt):
                        self._aliens[row][col] = None
                        self._bolts.remove(bolt)
        if self._ship != None:
            if self._ship.collides(bolt):
                self._lives = self._lives - 1
                self._bolts.remove(bolt)
                self._savedx = self._ship.getX()
                self._ship = None

    def aliensDead(self):
        """
        Returns True if all of the aliens are dead.
        """
        return self.bottomRow() == None
