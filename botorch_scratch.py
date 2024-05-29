import random
from controller import knob_set, metric_set
from sklearn.preprocessing import OneHotEncoder, StandardScaler , MinMaxScaler
import numpy as np
import torch
from botorch.models import SingleTaskGP
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.optim import optimize_acqf
from botorch.acquisition import UpperConfidenceBound
from botorch import fit_gpytorch_model
from botorch.models.transforms import Standardize
from botorch.utils.transforms import normalize, unnormalize
from botorch.fit import fit_gpytorch_model


def gen_random_data(target_data):
    random_knob_result = {}
    for name in target_data.knob_labels:
        vartype = knob_set[name]['type']
        # if vartype == 'bool':
        #     flag = random.randint(0, 1)
        #     if flag == 0:
        #         random_knob_result[name] = False
        #     else:
        #         random_knob_result[name] = True
        if (vartype == 'enum' or vartype == 'bool'):
            enumvals = knob_set[name]['enumval']
            enumvals_len = len(enumvals)
            rand_idx = random.randint(0, enumvals_len - 1)
            random_knob_result[name] = knob_set[name]['enumval'][rand_idx]
            # random_knob_result[name] = rand_idx
        elif vartype == 'int':
            minval=knob_set[name]['minval']
            maxval=knob_set[name]['maxval']
            random_knob_result[name] = random.randint(int(minval), int(maxval))
        elif vartype == 'real':
            minval=knob_set[name]['minval']
            maxval=knob_set[name]['maxval']
            random_knob_result[name] = random.uniform(float(minval), float(maxval))
        # elif vartype == STRING:
        #     random_knob_result[name] = "None"
        # elif vartype == TIMESTAMP:
        #     random_knob_result[name] = "None"
    return random_knob_result



def configuration_recommendation(target_data, runrec=None):
    
    if target_data.num_previousamples < 70 and runrec is None:
        print("Running configuration recommendation...")  # Give random recommendation initially

        return gen_random_data(target_data)

    weights = [1, 0]  # Adjust as needed
    # Identify the index of the categorical variable
    categorical_indices = [
        i for i, label in enumerate(target_data.knob_labels)
        if knob_set[label]['type'] in ['enum', 'bool']
    ]
    encoder = OneHotEncoder(sparse_output=False)
    scaler_x = MinMaxScaler()

    X = np.vstack([target_data.previous_knob_set, target_data.new_knob_set])
    y = np.vstack([target_data.previous_metric_set, target_data.new_metric_set])

    # Apply one-hot encoding to the categorical variable
    if categorical_indices:
        X_categorical = encoder.fit_transform(X[:, categorical_indices])
        X_numerical = np.delete(X, categorical_indices, axis=1)
        X_final = np.hstack([X_numerical, X_categorical])
    else:
        X_final = X  # No categorical data

    X_scaled = scaler_x.fit_transform(X_final)
    scaler_y = MinMaxScaler()
    y_scaled = scaler_y.fit_transform(y)
    train_x = torch.tensor(X_scaled, dtype=torch.float64)

    # Normalize and weight the metrics
    metric_labels_list = list(target_data.metric_labels)
    train_y = torch.tensor(y_scaled, dtype=torch.float64)

    # Apply less-is-better or greater-is-better transformations
    for i, label in enumerate(metric_labels_list):
        if metric_set[label]['lessisbetter']:
            print(metric_set[label]['lessisbetter'])
            train_y[:, i] = -train_y[:, i]

    # Apply the weights and compute a weighted sum
    weights_tensor = torch.tensor(weights, dtype=torch.float64)
    weighted_train_y = torch.matmul(train_y, weights_tensor).unsqueeze(-1)

    gp_model = SingleTaskGP(train_x, weighted_train_y)
    mll = ExactMarginalLogLikelihood(gp_model.likelihood, gp_model)
    fit_gpytorch_model(mll)

    UCB = UpperConfidenceBound(model=gp_model, beta=3.0)
    bounds = torch.stack([torch.zeros(train_x.shape[1]), torch.ones(train_x.shape[1])])

    candidate, _ = optimize_acqf(
        acq_function=UCB,
        bounds=bounds,
        q=1,  # Number of candidates to return
        num_restarts=10,
        raw_samples=100,
    )
    
    print(candidate)
    new_knob_settings = scaler_x.inverse_transform(candidate.detach().numpy())[0]
    recommended_knobs = {}

    print("new_knob_settings:", new_knob_settings)
    print("target_data.knob_labels:", target_data.knob_labels)
 
    if categorical_indices:
        num_numerical = len(target_data.knob_labels) - len(encoder.categories_)
    else:
        num_numerical = len(target_data.knob_labels)
    for i, label in enumerate(target_data.knob_labels):
        if i in categorical_indices:
            # Extract only the relevant categorical encoding
            start_idx = num_numerical + sum(len(cat) for cat in encoder.categories_[:categorical_indices.index(i)])
            end_idx = start_idx + len(encoder.categories_[categorical_indices.index(i)])
            category_idx = np.argmax(new_knob_settings[start_idx:end_idx])
            recommended_knobs[label] = encoder.categories_[categorical_indices.index(i)][category_idx]
        else:
            raw_value = new_knob_settings[i]
            knob_info = knob_set[label]
            if knob_info['type'] == 'int':
                bounded_value = int(np.clip(raw_value, knob_info['minval'], knob_info['maxval']))
            else:
                bounded_value = raw_value
            recommended_knobs[label] = bounded_value

    print("Recommended knob settings:", recommended_knobs)
    return recommended_knobs

