import os
import shutil
import json5 as json
import logging
from typing import Any, Optional

class ConfigManager:
    def __init__(self, main_config_path: str):
        self.logger = logging.getLogger(__name__)
        self.main_config_path = main_config_path
        self.config_dir = os.path.dirname(main_config_path)
    
    def read_config(self, config_path: str) -> dict:
        """Read a JSON configuration file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error reading config {config_path}: {e}")
            return {}
    
    def find_max_open_trades(self) -> Optional[int]:
        """
        Find max_open_trades by searching through main and additional configs
        
        Search order:
        1. Main config
        2. Additional config files
        3. Return None if not found
        """
        # Read main config
        main_config = self.read_config(self.main_config_path)
        
        # Check main config first
        if 'max_open_trades' in main_config:
            return main_config['max_open_trades']
        
        # If not in main config, check additional config files
        additional_configs = main_config.get('add_config_files', [])
         
        for config_filename in additional_configs:
            full_path = os.path.join(self.config_dir, config_filename)
            sub_config = self.read_config(full_path)
            
            if 'max_open_trades' in sub_config:
                self.logger.info(f"Found max_open_trades in {config_filename}")
                return sub_config['max_open_trades']
        
        self.logger.warning("max_open_trades not found in any configuration")
        return None
    
    def update_max_open_trades(self, new_max_trades: int) -> bool:
        """
        Update max_open_trades in the appropriate configuration file
        
        Strategy:
        1. If in main config, update main config
        2. If in a sub-config, update that specific sub-config
        3. If not found, add to main config
        """
        # Read main config
        main_config = self.read_config(self.main_config_path)
        
        # Track whether update happened
        config_updated = False
        update_path = self.main_config_path
        
        # If in main config, update main config
        if 'max_open_trades' in main_config:
            main_config['max_open_trades'] = new_max_trades
            config_updated = True
        
        # Check additional config files if not found in main config
        if not config_updated:
            additional_configs = main_config.get('add_config_files', [])
            
            for config_filename in additional_configs:
                full_path = os.path.join(self.config_dir, config_filename)
                sub_config = self.read_config(full_path)
                
                if 'max_open_trades' in sub_config:
                    sub_config['max_open_trades'] = new_max_trades
                    update_path = full_path
                    config_updated = True
                    break
        
        # If still not found, add to main config
        if not config_updated:
            main_config['max_open_trades'] = new_max_trades
            update_path = self.main_config_path
            config_updated = True
        
        # Backup original file
        backup_path = f"{update_path}.bak"
        try:
            #os.copy(update_path, backup_path)
            #shutil.copy(update_path, backup_path)
            
            # Write updated config
            with open(update_path, 'w') as f:
                json.dump(main_config if update_path == self.main_config_path else sub_config, 
                          f, indent=2,ensure_ascii=False, quote_keys=True)
            
            self.logger.info(f"Updated max_open_trades in {os.path.basename(update_path)}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to update config: {e}")
            return False

if __name__ == "__main__":
    x = ConfigManager("/home/devin/develop/ft_userdata/user_data/config.json")
    ret = x.find_max_open_trades()
    print(ret)
    ret = x.update_max_open_trades(9)
    print(ret)  
    ret = x.find_max_open_trades()
    print(ret)
