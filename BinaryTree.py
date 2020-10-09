from typing import List
from typing import Tuple
import math


class Stack:

    def __init__(self, elements=[]):#这里[]是属于类变量的
        if len(elements) == 0:
            self.stack = [] #这里[]是属于实例变量的
        else:
            self.stack = [e for e in elements]

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        element = self.stack[-1]
        del self.stack[-1]
        return element

    def is_empty(self):
        if self.length() > 0:
            return False
        else:
            return True

    def top(self):
        if self.is_empty():
            raise Exception('Stack is empty!')
        return self.stack[-1]

    def length(self):
        return len(self.stack)

    def print_stack(self):
        print(self.stack)


class Express:
    def __init__(self, express:List[str]):
        self.express = express

    def to_list(self):
        string = list(self.express) #type:List[str]
        result = []
        num = ''
        for c in string:
            #如果是空白字符，不处理
            if c == ' ':
                continue
            #如果是数字或是小数点，那么合并成一个数
            if c.isnumeric() or c == '.':
                num += c
            #是操作符时
            else:
                #操作符前有数字，将数字推入
                if num != '':
                    result.append(str(float(num)))
                    num = ''
                #将操作符推入
                result.append(c)
        #最后如果有数字则推入
        if num != '':
            result.append(str(float(num)))
        self.express = result
        return result

    def is_valid(self):
        pass

    def to_post_fix(self):
        #先转换成操作符列表
        self.to_list()
        output = Stack()
        temp = Stack()
        operators = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '(': 3
        }
        for i in range(len(self.express)):
            operator = self.express[i]
            # 操作符是右括号
            if operator == ')':
                # 将操作符栈弹出直到遇到左括号
                while temp.top() != '(':
                    output.push(temp.pop())
                # 弹出左括号但不输出
                temp.pop()
            # 如果操作符是除了右括号之外的
            elif operator in operators.keys():
                # 操作符栈空或栈顶优先级较低，直接入栈
                if temp.length() == 0 or operators[temp.top()] < operators[operator]:
                    temp.push(operator)
                else:
                    # 将操作符栈不断弹出，直到优先级低的操作符
                    while temp.length() > 0 and operators[temp.top()] >= operators[operator]:
                        #如果遇到左括号则结束
                        if temp.top() == '(':
                            break
                        output.push(temp.pop())
                    # 遇到优先级低的操作符，将当前操作符推入栈
                    temp.push(operator)
            # 如果操作符是数字，直接输入
            else:
                output.push(operator)
        # 最后将操作符栈中所有操作符弹出到输出
        while temp.length() > 0:
            output.push(temp.pop())
        self.express = output
        return output.stack


class BinaryTree:
    def __init__(self, element=None, left=None, right=None):
        self.element = element
        self.left = left
        self.right = right

    def print_tree(self):
        node = self
        gap_num = math.pow(2, self.height() + 1)
        self.__print_layer(layer=[(self, gap_num / 2, 0)])

    #求树的高度
    def height(self, node=None):
        if node is None:
            node = self

        if node.left is not None:
            left_height = self.height(node=node.left) + 1
        else:
            left_height = 0
        if node.right is not None:
            right_height = self.height(node=node.right) + 1
        else:
            right_height = 0
        height = left_height if left_height > right_height else right_height
        #print('height: {}'.format(height))
        return height

    def __print_layer(self, layer:list):
        '''
        :param layer: 是一个元组的列表，元组组成为（node, gap_num, base）
        :node: 是二叉树节点
        :gap_num: 是缩进的单位
        :base: 是父节点缩进单位
        :return:
        '''
        places = 0
        unit = 4 #缩进的单位
        total = 0 #已经打印出来的字符数
        new_layer = []
        for obj in layer:
            node = obj[0] #type:BinaryTree
            gap_num = obj[1]
            base = obj[2]
            node_element = node.element #type:str
            places = unit * gap_num - total
            total = unit * gap_num
            print(node_element.rjust(int(places), ' ') , end='')
            if node.left is not None:
                new_layer.append((node.left, gap_num - math.fabs(gap_num - base) / 2, gap_num))#如果是左儿子，在其一半处, 且下一个基线是上一个基线
            if node.right is not None:
                new_layer.append((node.right, gap_num + math.fabs(gap_num - base) / 2, gap_num))#如果是右儿子，在其二分之三处
        print()
        if len(new_layer) == 0:
            return None
        else:
            self.__print_layer(new_layer)



if __name__ == '__main__':
    #a = '1.1 + 2.1*3.1 + (4.1 * 5.1 + 6.1)*7.1'
    #a = '1.1 - 2.1 - 3.1*2.234 -5/(24+23.4/34)'
    a = '(1 + 2) * (3*(4 + 5))'
    express = Express(a)
    post_fix = express.to_post_fix()
    #print(post_fix)
    express_tree = Stack()
    operators = ['+', '-', '*', '/']
    for element in post_fix:
        #如果元素是操作数就创建单节点树推入栈中
        if element not in operators:
            express_tree.push(BinaryTree(element=element))
        else:
            # 如果元素是操作符就弹出两棵树，以操作符为根创建成一棵树
            temp_tree = BinaryTree(element=element, left=express_tree.pop(), right=express_tree.pop())
            #将新树推入栈中
            express_tree.push(temp_tree)
    express_tree = express_tree.pop()
    express_tree.print_tree()
