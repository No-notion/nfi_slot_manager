# database.py
import sqlite3
import logging
from typing import Dict, Any, Tuple

class TradeDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def execute_query(self, query: str) -> str:
        """Execute a SQLite query and return result"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else "0"
        except Exception as e:
            self.logger.error(f"Database query error: {e}")
            return "0"
    
    def get_trade_stats(self) -> Dict[str, Any]:
        """Retrieve comprehensive trade statistics"""
        query = """
        WITH trade_stats AS (
            SELECT 
                COUNT(*) as total_open,
                SUM(CASE WHEN close_profit >= 0 THEN 1 ELSE 0 END) as profit_trades,
                SUM(CASE WHEN close_profit < 0 THEN 1 ELSE 0 END) as loss_trades,
                AVG(CASE WHEN close_profit < 0 THEN close_profit ELSE NULL END) as avg_loss
            FROM trades 
            WHERE is_open=1
        ),
        derisk_count AS (
            SELECT COUNT(DISTINCT t.id) as derisk_trades
            FROM trades t 
            JOIN orders o ON t.id = o.ft_trade_id 
            WHERE t.is_open=1 AND o.ft_order_tag='d'
        )
        SELECT 
            total_open, 
            derisk_trades,
            profit_trades,
            loss_trades,
            ROUND(COALESCE(avg_loss, 0), 4) as avg_loss
        FROM trade_stats, derisk_count;
        """
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                
                return {
                    'total_open': result[0] if result else 0,
                    'derisk_trades': result[1] if result else 0,
                    'profit_trades': result[2] if result else 0,
                    'loss_trades': result[3] if result else 0,
                    'avg_loss': result[4] if result else 0
                }
        except Exception as e:
            self.logger.error(f"Trade stats retrieval error: {e}")
            return {
                'total_open': 0,
                'derisk_trades': 0,
                'profit_trades': 0,
                'loss_trades': 0,
                'avg_loss': 0
            }
    
    def get_max_loss_trade(self) -> float:
        """Get maximum loss trade"""
        query = "SELECT COALESCE(MIN(close_profit), 0) FROM trades WHERE is_open=1;"
        return float(self.execute_query(query))

