### RAMEN Method Overview
The Ramen method is composed of two major components: random walks to select the most relevant variables to the COVID-19 outcomes (severity or long-COVID) 
and build a draft candidate network; Genetic Algorithm to find the optimized network that represents the relationships between different clinical 
variables based on the candidate network draft from the random walk. 
Random walks: Frist, we calculate mutual information between very possible pairs of clinical variables (all possible edges). All the calculated mutual 
information will be normalized and represented as the transition probability between clinical variables (edges). We then perform random walks starting 
from each non-terminal variables (all variables other than the COVID outcomes: severity or long COVID) for N random steps. A random walk will stop once 
it reaches the destination (absorbing terminal nodes: severity or long-COVID) or run out of steps. After the random walks, we will count the number of 
visits for each of the edges in all successful random walks (the random walks that reache the terminal destination within N steps). Next, we perform 
random permutations of the transition probabilities between all nodes (edges). With the random transition probabilities, we will reperform random walks 
to get the number of visits for all edges by random.  Third, we will then employ random permutations to filer edges that are not significiantly visited. 
Genetic Algorithm: The network with all remaining significant edges (so do the nodes that are connected by those edges) will be used as the starting point 
to search for the Bayesian network with a Genetic Algorithm. First, we will generate candidate parent networks from the candidate network obtained with 
random walks. Next, we will crossover all those parent networks to produce offspring networks. Third, each of the offspring networks will mutate to 
produce more candidate networks. Fourth, all these candidate networks (parents, offspring, and their mutations) will be scored to select the best networks 
as the parents for the next generation. We will keep performing the above ‘evolution’ process until convergence to obtain the final relationship network.

![Y8%QE}`V(K11GO75 0PFS3N](https://user-images.githubusercontent.com/62433629/213577208-9bfea64a-84a3-4724-91ff-da09dc2aa5a9.png)

## Technical Summary

# How to install
To install Ramen, run the following command "pip install git+https://github.com/mcgilldinglab/RAMEN" on command prompt. 

# How to use
To use Ramen, import the "Ramen" class from ramen.Ramen and initialize a Ramen object. The only mandatory parameter for the constructor is a csv for the data. The data should be processed before using Ramen. Ramen will discretize the data, and remove the variables that have a certain threshold of missing values. It is possible to adjust the threshold through the constructor or parameter of the Ramen object. To continue the next steps, a end_var must be set as well.

random_walk( self, num_exp = 10, num_walks = 50000, num_steps = 7, p_value = 0.05, mode = "default" ):
    
genetic_algorithm( self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100 )

3) example pipeline
