import pandas as pd
import numpy as np
from sportsipy.nfl.boxscore import Boxscores, Boxscore
import requests 
import time

def get_schedule(year):
    weeks = list(range(1,18))
    schedule_df = pd.DataFrame()
    for w in range(len(weeks)):
        date_string = str(weeks[w]) + '-' + str(year)
        try:
            print(f"Retrieving schedule for Week {weeks[w]} - {year}")
            time.sleep(15)
            week_scores = Boxscores(weeks[w],year)   
        except:
            return 'Failed to retrieve schedule.'     
        week_games_df = pd.DataFrame()
        for g in range(len(week_scores.games[date_string])):
            game = pd.DataFrame(week_scores.games[date_string][g], index = [0])[['away_name', 'away_abbr','home_name', 'home_abbr','winning_name', 'winning_abbr' ]]
            game['week'] = weeks[w]
            week_games_df = pd.concat([week_games_df,game])
        schedule_df = pd.concat([schedule_df, week_games_df]).reset_index().drop(columns = 'index')
    return schedule_df

def get_schedule_for_week(year, week):
    # weeks = list(range(1,18))
    schedule_df = pd.DataFrame()
    # for w in range(len(weeks)):
    date_string = str(week) + '-' + str(year)
    try:
        print(f"Retrieving schedule for Week {week} - {year}")
        time.sleep(15)
        week_scores = Boxscores(week,year)   
    except:
        return 'Failed to retrieve schedule.'     
    week_games_df = pd.DataFrame()
    for g in range(len(week_scores.games[date_string])):
        game = pd.DataFrame(week_scores.games[date_string][g], index = [0])[['away_name', 'away_abbr','home_name', 'home_abbr','winning_name', 'winning_abbr' ]]
        game['week'] = week
        week_games_df = pd.concat([week_games_df,game])
    schedule_df = pd.concat([schedule_df, week_games_df]).reset_index().drop(columns = 'index')
    return schedule_df

def createBlankGameStats():
    # df = pd.DataFrame(columns=['away_first_downs', 'away_fourth_down_attempts',
    #         'away_fourth_down_conversions', 'away_fumbles', 'away_fumbles_lost',
    #         'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts',
    #         'away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards',
    #         'away_penalties', 'away_points', 'away_rush_attempts',
    #         'away_rush_touchdowns', 'away_rush_yards', 'away_third_down_attempts',
    #         'away_third_down_conversions', 'away_time_of_possession',
    #         'away_times_sacked', 'away_total_yards', 'away_turnovers',
    #         'away_yards_from_penalties', 'away_yards_lost_from_sacks', 
    #         'home_first_downs', 'home_fourth_down_attempts',
    #         'home_fourth_down_conversions', 'home_fumbles', 'home_fumbles_lost',
    #         'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts',
    #         'home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards',
    #         'home_penalties', 'home_points', 'home_rush_attempts',
    #         'home_rush_touchdowns', 'home_rush_yards', 'home_third_down_attempts',
    #         'home_third_down_conversions', 'home_time_of_possession',
    #         'home_times_sacked', 'home_total_yards', 'home_turnovers',
    #         'home_yards_from_penalties', 'home_yards_lost_from_sacks'])
    df = pd.DataFrame(columns= ['attendance', 'away_first_downs', 'away_fourth_down_attempts',
                    'away_fourth_down_conversions', 'away_fumbles', 'away_fumbles_lost',
                    'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts',
                    'away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards',
                    'away_penalties', 'away_points', 'away_rush_attempts',
                    'away_rush_touchdowns', 'away_rush_yards', 'away_third_down_attempts',
                    'away_third_down_conversions', 'away_time_of_possession',
                    'away_times_sacked', 'away_total_yards', 'away_turnovers',
                    'away_yards_from_penalties', 'away_yards_lost_from_sacks', 'date',
                    'datetime', 'duration', 'home_first_downs', 'home_fourth_down_attempts',
                    'home_fourth_down_conversions', 'home_fumbles', 'home_fumbles_lost',
                    'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts',
                    'home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards',
                    'home_penalties', 'home_points', 'home_rush_attempts',
                    'home_rush_touchdowns', 'home_rush_yards', 'home_third_down_attempts',
                    'home_third_down_conversions', 'home_time_of_possession',
                    'home_times_sacked', 'home_total_yards', 'home_turnovers',
                    'home_yards_from_penalties', 'home_yards_lost_from_sacks',
                    'losing_abbr', 'losing_name', 'over_under', 'roof', 'stadium',
                    'surface', 'time', 'vegas_line', 'weather', 'winner', 'winning_abbr',
                    'winning_name', 'won_toss'])
    return df

