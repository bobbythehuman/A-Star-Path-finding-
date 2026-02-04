import tkinter as tk
import a_star_path_finder as pf
import extra.cg as cg
import extra.cn as cn
from enum import Enum


class ButtonState(Enum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    PATH = 4


class ButtonCreator:
    def __init__(self, button, xPos, yPos, y_size):
        self.xPos = xPos + 1
        self.yPos = y_size - yPos
        self.state = ButtonState.EMPTY
        self.button = button
        self.name = self.strip(button._w)
        self.node: cn.createNode = None

    @staticmethod
    def strip(value):
        return value[2:]


def create_button(window, x, y, y_size):
    b = tk.Button(window, bg="white", activebackground="white", height=2, width=3)
    b.grid(column=x, row=y, sticky="news")
    b["command"] = lambda: click(b)
    new_button = ButtonCreator(b, x, y, y_size)
    buttons[new_button.name] = new_button
    grid.link(new_button)
    if not new_button.node.walkable:
        walls.append(new_button)
        grid.wall(new_button.xPos, new_button.yPos)
        new_button.state = ButtonState.WALL
        new_button.button["bg"] = "black"
        new_button.button["activebackground"] = "black"


def update_button_state(button, new_state):
    button_value = buttons[ButtonCreator.strip(button._w)]
    # Delegate to set_button_state so node/wall/path data stay consistent
    set_button_state(button_value, new_state)


def clear_path():
    for node in path:
        # If the node has been turned into a WALL or is START/END, leave it as-is
        if node.button.state in (ButtonState.WALL, ButtonState.START, ButtonState.END):
            continue
        node.button.state = ButtonState.EMPTY
        node.button.button["bg"] = colour[node.button.state]
        node.button.button["activebackground"] = colour[node.button.state]
        node.reset()


def set_button_state(button_value, new_state):
    # Update logical state and UI
    button_value.state = new_state
    button_value.button["bg"] = colour[button_value.state]
    button_value.button["activebackground"] = colour[button_value.state]

    # Keep node model consistent with the button state
    if new_state == ButtonState.EMPTY:
        button_value.node.walkable = True
        button_value.node.state = "-"
        # If it was a wall, remove it
        if button_value in walls:
            walls.remove(button_value)
            grid.removeWall(button_value.xPos, button_value.yPos)
        # If it was part of the last path, remove it
        if button_value.node in path:
            try:
                path.remove(button_value.node)
            except ValueError:
                pass
        # If this button was an endpoint, clear that reference
        if end_points[0] == button_value:
            end_points[0] = None
        if end_points[1] == button_value:
            end_points[1] = None

    elif new_state == ButtonState.WALL:
        button_value.node.walkable = False
        button_value.node.state = "@"
        # If this button was an endpoint, clear that reference
        if end_points[0] == button_value:
            end_points[0] = None
        if end_points[1] == button_value:
            end_points[1] = None
        if button_value not in walls:
            walls.append(button_value)
            grid.wall(button_value.xPos, button_value.yPos)

    elif new_state == ButtonState.START:
        button_value.node.walkable = True
        button_value.node.state = "S"
        if button_value in walls:
            walls.remove(button_value)
            grid.removeWall(button_value.xPos, button_value.yPos)

    elif new_state == ButtonState.END:
        button_value.node.walkable = True
        button_value.node.state = "E"
        if button_value in walls:
            walls.remove(button_value)
            grid.removeWall(button_value.xPos, button_value.yPos)

    elif new_state == ButtonState.PATH:
        # PATH is a visual/state only; node remains walkable
        button_value.node.walkable = True
        button_value.node.state = "*"

    # Ensure the underlying node.reset() will behave correctly when needed
    return button_value


def click(button):
    global path
    button_value = buttons[ButtonCreator.strip(button._w)]

    # If the user clicks a path node, convert it to a wall
    if button_value.state == ButtonState.PATH:
        new_state = ButtonState.WALL
    else:
        # Cycle states explicitly
        if button_value.state == ButtonState.EMPTY:
            new_state = ButtonState.WALL
        elif button_value.state == ButtonState.WALL:
            new_state = ButtonState.START
        elif button_value.state == ButtonState.START:
            new_state = ButtonState.END
        elif button_value.state == ButtonState.END:
            new_state = ButtonState.EMPTY
        else:
            new_state = ButtonState.EMPTY

    # Apply new state to the UI and model
    update_button_state(button, new_state)

    if end_points[0] == end_points[1] == None:
        path.clear()

    clear_path()

    if new_state == ButtonState.START:
        set_start_point(button_value)

    elif new_state == ButtonState.END:
        set_end_point(button_value)

    if end_points[0] == end_points[1]:
        end_points[0] = None

    if all(end_points):
        start_node = end_points[0].node
        end_node = end_points[1].node
        if not skip:
            new_path = pf.findPath(start_node, end_node, grid, search_type)
            nodes_search = new_path[0]
            new_path.pop(0)
        else:
            new_path = path.copy()
            nodes_search = 0
        path.clear()

        if new_path:
            for node in new_path:
                # Don't overwrite the start or end button appearance
                if node.button.state in (ButtonState.START, ButtonState.END):
                    continue
                set_button_state(node.button, ButtonState.PATH)
            path += new_path.copy()
            print("nodes in path", len(path))
        else:
            print("no path")
        print("nodes searched", nodes_search)
        print()


def set_start_point(button_value):
    prev = end_points[0]
    if prev:
        prev.state = ButtonState.EMPTY
        set_button_state(prev, ButtonState.EMPTY)
        prev.node.state = "-"
    button_value.node.walkable = True
    end_points[0] = button_value
    # Use a simple string marker for display/debug
    button_value.node.state = "S"
    # Make sure the button UI reflects that it's the start
    set_button_state(button_value, ButtonState.START)


def set_end_point(button_value):
    prev = end_points[1]
    if prev:
        prev.state = ButtonState.EMPTY
        set_button_state(prev, ButtonState.EMPTY)
        prev.node.state = "-"
    end_points[1] = button_value
    end_points[0] = None
    # Use a simple string marker for display/debug
    button_value.node.state = "E"
    # Make sure the button UI reflects that it's the end
    set_button_state(button_value, ButtonState.END)


colour = {
    ButtonState.EMPTY: "white",
    ButtonState.START: "green",
    ButtonState.END: "red",
    ButtonState.WALL: "black",
    ButtonState.PATH: "blue",
}
buttons = {}

size = [20, 20]

# search_type = "around"
search_type = "infront"
# search_type = "diagonal"

grid = cg.createGrid(size[0], size[1], 30)
end_points: list[ButtonCreator | None] = [None, None]
walls = []
path = []
skip = False

window = tk.Tk()
for x in range(size[0]):
    window.columnconfigure(x, weight=1, minsize=10)
    window.rowconfigure(x, weight=1, minsize=5)
    for y in range(size[1]):
        create_button(window, x, y, size[1])

# w = main(size[0], size[1])

tk.mainloop()
