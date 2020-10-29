import numpy as np
import plotly.graph_objects as go

def cumulative_exploration_plot(arms_rewards):
    fig = go.Figure()
    x=list(range(len(arms_rewards['arms_rewards'])))

    for arm, values in arms_rewards['arms_rewards'].items():
        fig.add_trace(
            go.Scatter(name=arms_rewards['brands'][arm],
                        x=x,
                        y=np.cumsum(np.abs(values)),
                        mode='lines',
                        line=dict(width=0.5),
                        stackgroup='one',
                        groupnorm='percent' # define stack group
                )
        )

    fig.update_layout( 
                    xaxis_title_text='<b>Time</b>', 
                    yaxis_title_text='<b>Cummulative Exploration Arm</b>',
                    title='''<b>Cumulative Exploration Arms over time</b><br>How our algorithm explored different arms over time'''
                )
    return fig

def cumulative_reward_plot(arms_rewards):
    fig = go.Figure()
    x=list(range(len(arms_rewards['arms_rewards'])))

    for arm, values in arms_rewards['arms_rewards'].items():
        fig.add_trace(
            go.Scatter(name=arms_rewards['brands'][arm],
                        x=x,
                        y=np.cumsum(values),
                        mode='lines',
                        line=dict(width=0.5),
                )
        )

    fig.update_layout( 
                    xaxis_title_text='<b>Time</b>', 
                    yaxis_title_text='<b>Cummulative Reward</b>',
                    title='''<b>Cumulative Reward of Arms</b><br>How much reward the arm accumulated over time'''
                )
    return fig

def show_best_arm(arms_rewards):
    '''
    Returns the name of the best arm (beer)
    '''
    arms_average_rewards = [np.mean(arms_rewards['arms_rewards'][arm]) for arm in arms_rewards['arms_rewards']]
    best_arm_index = str(np.argmax(arms_average_rewards))

    return arms_rewards['brands'][best_arm_index]