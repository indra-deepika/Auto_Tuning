# Methodology 

Our methodolgy for tuning database hyperparmeters can be divided into 2 parts 

1. Finding the relevant knobs to tune for a specific workload
2. Tuning these revelant knobs for that workload


## Determing Relevant Tuning Knobs 
We can optimize database performance by identifying the most impactful configuration settings (knobs) for a specific workload. 

#### Random Forest 
Random Forest is an ensemble learning method suitable for both regression and classification tasks. It builds multiple decision trees during training and combines their outcomes by averaging the predictions for regression, or choosing the majority vote for classification.
##### Application in Database Performance Tuning
For our use case, understanding how configuration parameters influence database performance is crucial. Random Forest is especially advantageous for this purpose because it effectively handles complex, non-linear relationships between features, a common characteristic in system performance data.
##### Feature Importance Mechanism
The model identifies which configuration parameters significantly impact performance metrics through its feature importance mechanism. This mechanism ranks each feature based on its contribution to reducing the variance (in regression) or impurity (in classification) of the predicted values.

<!-- Feature importance is determined by measuring the reduction in prediction variance or impurity attributed to each feature across all trees in the forest.
 -->
**Process Overview:**
* Decrease in Impurity: For each split in each tree in the forest that uses a particular feature, the decrease in impurity (for classification) or variance (for regression) is calculated.
* Average Decrease: The decrease in impurity or variance contributed by each feature is averaged across all trees in the forest.
* Normalization: The importance scores for all features are then normalized to sum up to one, allowing for easy comparison of their relative importance.



#### Anova 

ANOVA (Analysis of Variance) is a statistical method used to determine if there are any statistically significant differences between the means of three or more independent groups. It helps identify whether different groups have different effects on a dependent variable.

In this context, the independent variables are the different configuration parameters (knobs) for RocksDB, and the dependent variable is the performance metric (e.g., operations per second).

ANOVA compares the variation within each group to the variation between the groups. If the between-group variation is significantly larger than the within-group variation, it suggests that the parameter values affect the performance.


- F-Statistic: This value indicates the ratio of between-group variance to within-group variance. A higher F-statistic suggests a greater degree of variation between groups relative to within groups.

- P-Value: This value indicates the probability that the observed differences are due to chance. A low p-value (typically less than **0.05**) suggests that the differences are statistically significant.

If ANOVA shows that there are significant differences between the means of groups, it implies that setting certain parameter values has a significant impact on performance. This indicates that tuning these parameters can lead to measurable improvements in performance.


**Determining Tuning Knob :**

<!-- To determine the most influential configuration knobs for optimizing database performance under a certain workload , we collected approximately 1500 samples of performance data under various configuration combination in that workload using db_bench. We applied Random Forest Regression to calculate feature importance, identifying the knobs that significantly impact performance metrics. Additionally, we performed ANOVA to statistically validate the influence of these knobs. Combining the results from both methods, we compiled a list of the most impactful knobs for that workload and passed them to the configuration recommendation algorithm for focused optimization. -->



First, we collect around 1500 samples of performance data,, under various configuration combinations using db_bench, a database benchmarking tool. Then, we use Random Forest Regression to analyze this data to rank the importance of each knob's influence on performance. Finally, we use Analysis of Variance (ANOVA) to statistically validate these rankings.

Combining the results from both methods, we compiled a list of the most impactful knobs for that specific workload and passed them to the configuration recommendation algorithm for focused optimization.


