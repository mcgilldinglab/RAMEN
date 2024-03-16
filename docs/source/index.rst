
Welcome to RAMEN's documentation!
=================================

The Ramen method is composed of two major components: random walks to select the most relevant variables to the COVID-19 outcomes (severity or long-COVID) and build a draft candidate network; Genetic Algorithm to find the optimized network that represents the relationships between different clinical variables based on the candidate network draft from the random walk. Random walks: Frist, we calculate mutual information between very possible pairs of clinical variables (all possible edges). All the calculated mutual information will be normalized and represented as the transition probability between clinical variables (edges). We then perform random walks starting from each non-terminal variables (all variables other than the COVID outcomes: severity or long COVID) for N random steps. A random walk will stop once it reaches the destination (absorbing terminal nodes: severity or long-COVID) or run out of steps. After the random walks, we will count the number of visits for each of the edges in all successful random walks (the random walks that reache the terminal destination within N steps). Next, we perform random permutations of the transition probabilities between all nodes (edges). With the random transition probabilities, we will reperform random walks to get the number of visits for all edges by random. Third, we will then employ random permutations to filer edges that are not significiantly visited. Genetic Algorithm: The network with all remaining significant edges (so do the nodes that are connected by those edges) will be used as the starting point to search for the Bayesian network with a Genetic Algorithm. First, we will generate candidate parent networks from the candidate network obtained with random walks. Next, we will crossover all those parent networks to produce offspring networks. Third, each of the offspring networks will mutate to produce more candidate networks. Fourth, all these candidate networks (parents, offspring, and their mutations) will be scored to select the best networks as the parents for the next generation. We will keep performing the above ‘evolution’ process until convergence to obtain the final relationship network.

.. toctree::
   :maxdepth: 2

   installation
   api
   example.rst
   credits
