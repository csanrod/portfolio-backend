"""Centralized logging configuration for the portfolio backend application.

This module provides a standardized logger instance with consistent formatting
for all modules in the application.
"""
import logging
import os
import sys

def setup_logger(name: str = "portfolio", level: int | None = None) -> logging.Logger:
    """Create or retrieve a logger with standardized formatting.
    
    Configures a logger with consistent formatting across the application.
    Handles module name normalization and prevents duplicate handlers.
    
    Args:
        name: Logger name, typically __name__ from the calling module.
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               If None, reads from LOG_LEVEL environment variable or defaults to INFO.
        
    Returns:
        Configured logging.Logger instance ready for use.
    """
    # Clean module name for consistent logging across different execution contexts
    clean_name = name
    
    # Remove "src." prefix if present (handles both "src.portfolio.*" and "portfolio.*")
    if clean_name.startswith("src."):
        clean_name = clean_name[4:]
    
    # Handle __main__ by using a generic fallback
    # This works for any module executed as __main__
    if clean_name == "__main__":
        clean_name = "portfolio.__main__"
    
    logger = logging.getLogger(clean_name)
    
    # Determine logging level
    if level is None:
        level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(level)
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        # Create formatter with complete information
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        # Prevent propagation to avoid duplicate logs
        logger.propagate = False
    
    return logger
