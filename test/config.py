import json


class Config:
    with open('./test/commands.json', 'r') as f:
        COMMANDS = json.load(f)


    with open('./test/config.json', 'r') as f:
        config = json.load(f)

    DISCORD_TOKEN = config['discord_token']
    PREFIX = config['prefix']


    @classmethod
    def reload(cls):
        with open('./test/commands.json', 'r') as f:
            cls.COMMANDS = json.load(f)


        with open('./test/config.json', 'r') as f:
            config = json.load(f)

        cls.DISCORD_TOKEN = config['discord_token']
        cls.PREFIX = config['prefix']
