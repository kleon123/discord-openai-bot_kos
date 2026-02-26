import os
import sys

# Function to get environment variable with error handling
def get_env_var(var_name):
    """Retrieve an environment variable or exit on failure."""
    value = os.getenv(var_name)
    if value is None:
        print(f'Error: Environment variable {var_name} not set.')
        sys.exit(1)
    return value

# Read the token from the environment variables
TOKEN = get_env_var('DISCORD_TOKEN')

# ... rest of your main.py code here ...