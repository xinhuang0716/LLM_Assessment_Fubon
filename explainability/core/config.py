from dataclasses import dataclass

@dataclass
class CoTConfig:

    # level 2
    step_ratio_lb: float = 0.8
    step_ratio_ub: float = 1.2

    # level 3
    weight_ops: float = 0.4
    weight_num: float = 0.4
    weight_words: float = 0.2

    # level 4
    weight_accuray: float = 0.75
    weight_coherence: float = 0.25

    # overall
    weight_l1: float = 0.4
    weight_l2: float = 0.15
    weight_l3: float = 0.2
    weight_l4: float = 0.25

    # pass rule
    coherence_threshold: float = 0.6
    overall_threshold: float = 0.8 
    avg_overall_threshold: float = 0.8

@dataclass
class CitationConfig:
    pass_threshold: float = 0.8 # indivaul
    avg_overall_threshold: float = 0.8 # average

