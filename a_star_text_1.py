import extra.cg as cg
from random import randint


def findPath(startNode, finishNode, grid, searchType) -> list:
    nodesSearch = 0

    openNodes = []
    closedNode = []
    openNodes.append(startNode)

    while len(openNodes) > 0:
        currentNode = openNodes[0]
        for i in range(1, len(openNodes)):
            if (
                openNodes[i].fCost < currentNode.fCost
                or openNodes[i].fCost == currentNode.fCost
            ):
                if openNodes[i].hCost < currentNode.hCost:
                    currentNode = openNodes[i]

        nodesSearch += 1

        openNodes.remove(currentNode)
        closedNode.append(currentNode)

        if currentNode == finishNode:
            nodepath = retracePath(startNode, finishNode)
            nodepath.insert(0, nodesSearch)
            return nodepath

        nodeneighbours = grid.getNeighbours(currentNode, searchType)
        for neighbourNode in nodeneighbours:
            if not neighbourNode.walkable or neighbourNode in closedNode:
                continue

            costToNeighbour = currentNode.gCost + getDistance(
                currentNode, neighbourNode
            )
            if costToNeighbour < neighbourNode.gCost or neighbourNode not in openNodes:
                neighbourNode.gCost = costToNeighbour
                neighbourNode.hCost = getDistance(neighbourNode, finishNode)
                neighbourNode.update()
                neighbourNode.parent = currentNode
                if neighbourNode not in openNodes:
                    openNodes.append(neighbourNode)
                    if neighbourNode.state != 3:
                        neighbourNode.state = "-"
    return [nodesSearch]


def retracePath(startNode, finishNode):
    path = []
    currentNode = finishNode
    while currentNode != startNode:
        parentNode = currentNode.parent
        if currentNode.state != 2 and currentNode.state != 3:
            path.append(currentNode)
            currentNode.state = "#"
        currentNode = parentNode
    path.reverse()
    return path


def getDistance(nodeA, nodeB):
    dstX = abs(nodeA.xPos - nodeB.xPos)
    dstY = abs(nodeA.yPos - nodeB.yPos)

    if dstX > dstY:
        return 14 * dstY + 10 * (dstX - dstY)
    return 14 * dstX + 10 * (dstY - dstX)


def resetGrid(grid):
    for y in grid.nodes:
        for x in y:
            x.state = "-"


if __name__ == "__main__":

    grid = cg.createGrid(15, 15, 0)
    # start=[randint(1,10),randint(1,10)]
    # finish=[randint(1,10),randint(1,10)]
    
    start = [2, 7]
    finish = [14, 7]
    
    for x in range(1,11):
        grid.wall(7,x)
    
    for x in range(3,16):
        grid.wall(11,x)
        

    startNode = grid.getNode(start[0] - 1, start[1] - 1)
    startNode.state = 2
    finishNode = grid.getNode(finish[0] - 1, finish[1] - 1)
    finishNode.state = 3

    grid.display()
    path = findPath(startNode, finishNode, grid, "infront")
    grid.display()
    print(path)
