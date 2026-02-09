import numpy as np 
import random
import tqdm
import math



def grid_simulation(grid, new_idx, num_generation, dim, deme_pop, s, r, migration_prob, mutant_prob): 
    rng = np.random.default_rng()

    for gen in tqdm.tqdm(range(num_generation)):

        #reproducing and mutating 
        j=0
        for row in grid:
            i=0  
            for deme in row: 
                num_new = 0 
                for variant, pop in deme.items(): 
                    #print ('pop' + str(pop))
                    #print("variant" + str(variant))
                    if (variant ==0):
                        offspring = rng.binomial(pop, r)
                    else: 
                        offspring = rng.binomial(pop, r*(1+s))
                    new = rng.binomial(offspring, mutant_prob)
                    num_new+=new
                    #print("offspring" + str(offspring))
                    #print("num_new"  + str(num_new))
                    #print("new" + str(new))
                    #update population of current type
                    #print("pop " + str(pop))
                    #print("offspring " + str(offspring))
                    #print("new" + str(new))
                    deme[variant] = pop + offspring - new 
                    #print("before variant" + str(variant))
                    #print("before pop" + str(pop))
                    #print("after pop" + str(deme[variant]))
                    #create new mutant population 
                for idx in range(new_idx, new_idx + num_new): 
                    #print(idx)
                    deme[idx] = 1 
                new_idx+=num_new 
                i+=1 
            j+=1
        #migration  
        j = 0 
        for row in grid:  
            i=0
            for deme in row: 
                for variant, pop in deme.items():
                    #print("variant" + str(variant)) 
                    #print("pop" + str(pop))
                    migrate = rng.binomial(pop, migration_prob)
                    #print("migrate" + str(migrate))
                    deme[variant] -= migrate
                    #print("variant" + str(variant)) 
                    #print("deme[variant]" + str(deme[variant]))
                    #print("pop" + str(pop))

                    for m in range(migrate): 
                        locations = [(i-1, j-1),(i-1, j), (i-1, j+1), (i, j+1), (i+1, j+1), (i+1, j), (i+1, j-1), (i, j-1)]
                        loc_idx = random.randint(0, 7)
                        """
                        -------
                        |0|1|2|
                        |7|x|3|
                        |6|5|4|
                        -------
                        """
                        new_row,new_col = locations[loc_idx] 
                        #making sure not out of bound 
                        if new_row >= 0 and new_col >= 0 and new_row < dim and new_col <dim:
                            try:
                                grid[new_row][new_col][variant] += 1
                            except KeyError:
                                grid[new_row][new_col][variant] = 1
                i+=1 
            j+=1
        #sample down  
        for row in grid:  
            for deme in row: 
                total_pop = 0 
                for variant, pop in deme.items(): 
                    total_pop+=pop 
                #print("total_pop" + str(total_pop))
                for variant, pop in deme.items():  
                    if total_pop != 0: 
                        deme[variant] = math.ceil(deme[variant] * deme_pop / total_pop) #issue: doesnt necesarily add to 20
                    #print("variant" + str(variant))
                    #print("pop" + str(pop))
                    #print("variant" + str(variant))
                    #print("pop" + str(deme[variant]))
      
    return grid, new_idx