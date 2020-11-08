""" Write a script to remove an empty tuple(s) from a list of tuples. """

sample_list = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
output_list = [t for t in sample_list if t]
