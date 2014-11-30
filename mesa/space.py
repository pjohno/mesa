'''
Mesa Space Module
=================================

Objects used to add a spatial component to a model.

Grid: base grid, a simple list-of-lists.

MultiGrid: extension to Grid where each cell is a set of objects.

'''
# Instruction for PyLint to suppress variable name errors, since we have a
# good reason to use one-character variable names for x and y.
# pylint: disable=invalid-name

class Grid(object):
    '''
    Base class for a square grid.

    Grid cells are indexed by [y][x], where [0][0] is assumed to be the top-left
    and [height-1][width-1] is the bottom-right. If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether to treat the grid as a torus.

        grid: Internal list-of-lists which holds the grid cells themselves.
        default_val: Lambda function to populate each grid cell with None.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
    '''

    width = None
    height = None
    torus = False
    grid = None
    default_val = lambda s: None

    def __init__(self, height, width, torus):
        '''
        Create a new grid.

        Args:
            height, width: The height and width of the grid
            torus: Boolean whether the grid wraps or not.
        '''
        self.height = height
        self.width = width
        self.torus = torus

        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.default_val())
            self.grid.append(row)

    def __getitem__(self, index):
        return self.grid[index]

    def _get_x(self, x):
        '''
        Convert X coordinate, handling torus looping.
        '''
        if x >= 0 and x < self.width:
            return x
        if not self.torus:
            raise Exception("Coordinate out of bounds.")
        else:
            return x % self.width

    def _get_y(self, y):
        '''
        Convert Y coordinate, handling torus looping.
        '''
        if y >= 0 and y < self.height:
            return y
        if not self.torus:
            raise Exception("Coordinate out of bounds.")
        else:
            return y % self.height

    def get_neighbors(self, x, y, moore, include_center=False):
        '''
        Return a list of neighbors to a certain point.

        Args:
            x, y: Coordinates for the neighborhood to get.
            moore: If True, return Moore neighborhood (including diagonals)
                   If False, return Von Neumann neighborhood (exclude diagonals)
            include_center: If True, return the (x, y) cell as well. Otherwise,
                            return surrounding cells only.

        Returns:
            A list of non-None objects in the given neighborhood; at most 9 if
            Moore, 5 if Von-Neumann (8 and 4 if not including the center).
        '''
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0 and not include_center:
                    continue
                # Skip diagonals on Moore neighborhood.
                if not moore and dy != 0 and dx != 0:
                    continue
                # Skip if not a torus and new coords out of bounds.
                if not self.torus and (not (0 < dx+x < self.width) or
                        not (0 < dy+y < self.height)):
                    continue

                px = self._get_x(x + dx)
                py = self._get_y(y + dy)
                self._add_members(neighbors, px, py)
        return neighbors

    def _add_members(self, target_list, x, y):
        '''
        Helper method to append the contents of a cell to the given list.
        Override for other grid types.
        '''
        if self.grid[y][x] is not None:
            target_list.append(self.grid[y][x])




class MultiGrid(Grid):
    '''
    Grid where each cell can contain more than one object.

    Grid cells are indexed by [y][x], where [0][0] is assumed to be the top-left
    and [height-1][width-1] is the bottom-right. If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other.

    Each grid cell holds a set object.

    Properties:
        width, height: The grid's width and height.

        torus: Boolean which determines whether to treat the grid as a torus.

        grid: Internal list-of-lists which holds the grid cells themselves.
        default_val: Lambda function to populate grid cells with an empty set.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
    '''

    default_val = lambda s: set()

    def _add_members(self, target_list, x, y):
        '''
        Helper method to add all objects in the given cell to the target_list.
        '''
        for a in self.grid[y][x]:
            target_list.append(a)

