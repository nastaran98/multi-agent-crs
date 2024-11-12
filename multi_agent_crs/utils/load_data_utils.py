import pandas as pd
def load_testset(config):
    test_set_path = config['testset_path']
    testset = pd.read_csv(test_set_path, encoding='utf-8')
    return testset