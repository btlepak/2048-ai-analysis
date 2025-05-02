import random
import sys
import math
import time
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
    def __init__(self):
        self.maxDepth = 6  # Max depth for search
        self.exponent = 1  # Weight exponent
        self.weights = [40, 200, 270, 500]  # Heuristic weights

    def getMove(self, grid): # Find the optimal move using the Expectiminimax algorithm
        move = self.expectiminimax(grid)
        if move is None: # If no optimal move is found, choose randomly among available moves
            return random.choice(grid.getAvailableMoves())[0]
        return move 

    def expectiminimax(self, grid): # Expectiminimax algorithm to determine the optimal move
        best_move = self.maxi(grid, 0, -sys.maxsize - 1, sys.maxsize)
        return best_move[0]

    def maxi(self, grid, depth, alpha, beta): # Function to handle Maximize nodes
        if self.cutoffTest(grid, depth):
            return (None, self.evaluate(grid))
        
        direction, maxUtil = None, (-sys.maxsize - 1)
        for move in grid.getAvailableMoves():
            util = self.chance(move[1], depth + 1, alpha, beta) 
            if util > maxUtil:
                direction, maxUtil = move[0], util
            if maxUtil>= beta: 
                break
            alpha = max(alpha, maxUtil)
        
        return (direction, maxUtil)
    
    def mini(self, grid, depth, number, alpha, beta): # Function to handle Minimize nodes
        if self.cutoffTest(grid, depth):
            return self.evaluate(grid)
        
        minUtil = sys.maxsize

        child_limit = 3  # Limit the number of child nodes
        count = 0
        for pos in grid.getAvailableCells():
            new_grid = grid.clone()
            new_grid.insertTile(pos, number)
            util = self.maxi(new_grid, depth + 1, alpha, beta)
            minUtil = min(util[1], minUtil)

            if minUtil <= beta or count >= child_limit:
                break
            
            count += 1
            beta = min(minUtil, beta)
        
        return minUtil
    
    def chance(self, grid, depth, alpha, beta):# Function to handle Chance nodes in the Expectiminimax algorithm.
        if self.cutoffTest(grid, depth):
            return self.evaluate(grid)

        left = 0.9 * self.mini(grid, depth + 1, 2, alpha, beta)
        right = 0.1 * self.mini(grid, depth + 1, 4, alpha, beta)
        return (left + right) / 2
    
    def evaluate(self, grid): # Function to evaluate the value of the grid
        self.exponent = math.ceil(grid.getMaxTile() / 2048)  # Calculate the exponent
        possible_merges = self.countPossibleM(grid)  # Calculate the number of possible merges
        grid_value = self.calculateGridValue(grid)  # Calculate the grid value
        monotonicity = self.monotonicity(grid)  # Calculate the monotonicity
        open_tiles = math.pow(len(grid.getAvailableCells()), self.exponent)  # Calculate the number of open tiles
        score = self.weights[0]*grid_value + self.weights[1]*monotonicity + self.weights[2]*possible_merges + self.weights[3]*open_tiles  # Calculate the score
        return score

    def monotonicity(self, grid): # Function to calculate the monotonicity
        monotonicity = 0    
        for row in range(3):
            for col in range(3):
                if grid.map[row][col] >= grid.map[row][col+1]:
                    monotonicity += 1
                if grid.map[col][row] >= grid.map[col][row+1]:
                    monotonicity += 1
        return math.pow(monotonicity, self.exponent)

    def calculateGridValue(self, grid): # Function to calculate the value of the grid
        topLeft = [[128, 64, 16, 8], [32, 16, 8, 4], [16, 8, 4, 2], [8, 4, 2, 2]]
        count = 0
        for row in range(len(grid.map)):
            for col in range(len(grid.map[row])):
                count += topLeft[row][col] * grid.map[row][col]
        return math.pow(count, 2)

    def cutoffTest(self, grid, depth): # Function to check if maximum depth is reached
        if depth > self.maxDepth:
            return True
        return False 
    
    def countPossibleM(self, grid): # Function to count the number of possible merges
        open_cells = len(grid.getAvailableCells())
        most_merges = 0
        for move in grid.getAvailableMoves():
            next_grid = move[1]
            next_open_cells = len(next_grid.getAvailableCells())
            most_merges += open_cells - next_open_cells
        return math.pow(most_merges, self.exponent)
    
    def alphabeta(self, grid, ismax, alpha, beta, depth, timelimit): # If the time limit is exceeded, return the evaluation value of the current board and -1.
        if time.process_time() > timelimit:
            return [self.evalfn(grid), -1]
        if depth == 0: # If the depth reaches 0, return the evaluation value of the current board and -1.
            return [self.evalfn(grid), -1]
        if not grid.canMove(): # If unable to move, return the evaluation value of the current board and -1.
            return [self.evalfn(grid), -1]
        
        if ismax: # at max level, initialize alpha
            minmaxUtil, minimaxMove = -float('inf'), -1
            moves = grid.getAvailableMoves()
            for i in moves:
                gridCopy = grid.clone()
                gridCopy.move(i)
                new_util, _ = self.alphabeta(gridCopy, False, alpha, beta, depth-1, timelimit)
                if new_util > minmaxUtil:
                    minmaxUtil, minimaxMove = new_util, i
                # pruning
                if minmaxUtil >= beta:
                    break
                # update alpha
                if minmaxUtil > alpha:
                    alpha = minmaxUtil
        else: # at min level, initialize beta
            minmaxUtil, minimaxMove = float('inf'), -1
            cells = grid.getAvailableCells()
            if not cells:
                return minmaxUtil, minimaxMove
            for i in cells:
                gridCopy2 = grid.clone()
                gridCopy2.insertTile(i, 2)
                new_util, _ = self.alphabeta(gridCopy2, True, alpha, beta, depth-1, timelimit)
                if new_util < minmaxUtil:
                    minmaxUtil, minimaxMove = new_util, -1
                if minmaxUtil <= alpha:
                    break
                gridCopy4 = grid.clone()
                gridCopy4.insertTile(i, 4)
                new_util, _ = self.alphabeta(gridCopy4, True, alpha, beta, depth-1, timelimit)
                if new_util < minmaxUtil:
                    minmaxUtil, minimaxMove = new_util, -1
                if minmaxUtil <= alpha:
                    break
                if minmaxUtil < beta:
                    beta = minmaxUtil
        return minmaxUtil, minimaxMove   
    
    def heuristic(self, grid):    # Copy the grid values into a single list
        copygrid = []
        for i in range(4):
            copygrid.extend(grid.map[i])
        
        maxTile = max(copygrid)    # Find the maximum tile value and count the number of empty tiles
        emptyTiles = len([i for i, x in enumerate(copygrid) if x == 0])
        
        sum = 0    # Initialize the sum and weights for each tile position
        weights = [17, 16, 15, 14, 9, 10, 11, 12, 8, 7, 6, 5, 1, 2, 3, 4]
        
        if maxTile == copygrid[0]:    # If the maximum tile is at the top-left corner, double its value
            sum += copygrid[0] * weights[0] * 2
        
        for i in range(16):    # Calculate the sum of weighted tile values
            sum += copygrid[i] * weights[i]
        
        # Calculate smoothness as the absolute differences between neighboring tiles
        smoothness = abs(copygrid[1] - copygrid[0]) + abs(copygrid[2] - copygrid[1]) + abs(copygrid[3] - copygrid[2]) + abs(copygrid[5] - copygrid[4]) + abs(copygrid[6] - copygrid[5]) + abs(copygrid[7] - copygrid[6]) + abs(copygrid[9] - copygrid[8]) + abs(copygrid[10] - copygrid[9]) + abs(copygrid[11] - copygrid[10]) + abs(copygrid[13] - copygrid[12]) + abs(copygrid[14] - copygrid[13]) + abs(copygrid[15] - copygrid[14]) + abs(copygrid[4] - copygrid[0]) + abs(copygrid[8] - copygrid[4]) + abs(copygrid[12] - copygrid[8]) + abs(copygrid[5] - copygrid[1]) + abs(copygrid[9] - copygrid[5]) + abs(copygrid[13] - copygrid[9]) + abs(copygrid[6] - copygrid[2]) + abs(copygrid[10] - copygrid[6]) + abs(copygrid[14] - copygrid[10]) + abs(copygrid[7] - copygrid[3]) + abs(copygrid[11] - copygrid[7]) + abs(copygrid[15] - copygrid[11])
        
        # Calculate the heuristic value as the sum of tile values, empty tiles, and smoothness
        sum = sum + emptyTiles * emptyTiles - smoothness
        return sum