# Update to actually pass in a game_stats dataframe instead of a Boxscore obj
def game_data(game_df,game_stats):
    try:
        away_team_df = game_df[['away_name', 'away_abbr', 'away_score']].rename(columns = {'away_name': 'team_name', 'away_abbr': 'team_abbr', 'away_score': 'score'})
        home_team_df = game_df[['home_name','home_abbr', 'home_score']].rename(columns = {'home_name': 'team_name', 'home_abbr': 'team_abbr', 'home_score': 'score'})
        try:
            if game_df.loc[0,'away_score'] > game_df.loc[0,'home_score']:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [1], 'game_lost' : [0]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [1]}),left_index = True, right_index = True)
            elif game_df.loc[0,'away_score'] < game_df.loc[0,'home_score']:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [1]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [1], 'game_lost' : [0]}),left_index = True, right_index = True)
            else: 
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [0]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [0]}),left_index = True, right_index = True)
        except TypeError:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [np.nan], 'game_lost' : [np.nan]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [np.nan], 'game_lost' : [np.nan]}),left_index = True, right_index = True)        
        # try:
        #     away_stats_df = game_stats.dataframe[['away_first_downs', 'away_fourth_down_attempts',
        #         'away_fourth_down_conversions', 'away_fumbles', 'away_fumbles_lost',
        #         'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts',
        #         'away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards',
        #         'away_penalties', 'away_points', 'away_rush_attempts',
        #         'away_rush_touchdowns', 'away_rush_yards', 'away_third_down_attempts',
        #         'away_third_down_conversions', 'away_time_of_possession',
        #         'away_times_sacked', 'away_total_yards', 'away_turnovers',
        #         'away_yards_from_penalties', 'away_yards_lost_from_sacks']].reset_index().drop(columns ='index').rename(columns = {
        #         'away_first_downs': 'first_downs', 'away_fourth_down_attempts':'fourth_down_attempts',
        #         'away_fourth_down_conversions':'fourth_down_conversions' , 'away_fumbles': 'fumbles', 'away_fumbles_lost': 'fumbles_lost',
        #         'away_interceptions': 'interceptions', 'away_net_pass_yards':'net_pass_yards' , 'away_pass_attempts': 'pass_attempts',
        #         'away_pass_completions':'pass_completions' , 'away_pass_touchdowns': 'pass_touchdowns', 'away_pass_yards': 'pass_yards',
        #         'away_penalties': 'penalties', 'away_points': 'points', 'away_rush_attempts': 'rush_attempts',
        #         'away_rush_touchdowns': 'rush_touchdowns', 'away_rush_yards': 'rush_yards', 'away_third_down_attempts': 'third_down_attempts',
        #         'away_third_down_conversions': 'third_down_conversions', 'away_time_of_possession': 'time_of_possession',
        #         'away_times_sacked': 'times_sacked', 'away_total_yards': 'total_yards', 'away_turnovers': 'turnovers',
        #         'away_yards_from_penalties':'yards_from_penalties', 'away_yards_lost_from_sacks': 'yards_lost_from_sacks'})
        #     home_stats_df = game_stats.dataframe[['home_first_downs', 'home_fourth_down_attempts',
        #             'home_fourth_down_conversions', 'home_fumbles', 'home_fumbles_lost',
        #             'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts',
        #             'home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards',
        #             'home_penalties', 'home_points', 'home_rush_attempts',
        #             'home_rush_touchdowns', 'home_rush_yards', 'home_third_down_attempts',
        #             'home_third_down_conversions', 'home_time_of_possession',
        #             'home_times_sacked', 'home_total_yards', 'home_turnovers',
        #             'home_yards_from_penalties', 'home_yards_lost_from_sacks']].reset_index().drop(columns = 'index').rename(columns = {
        #             'home_first_downs': 'first_downs', 'home_fourth_down_attempts':'fourth_down_attempts',
        #             'home_fourth_down_conversions':'fourth_down_conversions' , 'home_fumbles': 'fumbles', 'home_fumbles_lost': 'fumbles_lost',
        #             'home_interceptions': 'interceptions', 'home_net_pass_yards':'net_pass_yards' , 'home_pass_attempts': 'pass_attempts',
        #             'home_pass_completions':'pass_completions' , 'home_pass_touchdowns': 'pass_touchdowns', 'home_pass_yards': 'pass_yards',
        #             'home_penalties': 'penalties', 'home_points': 'points', 'home_rush_attempts': 'rush_attempts',
        #             'home_rush_touchdowns': 'rush_touchdowns', 'home_rush_yards': 'rush_yards', 'home_third_down_attempts': 'third_down_attempts',
        #             'home_third_down_conversions': 'third_down_conversions', 'home_time_of_possession': 'time_of_possession',
        #             'home_times_sacked': 'times_sacked', 'home_total_yards': 'total_yards', 'home_turnovers': 'turnovers',
        #             'home_yards_from_penalties':'yards_from_penalties', 'home_yards_lost_from_sacks': 'yards_lost_from_sacks'})
        # except:
        away_stats_df = game_stats[['away_first_downs', 'away_fourth_down_attempts',
                'away_fourth_down_conversions', 'away_fumbles', 'away_fumbles_lost',
                'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts',
                'away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards',
                'away_penalties', 'away_points', 'away_rush_attempts',
                'away_rush_touchdowns', 'away_rush_yards', 'away_third_down_attempts',
                'away_third_down_conversions', 'away_time_of_possession',
                'away_times_sacked', 'away_total_yards', 'away_turnovers',
                'away_yards_from_penalties', 'away_yards_lost_from_sacks']].reset_index().drop(columns ='index').rename(columns = {
                'away_first_downs': 'first_downs', 'away_fourth_down_attempts':'fourth_down_attempts',
                'away_fourth_down_conversions':'fourth_down_conversions' , 'away_fumbles': 'fumbles', 'away_fumbles_lost': 'fumbles_lost',
                'away_interceptions': 'interceptions', 'away_net_pass_yards':'net_pass_yards' , 'away_pass_attempts': 'pass_attempts',
                'away_pass_completions':'pass_completions' , 'away_pass_touchdowns': 'pass_touchdowns', 'away_pass_yards': 'pass_yards',
                'away_penalties': 'penalties', 'away_points': 'points', 'away_rush_attempts': 'rush_attempts',
                'away_rush_touchdowns': 'rush_touchdowns', 'away_rush_yards': 'rush_yards', 'away_third_down_attempts': 'third_down_attempts',
                'away_third_down_conversions': 'third_down_conversions', 'away_time_of_possession': 'time_of_possession',
                'away_times_sacked': 'times_sacked', 'away_total_yards': 'total_yards', 'away_turnovers': 'turnovers',
                'away_yards_from_penalties':'yards_from_penalties', 'away_yards_lost_from_sacks': 'yards_lost_from_sacks'})
        home_stats_df = game_stats[['home_first_downs', 'home_fourth_down_attempts',
                'home_fourth_down_conversions', 'home_fumbles', 'home_fumbles_lost',
                'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts',
                'home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards',
                'home_penalties', 'home_points', 'home_rush_attempts',
                'home_rush_touchdowns', 'home_rush_yards', 'home_third_down_attempts',
                'home_third_down_conversions', 'home_time_of_possession',
                'home_times_sacked', 'home_total_yards', 'home_turnovers',
                'home_yards_from_penalties', 'home_yards_lost_from_sacks']].reset_index().drop(columns = 'index').rename(columns = {
                'home_first_downs': 'first_downs', 'home_fourth_down_attempts':'fourth_down_attempts',
                'home_fourth_down_conversions':'fourth_down_conversions' , 'home_fumbles': 'fumbles', 'home_fumbles_lost': 'fumbles_lost',
                'home_interceptions': 'interceptions', 'home_net_pass_yards':'net_pass_yards' , 'home_pass_attempts': 'pass_attempts',
                'home_pass_completions':'pass_completions' , 'home_pass_touchdowns': 'pass_touchdowns', 'home_pass_yards': 'pass_yards',
                'home_penalties': 'penalties', 'home_points': 'points', 'home_rush_attempts': 'rush_attempts',
                'home_rush_touchdowns': 'rush_touchdowns', 'home_rush_yards': 'rush_yards', 'home_third_down_attempts': 'third_down_attempts',
                'home_third_down_conversions': 'third_down_conversions', 'home_time_of_possession': 'time_of_possession',
                'home_times_sacked': 'times_sacked', 'home_total_yards': 'total_yards', 'home_turnovers': 'turnovers',
                'home_yards_from_penalties':'yards_from_penalties', 'home_yards_lost_from_sacks': 'yards_lost_from_sacks'})
        away_team_df = pd.merge(away_team_df, away_stats_df,left_index = True, right_index = True)
        home_team_df = pd.merge(home_team_df, home_stats_df,left_index = True, right_index = True)
        try:
            away_team_df['time_of_possession'] = (int(away_team_df['time_of_possession'].loc[0][0:2]) * 60) + int(away_team_df['time_of_possession'].loc[0][3:5])
            home_team_df['time_of_possession'] = (int(home_team_df['time_of_possession'].loc[0][0:2]) * 60) + int(home_team_df['time_of_possession'].loc[0][3:5])
        except:
            away_team_df['time_of_possession'] = np.nan
            home_team_df['time_of_possession'] = np.nan
    except:
        print("ERROR")
        away_team_df = pd.DataFrame()
        home_team_df = pd.DataFrame()
    return away_team_df, home_team_df

