# 典型的多对多问题,毫无疑问地使用图来解决,最终确定用户角色肯定不可能产生环路,所以使用有向无环图(DAG)来解决
# 不清楚怎么细化设计,暂时用字典替代,直接叫read,write是为了方便理解,实际上不秦楚权限的具体内容
################################################################################################################
                                            #!attention!#
                                            # DAG manual #
    # 角色看作图的节点,将权限依赖关系看作节点之间的有向边,即可得到一个有向无环图
    # 有向无环图的拓扑排序即为权限的优先级,优先级越高,权限越大
################################################################################################################

################################################################################################################
                                # 核心作用为分离了权限组和用户组#
################################################################################################################

# 让权限组可以被多个用户组使用,而用户组也可以使用多个权限组
# 也可以实现权限组的依赖,即权限组的权限是依赖于其他权限组的权限的

# 并且添加了权重,如果出现多个权限组的权限冲突,则使用权重最高的权限组的权限
# 如果出现依赖bug,很明显是出现了环路,检查一下权限组的依赖关系即可,只要不出现环路,就不会出现依赖bug
# 如果真的出现了环路...等于死循环递归=卡死...设计权限组的时候就需要严格遵守依赖关系...
# 建议为实例权限组添加单元测试...做好防御性编程...防止出现环路,理论上可以测出来

# 搬运大哥实现的数据结构
# 魔改了一下,添加了用户类,用户类用于确定用户组
    # 1.为DAG的初始化添加了用户组的初始化
    # 2.添加了priority属性,用于确定权限组的优先级
    # 3.!!! 单元测试是被我用来测试代码可用性的,没有测试过优先级!!!
class User:
    def __init__(self, name, roles):
        self.name = name
        self.roles = roles
        
class Node:
    def __init__(self, name, permissions, priority):
        self.name = name
        self.permissions = permissions
        self.priority = priority
class DAG:
    def __init__(self):
        self.graph = {}
        self.users = {} 

    def add_node(self, node):
        self.graph[node.name] = node
        self.graph[node.name] = node

    def add_user(self, user):
        self.users[user.name] = user

    def remove_node(self, node_name):
        if node_name in self.graph:
            del self.graph[node_name]

    def add_edge(self, node_name1, node_name2):
        if node_name1 in self.graph and node_name2 in self.graph:
            self.graph[node_name1].permissions.update(self.graph[node_name2].permissions)

    def remove_edge(self, node_name1, node_name2):
        if node_name1 in self.graph and node_name2 in self.graph:
            for permission in self.graph[node_name2].permissions:
                if permission in self.graph[node_name1].permissions:
                    del self.graph[node_name1].permissions[permission]

    def get_permissions(self, node_name):
        permissions = self.graph[node_name].permissions
        for key in permissions:
            if permissions[key] < self.graph[node_name].priority:
                permissions[key] = self.graph[node_name].priority
        return permissions
    
    def get_priority(self, node_name):
        return self.graph[node_name].priority


# 此实例用于演示权限组的权限扩展
str_dag = DAG()
# 创建权限组A,权限内容为{'read': 1},优先级为1
node_A = Node('A', {'read': 1}, 1)
str_dag.add_node(node_A)

# 创建权限组B,权限内容为{'write': 1},优先级为2
node_B = Node('B', {'write': 1}, 2)
str_dag.add_node(node_B)

# 创建权限组C,权限内容为{'execute': 1},优先级为3
node_C = Node('C', {'execute': 1}, 3)
str_dag.add_node(node_C)

# 设置权限组B依赖权限组A,即B的权限是A的权限加上B自身的权限
str_dag.add_edge('B', 'A')

# 设置权限组C依赖权限组B
str_dag.add_edge('C', 'B')

# 获取权限组C的权限
permissions = str_dag.get_permissions('C')
print(permissions)  

# 输出：{'execute': 3, 'write': 2, 'read': 1}

# 权限扩展
# 创建权限组D,权限内容为{'delete': 1},优先级为4
node_D = Node('D', {'delete': 1}, 4)
str_dag.add_node(node_D)

# 创建权限组E,权限内容为{'update': 1},优先级为5
node_E = Node('E', {'update': 1}, 5)
str_dag.add_node(node_E)

# 设置权限组D依赖权限组C
str_dag.add_edge('D', 'C')

# 设置权限组E依赖权限组D
str_dag.add_edge('E', 'D')

# 获取权限组D的权限
permissions = str_dag.get_permissions('D')
print("D")
print(permissions)  
# 获取权限组E的权限
permissions = str_dag.get_permissions('E')
print("E")
print(permissions)  # 输出：{'update': 5, 'delete': 4, 'execute': 3, 'write': 2, 'read': 1}



# 如何确定权限组并且给用户组赋予权限
str_dag2 = DAG()

# 创建权限组A,权限内容为{'read': 1},优先级为1
node_A = Node('A', {'read': 1}, 1)
str_dag2.add_node(node_A)

# 创建权限组B,权限内容为{'write': 1},优先级为2
node_B = Node('B', {'write': 1}, 2)
str_dag2.add_node(node_B)

# 创建权限组C,权限内容为{'execute': 1},优先级为3
node_C = Node('C', {'execute': 1}, 3)
str_dag2.add_node(node_C)

# 设置权限组B依赖权限组A,即B的权限是A的权限加上B自身的权限
str_dag2.add_edge('B', 'A')

# 设置权限组C依赖权限组B
str_dag2.add_edge('C', 'B')

# 创建用户admin,角色为A和B,此时admin的权限为A和B的权限
# 允许同时获得多个权限组,所以admin的权限为A和B的权限的并集,输入为 A 和 B
# 输出会有两个read ,但是优先级不一样 
# 其他乱七八糟的同理
user_admin = User('admin', ['A', 'B'])
str_dag2.add_user(user_admin)

user_admin2 = User('admin2', ['B'])
str_dag2.add_user(user_admin2)
# 创建用户 sys_execute ,角色为C , C依赖B和A,因此sys_execute的权限最高
sys_execute = User('sys_execute', ['C'])
str_dag2.add_user(sys_execute)

# 获取用户admin的所有权限
permissions = []
for role in str_dag2.users['admin'].roles:
    permissions.append(str_dag2.get_permissions(role))
print(permissions)

# 获取用户 admin2 的所有权限
permissions = []
for role in str_dag2.users['admin2'].roles:
    permissions.append(str_dag2.get_permissions(role))
print(permissions)  

# 获取用户 sys_execute 的所有权限
permissions = []
for role in str_dag2.users['sys_execute'].roles:
    permissions.append(str_dag2.get_permissions(role))
print(permissions)  # 输出：[{'execute': 3, 'write': 3, 'read': 3}]

# 去除重复权限
def merge_permissions(permissions_list):
    merged_permissions = {}
    for permissions in permissions_list:
        for permission, level in permissions.items():
            if permission not in merged_permissions or level > merged_permissions[permission]:
                merged_permissions[permission] = level
    return [merged_permissions]

permissions_list = [{'read': 1}, {'write': 2, 'read': 2}]
print(merge_permissions(permissions_list))  # 输出：[{'read': 2, 'write': 2}]


# CREATE TABLE nodes (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     permissions JSON NOT NULL,
#     priority INT NOT NULL
# );

# CREATE TABLE edges (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     from_node_id INT,
#     to_node_id INT,
#     FOREIGN KEY (from_node_id) REFERENCES nodes(id),
#     FOREIGN KEY (to_node_id) REFERENCES nodes(id)
# );