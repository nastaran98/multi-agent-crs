from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import yaml
import csv
import ast

def get_config():
    with open('E://Master/Thesis/nastaran multi agent crs/user_profile_generator/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def get_model(config):
    api_key = config['OPENAI_API_KEY']
    model_name = config['profile_generator_agent']['model']
    model = ChatOpenAI(model=model_name, api_key=api_key)
    return model

def generate_dataset_agent():
    config = get_config()
    model = get_model(config)
    prompt = config['profile_generator_agent']['prompt']
    prompt_template = ChatPromptTemplate.from_messages([("user", prompt)])
    generator_agent = prompt_template | model

    return generator_agent

def profile_examples():
    examples = pd.read_csv('profiles.csv',encoding='utf-8-sig')
    examples = examples['profiles'].sample(n=10)
    examples = examples.to_list()
    return examples

def generator_pipeline():
    agent = generate_dataset_agent()
    example_list = profile_examples()

    with open('profiles.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        result = agent.invoke({'example': example_list})
        start_index = result.content.find('[')
        end_index = result.content.rfind(']') + 1

        result = ast.literal_eval(result.content[start_index:end_index])
        for i in result:
            writer.writerows([[i]])

if __name__ == '__main__':
    generator_pipeline()