def game_data_up_to_week(weeks,year):
    weeks_games_df = pd.DataFrame()
    for w in range(len(weeks)):
        date_string = str(weeks[w]) + '-' + str(year)        
        # week_scores = Boxscores(weeks[w],year)
        try:
            print(f"Retrieving scores for Week {weeks[w]} - {year}")
            time.sleep(15)
            week_scores = Boxscores(weeks[w],year)   
        except:
            return 'Failed to retrieve schedule.'       
        week_games_df = pd.DataFrame()         
        for g in range(len(week_scores.games[date_string])):             
            game_str = week_scores.games[date_string][g]['boxscore']             
            # game_stats = Boxscore(game_str)
            try:
                print(f"Retrieving boxscore for {game_str} Week {weeks[w]} - {year}")
                time.sleep(15)
                game_stats = Boxscore(game_str)
            except:
                return 'Failed to retrieve schedule.'         
            game_df = pd.DataFrame(week_scores.games[date_string][g], index = [0])             
            away_team_df, home_team_df = game_data(game_df,game_stats)  
                       
            away_team_df['week'] = weeks[w]
            home_team_df['week'] = weeks[w]
            week_games_df = pd.concat([week_games_df,away_team_df])             
            week_games_df = pd.concat([week_games_df,home_team_df])         
            weeks_games_df = pd.concat([weeks_games_df,week_games_df])     
    # print(weeks_games_df)
    return weeks_games_df

