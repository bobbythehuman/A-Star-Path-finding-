# might need to use if issue occurs
# import extra.cn as cn
import cn
from random import choices


class createGrid:
    def __init__(self, sizeX, sizeY, blockOff):
        self.Xsize = sizeX
        self.Ysize = sizeY
        self.nodes = []
        for y in range(self.Ysize):
            temp = []
            for x in range(self.Xsize):
                wallType = choices([True, False], weights=[100 - blockOff, blockOff])[0]
                if wallType:
                    temp.append(cn.createNode(wallType, x + 1, y + 1, "-"))
                else:
                    temp.append(cn.createNode(wallType, x + 1, y + 1, "@"))
            self.nodes.append(temp)

    def display(self):
        for line in reversed(self.nodes):
            temp = []
            for item in line:
                temp.append(item.state)
            print(*temp)
        print()

    def getNode(self, x, y):
        return self.nodes[y][x]

    def getNeighbours(self, node, searchType):
        neighbours = []
        if searchType == "around":
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    checkX = node.xPos + x
                    checkY = node.yPos + y

                    if (
                        checkX > 0
                        and checkX <= self.Xsize
                        and checkY > 0
                        and checkY <= self.Ysize
                    ):
                        neighbourNode = self.getNode(checkX - 1, checkY - 1)
                        neighbours.append(neighbourNode)

        elif searchType == "diagonal":
            for x in range(-1, 2, 2):
                for y in range(-1, 2, 2):
                    if x == 0 and y == 0:
                        continue
                    checkX = node.xPos + x
                    checkY = node.yPos + y

                    if (
                        checkX > 0
                        and checkX <= self.Xsize
                        and checkY > 0
                        and checkY <= self.Ysize
                    ):
                        neighbourNode = self.getNode(checkX - 1, checkY - 1)
                        neighbours.append(neighbourNode)

        elif searchType == "infront":
            for x in range(-1, 2, 2):
                checkX = node.xPos + x
                checkY = node.yPos

                if (
                    checkX > 0
                    and checkX <= self.Xsize
                    and checkY > 0
                    and checkY <= self.Ysize
                ):
                    neighbourNode = self.getNode(checkX - 1, checkY - 1)
                    neighbours.append(neighbourNode)

            for y in range(-1, 2, 2):
                checkX = node.xPos
                checkY = node.yPos + y

                if (
                    checkX > 0
                    and checkX <= self.Xsize
                    and checkY > 0
                    and checkY <= self.Ysize
                ):
                    neighbourNode = self.getNode(checkX - 1, checkY - 1)
                    neighbours.append(neighbourNode)

        return neighbours

    def wall(self, x, y):
        node = self.getNode(x - 1, y - 1)
        node.state = "@"
        node.walkable = False

    def removeWall(self, x, y):
        node = self.getNode(x - 1, y - 1)
        node.state = "-"
        node.walkable = True

    def link(self, button):
        pos = [button.xPos, button.yPos]
        node = self.getNode(pos[0] - 1, pos[1] - 1)
        node.button = button
        button.node = node
