import numpy as np 
import random
import tqdm
import math



def linear_simulation(vector, new_idx, num_generation, dim, deme_pop, s, r, migration_prob, mutant_prob): 
    rng = np.random.default_rng()

    for gen in  tqdm.tqdm(range(num_generation)):
        i=0  
        #reproducing and mutating 
        for deme in vector:
            num_new = 0 
            for variant, pop in deme.items(): 
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
        #migration 
        i=0
 
        for deme in vector:  
            for variant, pop in deme.items():

                migrate = rng.binomial(pop, migration_prob)

                deme[variant] -= migrate

                for m in range(migrate):
                    locations = [i-1, i+1]
                    loc_idx = random.randint(0, 1)
                    """
                    -------
                    |0|x|1|
                    -------
                    """
                    new_i = locations[loc_idx] 
                    if new_i >= 0 and new_i < dim: 
                        try:
                            vector[new_i][variant] += 1
                        except KeyError:
                            vector[new_i][variant] = 1
            i+=1 
        #sample down  
        for deme in vector:  
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
      
    return vector, new_idx