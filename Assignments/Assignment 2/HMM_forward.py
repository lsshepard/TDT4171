import numpy as np


O_T = np.array([[0.9, 0] , [0, 0.2]])
O_F = np.array([[0.1, 0] , [0, 0.8]])


T = np.array([[0.7, 0.3], [0.3, 0.7]])
T_transposed = np.transpose(T)

# f_1:t+1 = alpha * O_t+1 T_transposed f_1:t
def forward(U):
    f = np.zeros((len(U)+1, 2))     # U is indexed 1 timestep behind so f[i+1] corrresponds to U[i]
    f[0] = np.array([0.5, 0.5])     # start with uniform prior
    for i in range(len(U)):
        O_i = O_T if U[i] else O_F  # select correct observatio matrix
        unnormalized_f = O_i @ T_transposed @ f[i]                  # calculate unnormalized probablities
        normalized_f = unnormalized_f / np.sum(unnormalized_f)      # normalize probabilities
        f[i+1] = normalized_f
    return f

U = [True, True] # evidence
f = forward(U)
print('U:', U)
print('f:', f)

U = [True, True, False, True, True] # evidence
f = forward(U)
print('U:', U)
print('f:', f)