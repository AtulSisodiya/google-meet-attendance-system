import json
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
def get(filename):
    with open(filename) as f:
        data=json.load(f)
    return dotdict(data)

def whget(filename):
    with open(filename) as f:
        data=json.load(f)
    return (data)
def write_data(di):
    with open('config.json', 'w') as fp:
        json.dump(di, fp)
config=get("./config.json")
whconfig=whget("./config.json")