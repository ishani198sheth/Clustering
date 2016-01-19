
#importing libraries
import heapq
import math
import sys
import itertools

#function definitions are define here

#function to calculate euclidean distance
def euclidean_distance(a, b):
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))
    
#function to calculate centroid of the cluster
def centroid(cluster):
    if len(cluster)>0:
        centroid = [0 for i in range(len(cluster[0]))]
        for point in cluster:
            for i in range(len(point)):
                centroid[i] += point[i]
        for i in range(len(centroid)):
            centroid[i] = centroid[i]/len(cluster)
        return centroid
    else:
        print('Empty Cluster')
        return None
        
# function to convert the nested list of lists of cluster into list of lists
# This function flattens the nested lists
def cluster_conversion(cluster):
    cluster_converted=[]
    for item in cluster:
        for k in item:
            if isinstance(k,list):
                if k not in cluster_converted:
                    cluster_converted.append(k)
            else:
                if item not in cluster_converted:
                    cluster_converted.append(item)           
        
    return cluster_converted

#funtion to generate heap from the list of points
def generate_heap(list_of_points):
    heap=[]
    for i in range(0,len(list_points)):
        for j in range(i+1,len(list_points)):
            #checks if the two points are the same points i.e does not calculate distance for point A and A
            if list_points[j]!=list_points[i]:    
                
                 #calculates the euclidean distance between 2 points
                distance_i_j=euclidean_distance(list_points[i],list_points[j])  
                        
                #pushes the [distance_between_2_points,[list_of_the_2_points]] to the heap
                #heapification is done based on the distances between two points
                heapq.heappush(heap,[distance_i_j,[list_points[i],list_points[j]]]) 
            
    #heapq.heapify(heap)
    return heap

#function to generate clusters from the heap
def cluster_generation(heap,list_points,list_clusters):
    cluster_details=[]
    cluster_formed=[]
    count=0
    if len(heap)!=0 and len(list_points)>1:
        element = heapq.heappop(heap)  # pops the top element(min dist) from min heap
        
        #checks if the element to be combined are not combined with other elements
        for e in element[1]:
            if e in list_points:
                count+=1
                
        #if the point is not already clustered
        if count== len(element[1]):
            
            for e in element[1]:
              
                cluster_formed.append(list_clusters[(list_points.index(e))])
                #cluster_formed+=[list_clusters[(list_points.index(e))]]
                list_clusters.remove(list_clusters[(list_points.index(e))])  #remove individual elements from list of clusters
                list_points.remove(e) #remove the individual points from list of points
            converted_cluster=cluster_conversion(cluster_formed)
                   
            new_point=centroid(converted_cluster)  #calculate new centroid
            list_points.insert(0,new_point)   #add the new centroid as a point for the new cluster
            list_clusters.insert(0,converted_cluster)  # add the new cluster formed to list of clusters
            #iteration= iteration-1
        
      #if any of the popped element is already clustered then recall the cluster generation
      #to form a new cluster ignoring the one popped
        else:
            #element = heapq.heappop(heap)
            cluster_generation(heap,list_points,list_clusters)
    
    # append the final values to be returned after a valid cluster is formed
    cluster_details.append(list_points)
    cluster_details.append(list_clusters)
    return cluster_details

# function to get all indexes of the duplicate element
def duplicates(lst, list):
    return [i for i, x in enumerate(lst) if x == list]

