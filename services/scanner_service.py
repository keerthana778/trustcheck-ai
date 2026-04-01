def execute_full_scan():
    """PERSON 3: Mock infrastructure evidence."""
    return {
        "s3_buckets": [
            {"name": "prod-data", "encrypted": True},
            {"name": "internal-logs", "encrypted": False} 
        ],
        "iam": {
            "users": [
                {"username": "admin", "mfa_enabled": True},
                {"username": "dev-intern", "mfa_enabled": False} 
            ]
        }
    }