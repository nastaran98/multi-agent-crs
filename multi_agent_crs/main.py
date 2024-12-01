import sys
sys.path.append('E:/Master/Thesis/nastaran multi agent CRS/')

import pandas as pd

from multi_agent_crs.utils import set_config, process_data, load_testset
from multi_agent_crs.graph import create_graph
import csv

if __name__ == '__main__':
    config = set_config()
    app = create_graph()
    #Plan and tool use
    # testset = load_testset(config)
    # results = []
    # for i, r in testset.iterrows():
    #     responses = []
    #     task = r['user_query']
        
    #     try:
    #         for s in app.stream({"task": task, "config": config}):
    #             response_data = {k: v for k, v in s.items() if k != 'config'}
    #             print(response_data)
    #             responses.append(response_data)
    #     except Exception as e:
    #         # Add exception information to the responses if an error occurs
    #         error_message = {"error": str(e)}
    #         print(f"Error for task '{task}': {error_message}")
    #         responses.append(error_message)
        
    #     results.append([task, responses])

    # results_df = pd.DataFrame(results, columns=['Task', 'Responses'])
    # results_df.to_csv(config['results_path'], encoding='utf-8-sig')
    ########################################################
    # df = pd.read_csv('E://Master/Thesis/nastaran multi agent crs/datasets/Dialogue Plan Test set - Generated Profiles.csv')[5:6]
    # with open('E://Master/Thesis/nastaran multi agent crs/results/personalized_plan.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows([['dialogue_history', 'profile','plan']])
    #     for index, row in df.iterrows():
    #         print(index)
    #         profile = row['profile']
    #         responses = []
    #         task = row['dialogue_history']
    #         for s in app.stream({"task": task, "config": config, 'profile': profile}):
    #             response_data = {k: v for k, v in s.items() if k != 'config'}
    #             writer.writerows([[task, profile, response_data]])
    ########################################################
    # df = pd.read_csv('E://Master/Thesis/nastaran multi agent crs/datasets/short_dialogues.csv', encoding='utf-8-sig')
    # with open('E://Master/Thesis/nastaran multi agent crs/results/profiles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows([['dialogue_history','plan','profile']])
    #     for index, row in df.iterrows():  
    #         steps = eval(row['plan - 4o'])['plan']['steps']
    #         dialogue_history = row['dialogue_history']
    #         plan = row['plan - 4o']
            
    #         # Check if 'user_profile' exists in any step
    #         user_profile_present = any(tool == 'user_profile' for _, _, tool, _ in steps)

    #         # Retrieve the step with 'user_profile' if it exists
    #         user_profile_step = next((step for step in steps if step[2] == 'user_profile'), None)

    #         if user_profile_present and user_profile_step:
    #             # Unpack the step details
    #             _, step_name, tool, tool_input = user_profile_step
    #             writer.writerows([[dialogue_history, plan, tool_input]])
    #         else:
    #             # Save an empty string if 'user_profile' is not present
    #             writer.writerows([[dialogue_history, plan, " "]])
            
    responses = []
    task = 'چطور می تونیم با شرایط سخت زندگی کنار بیایم و معنی واقعی زندگی رو پیدا کنیم؟'
    
    try:
        for s in app.stream({"task": task, "config": config}):
            response_data = {k: v for k, v in s.items() if k != 'config'}
            print(response_data)
            responses.append(response_data)
    except Exception as e:
        # Add exception information to the responses if an error occurs
        error_message = {"error": str(e)}
        print(f"Error for task '{task}': {error_message}")
        responses.append(error_message)
        