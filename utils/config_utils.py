def env_onoff_to_bool(value, default=False):
    """
    Convert environment variable to boolean based on 'on'/'off' values.
    
    Args:
        key (str): Environment variable name
        default (bool): Default value if env var is not set
        
    Returns:
        bool: True if env var is 'on' (case-insensitive), False otherwise
    """
    if value is None:
        return default
    return value.lower() == "on"
