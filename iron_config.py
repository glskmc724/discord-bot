CONF_FILENAME = "bot.conf"
DISCORD_CONFIG = ["discord_bot_token"]
YOUTUBE_CONFIG = ["youtube_api_key"]
CONFIG = [DISCORD_CONFIG, YOUTUBE_CONFIG]

class Config:
    discord = {}
    youtube = {}
    config_list = [discord, youtube]
    def __init__(self):
        conf_file = open(CONF_FILENAME, "r")
        confs = conf_file.readlines()       

        for conf in confs:
            if (conf[0] == "#"):
                continue
            else:
#               init config
                idx = 0
                for config_list in CONFIG:
                    for config in config_list:
                        config_len = len(config)
                        if (conf[:config_len] == config):
                            data = conf.split("=")[1].replace("\n", "")
                            self.config_list[idx][config] = data.replace("\"", "")
                    idx += 1
