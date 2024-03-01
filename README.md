# nfl-predictor
Predict winners of NFL games

## Sources

1. Elo data:
https://github.com/fivethirtyeight/data/tree/master/nfl-elo

1. Sports Reference Bot - Data Usage info:
https://www.sports-reference.com/data_use.html

1. Gitlab NB reference:
https://gitlab.com/mcmillenkel/nfl_predicting_game_outcomes/-/blob/master/NFL_game_prediction.ipynb

## Summary
I used the resources listed above and adjusted what I needed to to fit my use-case. I relied heavily on the notebook found in the Gitlab link I posted but I adjusted the way some of the functions work and made them a bit more efficient. 

I utilized the combination of helper.py and updatebyweek.py to "hack" together an ML pipeline. 
### updateweek.py
1. Updates the current NFL schedule we have on file
1. Gathers fresh data from last weeks games and new data for the current week
1. Combines the year's worth of data with last week and current week
1. Uses the dataset generated above to deliver train and test dataframes

### helper.py
This helper's main function is `prep_test_train()`. It calls other functions within the file to retrieve Box Scores and game data for each game. I adjusted the original code found in the Gitlab link to make sure I wasn't hitting API limits and that I was accounting for games that haven't started (want to include these to predict future outcomes). I also made added some functions to easily run a "mock" ML pipeline easier in `updateweek.py`:
- get_schedule_for_week() makes it easy to add on the weeks schedule to existing year schedule instead of fetching entire year every time
- game_data_up_to_week() allows us to grab last week's updated data (now scores are present after game finishes) and grab next week's data and refresh and append to our existing Weekly Data, respectively. This avoids us needing to retrieve the entire year's worth of game data every time. 

### nfl.ipynb
This notebook is where I would manually read in the train file, `comp_games_df_{current_week}.csv`, and test file, `pred_games_df_{current_week}.csv`. After reading in the files, I run a train_test_split() on the training data to train and test our models. I make sure to train on more 2022 data than test as the model needs to be better trained towards recent data. The 2023 training data is split at 50%. After training and testing and confirming we will get valid results, I pass in our test data, `pred_games_df_{current_week}.csv` to receive predictions.

#### Models
First you will find a Logistic Regression Model and an XGBoost Classifier Model. Second, I include a Grid Search using an XGBoost Model using `roc_auc` as the scoring method with cross-validation set to 5. Third, you will see an ensemble model using XGBoost and Logistic Regression in which case I am taking the average prediction from the two models.

#### Evaluation
For each model you will see their respective evaluation metrics like Accuracy, AUC, and for XGBoost I include feature importance.

### Predictions
The predictions are displayed in the format:
"The *Away Team* has a probability of *X* of beating the *Home Team*"

## Model History
All models are saved in the model_history folder. The AUC and accuracy reported after training are recorded in the model_history/models.csv file.

## Conclusion & Next Steps
Overall, the models didn't perform very well. They came out to about 60%-65% accuracy every week. Here are some notes on the data that could've been adjusted for better model performance
1. The elo data isnt perfect. It's grabbing elo information from the year prior which isn't always accurate. For example, the elo file is using Derek Carr's QB stats for the Raiders even though their QB for the 2023 season was Jimmy Garoppolo. 
1. Feature selection process can be better. I was more concerned about building this out end-to-end for my first go at this, so I was just happy to get results from the models -- I never had enough time to fine-tune them and/or go through proper feature selection.
1. Injuries. I didn't account for injuries or if certain players were traded/out which could effect certain outcomes.

Based on the points from above, I'd love to find proper elo data for next season and possibly look into other types of models like Neural Networks or Time Series. I'd also like to find more granular data on the players to assure I'm joining in info on ACTIVE players for each game rather than just relying on the somewhat-accurate elo data.