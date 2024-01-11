from typing import Union, Any
from logging import log, INFO, WARNING, ERROR

class Graph:
    def __init__(self, directed: bool = False) -> None:
        self._nodes: list[ dict[ Any , dict[ str , Any ] ] ] = None      ## a list because i have to directly
        self._edges: dict[ tuple[ Any ] , dict [ str , Any ] ] = None    ## access the nodes from adj. matrix
        self._adj_matrix: list[ list[ int ] ] = None
        self.IS_DIRECTED = directed

    def show_adj_mat(self) -> None:
        for row in self._adj_matrix:
            for col in row:
                print(col, end=", ")
            print()

    def add_node(self, node: Any, **attrs) -> bool:
        """
        Adds a node to the graph with attrs as the node's attributes.
        """

        if self._nodes != None and self._adj_matrix != None:

            for _node in self._nodes:
                if node in _node.keys():
                    log(ERROR, "  A node with the same name already exists.")
                    return False

            self._nodes.append(
                {
                    node: {}
                }
            )

            for index in range(len(self._adj_matrix)):
                self._adj_matrix[index].append(0)
            self._adj_matrix.append( [ 0 ] * ( len( self._adj_matrix ) + 1 ) )

        else:

            self._nodes = [
                {
                    node: {}
                }
            ]

            self._adj_matrix = [[0]]

        for attr in attrs.keys():
            self._nodes[-1][node][attr] = attrs[attr]

        return True
    
    def add_nodes_from(self, nodes_to_add: Union["Graph", list[Any]], **attrs) -> bool:
        """
            Adds nodes to the graph with attrs as the nodes' attributes.\n
            `nodes_to_add` can be: a `Graph` obj, a `list` of nodes, a `list`\n
            of `dictionary` of nodes along with that node's specific attribute.
        """

        if type(nodes_to_add) == self.__class__:

            for node in nodes_to_add._nodes:
                for node_name in node.keys():
                    self.add_node(node_name, **{**node[node_name], **attrs})    ## global attrs overwrite node attrs
            return True
        
        elif type(nodes_to_add) == list:

            for maybe_node in nodes_to_add:

                if type(maybe_node) != tuple:
                    self.add_node(maybe_node, **attrs)
                else:
                    self.add_node(maybe_node[0], **{**attrs, **maybe_node[1]})  ## node attrs overwrite global attrs
            
            return True

        else:
            log(
                ERROR,
                " Nodes to be added can either be a list of nodes,              \
                list of tuples of nodes and their attributes or a Graph object."
            )
            return False
    
    def remove_node(self, node_to_remove: Any) -> bool:
        """
            Removes the node `node_to_remove` along with all the attrs and edges related to that node.
        """

        for index, node in enumerate(self._nodes):
            if node_to_remove in node.keys():

                self._nodes.remove(node)            ## remove the node

                self._adj_matrix.pop(index)         ## remove the row in adj. matrix
                for row in self._adj_matrix:
                    row.pop(index)                  ## remove the column in adj. matrix
                
                for edge in self._edges.keys():     ## remove the edges
                    if node_to_remove in edge:
                        self._edges.pop(edge)

                return True
        
        return False
    
    def remove_nodes_from(self, **nodes_to_remove: Any) -> bool:
        for node in nodes_to_remove:
            allGood = self.remove_node(node)
            if not allGood:
                return False
        return True
    
    def add_edge(self, from_node, to_node, **attrs) -> bool:

        if [from_node] not in [list(node.keys()) for node in self._nodes]:
            self.add_node(from_node)
        if [to_node] not in [list(node.keys()) for node in self._nodes]:
            self.add_node(to_node)

        from_node_index = None
        to_node_index = None
        for index, node in enumerate(self._nodes):  ## fetch the indices of the from and to nodes.
            for node_name in node.keys():
                if from_node == node_name:
                    from_node_index = index
                if to_node == node_name:
                    to_node_index = index
        if from_node_index == None or to_node_index == None:
            log(ERROR, " IMPOSSIBLE ERROR.")
            self.remove_nodes_from(from_node, to_node)
            return False

        if self._adj_matrix[from_node_index][to_node_index] == 1:
            log(ERROR, f" An edge between {from_node} and {to_node} already exists.")
            return False

        else:
            if self.IS_DIRECTED:
                if self._edges == None:
                    self._edges = {
                        (from_node, to_node): attrs
                    }
                else:
                    self._edges[(from_node, to_node)] = attrs
                self._adj_matrix[from_node_index][to_node_index] = 1
            else:
                if self._edges == None:
                    self._edges = {
                        (from_node, to_node): attrs
                    }
                else:
                    self._edges[(from_node, to_node)] = attrs
                self._adj_matrix[from_node_index][to_node_index] = 1
                self._adj_matrix[to_node_index][from_node_index] = 1

        return True
    
    def add_edges_from(self, edges_to_add: list[tuple[Any]], **attrs) -> bool:
        
        if type(edges_to_add) == self.__class__:

            for edge in edges_to_add._edges.keys():
                    self.add_edge(*edge, **{**edge[edge], **attrs})             ## global attrs overwrite node attrs
            return True

        elif type(edges_to_add) == list:

            for edge in edges_to_add:

                if len(edge) == 2:
                    self.add_edge(edge[0], edge[1], **attrs)
                else:
                    self.add_edge(edge[0], edge[1], **{**attrs, **edge[2:]})
            
            return True

        else:
            log(
                ERROR,
                " Nodes to be added can either be a list of nodes,              \
                list of tuples of nodes and their attributes or a Graph object."
            )
            return False

g = Graph()
g.add_node(1, color = "red", size = 4)
g.show_adj_mat()
print(g._nodes, sep="\n", end="\n\n")

g.add_node(2)
g.show_adj_mat()
print(g._nodes, sep="\n", end="\n\n")

print("--RESET--")

g2 = Graph()
g2.add_nodes_from(g, size=2)
g2.show_adj_mat()
print(g2._nodes, sep="\n", end="\n\n")

g2.add_edge(3, 4, weight=8.5)
g2.add_edge(2, 1, strength=2)
g2.show_adj_mat()
print(g2._edges, end="\n\n")

print("--RESET--")

g3 = Graph()
g3.add_nodes_from([(1, dict(size=11)), (2, {"color": "blue"})], speed=42)
g3.show_adj_mat()
print(g3._nodes, sep="\n", end="\n\n")

print("--RESET--")