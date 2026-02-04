
# A‑Star Path Finding 🔧

A small Python project demonstrating the A* path finding algorithm in both a simple GUI and two text-based UIs.

## Files
- `a_star_gui.py` — Opens a GUI grid (Tkinter). Cells can be clicked to cycle: **Empty → Wall → Start → End → Empty**. Walls are shown as black buttons; when a start and end exist the algorithm automatically computes and shows a path.
- `a_star_text_1.py` — Text-based UI (console) showing the grid in one format.
- `a_star_text_2.py` — Alternate text-based UI (console) with a different representation.

## Usage
Run any interface with Python 3:

```bash
python a_star_gui.py
python a_star_text_1.py
python a_star_text_2.py
```

**Note:** The GUI typically requires Tkinter (standard in most Python installs).

---

## Configuration
You can modify grid size and other parameters directly in the source files.

### Movement Types
```
Around   Infront    Diagonal
* * *       *        *   *
* A *     * I *        D
* * *       *        *   *
```

for `a_star_gui.py` you can change the `size` variable and movement type: 
``` py
size = [20, 20]

# search_type = "around"
search_type = "infront"
# search_type = "diagonal"
```

for `a_star_text_1.py`, adjusting parameter:
``` py
# adjust the grid size
grid = cg.createGrid(15, 15, 0)

# start and end points
start = [2, 7]
finish = [14, 7]

# add in walls with
grid.wall(x, y)

# adjust movement type
movementType = "around"
# movementType = "infront"
# movementType = "diagonal"
path = findPath(startNode, finishNode, grid, movementType)
```

for `a_star_text_2.py`, modify the grid and parameters like so:
``` py
# adjust the grid size
rows = 22
cols = 78

# set start and end points
start = (1, 1)
end = (20, 76)
for point in finder.findpath(start, end):
    pass

# add walls
position1 = (10, 10)
position2 = (15, 20)
setline(matrix, position1, position2)
```

---

Enjoy experimenting with A* path finding!