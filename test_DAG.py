import unittest
from DAG import DAG, Node, User
import unittest
from DAG import DAG, Node, User

class TestDAG(unittest.TestCase):
    def setUp(self):
        self.dag = DAG()

    def test_add_node(self):
        node = Node("A", {"read": 1}, 1)
        self.dag.add_node(node)
        self.assertIn("A", self.dag.graph)

    def test_add_user(self):
        user = User("John", ["A", "B"])
        self.dag.add_user(user)
        self.assertIn("John", self.dag.users)

    def test_remove_node(self):
        node = Node("A",{"read": 1}, 1)
        self.dag.add_node(node)
        self.dag.remove_node("A")
        self.assertNotIn("A", self.dag.graph)

    def test_add_edge(self):
        node1 = Node("A",{"read": 1}, 1)
        node2 = Node("B",{"read": 1}, 1)
        self.dag.add_node(node1)
        self.dag.add_node(node2)
        self.dag.add_edge("A", "B")
        self.assertEqual(self.dag.graph["A"].permissions, self.dag.graph["B"].permissions)

    def test_remove_edge(self):
        node1 = Node("A",{"read": 1}, 1)
        node2 = Node("B",{"read": 1}, 1)
        node1.permissions = {"read": 1, "write": 2}
        node2.permissions = {"read": 2, "write": 3}
        self.dag.add_node(node1)
        self.dag.add_node(node2)
        self.dag.remove_edge("A", "B")
        self.assertNotIn("read", self.dag.graph["A"].permissions)

    def test_get_permissions(self):
        node = Node("A",{"read": 1}, 1)
        node.permissions = {"read": 1, "write": 2}
        node.priority = 2
        self.dag.add_node(node)
        permissions = self.dag.get_permissions("A")
        self.assertEqual(permissions, {"read": 2, "write": 2})
    def test_get_priority(self):
        node = Node("A",{"read": 1}, 1)
        node.permissions = {"read": 1, "write": 2}
        node.priority = 2
        self.dag.add_node(node)
        priority = self.dag.get_priority("A")
        self.assertEqual(priority, 2)

if __name__ == '__main__':
    unittest.main()