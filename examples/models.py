import networkx as nx
import numpy as np
import matplotlib.pylab as plt

def example_multiple_mergers():
    G = nx.DiGraph()
    G.add_node('Ancestral', nu=1, T=0)
    G.add_node('Early 1', nu=1, T=0.1)
    G.add_node('Early 2', nu=1, T=0.1)
    G.add_node('Pop A', nu=2, T=0.1, pulse={('Pop B',.5,.05)})
    G.add_node('Pop B', nu=1, T=0.2)
    G.add_node('Pre', nu=2, T=0.1)
    G.add_node('Left', nu=1, T=0.3)
    G.add_node('Right', nu=1, T=0.1)
    G.add_edges_from([('Ancestral','Early 1'),('Ancestral','Early 2'),('Early 1','Left'),('Early 2','Pop B'),('Pop A','Pre')])
    G.add_weighted_edges_from([('Early 1','Pop A',.25),('Early 2','Pop A',.75),
        ('Pre','Right',.1),('Pop B','Right',.9)])
    return G



def complicated_merger_model():
    G = nx.DiGraph()
    G.add_node('root', nu=1, T=0)
    G.add_node('A', nu=2, T=.2)
    G.add_node('B', nu=1.5, T=.1)
    G.add_node('C', nu=.5, T=.2)
    G.add_node('D', nu=2., T=.1)
    G.add_node('E', nu=.2, T=.1)
    G.add_node('F', nu=1, T=.1)
    G.add_node('G', nu=2, T=.2)
    G.add_node('H', nu=.3, T=.1)
    G.add_node('I', nu=.2, T=.05)
    G.add_node('J', nu=.1, T=.05)
    G.add_node('K', nu=.5, T=.15, pulse={('G', .5, .2)}) # halfway down K branch, 0.2 pulse to G
    G.add_node('L', nu=1, T=.15)
    G.add_node('pop1', nu=1, T=.1)
    G.add_node('pop2', nu=1.5, T=.05)
    G.add_node('pop3', nu=.5, T=.1)
    G.add_node('pop4', nu=.75, T=.15)
    
    G.add_edges_from([('root','A'), ('root','B'), ('B','C'), ('B','D'), ('A','E'),
        ('E','F'), ('E','G'), ('F','H'), ('G','J'), ('G','pop3'), ('H','pop1'),
        ('H','I'), ('C','K'), ('C','L')])
    G.add_weighted_edges_from([('D','E',.2), ('A','E',.8)])
    G.add_weighted_edges_from([('I','pop2',.4), ('J','pop2',.6)])
    G.add_weighted_edges_from([('K','pop4',.5), ('L','pop4',.5)])
    return G


"""
Out of Africa example
"""

def ooa(params):
    """
    The 13 parameter out of Africa model from Gutenkunst et al. (2009)
    """
    (nuA, TA, nuB, TB, nuEu0, nuEuF, nuAs0,
        nuAsF, TF, mAfB, mAfEu, mAfAs, mEuAs) = params
    
    G  = nx.DiGraph()
    G.add_node('root', nu=1, T=0)
    G.add_node('A', nu=nuA, T=TA)
    G.add_node('B', nu=nuB, T=TB, m={'YRI':mAfB})
    G.add_node('YRI', nu=nuA, T=TB+TF, m={'B':mAfB, 'CEU':mAfEu, 'CHB': mAfAs})
    G.add_node('CEU', nu0=nuEu0, nuF=nuEuF, T=TF, m={'YRI':mAfEu, 'CHB':mEuAs})
    G.add_node('CHB', nu0=nuAs0, nuF=nuAsF, T=TF, m={'YRI':mAfAs, 'CEU':mEuAs})
    
    G.add_edges_from([('root','A'), ('A','B'), ('A','YRI'), ('B','CEU'),
                      ('B','CHB')])
    
    return G

