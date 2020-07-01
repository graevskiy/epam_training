
from memory_profiler import profile


def get_for_loop_iterator(values):
    for i in values:
        if isinstance(i, list):
            yield from get_for_loop_iterator(i)
        else:
            yield i


def flatten_without_rec(non_flat):    
    flat = []    
    while non_flat: #runs until the given list is empty.        
        e = non_flat.pop()            
        if type(e) == list: #checks the type of the poped item.                
            non_flat.extend(e) #if list extend the item to given list.
        else:        
            flat.append(e) #if not list then add it to the flat list.            
    return flat

@profile
def main():
    l = [[1,2,3], 4, [5, 6, [7, 8, 9, [10, 11], 12, [13]]]] * 999    
    res1 = list(get_for_loop_iterator(l))
    l = [[1,2,3], 4, [5, 6, [7, 8, 9, [10, 11], 12, [13]]]] * 999
    res2 = flatten_without_rec(l)
    
if __name__ == "__main__":
    main()