#TODO: figure out if we just need to wait for Boxscore() to populate?
def game_data_for_week(week,year):
    # weeks_games_df = pd.DataFrame()    
    date_string = str(week) + '-' + str(year)        
    # week_scores = Boxscores(weeks[w],year)
    try:
        print(f"Retrieving boxscores for Week {week} - {year}")
        time.sleep(15)
        week_scores = Boxscores(week,year)   
    except:
        return 'Failed to retrieve schedule.'       
    week_games_df = pd.DataFrame()    
    for g in range(len(week_scores.games[date_string])):             
        game_str = week_scores.games[date_string][g]['boxscore']             
        # game_stats = Boxscore(game_str)
        try:
            print(f"Retrieving boxscore for {game_str} Week {week} - {year}")
            time.sleep(15)
            game_stats = Boxscore(game_str)
        except:
            # return 'Failed to retrieve schedule.'         
            print('Game has not started or failed to retrieve.')
        game_df = pd.DataFrame(week_scores.games[date_string][g], index = [0])
        try:
            away_team_df, home_team_df = game_data(game_df,game_stats.dataframe)  
        except:
            print('Using blank game_stats')
            # game_stats = pd.DataFrame(columns=)
            game_stats = createBlankGameStats()
            away_team_df, home_team_df = game_data(game_df,game_stats)  
        away_team_df['week'] = week
        home_team_df['week'] = week
        week_games_df = pd.concat([week_games_df,away_team_df])             
        week_games_df = pd.concat([week_games_df,home_team_df])         
        # weeks_games_df = pd.concat([weeks_games_df,week_games_df])     
    return week_games_df

