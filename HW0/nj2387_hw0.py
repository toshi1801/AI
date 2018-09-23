"""
COMS W4701 Artificial Intelligence - Homework 0

In this assignment you will implement a few simple functions reviewing
basic Python operations and data structures.

@author: NAMAN JAIN (nj2387)
"""


def manip_list(list1, list2):
    # Print the last element of list1
    print(list1[-1])
    
    # Remove the last element of list1
    list1.pop(-1)
    
    # Change the second element of list2 to be identical to the first element of list1.
    list2[1]  = list1[0]
    
    # Print a concatenation of list1 and list2 without modifying the two lists.
    print(list1 + list2)
    
    # Return a single list consisting of list1 and list2 as its two elements.
    return [list1, list2]


def manip_tuple(obj1, obj2):
    # Create a tuple of the two object parameters.
    new_tuple = (obj1, obj2)

    # Attempt to modify the tuple by reassigning the first item--Python should throw an exception upon execution.
    new_tuple[0] = 'AI'


def manip_set(list1, list2, obj):
    # Create a set called set1 using list1.
    set1 = set(list1)

    # Create a set called set2 using list2.
    set2 = set(list2)

    # Add obj to set1.
    set1.add(obj)

    # Test if obj is in set2 (print True or False)
    print(True if obj in set2 else False)

    # Print the difference of set1 and set2.
    print(set1 - set2)

    # Print the union of set1 and set2.
    print(set1 | set2)

    # Print the intersection of set1 and set2.
    print(set1 & set2)

    # Remove obj from set1.
    set1.remove(obj)


def manip_dict(tuple1, tuple2, obj):
    # Create a dictionary such that elements of tuple1 serve as the keys for elements of tuple2.
    dict1 = {tuple1[i]:tuple2[i] for i,_ in enumerate(tuple2)} 
    
    # Print the value of the dictionary mapped by obj.
    print(dict1[obj])
    
    # Delete the dictionary pairing with the obj key.
    dict1.pop(obj, None)
    
    # Print the length of the dictionary.
    print(len(dict1))
    
    # Add a new pairing to the dictionary mapping from obj to the value 0.
    dict1[obj] = 0
    
    # Return a list in which each element is a two-tuple of the dictionary's key-value pairings.
    return [(key, value) for key, value in dict1.items()]

if __name__ == "__main__":
    #Test case
    print(manip_list(["artificial", "intelligence", "rocks"], [4701, "is", "fun"]))

    try: manip_tuple("oh", "no")
    except TypeError: print("Can't modify a tuple!")

    manip_set(["sets", "have", "no", "duplicates"], ["sets", "operations", "are", "useful"], "yeah!")

    print(manip_dict(("list", "tuple", "set"), ("ordered, mutable", "ordered, immutable", "non-ordered, mutable"), "tuple"))