![image](https://hackmd.io/_uploads/ryeyLbxSV0.png)


## Configuration Recommendation
### Overview
We are using Bayesian Optimization to tune hyperparameters for RocksDB to optimize its performance. Bayesian Optimization is effective for hyperparameter tuning, especially when the objective function is expensive to evaluate and does not have a closed form.

### Key Components of Bayesian Optimization

1. **True Objective Function**:
   - The true objective function represents the performance of the database given certain configuration parameters.
   - This function is initially unknown, and we treat the database as a black box. Our goal is to approximate this function through limited evaluations (benchmarking the DB).

2. **Surrogate Model**:
   - A surrogate model approximates the true objective function based on the sampled data points.
   - We use a Gaussian Process Regression (GPR) model as the surrogate model. GPR provides a probabilistic prediction of the function, including mean and uncertainty estimates.

3. **Acquisition Function**:
   - The acquisition function guides the selection of the next set of parameters to evaluate.
   - We use the Upper Confidence Bound (UCB) acquisition function, which balances exploration (sampling areas with high uncertainty) and exploitation (sampling areas with high expected performance).



### Function Distribution Estimation with Gaussian Process Regression:
GPR is applied to model the relationship between configuration values (parameters) and their corresponding performance metrics. This modeling involves estimating the distribution of the function that maps configuration settings to expected performance outcomes. GPR provides two crucial statistical measures for any given set of parameters ```X```:

1. Mean ```m(X)```: Represents the expected outcome
2. Standard Deviation ```s(X)```: Indicates the uncertainty or variability of the outcomes


### Acquisition Function: Upper Confidence Bound (UCB)

The acquisition function determines the next set of parameters to evaluate. The UCB algorithm is defined as:

`U(X) = m(X) + k * s(X)`

Where:
1. **m(X)**: The mean prediction from the GPR model. If  m(X)  is high, it indicates that the estimated performance is high.
2. **s(X)**: The standard deviation from the GPR model. If s(X)  is high, it indicates high uncertainty, suggesting that the area around  X is less explored.
3. **k**: A positive coefficient that adjusts the balance between exploration and exploitation. A higher value of k encourages exploration.

### Procedure

1. **Initialize**:
   - Begin with an initial set of parameter values and their corresponding performance metrics obtained through benchmarking.

2. **Surrogate Model Training**:
   - Train the Gaussian Process Regression model using the initial benchmark data. The model learns the relationship between the parameters and performance metrics.

3. **Acquisition Function Evaluation**:
   - Use the UCB acquisition function to determine the next set of parameters to evaluate. The function combines the mean and uncertainty estimates from the GPR model.

4. **Benchmarking**:
   - Evaluate the performance of the database with the new set of parameters. Collect the performance metrics.

5. **Update**:
   - Add the new data point (parameters and corresponding performance metrics) to the dataset.
   - Retrain the GPR model with the updated dataset.

6. **Iteration**:
   - Repeat steps 3-5 until a stopping criterion is met (e.g., a maximum number of iterations or a satisfactory performance level).

![image](https://hackmd.io/_uploads/r1_uWer4A.png)

<!-- 
### Objective

The goal of this process is to find the set of parameters \( X \) that maximizes the acquisition function \( U(X) \). This ensures a balance between leveraging known high-performing configurations (exploitation) and investigating new, uncertain configurations (exploration). By adjusting the coefficient \( k \), we can control the emphasis on exploration versus exploitation.

### Conclusion

By methodically navigating the parameter space using Bayesian Optimization, we efficiently identify the optimal configuration settings for RocksDB. This approach ensures that we make the best use of available resources and time, ultimately leading to superior database performance.

 -->
## References 

1. Otter Tune : 
2. Auto Tikv : An automatic configuration tuning framework for TiKV using Bayesian Optimization.
3. Improvement of RocksDB Performance via Large-Scale Parameter Analysis and Optimization : methodology for determining revelant knobs was based on this paper


## Future Work

1. Workload Mapping : Mapping present workload with already present / collected data to leverage previous knowledge in configuration recommendation. Would be useful when we have to dynamically determine the workload type.


<!-- 
### Guiding Sampling with an Acquisition Function:

The acquisition function determines the next set of parameters to evaluate. It balances the trade-off between exploiting known areas with high mean outcomes and exploring new areas with high uncertainty.

The **Upper Confidence Bound (UCB)** algorithm is a popular choice for this function. It is
defined as ```U(X) = m(X) + k*s(X)```, where:

1. ```s(X)``` : *Standard Deviation*: if it is large, it means the difference among the data is large, and there is not much data around X. Therefore, the algorithm must explore new points in unknown areas.

2. ```m(X)``` : *Mean* : if it is large, it indicates that the mean value of the estimated Y is large, and the algorithm should find better points using the known data.

3. ```k``` : A positive coefficient that adjusts the balance between exploration and exploitation.A higher value of k leans the algorithm towards exploring less known areas.

### Gaussian Process Regression (GPR)

**Function Distribution Estimation**:
GPR models the relationship between configuration parameters and their corresponding performance metrics. It provides two key statistical measures for any given set of parameters \( X \):

1. **Mean (\( m(X) \))**: Represents the expected performance outcome for the given parameters.
2. **Standard Deviation (\( s(X) \))**: Represents the uncertainty or variability of the performance outcome for the given parameters.

### Acquisition Function: Upper Confidence Bound (UCB)

The acquisition function determines the next set of parameters to evaluate. The UCB algorithm is defined as:

``` U(X) = m(X) + k.s(X) ```

Where:
1. ```m(X)```: The mean prediction from the GPR model. If ```m(X)``` is high, it indicates that the estimated performance is high.

3. **\( s(X) \)**: The standard deviation from the GPR model. If \( s(X) \) is high, it indicates high uncertainty, suggesting that the area around \( X \) is less explored.
4. **\( k \)**: A positive coefficient that adjusts the balance between exploration and exploitation. A higher value of \( k \) encourages exploration.

The goal is to find the set of parameters ```X```  that maximizes the acquisition function ```U(X)```, indicating either a high expected outcome or significant uncertainty warranting exploration. The one with the largest ```U(X)``` value is identified as the recommendation result.


This approach methodically navigates the parameter space, ensuring an equilibrium between leveraging well-understood configurations and venturing into unexplored territories for potentially superior outcomes. By modulating the coefficient k, one can fine-tune the emphasis on exploitation versus exploration
 -->
