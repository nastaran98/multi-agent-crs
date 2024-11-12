import yaml
import os 
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import pandas as pd

def set_config():
    with open('E:\Master\Thesis\\nastaran multi agent crs\configs\config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def get_model(config, key):
    model_name = config[key]["model"]
    if 'gpt' in model_name:
        api_key = config['OPENAI_API_KEY']
        model = ChatOpenAI(model=model_name, api_key=api_key)
    if 'llama' in model_name:
        api_key = config['GROQ_API_KEY']
        model = ChatGroq(model=model_name, api_key=api_key)
    return model

def get_planner_model(config):
    model_name = config["planner_agent"]["model"]
    if 'gpt' in model_name:
        api_key = config['OPENAI_API_KEY']
        model = ChatOpenAI(model=model_name, api_key=api_key)
    if 'llama' in model_name:
        api_key = config['GROQ_API_KEY']
        model = ChatGroq(model=model_name, api_key=api_key)
    return model

def get_action_model(config):
    model_name = config["action_predictor_agent"]["model"]
    if 'gpt' in model_name:
        api_key = config['OPENAI_API_KEY']
        model = ChatOpenAI(model=model_name, api_key=api_key)
    if 'llama' in model_name:
        api_key = config['GROQ_API_KEY']
        model = ChatGroq(model=model_name, api_key=api_key)
    return model


def get_solver_model(config):
    model_name = config["solver_agent"]["model"]
    if 'gpt' in model_name:
        api_key = config['OPENAI_API_KEY']
        model = ChatOpenAI(model=model_name, api_key=api_key)
    if 'llama' in model_name:
        api_key = config['GROQ_API_KEY']
        model = ChatGroq(model=model_name, api_key=api_key)
    return model

def get_planner_prompt(config):
    planner_prompt = config["planner_agent"]["prompt"]
    return planner_prompt

def get_action_predictor_agent_prompt(config):
    action_predictor_agent_prompt = config["action_predictor_agent"]["prompt"]
    return action_predictor_agent_prompt

def load_from_txt_file(file_path):
    with open(file_path, 'r',encoding='utf-8-sig') as f:
        data = f.read()
        data = eval(data)
    return data    

def process_data(config):
    all_books = []
    # for _, value in data.items():
    # for books in value:
    #     # Ensure that each entry in books is a dictionary
    #     if isinstance(books, dict):
    #         all_books.append(books)
    #     elif isinstance(books, list):
    #         # If books is a list, add its dictionary items to all_books
    #         all_books.extend(item for item in books if isinstance(item, dict))
    #     else:
    #         print(f"Skipping non-dictionary entry: {books}")

    data_path = config['dataset_txt_path']
    result_path = config['dataset_path']
    data = load_from_txt_file(data_path)
    for _, value in data.items():
        for _, books in value.items():
            all_books.extend(books)
    df = pd.DataFrame(all_books)
    df.to_csv(result_path, encoding='utf-8-sig')

def load_data(config):
    data_path = config['dataset_path']
    data = pd.read_csv(data_path)
    return data

