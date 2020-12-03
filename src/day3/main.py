from src.classes import Forest, ForestNavigator, Tobogan
import numpy as np
if __name__ == "__main__":
    forest = Forest("input.txt")
    forest_navigator = ForestNavigator(forest, slope=(1,3))
    tobogan = Tobogan(forest_navigator)
    print(f"Part 1: {tobogan.calculate_trees_hit()}")

    ##########PART 2 ##################
    slopes = [(1,1),(1,3),(1,5),(1,7),(2,1)]
    res = []
    for slope in slopes:
        forest_navigator = ForestNavigator(forest, slope=slope)
        tobogan = Tobogan(forest_navigator)
        res.append(tobogan.calculate_trees_hit())
    print(f"Part 2: {res=}, {np.prod(res)}")
