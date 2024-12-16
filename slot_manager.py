# slot_manager.py
import json
import logging
import subprocess
import time
from typing import Tuple
from datetime import datetime, timedelta
import os
from config_manager import ConfigManager

class SlotManager:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.configManager = ConfigManager(self.config.CONFIG_PATH)
    
    def check_cooldown(self) -> bool:
        """Check if cooldown period has passed"""
        if not os.path.exists(self.config.COOLDOWN_FILE):
            return True
        
        with open(self.config.COOLDOWN_FILE, 'r') as f:
            last_update = float(f.read().strip())
        
        elapsed_minutes = (time.time() - last_update) / 60
        return elapsed_minutes >= self.config.COOLDOWN_MINUTES
    
    def update_cooldown(self):
        """Update cooldown timestamp"""
        with open(self.config.COOLDOWN_FILE, 'w') as f:
            f.write(str(time.time()))
    
    def calculate_free_slots(
        self, derisk_count: int, loss_count: int, 
        avg_loss: float, max_loss: float
    ) -> Tuple[int, str]:
        """Dynamic free slots calculation"""
        free_slots = self.config.BASE_FREE_SLOTS
        log_messages = []
        
        # De-risk trade impact
        if derisk_count > 0:
            derisk_reduction = derisk_count // 2
            if free_slots > derisk_reduction + 1:
                free_slots -= derisk_reduction
                log_messages.append(f"Reduced {derisk_reduction} slots due to de-risk trades({derisk_count})")
            else:
                free_slots = 1
                log_messages.append("De-risk trades reduced slots to minimum 1")
        
        # Loss impact
        if avg_loss < 0:
            abs_loss = abs(avg_loss)
            if 0.03 <= abs_loss <= 0.05:
                free_slots = max(free_slots - 1, 1)
                log_messages.append(f"Average loss({abs_loss}) between 0.03-0.05, reduced 1 slot")
            elif abs_loss > 0.05:
                free_slots = max(free_slots - 2, 1)
                log_messages.append(f"Average loss({abs_loss}) above 0.05, reduced to {free_slots} slots")
        
        # Maximum loss impact
        if max_loss < -0.20:
            free_slots += 2
            log_messages.append(f"Max loss({max_loss}) below -0.20, added 2 slots")
        elif max_loss < -0.10:
            free_slots += 1
            log_messages.append(f"Max loss({max_loss}) below -0.10, added 1 slot")
        
        # Ensure minimum
        free_slots = max(free_slots, 1)
        
        return free_slots, ' | '.join(log_messages)
    
    def get_current_max_trades(self) -> int:
        """Read current max_open_trades from config"""
        try:
            ret = self.configManager.find_max_open_trades()
            return ret
        except Exception as e:
            self.logger.error(f"Config read error: {e}")
            return self.config.BASE_FREE_SLOTS
    
    def check_slot_limits(self, slots: int) -> int:
        """Ensure slots are within min and max limits"""
        return max(
            min(slots, self.config.MAX_SLOTS), 
            self.config.MIN_SLOTS
        )
    
    def update_config_max_trades(self, new_max: int):
        """Update max_open_trades in config file"""
        try:
            
            ret = self.configManager.update_max_open_trades(new_max)
            return True
        except Exception as e:
            self.logger.error(f"Config update error: {e}")
            return False
    
    def restart_container(self, container_name: str):
        """Restart Docker container"""
        try:
            subprocess.run(['docker', 'restart', container_name], check=True)
            time.sleep(10)  # Wait for container to restart
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Container restart failed: {e}")
            return False

