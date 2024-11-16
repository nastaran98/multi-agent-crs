import sys
sys.path.append('E:/Master/Thesis/nastaran multi agent CRS/')

import pandas as pd

from multi_agent_crs.utils import set_config, process_data, load_testset
from multi_agent_crs.graph import create_graph


if __name__ == '__main__':
    config = set_config()
    # task = '<user>من یه کتاب از خالد حسینی میخوام. <system>کتاب بادبادک باز اثر خالد حسینی میتونه کتاب خوبی براتون باشه. <user>نه اینو قبلا خوندم. یه کتاب دیگه بگو'    
    # task = '<user>من یه کتاب از خالد حسینی میخوام. <system>کتاب بادبادک باز اثر خالد حسینی میتونه کتاب خوبی براتون باشه. <user>نه اینو قبلا خوندم. یه کتاب دیگه بگو. <system> هزار خورشید تابان رو بخون <user> نه ولش کن. کتاب فلسفی چی داری؟'    
    # task = """
    #     <user> I want a book by Agatha Christie.
    #     <system> I recommend "And Then There Were None."
    #     <user> I've already read that one. Can you suggest another?
    #     <system> How about "The Murder of Roger Ackroyd"? It’s one of Christie’s most famous mysteries.
    #     <user> Hmm, I’ve read that one too. Do you have something less popular, maybe one of her lesser-known works?
    # """
    # task = """
    #     <user> I am a procnastinator. any good book for me?
    # """
    # task = """
    #     <user> I’m looking for a book about self-improvement, but not just the usual advice. I want something that focuses on how our way of thinking influences our success.
    # """
    # task = """
    #     <user> من یه کتاب درباره فلسفه میخوام.
    # """
    # task = """
    #     <user> من خیلی وقته احساس افسردگی میکنم. درست از وقتی همسرم رو از دست دادم. نمیدونم باید چیکار کنم.
    # """
    # task = """
    #     <user>میخوام برای همسرم کتاب بخرم. چه پیشنهادی داری؟
    # """
    ########################################################
    app = create_graph()
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
    task = """
    chat history: <user> صادق هدایت خیلی عجیبه. من بوف کور رو ازش خوندم افتضاح بود. اصلا خوشم نیومد. یه کتاب خوب داری ؟
    """
    for s in app.stream({"task": task, "config": config, 'profile': ''}):
        response_data = {k: v for k, v in s.items() if k != 'config'}
        print(response_data)
        print('*' * 20)