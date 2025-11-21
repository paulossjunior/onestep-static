import pandas as pd

def define_env(env):
    @env.macro
    def pd_read_json(path):
        return pd.read_json(path)
