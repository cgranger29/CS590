class Node:
    def __init__(self, val, children = None) -> None:
        self.val = val
        self.children = children



def find_LCA(t1, t2, root):

    ans = []
    def find_node(target_val, node) -> bool:
        if node.val == target_val:
            return True
        
        if node.children:
            for child in node.children:
                if find_node(target_val, child):
                    return True

        return False
    
    queue = [root]

    while queue:
        curr_node = queue.pop(0)
        if curr_node.children:
            for child_node in curr_node.children:
                queue.append(child_node)
        found_target_1 = find_node(t1, curr_node)
        found_target_2 = find_node(t2, curr_node)
        if found_target_1 and found_target_2:
            ans.append(curr_node.val)

    print(ans)
    return ans[-1]

node_11 = Node(11)    
node_10 = Node(10)
node_9 = Node(9)
node_8 = Node(8)
node_7 = Node(7, [node_8])
node_6 = Node(6, [node_10, node_11])
node_5 = Node(5, [node_9])
node_2 = Node(2, [node_5])
node_3 = Node(3, [node_6, node_7])
node_4 = Node(4)
root = Node(1, [node_2, node_3, node_4])

print(find_LCA(10, 11, root))

