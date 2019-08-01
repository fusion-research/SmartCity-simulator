""" This module is used to compute different scores once one step of the
simulation is done.

The city is evaluated wrt the following criteria :
* Pollution, How much the energies have poluted for this tick globally (ie.
  the mean of the pollution produced).
* Spendings, Sum of energy cost.
* Citizens' satisfaction (or happiness), Sum of satisfactions of all citizen
  weighted by the importance each citizen give to each criteria (eather,
  lighting).
"""
from itertools import cycle

from scipy.stats import beta as β_distribution
import numpy as np


def compute_scores(people, energies, lights, heaters):
    spendings_score = spendings(energies)
    pollution_score = pollution(energies)

    nuclear = energies.bought_amounts[1] / energies.bought_amounts.sum()
    satisfaction_score = satisfaction(people, lights, heaters, pollution_score, nuclear)
    return {
        "spendings": spendings_score,
        "pollution": pollution_score,
        "happiness": satisfaction_score
    }


def pollution(energies):
    tot = energies.pollution_factors * energies.bought_amounts
    return (tot / energies.bought_amounts.sum()).sum()


def compute_interraction_score(interraction, item):
    print("\n\nInterraction\n\n", interraction, item)
    return (interraction @ item.T) / interraction.sum(1)


def compute_score(params, scores):
    pdf_score = [β_distribution.pdf(score, a, b) for score, (a, b) in zip(scores, params)]

    try:
        print(params, next(scores), pdf_score)
    except:
        print("\n\nComputeScore\n\n", params, scores, pdf_score)
    return np.mean(pdf_score)


def satisfaction(people, lights, heaters, pollution_score, nuclear):
    pollution_score = compute_score(people.pollution, cycle([pollution_score]))

    nuclear_score = compute_score(people.nuclear, cycle([nuclear]))

    lights_inter = compute_interraction_score(people.lights_interraction, lights)
    light_score = compute_score(people.lights_pref, lights_inter)

    heaters_inter = compute_interraction_score(people.heaters_interraction, heaters)
    heat_score = compute_score(people.heater_pref, heaters_inter)

    print("Scores", pollution_score, nuclear_score, light_score, heat_score)

    return pollution_score + nuclear_score + light_score + heat_score


def spendings(energies):
    return (energies.bought_amounts * energies.costs).sum()


if __name__ == '__main__':
    pass


#TODO
"""
On veut que dans les paramètres il soit indiqué les valeurs de préférences de % de lumières
et de température

On estime ensuite la loi beta associée en considérant que le score/personne est la moyenne empirique
on stoque tout ça et roule ma poule

"""