# config.py
import os
from dataclasses import dataclass

@dataclass
class FreqTradeConfig:
    CONTAINER_NAME: str = "freqtrade"
    CONFIG_PATH: str = "/home/devin/develop/ft_userdata/user_data/config.json"
    DB_PATH: str = "/home/devin/develop/ft_userdata/user_data/tradesv3.sqlite"
    
    # Slot Management Parameters
    MIN_SLOTS: int = 6
    MAX_SLOTS: int = 20
    BASE_FREE_SLOTS: int = 3
    COOLDOWN_MINUTES: int = 30
    COOLDOWN_FILE: str = "/tmp/slots_update_cooldown"
