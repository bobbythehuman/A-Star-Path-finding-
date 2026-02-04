import bisect


class AStarPathfinding(object):
    class Node(object):
        # item must be hashable
        def __init__(self, item, parent=None, gscore=0, heuristic=0):
            self.item = item
            self.parent = parent
            self.gscore = gscore
            self.heuristic = heuristic

        def __eq__(self, other):
            return other.item == self.item

        def __lt__(self, other):
            return self.gscore + self.heuristic < other.gscore + other.heuristic

        def __hash__(self):
            return hash(self.item)

        def __repr__(self):
            return "<%s(%s)>" % (self.__class__.__name__, repr(self.item))

    def heuristic(self, src, des):
        raise NotImplementedError

    def getchildren(self, node):
        raise NotImplementedError

    def available(self, node):
        return True

    def generate(self, node):
        path = list()
        while node:
            path.append(node.item)
            node = node.parent
        return path

    def findpath(self, start, end):
        path = list()
        openpath = dict()
        queue = list()
        closepath = set()
        found = False
        target = self.Node(end)
        node = self.Node(start)
        node.heuristic = self.heuristic(node, target)

        openpath[start] = node
        queue.append(node)
        while openpath and not found:
            current = queue.pop(0)
            openpath.pop(current.item)
            closepath.add(current)
            for node in self.getchildren(current):
                if not self.available(node):
                    continue
                elif node in closepath:
                    continue
                elif node == target:
                    path = self.generate(node)
                    found = True
                    break
                else:
                    duplicated = openpath.get(node.item)
                    if not duplicated:
                        node.heuristic = self.heuristic(node, target)
                        openpath[node.item] = node
                        bisect.insort_left(queue, node)
                    elif duplicated.gscore > node.gscore:
                        left = bisect.bisect_left(queue, duplicated)
                        right = bisect.bisect_right(queue, duplicated)
                        queue.pop(queue.index(duplicated, left, right))
                        node.heuristic = self.heuristic(node, target)
                        openpath[node.item] = node
                        bisect.insort_left(queue, node)
        return path


class D2(AStarPathfinding):
    def __init__(self, matrix, rows, cols):
        self.matrix = matrix
        self.rows = rows
        self.cols = cols

    def heuristic(self, src, des):
        x1, y1 = src.item
        x2, y2 = des.item
        return abs(x1 - x2) + abs(y1 - y2)

    def getchildren(self, node):
        x, y = node.item
        return [
            self.Node((x + 1, y), parent=node, gscore=node.gscore + 1),
            self.Node((x - 1, y), parent=node, gscore=node.gscore + 1),
            self.Node((x, y + 1), parent=node, gscore=node.gscore + 1),
            self.Node((x, y - 1), parent=node, gscore=node.gscore + 1),
        ]

    def available(self, node):
        x, y = node.item
        return 0 <= x < self.cols and 0 <= y < self.rows and self.matrix[y][x] == " "


if __name__ == "__main__":

    def printmatrix(matrix, width, height):
        for i in range(height):
            msg = []
            for j in range(width):
                msg.append(matrix[i][j])
            print(str().join(msg))

    def setpoint(matrix, point, char="X"):
        x, y = point
        matrix[y][x] = char

    def setline(matrix, p1, p2, char="X"):
        if p1 != p2:
            x1, y1 = p1
            x2, y2 = p2
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    matrix[y][x1] = char
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    matrix[y1][x] = char

    rows = 22
    cols = 78
    matrix = [[" " for j in range(cols)] for i in range(rows)]

    # - -
    setline(matrix, (10, 4), (34, 3))
    setline(matrix, (44, 4), (68, 4))

    # | |
    setline(matrix, (10, 4), (10, 11))
    setline(matrix, (68, 4), (68, 11))

    # --
    setline(matrix, (10, 11), (68, 11))

    # - -
    setline(matrix, (0, 14), (34, 14))
    setline(matrix, (44, 14), (77, 14))

    finder = D2(matrix, rows, cols)
    for point in finder.findpath((39, 8), (39, 18)):
        setpoint(matrix, point, "*")
    printmatrix(matrix, cols, rows)

    import timeit

    timer = timeit.Timer(
        "finder.findpath((39, 8), (39, 18))", globals={"finder": finder}
    )
    print(timer.timeit(1000))