def agg_weekly_data(schedule_df,weeks_games_df,current_week,weeks):
    schedule_df = schedule_df[schedule_df['week'] < current_week]
    agg_games_df = pd.DataFrame()
    for w in range(1,len(weeks)):
        print(f'Cleaning up agg data for week {w}')
        games_df = schedule_df[schedule_df['week'] == weeks[w]]
        # if weeks[w]!=1:
        agg_weekly_df = weeks_games_df[weeks_games_df['week'] < weeks[w]].drop(columns = ['score','week','game_won', 'game_lost']).groupby(by=['team_name', 'team_abbr']).mean().reset_index()
        win_loss_df = weeks_games_df[weeks_games_df['week'] < weeks[w]][['team_name', 'team_abbr','game_won', 'game_lost']].groupby(by=['team_name', 'team_abbr']).sum().reset_index()
        # else:
            # agg_weekly_df = weeks_games_df[weeks_games_df['week'] <= weeks[w]].drop(columns = ['score','week','game_won', 'game_lost']).groupby(by=['team_name', 'team_abbr']).mean().reset_index()
            # win_loss_df = weeks_games_df[weeks_games_df['week'] <= weeks[w]][['team_name', 'team_abbr','game_won', 'game_lost']].groupby(by=['team_name', 'team_abbr']).sum().reset_index()
        win_loss_df['win_perc'] = win_loss_df['game_won'] / (win_loss_df['game_won'] + win_loss_df['game_lost'])         
        win_loss_df = win_loss_df.drop(columns = ['game_won', 'game_lost'])         
        try:             
            agg_weekly_df['fourth_down_perc'] = agg_weekly_df['fourth_down_conversions'] / agg_weekly_df['fourth_down_attempts']          
        except ZeroDivisionError:             
            agg_weekly_df['fourth_down_perc'] = 0         
            agg_weekly_df['fourth_down_perc'] = agg_weekly_df['fourth_down_perc'].fillna(0)         
        try:             
            agg_weekly_df['third_down_perc'] = agg_weekly_df['third_down_conversions'] / agg_weekly_df['third_down_attempts']          
        except ZeroDivisionError:             
            agg_weekly_df['third_down_perc'] = 0         
            agg_weekly_df['third_down_perc'] = agg_weekly_df['third_down_perc'].fillna(0)          
        agg_weekly_df = agg_weekly_df.drop(columns = ['fourth_down_attempts', 'fourth_down_conversions', 'third_down_attempts', 'third_down_conversions'])         
        agg_weekly_df = pd.merge(win_loss_df,agg_weekly_df,left_on = ['team_name', 'team_abbr'], right_on = ['team_name', 'team_abbr'])         
        away_df = pd.merge(games_df,agg_weekly_df,how = 'inner', left_on = ['away_name', 'away_abbr'], right_on = ['team_name', 'team_abbr']).drop(columns = ['team_name', 'team_abbr']).rename(columns = {'win_perc': 'away_win_perc', 'first_downs': 'away_first_downs', 'fumbles': 'away_fumbles', 'fumbles_lost':'away_fumbles_lost', 'interceptions':'away_interceptions', 'net_pass_yards': 'away_net_pass_yards', 'pass_attempts':'away_pass_attempts', 'pass_completions':'away_pass_completions', 'pass_touchdowns':'away_pass_touchdowns', 'pass_yards':'away_pass_yards', 'penalties':'away_penalties', 'points':'away_points', 'rush_attempts':'away_rush_attempts', 'rush_touchdowns':'away_rush_touchdowns', 'rush_yards':'away_rush_yards', 'time_of_possession':'away_time_of_possession', 'times_sacked':'away_times_sacked', 'total_yards':'away_total_yards', 'turnovers':'away_turnovers', 'yards_from_penalties':'away_yards_from_penalties', 'yards_lost_from_sacks': 'away_yards_lost_from_sacks', 'fourth_down_perc':'away_fourth_down_perc', 'third_down_perc':'away_third_down_perc'})         
        home_df = pd.merge(games_df,agg_weekly_df,how = 'inner', left_on = ['home_name', 'home_abbr'], right_on = ['team_name', 'team_abbr']).drop(columns = ['team_name', 'team_abbr']).rename(columns = {   'win_perc': 'home_win_perc', 'first_downs': 'home_first_downs', 'fumbles': 'home_fumbles', 'fumbles_lost':'home_fumbles_lost', 'interceptions':'home_interceptions', 'net_pass_yards': 'home_net_pass_yards', 'pass_attempts':'home_pass_attempts', 'pass_completions':'home_pass_completions', 'pass_touchdowns':'home_pass_touchdowns', 'pass_yards':'home_pass_yards', 'penalties':'home_penalties', 'points':'home_points', 'rush_attempts':'home_rush_attempts', 'rush_touchdowns':'home_rush_touchdowns', 'rush_yards':'home_rush_yards', 'time_of_possession':'home_time_of_possession', 'times_sacked':'home_times_sacked', 'total_yards':'home_total_yards', 'turnovers':'home_turnovers', 'yards_from_penalties':'home_yards_from_penalties', 'yards_lost_from_sacks': 'home_yards_lost_from_sacks', 'fourth_down_perc':'home_fourth_down_perc', 'third_down_perc':'home_third_down_perc'})         
        agg_weekly_df = pd.merge(away_df,home_df,left_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name', 'winning_abbr', 'week'], right_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name', 'winning_abbr', 'week'])         
        agg_weekly_df['win_perc_dif'] = agg_weekly_df['away_win_perc'] -  agg_weekly_df['home_win_perc']         
        agg_weekly_df['first_downs_dif'] = agg_weekly_df['away_first_downs'] -  agg_weekly_df['home_first_downs']         
        agg_weekly_df['fumbles_dif'] = agg_weekly_df['away_fumbles'] -  agg_weekly_df['home_fumbles']         
        agg_weekly_df['interceptions_dif'] = agg_weekly_df['away_interceptions'] -  agg_weekly_df['home_interceptions']         
        agg_weekly_df['net_pass_yards_dif'] = agg_weekly_df['away_net_pass_yards'] -  agg_weekly_df['home_net_pass_yards']         
        agg_weekly_df['pass_attempts_dif'] = agg_weekly_df['away_pass_attempts'] -  agg_weekly_df['home_pass_attempts']         
        agg_weekly_df['pass_completions_dif'] = agg_weekly_df['away_pass_completions'] -  agg_weekly_df['home_pass_completions']         
        agg_weekly_df['pass_touchdowns_dif'] = agg_weekly_df['away_pass_touchdowns'] -  agg_weekly_df['home_pass_touchdowns']         
        agg_weekly_df['pass_yards_dif'] = agg_weekly_df['away_pass_yards'] -  agg_weekly_df['home_pass_yards']         
        agg_weekly_df['penalties_dif'] = agg_weekly_df['away_penalties'] -  agg_weekly_df['home_penalties']         
        agg_weekly_df['points_dif'] = agg_weekly_df['away_points'] -  agg_weekly_df['home_points']         
        agg_weekly_df['rush_attempts_dif'] = agg_weekly_df['away_rush_attempts'] -  agg_weekly_df['home_rush_attempts']         
        agg_weekly_df['rush_touchdowns_dif'] = agg_weekly_df['away_rush_touchdowns'] -  agg_weekly_df['home_rush_touchdowns']         
        agg_weekly_df['rush_yards_dif'] = agg_weekly_df['away_rush_yards'] -  agg_weekly_df['home_rush_yards']         
        agg_weekly_df['time_of_possession_dif'] = agg_weekly_df['away_time_of_possession'] -  agg_weekly_df['home_time_of_possession']         
        agg_weekly_df['times_sacked_dif'] = agg_weekly_df['away_times_sacked'] -  agg_weekly_df['home_times_sacked']         
        agg_weekly_df['total_yards_dif'] = agg_weekly_df['away_total_yards'] -  agg_weekly_df['home_total_yards']         
        agg_weekly_df['turnovers_dif'] = agg_weekly_df['away_turnovers'] -  agg_weekly_df['home_turnovers']         
        agg_weekly_df['yards_from_penalties_dif'] = agg_weekly_df['away_yards_from_penalties'] -  agg_weekly_df['home_yards_from_penalties']         
        agg_weekly_df['yards_lost_from_sacks_dif'] = agg_weekly_df['away_yards_lost_from_sacks'] -  agg_weekly_df['home_yards_lost_from_sacks']         
        agg_weekly_df['fourth_down_perc_dif'] = agg_weekly_df['away_fourth_down_perc'] -  agg_weekly_df['home_fourth_down_perc']         
        agg_weekly_df['third_down_perc_dif'] = agg_weekly_df['away_third_down_perc'] -  agg_weekly_df['home_third_down_perc']         
        agg_weekly_df = agg_weekly_df.drop(columns = ['away_win_perc', 'away_first_downs', 'away_fumbles', 'away_fumbles_lost', 'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts','away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards', 'away_penalties', 'away_points', 'away_rush_attempts', 'away_rush_touchdowns', 'away_rush_yards', 'away_time_of_possession', 'away_times_sacked', 'away_total_yards', 'away_turnovers', 'away_yards_from_penalties', 'away_yards_lost_from_sacks','away_fourth_down_perc', 'away_third_down_perc','home_win_perc', 'home_first_downs', 'home_fumbles', 'home_fumbles_lost', 'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts','home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards', 'home_penalties', 'home_points', 'home_rush_attempts', 'home_rush_touchdowns', 'home_rush_yards', 'home_time_of_possession', 'home_times_sacked', 'home_total_yards', 'home_turnovers', 'home_yards_from_penalties', 'home_yards_lost_from_sacks','home_fourth_down_perc', 'home_third_down_perc'])   
        if (agg_weekly_df['winning_name'].isnull().values.any()): #and weeks[w]> 3):             
            agg_weekly_df['result'] = np.nan             
            print(f'Week {weeks[w]} games have not finished yet.')
            print(agg_weekly_df.shape)
        else:             
            agg_weekly_df['result'] = agg_weekly_df['winning_name'] == agg_weekly_df['away_name']             
            agg_weekly_df['result'] = agg_weekly_df['result'].astype('float')         
        agg_weekly_df = agg_weekly_df.drop(columns = ['winning_name', 'winning_abbr'])         
        agg_games_df = pd.concat([agg_games_df, agg_weekly_df])     
    agg_games_df = agg_games_df.reset_index().drop(columns = 'index')     
    # agg_games_df = agg_games_df.drop(index = 20, axis=0)
        # print('here2')
        # if weeks[w]==1:
        #     print('here')
        #     print(agg_games_df)     
    return agg_games_df 

