#The MIT License (MIT)
#Copyright (c) 2017 Nicola M.H. Riedmann

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy
import sys

E = 'X'  
goalState = '1 2 3,8 X 4,7 6 5'

def checkDone(puzzleState):
	return str(puzzleState) == goalState

def formattedPuzzle(puzzle):
	string = '{0} {1} {2},{3} {4} {5},{6} {7} {8}'.format(puzzle[0][0],puzzle[0][1],puzzle[0][2],puzzle[1][0],puzzle[1][1],puzzle[1][2],puzzle[2][0],puzzle[2][1],puzzle[2][2])
	#print(string)
	return string

def puzzleFromString(string):
	puzzle = []
	rows = string.split(",")

	for row in rows:
		list = row.split(' ')
		puzzle.append(list)
	# print(puzzle)
	# print(formattedPuzzle(puzzle))
	return puzzleState(puzzle)

def tS(a,b):
	return tuple(map(lambda x, y: x - y, a, b))

def tA(a,b):
	return tuple(map(lambda x, y: x + y, a, b))

class PuzzleState:
	puzzle = [['1', '2', '3'],['4','7','5'],['6',E,'8']]
	parent = None
	costFromStart = 0
	costF = 0

	def __init__(self, state2dArray, parent):
		self.puzzle = state2dArray
		self.parent = parent

	def getCost(self) :
		return self.costF #nPuzzleManhattanDistance(self.puzzle)

	def findEmpty(self) :
		eY = 0
		for row in self.puzzle:
			eX = 0
			for cell in row:
				if cell is E:
					return (eY,eX)
				eX += 1
			eY += 1
		return False

	def __hash__(self):
		h = hash(str(self))
		# print('hash: {0}'.format(h))
		return h

	def __eq__(self, other):
		e = (self.puzzle == other.puzzle)
		# print('{0} == {1} : {2}'.format(self, other, e))
		return e

	def __ne__(self, other): 
		n = not self.__eq__(other)
		print('{0} != {1} : {2}'.format(self, other, e))
		return n

	# def equalsPuzzle(self, state2dArray):
	# 	return self.puzzle == state2dArray

	# def equalsPuzzleString(self, formattedString):
	# 	return str(self) == formattedString

	def __repr__(self):
		return formattedPuzzle(self.puzzle)

	# def __str__(self):
	 	# return formattedPuzzle(self.puzzle)

	def getParentStr(self):
		return str(self.parent)

	def getStateAfterMovingTileFromCoordinates(self, empty, fieldCoordinates) :
		nextPuzzle = deepcopy(self.puzzle)
		nextPuzzle[empty[0]][empty[1]] = nextPuzzle[fieldCoordinates[0]][fieldCoordinates[1]] 
		nextPuzzle[fieldCoordinates[0]][fieldCoordinates[1]] = E
		return PuzzleState(nextPuzzle, self)

	def getSuccessorStates(self, wholeSearchTree):
		successors = []
		empty = self.findEmpty()
		L = tS(empty,(0,1)) #coords of tile left of current empty field
		R = tA(empty,(0,1)) #right of empty
		T = tS(empty,(1,0)) #top (above) empty
		B = tA(empty,(1,0)) #below empty
		if (L[1]>=0):
			puzzleState = self.getStateAfterMovingTileFromCoordinates(empty, L)
			if not puzzleState in wholeSearchTree:
				successors.append(puzzleState)
		if (R[1]<=2):
			puzzleState = self.getStateAfterMovingTileFromCoordinates(empty, R)
			if not puzzleState in wholeSearchTree:
				successors.append(puzzleState)
		if (T[0]>=0):
			puzzleState = self.getStateAfterMovingTileFromCoordinates(empty, T)
			if not puzzleState in wholeSearchTree:
				successors.append(puzzleState)
		if (B[0]<=2):
			puzzleState = self.getStateAfterMovingTileFromCoordinates(empty, B)
			if not puzzleState in wholeSearchTree:
				successors.append(puzzleState)
		return successors

def dfs(initialState, graph):

	level = 0
	stack = [initialState]
	wholeSearchTree = [initialState]
	done = checkDone(initialState)
	currentState = initialState

	while not checkDone(currentState):
		if currentState is stack[-1].parent:
			level += 1
		else: 
			level -= 1
		currentState = stack[-1]
		if not currentState is initialState:
			graph.add_edge(currentState.getParentStr(), str(currentState))
		print('\tdepth {0}\tChecking {1}'.format(level,currentState))
		successors = currentState.getSuccessorStates(wholeSearchTree)
		print('\t  added : {0}'.format(successors))
		for successor in successors:
			stack.append(successor)
			wholeSearchTree.append(successor)
		stack.remove(currentState)
		if len(stack)==0:
			return False, len(wholeSearchTree), wholeSearchTree
	return True, len(wholeSearchTree), wholeSearchTree
		

def bfs(initialState, graph):

	level = 0
	queue = [initialState]
	wholeSearchTree = [initialState]
	done = checkDone(initialState)

	while not done:
		#print('\tdepth {0}'.format(level))
		currentState = queue[0]
		successors = currentState.getSuccessorStates(wholeSearchTree)
		print('\t  added : {0}'.format(successors))
		for successor in successors:
			queue.append(successor)
			wholeSearchTree.append(successor)
			graph.add_edge(successor.getParentStr(), str(successor))
			if checkDone(successor):
				done = True
		#level += 1
		queue.remove(currentState)
		if len(queue)==0:
			return False, len(wholeSearchTree), wholeSearchTree
	return done, len(wholeSearchTree), wholeSearchTree

