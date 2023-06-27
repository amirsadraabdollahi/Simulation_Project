import random

import numpy as np


def generate_exponential_variable(parameter, count):
    return np.random.exponential(parameter, count)[0]


def weighted_sample_enum(enum_array, weight_enum_array):
    weights = [e.value for e in weight_enum_array]
    array_values = [e.name for e in weight_enum_array]
    sample = random.choices(array_values, weights)[0]
    for e in enum_array:
        if e.name == sample:
            return e
