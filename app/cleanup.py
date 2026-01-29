# cleanup.py

import os
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

RETENTION_DAYS = 30


def cleanup_old_audio_files(folder="tts_output"):
    """Delete audio files older than RETENTION_DAYS"""
    if not os.path.exists(folder):
        return
    
    cutoff_time = time.time() - (RETENTION_DAYS * 24 * 60 * 60)
    deleted_count = 0
    
    try:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                file_mtime = os.path.getmtime(filepath)
                if file_mtime < cutoff_time:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.info(f"Deleted old audio file: {filename}")
        
        if deleted_count > 0:
            logger.info(f"Cleanup complete: {deleted_count} files deleted")
        
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
