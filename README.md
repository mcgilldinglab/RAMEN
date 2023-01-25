# RAMEN Method Overview
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

# Technical Summary

## Installation
To install Ramen, run the following command "pip install git+https://github.com/mcgilldinglab/RAMEN" on command prompt. 

## Usage
To use Ramen, import the "Ramen" class from ramen.Ramen and initialize a Ramen object. The only mandatory parameter for the constructor is a csv for the data. The data should be processed before using Ramen. Ramen will discretize the data, and remove the variables that have a certain threshold of missing values. It is possible to adjust the threshold through the constructor or parameter of the Ramen object. To continue the next steps, a end_var must be set as well.

### Constuctor
__init__( self, csv_data = None, ref_save_name = "var_val_ref.pickle", end_string = "", bad_var_threshold = 500 )
*csv_data: This parameter is mandatory, it is the data in csv format. Preprocessing should be done before using it in Ramen. Missing values in the dataset should either be NaN or -999. Ramen will discretize the data to be used for the subsequent steps.
*end_string: This parameter must be the name in string of the variable that is studied in the dataset. If it is not a variable in the dataset, it will raise an Assertion Error.
*bad_var_threshold: All variables with less than this amount of non-missing values will be removed from the dataframe.

### Random Walk
random_walk( self, num_exp = 10, num_walks = 50000, num_steps = 7, p_value = 0.05, mode = "default" )
*num_exp: Number of experiments in the random walk.
*num_walks: Number of walks in one experiment of random walk.
*num_steps: Number of steps per walk.
*p_value: The p-value cutoff for the permutation test. Another standard cutoff is 0.01.
*mode: The correction to the p-value, currently "fdr" is implemented, otherwise, it defaults to "default", no correction.

### Genetic Algorithm
genetic_algorithm( self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100 )
*num_candidates: The number of starting candidates.
*end_thresh: If the increase in score from one generation to the next is less than 0.01, then it is considered a bad generation.
*mutate_num: The number of mutation children for each candidate.
*best_cand_num: The number of best candidates that is kept at each generation.
*bad_reprod_accept: The number of bad generations accepted before terminating. This counter is reset whenever there is a good generation.
*reg_factor: The score that is deducted for each edge in the network.
*hard_stop: Maximum iteration before terminating.

## Example Pipeline
