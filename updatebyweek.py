from sportsipy.nfl.boxscore import Boxscores, Boxscore
from helper import *

last_week = 16
current_week = 17
weeks = list(range(1,current_week + 1))
year = 2023

# Refresh the schedule
df_sched = pd.read_csv(f'schedules/schedule_df_{year}.csv')
df_sched_last_week = get_schedule_for_week(year,last_week)
df_sched = df_sched[df_sched['week']!=last_week]
df_sched = pd.concat([df_sched,df_sched_last_week])
df_sched.to_csv(f'schedules/schedule_df_{year}.csv', index=False)

try:
    df_last_week = pd.read_csv(f'weekly_game_data/weeks_games_df_{last_week}_{year}.csv')
except:
    df_last_week = game_data_for_week(last_week,year)
    df_last_week.to_csv(f'weekly_game_data/weeks_games_df_{last_week}_{year}.csv',index=False)
    df_curr_week = game_data_for_week(current_week,year)
    df_last_week.to_csv(f'weekly_game_data/weeks_games_df_{current_week}_{year}.csv',index=False)

df = pd.read_csv(f'game_data/weeks_games_df_{year}.csv')

# Remove last week from the source
df = df[df['week']!=last_week]

# Refresh (TRUNCATE) last week with result values AND add in current week with blank results
df = pd.concat([df, df_curr_week, df_last_week])
df.to_csv(f'game_data/weeks_games_df_{year}.csv',index=False)

pred_games_df, comp_games_df = prep_test_train(current_week,weeks,year) 

pred_games_df.to_csv(f'datasets/pred_games_df_{current_week}.csv',index=False)
comp_games_df.to_csv(f'datasets/comp_games_df_{current_week}.csv',index=False)
