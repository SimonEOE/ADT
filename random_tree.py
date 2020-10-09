import random


class Tree:

    class TreeNode:
        def __init__(self, element, first_child, next_sibling):
            self.element = element
            self.first_child = first_child
            self.next_sibling = next_sibling

    def create_tree(self, depth:int, elements:list):
        #随机选定根节点
        n = random.randint(0, len(elements) - 1)
        root = elements[n]
        del elements[n]
        #将节点分为不同层的数节点
        layers = {}
        layer_n = 0
        while depth > 1:
            max = len(elements) - depth + 1
            n = random.randint(1, max)
            random.shuffle(elements)
            layer_n += 1
            layers[layer_n] = elements[0:n]
            del elements[0:n]
            depth -= 1
        layers[layer_n + 1] = elements
        tree = self.TreeNode(element=root, first_child=None, next_sibling=None)
        #print(root)
        #print(layers)
        for i in range(1, len(layers) + 1):
            self.__insert_element(tree, i, 0, layers[i])
        self.tree = tree
        return tree


        '''
        1.对于每一层树节点n，确定其个数上界max，每一个深度至少一个，所以max = length - depth
        2.随机生成符合范围内的节点数n
        3.对树元素随机排列，提取前n个元素作为这一层的树节点，并从列表中删除，树的深度减1
        4.循环执行1到3知道深度为0
        '''

    def __insert_element(self, node, depth, current_depth, elements:list):
        if current_depth == depth - 1: #到达树的最底层
            if random.randint(0, 1) == 1: #如果随机得到1，那就在这节点增加一个子节点
                node.first_child = self.TreeNode(element=elements[0], first_child=None,next_sibling=None)
                del elements[0]
                if len(elements) > 0 :
                    self.__insert_element(node.first_child, depth, current_depth + 1, elements)
            if node.next_sibling is not None: #增加节点操作结束，切换到其兄弟节点执行增加操作
                if len(elements) > 0:
                    self.__insert_element(node.next_sibling, depth, current_depth, elements)
            else: #已经到最后一个父节点，剩下所有元素都要加到该父节点上
                if node.first_child is not None:
                    node = node.first_child
                    while node.next_sibling is not None:
                        node = node.next_sibling
                else:
                    node.first_child = self.TreeNode(elements[0], None, None)
                    del elements[0]
                    node = node.first_child
                for i in range(len(elements)):
                    node.next_sibling = self.TreeNode(elements[i], None, None)
                    node = node.next_sibling



        elif current_depth == depth: #为新增节点，需要判断是否增加兄弟节点
            if random.randint(0, 1) == 1: #如果随机得到1, 就增加一个兄弟节点
                node.next_sibling = self.TreeNode(elements[0], None, None)
                del elements[0]
                if len(elements) > 0:
                    self.__insert_element(node.next_sibling, depth, current_depth, elements)
        else:
            if (node.first_child is not None) and (len(elements) > 0):
                self.__insert_element(node.first_child, depth, current_depth + 1, elements)
            if (node.next_sibling is not None) and (len(elements) > 0):
                self.__insert_element(node.next_sibling, depth, current_depth, elements)


    '''
    1 遍历节点，如果是最后节点，判断是否增加节点并执行
        1.1 如果有增加节点，将新增节点传入函数
        1.2 如果没有新增
    '''
    def print_tree(self):
        self.__print_node(self.tree, 0)

    def __print_node(self, node, depth):
        print(' ' * depth * 4 + str(node.element))
        if node.first_child is not None:
            self.__print_node(node.first_child, depth + 1)
        if node.next_sibling is not None:
            self.__print_node(node.next_sibling, depth)

if __name__ == '__main__':
    a = [random.randint(1,200) for i in range(300)]
    tree = Tree()
    tree.create_tree(30, a)
    tree.print_tree()