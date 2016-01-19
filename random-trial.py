
#def duplicates(lst, item):
#    return [i for i, x in enumerate(lst) if x == item]
#
#list1=[1,2,3,4,1,2]
##temp=[]
##for element in list1:
##    if element not in temp:
##        temp.append(element)
##        duplicate=duplicates(list1,element)
##        for e in duplicate:
##            print e
#print list1[1]

from compiler.ast import flatten

print flatten([0, [1, 2], [3, 4, [5, 6]], 7])
 
graph=nx.Graph()
graph.add_node(1)
graph.add_node(2)
graph.add_edge(1,2)



print list(graph.edges())