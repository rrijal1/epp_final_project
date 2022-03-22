"""Run a Schelling (1969, :cite:`Schelling69`) segregation
model and store a list with locations by type at each cycle.

The scripts expects that a model name is passed as an
argument. The model name must correspond to a file called
``[model_name].json`` in the "IN_MODEL_SPECS" directory.

"""
import json
import pickle

import numpy as np
import pandas as pd
import pytask
from scipy.io import loadmat

from src.config import BLD
from src.config import SRC
from src.model_code.agent import Agent


annots = loadmat('C:/Users/rijal/epp-materials/EPP_Final_Project/monetary_shocks/Matlab/Reference Code/Matlab/BondSpreads.mat')

annots['s']

data = annots['s'][0, 0][0]

# data = [[row.flat[0] for row in line] for line in annots['s'][0]]

cols = annots['s'][0, 0][1]

col_names = [i.item() for i in cols[0].tolist()]

data_points = [i.tolist() for i in data]


df = pd.DataFrame(data_points, columns=col_names)


@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            {
                "model": SRC / "model_specs" / f"{model_name}.json",
                "agent": SRC / "model_code" / "agent.py",
                "data": BLD / "data" / "initial_locations.csv",
            },
            BLD / "analysis" / f"schelling_{model_name}.pickle",
        )
        for model_name in ["baseline", "max_moves_2"]
    ],
)
def task_schelling(depends_on, produces):
    model = json.loads(depends_on["model"].read_text(encoding="utf-8"))

    np.random.seed(model["rng_seed"])

    # Load initial locations and setup agents
    initial_locations = np.loadtxt(depends_on["data"], delimiter=",")
    agents = setup_agents(model, initial_locations)
    # Run the main analysis
    locations_by_round = run_analysis(agents, model)
    # Store list with locations after each round
    with open(produces, "wb") as out_file:
        pickle.dump(locations_by_round, out_file)
