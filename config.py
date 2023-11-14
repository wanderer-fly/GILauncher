import os
import sys


import yaml

class Config:
    def __init__(self):
        try:
            with open('config.yaml', 'r') as config_file:
                self.config = yaml.load(config_file, Loader = yaml.FullLoader)
        except:
            self.gen_config()
            with open('config.yaml', 'r') as config_file:
                self.config = yaml.load(config_file, Loader = yaml.FullLoader)

    def read_config(self):    
        return self.config
    
    def set_config(self, key, value):
        self.config[key] = value
        with open('config.yaml', 'w') as config_file:
            yaml.dump(self.config, config_file, default_flow_style=False)

    def gen_config(self):
        data = {
            'game_path': None,
            'unlockfps': False
        }
        
        with open('config.yaml', 'w') as file:
            yaml.dump(data, file, default_flow_style=False)