def kamm_model():
    """
    8-11 population model (depending on how you count)
    There is some confusion (to me) about the LBK/Sard branches.. need to 
    figure that out.
    """
    # population sizes
    generation_time = 25
    N_Losch = 1.92e3
    N_Mbu = 1.73e4
    N_Mbu_Losch = 2.91e4
    N_Han = 6.3e3
    N_Han_Losch = 2.34e3
    N_Nean_Losch = 1.82e4
    N_Nean = 86.9
    N_LBK = 75.7
    N_Sard = 1.5e4
    N_Sard_LBK = 1.2e4
    N_Basal = N_Losch
    N_Ust = N_Basal
    N_MA1 = N_Basal
    # population merge times in years, divided by generation time
    t_Mbu_Losch = 9.58e4 / generation_time
    t_Han_Losch = 5.04e4 / generation_time
    t_Ust_Losch = 5.15e4 / generation_time
    t_Nean_Losch = 6.96e5 / generation_time
    t_MA1_Losch = 4.49e4 / generation_time
    t_LBK_Losch = 3.77e4 / generation_time
    t_Basal_Losch = 7.98e4 / generation_time
    t_Sard_LBK = 7.68e3 / generation_time
    t_GhostWHG_Losch = 1.56e3 / generation_time
    # pulse admixture times and fractions
    p_Nean_to_Eur = 0.0296
    t_Nean_to_Eur = 5.68e4 / generation_time
    p_Basal_to_EEF = 0.0936
    t_Basal_to_EEF = 3.37e4 / generation_time
    p_GhostWHG_to_Sard = 0.0317
    t_GhostWHG_to_Sard = 1.23e3 / generation_time
    # sample_times (in years), divided by estimated generation time
    t_Mbuti = 0
    t_Han = 0
    t_Sardinian = 0
    t_Loschbour = 7.5e3 / generation_time
    t_LBK = 8e3 / generation_time
    t_MA1 = 24e3 / generation_time
    t_UstIshim = 45e3 / generation_time
    t_Altai = 50e3 / generation_time

    Ne = N_Nean_Losch # set ancestral size as reference Ne

    # figure out the timing of the pulses as proportions along the source branches
    frac_nean_pulse = 1-(t_Nean_to_Eur-t_Altai)/(t_Mbu_Losch-t_Altai)
    frac_losch_pulse = 1
    
    G = nx.DiGraph()
    G.add_node('root', nu=1, T=0)
    # neanderthals
    G.add_node('Neand_const', nu=N_Nean_Losch/Ne, 
               T=(t_Nean_Losch-t_Mbu_Losch)/2/Ne)
    G.add_edge('root','Neand_const')
    G.add_node('Neanderthal', nu0=N_Nean_Losch/Ne, nuF=N_Nean/Ne,
               T=(t_Mbu_Losch-t_Altai)/2/Ne,
               pulse={('Ust_Losch',frac_nean_pulse,p_Nean_to_Eur)})
    G.add_edge('Neand_const','Neanderthal')
    
    G.add_node('Mbu_Losch', nu=N_Mbu_Losch/Ne,
               T=(t_Nean_Losch-t_Mbu_Losch)/2/Ne)
    G.add_edge('root','Mbu_Losch')
    
    # mbuti split
    G.add_node('Mbuti', nu=N_Mbu/Ne,
               T=t_Mbu_Losch/2/Ne)
    G.add_node('Basal_Losch', nu=N_Han_Losch/Ne,
               T=(t_Mbu_Losch-t_Basal_Losch)/2/Ne)
    G.add_edges_from([('Mbu_Losch','Mbuti'),('Mbu_Losch','Basal_Losch')])
    
    # basal european split
    G.add_node('Basal Eur', nu=N_Basal/Ne,
               T=(t_Basal_Losch-t_Basal_to_EEF)/2/Ne,
               pulse={('LBK_Sard', 1, p_Basal_to_EEF)})
    G.add_node('Ust_Losch', nu=N_Han_Losch/Ne,
               T=(t_Basal_Losch-t_Ust_Losch)/2/Ne)
    G.add_edges_from([('Basal_Losch','Basal Eur'),('Basal_Losch','Ust_Losch')])
    
    # UstIshim split
    G.add_node('UstIshim', nu=N_Ust/Ne,
               T=(t_Ust_Losch-t_UstIshim)/2/Ne)
    G.add_node('Han_Losch', nu=N_Han_Losch/Ne,
               T=(t_Ust_Losch-t_Han_Losch)/2/Ne)
    G.add_edges_from([('Ust_Losch','UstIshim'),('Ust_Losch','Han_Losch')])
    
    # han split
    G.add_node('Han', nu=N_Han/Ne,
               T=(t_Han_Losch)/2/Ne)
    G.add_node('MA1_Losch', nu=N_Losch/Ne,
               T=(t_Han_Losch-t_MA1_Losch)/2/Ne)
    G.add_edges_from([('Han_Losch','Han'),('Han_Losch','MA1_Losch')])
    
    # MA1 split
    G.add_node('MA1', nu=N_MA1/Ne,
               T=(t_MA1_Losch-t_MA1)/2/Ne)
    G.add_node('LBK_Losch', nu=N_Losch/Ne,
               T=(t_MA1_Losch-t_LBK_Losch)/2/Ne)
    G.add_edges_from([('MA1_Losch','MA1'),('MA1_Losch','LBK_Losch')])
    
    # LBK split
    G.add_node('LBK_Sard', nu=N_Sard_LBK/Ne,
               T=(t_LBK_Losch-t_Sard_LBK)/2/Ne)
    G.add_node('Loschbour', nu=N_Losch/Ne,
               T=(t_LBK_Losch-t_GhostWHG_to_Sard)/2/Ne,
               pulse={('Sardinian',1,p_GhostWHG_to_Sard)})
    G.add_edges_from([('LBK_Losch','LBK_Sard'),('LBK_Losch','Loschbour')])
    
    # Sardinian-LBK split
    G.add_node('LBK', nu=N_LBK/Ne,
               T=t_Sard_LBK/2/Ne)
    G.add_node('Sardinian', nu=N_Sard/Ne,
               T=t_Sard_LBK/2/Ne)
    G.add_edges_from([('LBK_Sard','LBK'),('LBK_Sard','Sardinian')])
    
    return G