def nPuzzleManhattanDistance(puzzle):
	goalPositions = {'1':(0,0),'2':(1,0),'3':(2,0),'4':(2,1),'5':(2,2),'6':(1,2),'7':(0,2),'8':(0,1),E:(1,1)}
	h = 0
	y=0
	for row in puzzle:
		x=0
		for cell in row:
			dist = ( abs(x - goalPositions[cell][0]) + abs(y - goalPositions[cell][1]) )
			#print('{0} : {1} -- {2} = {3}'.format(cell, (x,y), goalPositions[cell],dist))
			h += dist
			x+=1
		y+=1
	return h

costBetweenNodes = 1 #uniform cost for this problem

def improve(parent, successor, openNodes, closedNodes):
	if successor in openNodes:
		if (parent.costFromStart + costBetweenNodes < successor.costFromStart) :
			successor.parent = parent
			successor.costF = parent.costFromStart + costBetweenNodes + nPuzzleManhattanDistance(successor.puzzle)
	elif successor in closedNodes:
		if (parent.costFromStart + costBetweenNodes < successor.costFromStart) :
			successor.parent = parent
			successor.costF = parent.costFromStart + costBetweenNodes + nPuzzleManhattanDistance(successor.puzzle)
			closedNodes.remove(successor)
			openNodes.append(successor)
	else:
		successor.parent = parent
		successor.costF = parent.costFromStart + costBetweenNodes + nPuzzleManhattanDistance(successor.puzzle)
		successor.costFromStart = parent.costFromStart + costBetweenNodes
		openNodes.append(successor)

def aStar(initialState, graph):
	#uses the commonly used manhattan distance
	#sum of distances of each number from it's correct position
	
	path = []

	initialState.costF = nPuzzleManhattanDistance(initialState.puzzle)

	done = checkDone(initialState)
	closedNodes = []
	openNodes = [initialState]

	while not len(openNodes) == 0 :
		selectedNode = sorted(openNodes, key=lambda puzzleState:puzzleState.getCost())[0]
		print('expanding node {0}'.format(selectedNode))
		path.append(selectedNode)
		if not selectedNode is initialState:
			graph.add_edge(selectedNode.getParentStr(), str(selectedNode))

		openNodes.remove(selectedNode)
		closedNodes.append(selectedNode)
		if checkDone(selectedNode):
			return True, len(path), path
		else :
			successors = selectedNode.getSuccessorStates(path)
			for successor in successors:
				improve(selectedNode, successor, openNodes, closedNodes)
	return False, len(path), path

def largerEqual(a,b) :
	return a >= b

def larger(a, b) :
	return a > b

def hillClimb(initialState, graph, compare=largerEqual) :
	path = [initialState]
	current = initialState
	print('initial state manhattanDistance = {0}'.format(nPuzzleManhattanDistance(initialState.puzzle)))

	while True :
		successors = current.getSuccessorStates(path)
		bestNeighbour = sorted(successors, key=lambda puzzleState:nPuzzleManhattanDistance(puzzleState.puzzle))[0]

		

		# hill climb stops if the best neighbour is worse than the current state
		# in this case we want the cost function to be minimal, so it should stop, if the neighbours manhattan distance is larger than the current one
		if compare(nPuzzleManhattanDistance(bestNeighbour.puzzle), nPuzzleManhattanDistance(current.puzzle)) : #end if value o f
			return checkDone(current), len(path), path

		graph.add_edge(str(current), str(bestNeighbour))

		current = bestNeighbour

		print('added node {0}, manhattanDistance = {1}'.format(current, nPuzzleManhattanDistance(current.puzzle)))
		path.append(current)
		

def main():
	puzzle = [['2', '8', '3'],['1','6','4'],['7',E,'5']]
	#puzzle = [[E, '4', '3'],['2','1','5'],['6','7','8']]
	# puzzle = [['1', '2', '3'],['4','7','5'],['6',E,'8']]

#	print(len(sys.argv))

	if len(sys.argv) < 2:
		print('Please start 8puzzleSolvers with on of the arguments below: \n\t bfs \n\t dfs \n\t a* \n\t hill')
		return False

	howWasStartStateSet = 'preset'
	if len(sys.argv) > 2:
		puzzle = puzzleFromString(sys.argv[3])
		howWasStartStateSet='entered'

	initialState = PuzzleState(puzzle, None)

	g = nx.DiGraph()
	g.add_node(str(initialState))

	if len(sys.argv) > 1:
		arg = sys.argv[1]
		print("Running {0} with preset start sate\n\t{1}\n".format(arg,initialState))
		if (arg == 'bfs'):
			result = bfs(initialState, g)
		elif (arg == 'dfs'):
			result = dfs(initialState, g)
		elif (arg == 'aStar'):
			result = aStar(initialState, g)
		elif (arg == 'hill'):
		 	result = hillClimb(initialState, g)
		elif (arg == 'hillImproved'):
		 	result = hillClimb(initialState, g, compare=larger)
		else:
			print('Entered argument {0} is not a supported search mode. \n Please start 8puzzleSolvers with on of the arguments below: \n\t bfs \n\t dfs \n\t a* \n\t hill'.format(arg))

	print('\n-------\nDONE\tSuccess : {0}, #Expanded Nodes : {1}'.format(result[0],result[1]))
	nx.nx_agraph.write_dot(g, '{0}_{1}.dot'.format(initialState,sys.argv[1]))
	#nx.draw(g, nx.nx_agraph.graphviz_layout(g, prog='dot'), with_labels=True, node_size=12000, node_color="w")
	#plt.show()


if __name__ == "__main__":
	main()