import numpy as np
import ast
import safetydance.extensions as sbe
from safetydance import step, step_data, Context, script

array_one = step_data(np.array)
array_two = step_data(np.array)
array_three = step_data(np.array)

@step
def step_one():
    array_one = np.random.rand(4,4)

@step
def step_two():
    array_two = np.random.rand(4,4)

@step
def step_three():
    array_three = np.random.rand(4,4)

@step
def step_four():
    print(f'Array 1:\n { array_one }\n'
          f'Array 2:\n { array_two }\n' 
          f'Array 3:\n { array_three }\n')

class variableLogger(ast.NodeTransformer):
    '''This class is a class that will allow us
    to visit specific pieces of the code. It is added to
    the registry here.
    '''
    def visit_Assign(self, node):
         if ((type(node.targets[0]) == ast.Subscript) and node.targets[0].value.id == 'context'):
           called_func = ast.Call\
               (func=ast.Name(id='print', ctx=ast.Load()), \
                args=[ast.Str(s=f'inside a new node here')], \
                keywords=[])
           newnode = ast.Expr(value=called_func)
         return [node, newnode]

    def visit_AnnAssign(self,node):
        logger.debug('In AnnAssign')
        return node
    
    def visit_AugAssign(self, node):
        logger.debug('In AugAssign')
        return node
    
addLogger = variableLogger()
sbe.register_stepbody_extension(addLogger)

@script
def main():
    print(f"Running Main!")
    print(f"Current stepbody registry: { sbe.STEPBODY_EXTENSION_REGISTRY }")
    step_one()
    step_two()
    step_three()
    step_four()
    print(f'Finished main!')

main()
