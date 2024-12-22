# NBA-Game-Predictor


- **Architecture**

    The architecture of my naive bayes classifier is based around my "stats" class. Any instance of "stats" has a Pandas data frame called dataBase, a list of categories of data that the instance of the class will use, a dictionary of the means of each continuous category, and a dictionary of the standard deviations of each continuous category.

    In my code, I create an instance of the stats class for the rows of the table where the home team wins, label = 1, and a separate instance for the rows of the table where the home team loses, label = 0. Thus the home team winning instance has a database of only rows of data where the home team wins, and the opposite for the lose instance.

    The driving function in the "stats" class is calcProb that takes an array of input data and returns the probability of that data existing in the current instance of dataBase. For each value in the input array, either discreteProb and statProb is called, depending on the label given to each category in the categories list of each "stats" instance. Categories that are discrete are labeled 0, continuous 1, and categories that should be ignored are labeled -1. 

    In statProb, a value and a category are passed in, and the probability of that value existing in the given category of the dataBase is returned. statProb is used only for continuous variables, so the probability of each input value occurring cannot be calculated by simply counting the occurrences of that value in the dataset. Instead the probability of the input value must be calculated using normal statistics. Initially, I check if the mean and standard deviation for the observed category is stored in my mean and standard deviation dictionaries, and if not I calculate them. Using the mean and standard deviation I calculate the probability of the input value occurring in the given category, and return that value.

    For discreteProb, the process is much faster as I simply count the number of occurrences of the input value, and divide by the total number of entries in the database for the instance of the stats class.

    Further, I have a dataRead function that takes in no parameters, and returns two "stats" objects; one for the winning data, and one for the losing data. Inside of this function, train_data.csv is read into a single Pandas data frame. Then, this original data frame is split into two sub sets, one for entries of label 1, and another for entries of label 0. These data frames are then passed to the "stats" constructor to create the stats objects that are then returned.

- **Preprocessing**

    As mentioned before, I split the data set into different categories; games where the home team won, and games where the home team lost. Each set of rows is sent to a separate instance of the "stats" class, and thus each instance of the class has a different data base.

    I did not adjust any columns of the data in my final product. I attempted to convert the win loss last five data column into instead a count of the number of wins in the last five games. However, this approach was unsuccessful as it did not help accuracy and I ultimately ended up leaving both home and away last five game records out of my final model.

    Otherwise, I left all of the other data as it was given in the provided csv files.

- **Model Building**

    When a row of input data is sent to the model to be judged, my model computes the probability of each data point occurring at runtime. However, to save some time, the mean and standard deviation for each category of data is computed only once, and then saved in a dictionary for later retrieval.

    The model utilizes the following laws of probability to compute the likelihood of winning and losing.

    $P(W| A, B, C, ... , Z) = \frac{P(W, A, B, C, ..., Z)}{P(A,B,C,...Z)}$

    $= \frac{P(A,B,C, ... Z | W)P(W)}{P(A,B,C,...Z)}$

    Because A,B,C, ...Z are given to be conditionally independent given W by the structure of a naive bayes classifier:

    $= \frac{P(A|W)P(B|W)P(C|W)...P(Z|W)P(W)}{P(A,B,C,...Z)}$

    The same can be done for losing data:

    $P(L| A, B, C, ... Z)= \frac{P(A|L)P(B|L)P(C|L)...P(Z|L)P(L)}{P(A,B,C,...Z)}$

    Once both the probability of winning given the evidence, and the probability of losing given the evidence are both calculated, you can compare the two values and the higher value indicates the more likely event and the choice by the classifier. As the term $P(A,B,C,...Z)$ is in the denominator of both formulas, this probability can be omitted from both calculations.

    Thus, the only things to be calculated are of the form P(Outcome given Category of Evidence). Thus, only the probabilities of a win or loss given a single piece of evidence are needed. To implement this, I first split the data based on wins and losses so that when any probabilities are calculated for categories of evidence, it will only be done given wins, or given losses. Thus in the "stats" instance for winning, all statistics gathered will be given a win, and the same for the losses instance of the class. 

    Given the assumption that all evidence is conditionally independent given the outcome of the game for the home team, calculating $P(A=a|W)$ can be done by simply finding the probability of $a$ existing in the database for winning. If the probability $P(A=a|W)$ is 0, then I simply set $P(A=a|W) = \frac{1}{100000}$ to prevent the total probability from going to 0.

    The last product $P(W)$, can be found by finding the proportion of rows in the table where the home team wins.

    Finally, all of these values can be multiplied to determine the likelihood of the winning team winning or losing.
