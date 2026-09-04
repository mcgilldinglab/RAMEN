# Paper

https://www.cell.com/cell-reports-methods/fulltext/S2667-2375(25)00058-X

# Documentation

- [API documentation](https://ramen20.readthedocs.io/en/latest/api.html)
- [RAMEN tutorial](./RAMEN_tutorial.ipynb)

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
      > pip install git+https://github.com/mcgilldinglab/RAMEN.git@development
   *Note:* This installs the current RAMEN development version and its required Python dependencies (NumPy, Pandas, SciPy, NetworkX, etc.).  
   To run the tutorial locally, install Jupyter with 
   `python -m pip install notebook ipykernel`.
   

3. **Validate installation.**  
   a. Open a Python interpreter and run:  
      ```python
      from ramen.Ramen import Ramen
      ```  
   > The package is successfully installed if there is no error.  
  



Note that scikit-network library is built on C++ and might require C++ build tools. If you don't have it, the following error will appear:
```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```
you can download the build tools on Visual Studio, and the error will be resolved.


## Usage

RAMEN accepts a CSV file in which rows represent samples and columns represent variables. The outcome variable is identified by its column name and may appear in any column. Missing values should be encoded as blank/NaN or -999.

For a complete workflow and downstream analysis, see the [RAMEN tutorial](./RAMEN_tutorial.ipynb). Detailed class and method parameters are available in the [API documentation](https://ramen20.readthedocs.io/en/latest/api.html).

# Credits
This repository is developed by __Yiwei Xiong__ and __Jingtao Wang__. We also have a web app http://dinglab.rimuhc.ca/pgm/ to interact with networks developed by __Xiaoxiao Shang__. This project is done under the supervision of Professor __Jun Ding__.

__Tingting Chen__ processed data allowing us to test our methods. Professor __Douglas D. Fraser__ provided an alternative dataset allowing us to check our method on an alternative dataset. Professor __Gregory Fonseca__ and __Simon Rousseau__ provided the dataset on which the method is built and provided insights into biology knowledge.

