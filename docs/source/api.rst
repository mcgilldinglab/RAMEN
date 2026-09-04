ramen module
=============
This section provides documentation for public APIs for RAMEN


.. class:: ramen.Ramen.Ramen
   
   This is the ramen class

   .. method:: __init__(self, csv_data="", end_string="", min_values=0)

      Constructor of the Ramen Object, which will be used to run random walk and genetic algorithm.

      :param csv_data: path to the data in csv form. Mandatory
      :type csv_data: str
      :param end_string: the destination variable of absorbing random walk. Mandatory.
      :type end_string: str
      :param min_values: number of minimum values in a column, if it is less, then the variable gets pruned.
      :type min_values: int

   .. method:: random_walk(self, num_walks=50000, num_steps=None, p_value=0.05, correction="no_correction")

      Method to begin the absorbing random walk once the Ramen object is initialized. The significant edges will be stored in ramen_object.signif_edges.

      :param num_walks: the number of random walks per experiment. (default value is 50000)
      :type num_walks: int
      :param num_steps: Maximum steps per random walk. If None, RAMEN automatically selects 3-9 steps according to the number of variables.
      :type num_steps: int or None
      :param p_value: the cutoff value to determine significance of edge visits. An edge is significant if it is below p_value. (default value is 0.05)
      :type p_value: float
      :param correction: choose correction method on the significant edges p-values. (supported correction: ["fdr", "no_correction"])
      :type correction: str

      :rtype: None

   .. method:: genetic_algorithm(self, num_candidates = 10, end_thresh = 0.01, mutate_num = 100, best_cand_num = 10, bad_reprod_accept = 10, reg_factor = 0.01, hard_stop = 100)
       
      Method to begin the genetic algorithm once random walk is complete. The result neetwork will be stored in ramen_object.network.

      :param num_candidates: number of initial candidates. (default value is 10)
      :type num_candidates: int
      :param end_thresh: if the score increase between generations are continuously below end_thresh, then it converges. (default value is 0.01)
      :type end_thresh: float
      :param mutate_num: the number of mutations per intermediate candidate after cross breeding. (default value is 100)
      :type mutate_num: int
      :param best_cand_num: the number of top candidates kept after a generation. (default value is 10)
      :type best_cand_num: int
      :param bad_reprod_accept: the number of generations with < end_thresh increase before convergeance. (default value is 10)
      :type bad_reprod_accept: int
      :param reg_factor: score penalty per edge (default value is 0.01)
      :type reg_factor: float
      :param hard_stop: maximum number of generations (default value is 100)
      :type hard_stop: int
      
      :rtype: None



   .. method:: set_end_string(self, end_string)

      Method to modify the end_string of absorbing random walk.

      :param end_string: name of end variable.
      :type end_string: str

      :rtype: None
   
   .. method:: get_signif_edges(self)

      Return a copy of the significant edges, or None if there are None.

      :return: list of tuples of len 2 representing edges tup<str, str>>
      :rtype: list

   .. method:: set_signif_edges(self, signif_edges)

      Set the significant edges.

      :param signif_edges: significant edges to set.
      :type signif_edges: list<tup<str, str>>

      :rtype: None

   .. method:: get_var_ref(self)

      Get the discrete to variable value reference.

      :return: dictionary of variable value mappings.
      :rtype: dict

   .. method:: get_mutual_info_array(self)

      Get the mutual information matrix.

      :return: 2D-array containing mutual information values.
      :rtype: numpy.array
    