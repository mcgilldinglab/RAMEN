
class EdgeVisitTracker(object):

    def __init__ (self, size):
        self.edgesTotalVisits = [0] * size
        self.edgesABVisits = [0] * size
        self.edgesBAVisits = [0] * size
        self.size = size
    
    def reset(self):
        self.edges = [0]*self.size

    def increment_tracker_from_list(self, liste):
        for i in range(len(liste)):
            self.edgesTotalVisits[i] += liste[i]
    
    def increment_AB_visits_from_list(self, liste):
        for i in range(len(liste)):
            self.edgesABVisits[i] += liste[i]

    def increment_BA_visits_from_list(self, liste):
        for i in range(len(liste)):
            self.edgesBAVisits[i] += liste[i]

    def pass_data_to_graph(self, graph):
        for i in range(len(self.edgesTotalVisits)):
            graph.es[i]["Time_Visited"].append(self.edgesTotalVisits[i])
            graph.es[i]["AB"].append(self.edgesABVisits[i])
            graph.es[i]["BA"].append(self.edgesBAVisits[i])
 