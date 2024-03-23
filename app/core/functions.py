import configparser
import toml


# 读取配置文件
def read_ini_config():
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    dict_config = {section: {key: value for key, value in config.items(section)} for section in config.sections()}
    return dict_config


# 读取toml配置文件
def read_toml_config():
    with open("config/config.toml", "r", encoding="utf-8") as f:
        return toml.load(f)