def get_elo():
    elo_df = pd.read_csv('nfl_elo_latest.csv')
    elo_df = elo_df.drop(columns = ['season','neutral' ,'playoff', 'elo_prob1', 'elo_prob2', 'elo1_post', 'elo2_post',
           'qbelo1_pre', 'qbelo2_pre', 'qb1', 'qb2', 'qb1_adj', 'qb2_adj', 'qbelo_prob1', 'qbelo_prob2',
           'qb1_game_value', 'qb2_game_value', 'qb1_value_post', 'qb2_value_post',
           'qbelo1_post', 'qbelo2_post', 'score1', 'score2'])
    elo_df.date = pd.to_datetime(elo_df.date)
    # elo_df = elo_df[elo_df.date < '01-05-2021']
    elo_df['team1'] = elo_df['team1'].replace(['KC', 'JAX', 'CAR', 'BAL', 'BUF', 'MIN', 'DET', 'ATL', 'NE', 'WSH',
           'CIN', 'NO', 'SF', 'LAR', 'NYG', 'DEN', 'CLE', 'IND', 'TEN', 'NYJ',
           'TB', 'MIA', 'PIT', 'PHI', 'GB', 'CHI', 'DAL', 'ARI', 'LAC', 'HOU',
           'SEA', 'OAK'],
            ['kan','jax','car', 'rav', 'buf', 'min', 'det', 'atl', 'nwe', 'was', 
            'cin', 'nor', 'sfo', 'ram', 'nyg', 'den', 'cle', 'clt', 'oti', 'nyj', 
             'tam','mia', 'pit', 'phi', 'gnb', 'chi', 'dal', 'crd', 'sdg', 'htx', 'sea', 'rai' ])
    elo_df['team2'] = elo_df['team2'].replace(['KC', 'JAX', 'CAR', 'BAL', 'BUF', 'MIN', 'DET', 'ATL', 'NE', 'WSH',
           'CIN', 'NO', 'SF', 'LAR', 'NYG', 'DEN', 'CLE', 'IND', 'TEN', 'NYJ',
           'TB', 'MIA', 'PIT', 'PHI', 'GB', 'CHI', 'DAL', 'ARI', 'LAC', 'HOU',
           'SEA', 'OAK'],
            ['kan','jax','car', 'rav', 'buf', 'min', 'det', 'atl', 'nwe', 'was', 
            'cin', 'nor', 'sfo', 'ram', 'nyg', 'den', 'cle', 'clt', 'oti', 'nyj', 
             'tam','mia', 'pit', 'phi', 'gnb', 'chi', 'dal', 'crd', 'sdg', 'htx', 'sea', 'rai' ])
    return elo_df

