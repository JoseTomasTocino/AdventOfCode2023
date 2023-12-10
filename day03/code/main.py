from dataclasses import dataclass
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass(eq=False)
class Number:
    value: int
    x0: int = 0
    x1: int = 0
    y: int = 0
    

@dataclass
class Symbol:
    value: str
    x: int = 0
    y: int = 0
    

def part_one(inp):
    numbers = []
    symbols = []
    
    matrix = defaultdict(lambda: defaultdict(int))

    for y, row in enumerate(inp.splitlines()):
        current = None
        
        for x, c in enumerate(row):
            if c.isdigit():
                if current is None:
                    current = Number(value=0, x0=x, x1=x, y=y)                    
                    numbers.append(current)

                current.value = current.value * 10 + int(c)
                current.x1 = x
                matrix[x][y] = current
                
            else:
                if current is not None:
                    current = None
                    
                if c != '.':
                    s = Symbol(value=c, x=x, y=y)
                    matrix[x][y] = s
                    symbols.append(s)
                   
    part_sum = 0
    
    for number in numbers:
        is_part = False
        
        # Check adjacent positions in matrix for a symbol
        # This checks top and bottom row
        for x in range(number.x0 - 1, number.x1 + 2):
            for y in [number.y - 1, number.y + 1]:
                if isinstance(matrix[x][y], Symbol):
                    is_part = True
                    break
            
            if is_part:
                break
            
        # This checks side positions
        if isinstance(matrix[number.x0 - 1][number.y], Symbol) or isinstance(matrix[number.x1 + 1][number.y], Symbol):
            is_part = True
        
        if is_part:
            part_sum += number.value
        
    #### Part two
    gear_ratio_sum = 0
    
    for symbol in symbols:

        if symbol.value != '*':
            continue
        
        operands = set()
        
        for x in range(symbol.x - 1, symbol.x + 2):
            for y in range(symbol.y - 1, symbol.y + 2):
                if isinstance(matrix[x][y], Number):
                    operands.add(matrix[x][y])
                    

        if len(operands) == 2:
            operands = list(operands)
            gear_ratio_sum += operands[0].value * operands[1].value

        # else:
        #     logger.info(f'Checking product at {symbol.x}, {symbol.y}, operands: {operands}')
            
        #     inplines = inp.splitlines()
        #     logger.info(inplines[symbol.y-1][symbol.x - 6:symbol.x + 6])
        #     logger.info(inplines[symbol.y][symbol.x - 6:symbol.x + 6])
        #     logger.info(inplines[symbol.y+1][symbol.x - 6:symbol.x + 6])
            
    return part_sum, gear_ratio_sum

def part_two(inp):
    pass
