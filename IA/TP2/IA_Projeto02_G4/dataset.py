import copy
from collections import defaultdict
from statistics import stdev

from qpsolvers import solve_qp

from probabilistic_learning import NaiveBayesLearner
from utils import *

class DataSet:
    # Inicialização 
    """
    id -> index
    name -> name
    local -> location
    rank -> rank
    desc -> description
    tf -> tuition and fees
    state -> in-state
    ue -> undergrad enrollment
    """
    def _init_(self, id=int, name= " ", local=" ", rank=int, des=" ", tf= int, state=" ", ue=int):
        self.id = id
        self.rank = rank 
        self.tf = tf
        self.ue = ue

        