def ragsdale_archaic_admixture():
    # set params
    (nuA, TA, nuB, TB, nuEu0, nuEuF, nuAs0, nuAsF, TF,
        mAfB, mAfEu, mAfAs, mEuAs,
        TMH, TN, f_mAA_begin, mAA, mNeand, T_arch_end) = (
        3.78, 1.11, 0.233, 0.100, 0.627, 2.87, 0.176, 16.2, 0.169,
        3.95, 0, 0.180, 0.859,
        0.528, 0.364, 0.566, 0.180, 0.112, 0.0967)
    
    # Ne = 3700
    
    # f_mAA_being tells us the fraction along the AA lineage that migration
    # with MH, A, and YRI begins
    
    Ttot = TF+TB+TA+TMH+TN
    TNeand = Ttot-T_arch_end
    TAA = TF+TB+TA+TMH-T_arch_end
    TAA_nomig = f_mAA_begin*TAA
    TAA_mig = (1-f_mAA_begin)*TAA
    
    G = nx.DiGraph()
    
    G.add_node('root', nu=1, T=0)
    
    G.add_node('Neand', nu=1, T=TNeand,
               m={'B':mNeand, 'CEU':mNeand, 'CHB':mNeand})
    G.add_node('MH_AA', nu=1, T=TN)
    G.add_node('AA_nomig', nu=1, T=TAA_nomig)
    G.add_node('AA', nu=1, T=TAA_mig,
               m={'MH':mAA, 'A':mAA, 'YRI':mAA})
    
    G.add_node('MH', nu=1, T=TMH,
               m={'AA':mAA})
    G.add_node('A', nu=nuA, T=TA,
               m={'AA':mAA})
    G.add_node('B', nu=nuB, T=TB,
               m={'Neand':mNeand, 'YRI':mAfB})
    
    G.add_node('YRI', nu=nuA, T=TB+TF,
               m={'AA':mAA, 'B':mAfB, 'CEU':mAfEu, 'CHB':mAfAs})
    G.add_node('CEU', nu0=nuEu0, nuF=nuEuF, T=TF,
               m={'Neand':mNeand, 'YRI':mAfEu, 'CHB':mEuAs})
    G.add_node('CHB', nu0=nuAs0, nuF=nuAsF, T=TF,
               m={'Neand':mNeand, 'YRI':mAfAs, 'CEU':mEuAs})
    
    edges = [('root','Neand'), ('root','MH_AA'), ('MH_AA','AA_nomig'),
             ('MH_AA','MH'), ('AA_nomig','AA'), ('MH','A'), ('A','YRI'), 
             ('A','B'), ('B','CEU'), ('B','CHB')]
    G.add_edges_from(edges)
    return G