#function to calculate recall and precision
def precision_recall(list_clusters,dictionary_points,labels):
    
    #inner function for precision_recall method
    def duplicates(lst, list):
        return [i for i, x in enumerate(lst) if x == list]
    
    # generating pairs from the clusters created by the algorithm
    temp_algo=[]
    for elements in list_clusters:
        temp=[]
        duplicate_list=[]
        #print elements
        for i in elements:
            
            if isinstance(i,list):
                if i not in duplicate_list:
                    duplicate_list.append(i)
                    items=duplicates(fix_list_points,i)
                    for e in items:
                        temp.append(e)
                #if fix_list_points.index(i) not in temp:
                #    temp.append(fix_list_points.index(i))
            else:
                if i not in duplicate_list:
                    duplicate_list.append(i)
                    duplicates=duplicates(fix_list_points,i)
                    for e in duplicates:
                        temp.append(e)
            #temp.append(fix_list_points.index(i))
        #print temp 
        temp.sort()
        temp_pairs=itertools.combinations(temp,2)
        for eachpair in temp_pairs:
            temp_algo.append(eachpair)
            
    # generating pairs from the clusters that are already created in the input file (gold-standard)
    temp_inputfile=[]
    for element in labels:
        temp=[]
        for e in dictionary_points:
            if dictionary_points[e]==element:
                temp.append(e)
        temp.sort()
        #print temp
        temp_pairs= itertools.combinations(temp,2)
        for eachpair in temp_pairs:
            temp_inputfile.append(eachpair)
    
    #total pairs discovered by the algorithm
    total_pairs_algo=len(temp_algo)
    
    #total pairs disco vered by gold-standard in input file
    total_pairs_input=len(temp_inputfile)
        
    #calculate the correctly identified pair in the input
    correct_pairs=0
    for pairs in temp_algo:
        if pairs in temp_inputfile:
            correct_pairs+=1
    
    #precision and recall calculations
    precision=float(correct_pairs)/total_pairs_algo 
    recall= float(correct_pairs)/total_pairs_input
    
    return [precision,recall]  

      
#taking the arguments from the command line

#input file to be read for the list of points
input_file=sys.argv[1]

#number of clusters that we need to return
k=int(sys.argv[2])

#reading the input-file
input_datafile = open(input_file, "r")
datafile_data = []
datafile_label=[]
datafile_dict = {}
labels=[]

for line in input_datafile:
    data = line.strip().split(',')
    
    #appending each point to the list
    intermediate_data=[]
    for i in range(0,len(data)-1):
        intermediate_data.append(float(data[i]))
    datafile_data.append(intermediate_data)
    
    #creating list of possible values for labels
    if data[len(data)-1] not in labels:
        labels.append(data[len(data)-1])
    
    #appending labels for each point 
    datafile_label.append(data[len(data)-1])

#creating dictionary with point index as key and label as value
duplicate_dataitem=[]        
for dataitem in datafile_data:
    if dataitem not in duplicate_dataitem:
        duplicate_dataitem.append(dataitem)
        duplicateitems=duplicates(datafile_data,dataitem)
        for data_item in duplicateitems:
            datafile_dict[data_item] = datafile_label[data_item]
    
#datafile_dict[datafile_data.index(intermediate_data)] = data[len(data)-1]

#creating list of clusters 

list_clusters=list(datafile_data)  #list of clusters which would be updated as and when required  
list_points=list(datafile_data)    #list of points which would be updated as and when required
fix_list_points=list(datafile_data) #fix list of points to be used for indexing
        
heap=[]
#points_in_heap=[]

#initially the number of clusters are the number of points
cluster_number=len(list_clusters)

#while number of desired clusters are not obtained
while cluster_number>k:
    #print list_points
    
    #generate heap
    heap=generate_heap(list_points)
    
    #after heap generation cluster formation 
    details=cluster_generation(heap,list_points,list_clusters)
    #print details[0]
    list_clusters= details[1]
    cluster_number=cluster_number-1
    
#printing the precision and recall
precision = precision_recall(list_clusters,datafile_dict,labels)
print precision[0] #precision
print precision[1] #recall

#printing the clusters
m=1
for elements in list_clusters:
    temp=[]
    duplicate_list=[]
    #print elements
    for i in elements:
        
        if isinstance(i,list):
            if i not in duplicate_list:
                duplicate_list.append(i)
                items=duplicates(fix_list_points,i)
                for e in items:
                    temp.append(e)
            #if fix_list_points.index(i) not in temp:
            #    temp.append(fix_list_points.index(i))
        else:
            if i not in duplicate_list:
                duplicate_list.append(i)
                duplicates=duplicates(fix_list_points,i)
                for e in duplicates:
                    temp.append(e)
        #temp.append(fix_list_points.index(i))
    #print temp  
    temp.sort() 
    print str(temp)
    m+=1
        
        