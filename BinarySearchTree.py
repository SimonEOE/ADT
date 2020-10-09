import math


class BinarySearchTree:
    def __init__(self):
        self.root = None

    class BinaryNode:
        def __init__(self, element, left=None, right=None):
            self.element = element
            self.left = left
            self.right = right

    def insert(self, element):
        # 单独处理根节点
        if self.root is None:  # 判断是否是根节点
            self.root = self.BinaryNode(element)
            return None
        self.__insert(self.root, element)

    def __insert(self, node, element):
        if node.element == element:
            return None
        elif node.element < element:
            if node.right is None:
                node.right = self.BinaryNode(element)
            else:
                self.__insert(node.right, element)
        else:
            if node.left is None:
                node.left = self.BinaryNode(element)
            else:
                self.__insert(node.left, element)

    def print_tree(self):
        node = self.root
        gap_num = math.pow(2, self.height() + 1)
        self.__print_layer(layer=[(self.root, gap_num / 2, 0)])

    # 求树的高度
    def height(self, node=None):
        if node is None:
            node = self.root

        if node.left is not None:
            left_height = self.height(node=node.left) + 1
        else:
            left_height = 0
        if node.right is not None:
            right_height = self.height(node=node.right) + 1
        else:
            right_height = 0
        height = left_height if left_height > right_height else right_height
        # print('height: {}'.format(height))
        return height

    def __print_layer(self, layer: list):
        '''
        :param layer: 是一个元组的列表，元组组成为（node, gap_num, base）
        :node: 是二叉树节点
        :gap_num: 是缩进的单位
        :base: 是父节点缩进单位
        :return:
        '''
        places = 0
        unit = 3  # 缩进的单位
        total = 0  # 已经打印出来的字符数
        new_layer = []
        for obj in layer:
            node = obj[0]
            gap_num = obj[1]
            base = obj[2]
            node_element = str(node.element)  # type:str
            places = unit * gap_num - total
            total = unit * gap_num
            print(node_element.rjust(int(places), ' '), end='')
            if node.left is not None:
                new_layer.append(
                    (node.left, gap_num - math.fabs(gap_num - base) / 2, gap_num))  # 如果是左儿子，在其一半处, 且下一个基线是上一个基线
            if node.right is not None:
                new_layer.append((node.right, gap_num + math.fabs(gap_num - base) / 2, gap_num))  # 如果是右儿子，在其二分之三处
        print()
        if len(new_layer) == 0:
            return None
        else:
            self.__print_layer(new_layer)

    def contains(self, element):
        if self.root is None:
            return False
        return self.__contains(self.root, element)

    def __contains(self, node, element):
        #如果节点刚好是则返回True
        if node.element == element:
            return True
        elif node.element < element: #元素在节点的右子树
            if node.right is None: #没有右子树则返回False
                return False
            else: #如果有右子树，则递归查找该元素
                return self.__contains(node.right, element)
        else: #元素在节点的左子树
            if node.left is None: #没有左子树则直接返回False
                return False
            else: #如果有左子树，则递归查找该元素
                return self.__contains(node.left, element)

    def find_min(self):
        if self.root is None:
            return None
        return self.__find_min(self.root)

    def __find_min(self, node):
        if node.left is None:
            return node.element
        else:
            return self.__find_min(node.left)

    def find_max(self):
        if self.root is None:
            return None
        return self.__find_max(self.root)

    def __find_max(self, node):
        if node.right is None:
            return node.element
        else:
            return self.__find_max(node.right)

    def remove(self, element):
        if not self.contains(element):
            return None
        self.__remove(self.root, element)

    def __remove(self, node, element):
        father_node = self.__get_father_node(element, node)
        if father_node is None:
            return None
        #获得要删除节点的引用
        if father_node.element < element:
            self_node = father_node.right
        elif father_node.element > element:
            self_node = father_node.left
        else: #元素等于自身，不在其节点之下
            self_node = node
        #要删除节点没有儿子情况
        if self_node.left is None and self_node.right is None:
            if father_node.element < element: #父节点删除右儿子
                father_node.right = None
            elif father_node.element > element: #父节点删除左儿子
                father_node.left = None
            else: #如果父节点是根节点，而对根节点的引用设置为None，否则删除失败
                if father_node == self.root:
                    self.root = None
                else:
                    return None
        #要删除节点只有单儿子情况
        if self_node.left is None:
            if father_node.element < element: #改变父节点右儿子为删除节点的右儿子
                father_node.right = self_node.right
            elif father_node.element > element: #改变父节点的左儿子为删除节点的右儿子
                father_node.left = self_node.right
            else: #如果父节点是根节点，而对根节点的引用设置为其儿子，否则删除失败
                if father_node == self.root:
                    self.root = self_node.right
                else:
                    return None
        if self_node.right is None:
            if father_node.element < element: #改变父节点右儿子为删除节点的左儿子
                father_node.right = self_node.left
            elif father_node.element > element: #改变父节点的左儿子为删除节点的左儿子
                father_node.left = self_node.left
            else: #如果父节点是根节点，而对根节点的引用设置为其儿子，否则删除失败
                if father_node == self.root:
                    self.root = self_node.left
                else:
                    return None
        #要删除的节点有两个儿子的情况
        if (not self_node.left is None) and (not self_node.right is None):
            min_element = self.__find_min(self_node.right) #找到被删除节右点子树里最小元素
            min_father_node = self.__get_father_node(min_element, self_node) #获得被删除节点子树里最小元素的父节点
            self.__remove(self_node, min_element) #递归删除被删除节点里最小元素节点
            self_node.element = min_element #将被删除的节点元素值设置为其子树里最小元素，完成删除

    #获取特定元素的节点
    def __get_father_node(self, element, node=None ):
        #如果不指定树节点，则默认为根节点
        if node is None:
            node = self.root
        # 如果刚好是根节点，则直接返回
        if node.element == element and node == self.root:
            return node
        elif node.element < element:  # 元素在节点的右子树
            if node.right is None:  # 没有右子树则返回None
                return None
            else:  # 如果有右子树
                if node.right.element == element: #右儿子符合则返回自己
                    return node
                else: #如果右儿子不符合，则递归寻找
                    return self.__get_father_node(element, node.right)
        else:  # 元素在节点的左子树
            if node.left is None:  # 没有左子树则直接返回None
                return None
            else:  # 如果有左子树
                if node.left.element == element: #左儿子符合则返回自己
                    return node
                else: #左儿子不符合，递归查找
                   return self.__get_father_node(element, node.left)

if __name__ == '__main__':
    elements = [25, 4, 10, 40, 99, 23,1, 32, 24, 41, -2, 21, 11, 10]
    binary_search_tree = BinarySearchTree()
    for element in elements:
        binary_search_tree.insert(element)
    binary_search_tree.print_tree()
    print(binary_search_tree.contains(12))
    print(binary_search_tree.find_min())
    print(binary_search_tree.find_max())
    binary_search_tree.remove(25)
    binary_search_tree.print_tree()
    binary_search_tree.remove(40)
    binary_search_tree.print_tree()