import os


def get_postgres_uri():
    """
    Get the postgresql uri from the environment variable.
    """
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", 5432)
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    db_name = os.environ.get("DB_NAME", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    """
    Get the api url from the environment variable.
    """
    host = os.environ.get("API_HOST", "localhost")
    port = os.environ.get("API_PORT", "80")
    return f"http://{host}:{port}"
