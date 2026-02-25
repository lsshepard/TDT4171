from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD
import numpy as np

G = DiscreteBayesianNetwork()

G.add_nodes_from([
                  'join_ntnui_tennis',
                  'money_saved',
                  'practises_per_week',
                  'prior_freetime',
                  'prior_tennis_level',
                  'freetime',
                  'tennis_level',
                  'utility'
                  ])

G.add_edge('join_ntnui_tennis', 'money_saved')
money_saved_cpd = TabularCPD(
                            'money_saved',
                             2,
                             [[0, 1], [1, 0]],
                             evidence=['join_ntnui_tennis'],
                             evidence_card=[2],
                             state_names={
                                'money_saved': ['0', '600'],
                                'join_ntnui_tennis': ['False', 'True']}
                             )

G.add_edge('join_ntnui_tennis', 'practises_per_week')
practises_per_week_cpd = TabularCPD(
                            'practises_per_week',
                             3,
                             [[1, 0.1], [0, 0.7], [0, 0.2]],
                             evidence=['join_ntnui_tennis'],
                             evidence_card=[2],
                             state_names={
                                'practises_per_week': ['0', '1', '2'],
                                'join_ntnui_tennis': ['False', 'True']}
                            )

prior_freetime_pd = TabularCPD(
                            'prior_freetime',
                             2,
                             [[0.5], [0.5]],
                             state_names={
                                'prior_freetime': ['15', '30'],
                                }
                             )

prior_tennis_level_pd = TabularCPD(
                            'prior_tennis_level',
                             2,
                             [[0.5], [0.5]],
                             state_names={
                                'prior_tennis_level': ['beginner', 'mid'],
                                }
                             )

join_ntnui_tennis_pd = TabularCPD(
    "join_ntnui_tennis", 2,
    [[0.5], [0.5]],
    state_names={"join_ntnui_tennis": ["False", "True"]}
)

G.add_edge('prior_freetime', 'freetime')
G.add_edge('practises_per_week', 'freetime')
freetime_cpd = TabularCPD(
                            'freetime',
                             3,
                             [[0.1, 0.5, 0.8, 0, 0.1, 0.1],
                              [0.8, 0.5, 0.2, 0.1, 0.1, 0.15],
                              [0.1, 0, 0, 0.9, 0.8, 0.75]],
                             evidence=['prior_freetime', 'practises_per_week'],
                             evidence_card=[2, 3],
                             state_names={
                                'freetime': ['10', '18', '25'],
                                'practises_per_week': ['0', '1', '2'],
                                'prior_freetime': ['15', '30']}
                            )

G.add_edge('prior_tennis_level', 'tennis_level')
G.add_edge('practises_per_week', 'tennis_level')
tennis_level_cpd = TabularCPD(
                            'tennis_level',
                             3,
                             [[1.0, 0.5, 0.2, 0, 0, 0],
                              [0, 0.5, 0.6, 1, 0.4, 0.2],
                              [0, 0, 0.2, 0, 0.6, 0.8]],
                             evidence=['prior_tennis_level', 'practises_per_week'],
                             evidence_card=[2, 3],
                             state_names={
                                'tennis_level': ['beginner', 'mid', 'advanced'],
                                'practises_per_week': ['0', '1', '2'],
                                'prior_tennis_level': ['beginner', 'mid']}
                            )



G.add_edge('money_saved', 'utility')
G.add_edge('tennis_level', 'utility')
G.add_edge('freetime', 'utility')

# Utility states (0..8)
utility_states = [str(i) for i in range(9)]

money_states = ["0", "600"]
freetime_states = ["10", "18", "25"]
tennis_states = ["beginner", "mid", "advanced"]

score_money = {"0": 0, "600": 0.3}
score_freetime = {"10": 0, "18": 1, "25": 2}
score_tennis = {"beginner": 0, "mid": 2, "advanced": 4}

# Build a deterministic CPD: P(U = u(m,f,t) | m,f,t) = 1
n_cols = len(money_states) * len(freetime_states) * len(tennis_states)
vals = np.zeros((len(utility_states), n_cols))

col = 0
for m in money_states:
    for f in freetime_states:
        for t in tennis_states:
            u = score_money[m] + score_freetime[f] + score_tennis[t]
            vals[int(u), col] = 1.0
            col += 1

utility_cpd = TabularCPD(
    variable="utility",
    variable_card=len(utility_states),
    values=vals.tolist(),
    evidence=["money_saved", "freetime", "tennis_level"],
    evidence_card=[2, 3, 3],
    state_names={
        "utility": utility_states,
        "money_saved": money_states,
        "freetime": freetime_states,
        "tennis_level": tennis_states,
    },
)
          


G.add_cpds(money_saved_cpd, practises_per_week_cpd, prior_freetime_pd, prior_tennis_level_pd, join_ntnui_tennis_pd, freetime_cpd, tennis_level_cpd, utility_cpd)

# print(G.get_cpds("utility"))
print(G.check_model())




from pgmpy.inference import VariableElimination
import numpy as np

# --- add missing edges ---
G.add_edge("money_saved", "utility")
G.add_edge("freetime", "utility")
G.add_edge("tennis_level", "utility")

# --- add missing prior for the root decision variable (required by pgmpy) ---
join_cpd = TabularCPD(
    "join_ntnui_tennis", 2,
    [[0.5], [0.5]],
    state_names={"join_ntnui_tennis": ["False", "True"]}
)

G.add_cpds(join_cpd)  # plus your other CPDs already added
assert G.check_model()

infer = VariableElimination(G)

def expected_utility(join_value: str) -> float:
    q = infer.query(["utility"], evidence={"join_ntnui_tennis": join_value}, show_progress=False)
    u_states = np.array([float(s) for s in q.state_names["utility"]])  # "0".."8" -> numbers
    return float(np.dot(u_states, q.values))

print("EU(join=False):", expected_utility("False"))
print("EU(join=True): ", expected_utility("True"))


from networkx.drawing.nx_pydot import to_pydot

dot = to_pydot(G)
dot.write_png("network.png")
print("Wrote network.png")

print(tennis_level_cpd)