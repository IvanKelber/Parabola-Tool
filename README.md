For my final project, I created an online parabola tool.

parabolas.py contains the function, find_general_parabola, that does the actual computations:
it accepts as its arguments a set of three points on the Cartesian plane and an angle and returns
the coefficients of an equation that passes through those points with an axis of symmetry that intersects
the y-axis at the given angle.  When the angle is greater than zero, it achieves this by rotating the
input points themselves and calculating the coefficients (a, b, c) for the equation for a standard vertical
parabola, then finding the focus and directrix and rotating those back in order to find the
coefficients (a, b, c, d, e, f) of a general case parabola.  The standard vertical parabola is
computed by entering values derived from the input points into a matrix and performing row operations
in order to solve a series of linear equations.

parabolas.html shows the structure of a basic web application that provides a user interface to
interact with parabolas.py.  Using flask and CSS, a grid is set up consisting of cells that form a grid,
with each cell acting as a coordinate on a graph.  When users click on three such cells, a JavaScript function
submits a hidden form using a POST request to send the selected coordinates to application.py, which sends the
information to parabolas.py and then renders parabolas.html again with the coordinates that lie on the parabola
darkened.  An angle button in the side navigation bar allows users to select the angle.