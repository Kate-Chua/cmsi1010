from math import radians
from Tree.core import Tree
from PIL import Image

background_color = (200, 0, 0)
leaf_color = (30, 160, 30)
trunk_width = 0.5
base_trunk_color = (0, 0, 200)
small_branch_color = (200, 0, 0)
branch_gradient = (*base_trunk_color, *small_branch_color)

trunk_length = 200
first_branch_line = (0, 0, 0, -trunk_length)
scales_and_angles = [(0.75, radians(-30)),
                     (0.2, radians(30), (0.2, radians(30)))]
age = 14

tree = Tree(pos=first_branch_line, branches=scales_and_angles)
tree.grow(age)
tree.move_in_rectangle()
image = Image.new("RGB", tree.get_size(), background_color)
tree.draw_on(image, branch_gradient, leaf_color, trunk_width)
image.show()
