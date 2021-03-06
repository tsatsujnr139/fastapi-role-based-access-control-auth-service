class Role:
    """
    Constants for the various roles scoped in the application ecosystem
    """

    GUEST = {
        "name": "GUEST",
        "description": "A Guest Account",
    }
    ACCOUNT_ADMIN = {
        "name": "ACCOUNT_ADMIN",
        "description": "Primary Administrator/Superuser For an Account",
    }

    ACCOUNT_MANAGER = {
        "name": "ACCOUNT_MANAGER",
        "description": "Day to Day Administrator of Events For an Account",
    }
    ADMIN = {
        "name": "ADMIN",
        "description": "Admin of Application Ecosystem",
    }
    SUPER_ADMIN = {
        "name": "SUPER_ADMIN",
        "description": "Super Administrator of Application Ecosystem",
    }
