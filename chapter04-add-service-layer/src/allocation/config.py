import os


def get_postgres_uri():
    """
    Get the postgresql uri from the environment variable.
    """
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    """
    Get the api url from the environment variable.
    """
    host = os.environ.get("API_HOST", "localhost")
    port = os.environ.get("API_PORT")
    return f"http://{host}:{port}"
