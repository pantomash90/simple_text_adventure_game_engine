import re #regex
import game_state

class Node:
    def __init__(self, val, left = None, right = None):
        self.__value = val
        self.__left = left
        self.__right = right
        
    def __str__(self):
        return f'{self.__value}'
    
    @property
    def left(self):
        return self.__left
    
    @property
    def right(self):
        return self.__right
    
    @property
    def value(self):
        return self.__value
    
    @property
    def isLeaf(self):
        if self.left == None and self.right == None:
            return True
        return False
    
    def evaluate(self) -> bool:
        if self.isLeaf:
            regexp = '[<>=]{1,2}'
            op = re.findall(regexp, self.__value)[0]
            fctrs = re.split(regexp, self.__value)
            
            match op:
                case '>=':
                    return game_state.getValue(fctrs[0]) >= int(fctrs[1])
                case '>':
                    return game_state.getValue(fctrs[0]) > int(fctrs[1])
                case '=':
                    return game_state.getValue(fctrs[0]) == int(fctrs[1])
                case '<':
                    return game_state.getValue(fctrs[0]) < int(fctrs[1])
                case '<=':
                    return game_state.getValue(fctrs[0]) <= int(fctrs[1])
                case '<>':
                    return game_state.getValue(fctrs[0]) != int(fctrs[1])
        else:
            eval_left = self.__left.evaluate()
            eval_right = self.__right.evaluate()
            
            match self.__value:
                case '&&':
                    return eval_left & eval_right
                case '||':
                    return eval_left | eval_right
                case '^':
                    return eval_left ^ eval_right
        

class ConditionParser:
    def __init__(self):
        pass
        
    def evaluate(self, txt: str) -> bool:
        self.__root = self.parse(txt)
        return self.__root.evaluate()
        
    def parse(self, txt) -> Node:
        parts = self.split_logical(txt)
        
        if not parts:
            value = txt
            left = None
            right = None
        else:
            value = parts[1]
            left = self.parse(parts[0])
            right = self.parse(parts[2])
        
        return Node(value, left, right)
    
    def split_logical(self, txt) -> list:
        parts = []
        depth = 0
        start = 0
        i = 0

        while i < len(txt):
            char = txt[i]

            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            # Check for operators only at top level
            elif depth == 0:
                if txt[i:i+2].strip() in ('&&', '||', '^'):
                    left = self.remove_outer_parentheses(txt[start:i].strip())
                    op = txt[i:i+2].strip()
                    right = self.remove_outer_parentheses(txt[i+2:].strip())
                    parts.append(left)
                    parts.append(op)
                    parts.append(right)
                    
                    i += 2
                    start = i
                    break
            i += 1
        
        return parts
        
    def remove_outer_parentheses(self, txt) -> str:
        depth = 0
        i = 0
        while i < len(txt):
            char = txt[i]
            
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                
            if depth == 0 and i < len(txt)-1:
                return txt
            i += 1
        
        if txt[0] == '(':
            txt = txt[1:txt.__len__()]
        if txt[-1] == ')':
            txt = txt[:txt.__len__()-1]
        return txt

class OutcomeParser():    
    def __init__(self):
        pass
    
    def parseOutcomeText(self, txt: str):
        if txt:
            self.__outcomes = re.split(";|,", txt)
            for o in self.__outcomes:
                self.modifyVariable(o)
        
    def modifyVariable(self, outcome: str):
        regexp = "(\\+|-|=)"
        res = re.split(regexp, outcome)
        var = res[0].strip()
        op = res[1].strip()
        val = int(res[2].strip())
        
        newVal = 0
        if op == "+":
            newVal = game_state.getValue(var) + val
        elif op == "-":
            newVal = game_state.getValue(var) - val
        elif op == "=":
            newVal = val
        else:
            return
        
        game_state.modifyValue(var, newVal)