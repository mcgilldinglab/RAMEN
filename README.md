# Paper

https://www.cell.com/cell-reports-methods/fulltext/S2667-2375(25)00058-X

# Documentation

https://ramen20.readthedocs.io/

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
  
![PipelineGraph](https://github.com/mcgilldinglab/RAMEN/blob/main/method.png)

# Technical Summary
## Installation
Set up the computational environment

**Timing:** <30 min

1. **Install and configure Conda (if not already available).**  
   a. Download and install Anaconda for your operating system. Follow the official instructions for your OS.  
   b. Create a new Conda environment to isolate the RAMEN installation. For example:  
      > conda create -n ramen_env python=3.13  
      > conda activate ramen_env  
   *Note:* This creates and activates an environment named `ramen_env` with Python 3.13. Using a fresh environment prevents version conflicts with other projects.

2. **Install the RAMEN software package and dependencies.**  
   a. Use pip to install RAMEN from the GitHub repository. In the activated environment, run:  
      > pip install git+https://github.com/mcgilldinglab/RAMEN.git@v1.0.0  
   *Note:* This downloads the RAMEN v1.0.0 source and automatically installs required Python libraries (NumPy, Pandas, SciPy, NetworkX, etc.).  
   *Troubleshooting 1:* Refer to documentation if dependency issues occur.

3. **Validate installation.**  
   a. Open a Python interpreter and run:  
      ```python
      from ramen.Ramen import Ramen
      ```  
   > The package is successfully installed if there is no error.  
   *Troubleshooting 2:* Ensure the installation completed without errors.

**CRITICAL:** Make sure the installation is successful before proceeding.

Note that scikit-network library is built on C++ and might require C++ build tools. If you don't have it, the following error will appear:
```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```
you can download the build tools on Visual Studio, and the error will be resolved.

## Usage
To use Ramen, import the "Ramen" class from ramen.Ramen and initialize a Ramen object. The data should be processed before using Ramen. Ramen will only remove the variables that have a certain threshold of non missing values and discretize the data. It is possible to adjust the threshold through the constructor or field of the Ramen object. An end variable must also be set, so that RandomWalk terminates upon reaching the variable. After initializing the Ramen object, random_walk can be run. random_walk must be run before genetic_algorithm, as the output from Random Walk is used as input for Genetic Algorithm to create the starting candidates. genetic_algorithm will generate the final network.

### Ramen Object Fields
* __df__ (pandas.DataFrame): discretized dataframe, must be input when creating the object.
* __var_ref__ (dictionary): dictionary mapping the real values to the discretized value e.g { variable: { "Yes" : 0, "No" : 1 } }.
* __end_string__ (string): variable indicating the termination node for random_walk. The string must represent a column in the dataframe.
* __mutual_info_array__ (np.array): 2D array continaining the mutual information for all pairs of variables, initialized at the constructor.
* __signif_edges__ (list): list containing all of the significant edges after random walk permutation test stored in string format. This field is None and is initialized after termination of random_walk.
* __network__ (networkx.DiGraph): graph object of the final network after terminating RAMEN method. This is set to None and initialized after termination of genetic_algorithm.

### Ramen Constructor
__init__( self, csv_data = None, ref_save_name = "var_val_ref.pickle", end_string = "", bad_var_threshold = 500 )
* __csv_data__ (string: path for a csv file): This parameter is mandatory, it is the data in csv format. Preprocessing should be done before using it in Ramen. Missing values in the dataset should either be NaN or -999. Ramen will discretize the data to be used for the subsequent steps.
* __end_string__ (string): This parameter must be the name in string of the variable that is studied in the dataset. If it is not a variable in the dataset, it will raise an Exception.
* __min_values__ (int): All variables with less than this amount of non-missing values will be removed from the dataframe.

### Random Walk Method
__random_walk( self, num_exp = 10, num_walks = 50000, num_steps = 7, p_value = 0.05, mode = "default" )__
* __num_exp__ (int): Number of experiments in the random walk.
* __num_walks__ (int): Number of walks in one experiment of random walk.
* __num_steps__ (int): Number of steps per walk.
* __p_value__ (float): The p-value cutoff for the permutation test. Another standard cutoff is 0.01.
* __correction__ (string): The correction to the p-value, currently "fdr" is implemented, otherwise, it defaults to "no_correction".

### Genetic Algorithm Method
__genetic_algorithm( self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100 )__
* __num_candidates__ (int): The number of starting candidates.
* __end_thresh__ (float): If the increase in score from one generation to the next is less than the end_thresh, then it is considered a bad generation.
* __mutate_num__ (int): The number of mutation children for each candidate.
* __best_cand_num__ (int): The number of best candidates that is kept at each generation.
* __bad_reprod_accept__ (int): The number of bad generations accepted before terminating. This counter is reset whenever there is a good generation.
* __reg_factor__ (float): The score that is deducted for each edge in the network.
* __hard_stop__ (int): Maximum iteration before terminating.

### Other methods
__load_signif_edges_pickle(self, filename)__ -> load signif_edges from a pickle file
* __filename__ (str): the path of the pickle saving the significant edges.

__set_end_string(self, end_string)__ -> set the end_string
* __end_string__ (str): new end string

__get_signif_edges(self)__ -> get the signif_edges

__set_signif_edges(self, signif_edges)__ -> set the signif_edges field
* __signif_edges__ (list): set the significant edges to be a new list of edges.

__get_var_ref(self)__ -> get the variable values mapping created from discretization

__get_mutual_info_array(self)__ -> get the mutual information matrix

__export_ramen_as_dict(self)__ -> return ramen results as a dictionary

{
  "DATASET_PATH": self.csv_data_name,
  "END_VARIABLE": self.end_string,
  "VAR_REF": self.var_ref,
  "RW_NETWORK": self.signif_edges,
  "FINAL_NETWORK": list(self.network.edges()),
  "RW_EDGE_VISIT": self.edge_visit_dict,
}

## Example usage

After installing Ramen package using the command above:

### Initializing Ramen object
<img width="1010" alt="Screen Shot 2023-01-26 at 10 28 55 AM" src="https://user-images.githubusercontent.com/76263492/214884830-fb6e61a1-c8df-418a-88e8-53e81918991d.png">

### Initiating Random Walk
<img width="996" alt="Screen Shot 2023-01-26 at 10 29 05 AM" src="https://user-images.githubusercontent.com/76263492/214884862-0b811731-3beb-407e-a5e0-385878e833d8.png">

### Initiating Genetic Algorithm
<img width="1000" alt="Screen Shot 2023-01-26 at 10 29 14 AM" src="https://user-images.githubusercontent.com/76263492/214884881-c33700c5-b2c0-4d73-b663-0b5c66a9370e.png">

### Implementation Example
Please refer also to this public implementation with RAMEN scripts ready to run! https://github.com/YWX2020/RAMENRunner

# Credits
This repository is developed by __Yiwei Xiong__ and __Jingtao Wang__. We also have a web app http://dinglab.rimuhc.ca/pgm/ to interact with networks developed by __Xiaoxiao Shang__. This project is done under the supervision of Professor __Jun Ding__.

__Tingting Chen__ processed data allowing us to test our methods. Professor __Douglas D. Fraser__ provided an alternative dataset allowing us to check our method on an alternative dataset. Professor __Gregory Fonseca__ and __Simon Rousseau__ provided the dataset on which the method is built and provided insights into biology knowledge.