def merge_rankings(agg_games_df,elo_df):
    
    agg_games_df = pd.merge(agg_games_df, elo_df, how = 'inner', left_on = ['home_abbr', 'away_abbr'], right_on = ['team1', 'team2']).drop(columns = ['date','team1', 'team2'])
    agg_games_df['elo_dif'] = agg_games_df['elo2_pre'] - agg_games_df['elo1_pre']
    agg_games_df['qb_dif'] = agg_games_df['qb2_value_pre'] - agg_games_df['qb1_value_pre']
    agg_games_df = agg_games_df.drop(columns = ['elo1_pre', 'elo2_pre', 'qb1_value_pre', 'qb2_value_pre'])
    return agg_games_df

def prep_test_train(current_week,weeks,year):
    current_week = current_week + 1
    try:
        schedule_df = pd.read_csv(f'schedules/schedule_df_{year}.csv')
        print("Reading schedule from CSV")
    except:
        print(f'Hitting API for schedule {year}')
        schedule_df  = get_schedule(year)
        schedule_df.to_csv(f'schedule_df_{year}.csv', index=False)
    try:
        weeks_games_df = pd.read_csv(f'weekly_game_data/weeks_games_df_{year}.csv')
        print(f"Reading week games - {year}")
    except:
        print(f'Hitting API for week games - {year}')
        weeks_games_df = game_data_up_to_week(weeks,year)
        weeks_games_df.to_csv(f'weeks_games_df_{year}.csv', index=False)
    
    agg_games_df = agg_weekly_data(schedule_df,weeks_games_df,current_week,weeks)
    agg_games_df['year'] = year
    agg_games_df.to_csv(f'agg_weekly_games/agg_games_df_{year}.csv', index=False)
    elo_df = get_elo()
    df_2022 = pd.read_csv('agg_weekly_games/agg_games_df_2022.csv')
    df_2022['year'] = 2022
    agg_games_df = pd.concat([df_2022, agg_games_df])
    final_df = merge_rankings(agg_games_df, elo_df)
    
    train_df = final_df[final_df.result.notna()]
    current_week = current_week - 1
    print(f'Creating test_df for week {current_week} - {year}')
    test_df = final_df[(final_df['week'] == current_week) & (final_df['year']==year)]
    print(test_df.shape)
    return test_df, train_df