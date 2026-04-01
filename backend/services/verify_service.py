def map_question_to_evidence(question, scan_data):
    q = question.lower()

    if "encrypt" in q or "bucket" in q:
        return scan_data.get("s3_buckets", [])

    elif "mfa" in q or "iam" in q or "user" in q or "root" in q or "password" in q:
        return scan_data.get("iam", {})

    elif "cloudtrail" in q or "logging" in q or "log" in q or "audit" in q:
        return scan_data.get("cloudtrail", {})

    return scan_data


def verify_answer(question, answer, evidence):
    q = question.lower()
    a = answer.lower()

    # Encryption checks
    if "encrypt" in q:
        if isinstance(evidence, list):
            unencrypted = [b["name"] for b in evidence if not b.get("encrypted", True)]
            if unencrypted:
                if "no" in a and ("any" in q or "left" in q):
                    return {
                        "status": "mismatch",
                        "explanation": f"Unencrypted buckets found: {', '.join(unencrypted)}"
                    }
                return {
                    "status": "mismatch",
                    "explanation": f"Unencrypted buckets found: {', '.join(unencrypted)}"
                }
        return {
            "status": "verified",
            "explanation": "All checked buckets are encrypted"
        }

    # Public access checks
    if "public access" in q or "publicly accessible" in q:
        if isinstance(evidence, list):
            public_buckets = [b["name"] for b in evidence if not b.get("public_access_blocked", True)]
            if public_buckets:
                return {
                    "status": "mismatch",
                    "explanation": f"Public access is not blocked for: {', '.join(public_buckets)}"
                }
        return {
            "status": "verified",
            "explanation": "Public access is blocked for all checked buckets"
        }

    # MFA checks
    if "mfa" in q:
        users = evidence.get("users", [])
        no_mfa = [u["username"] for u in users if not u.get("mfa_enabled", True)]

        if "root" in q:
            if not evidence.get("root_mfa_enabled", False):
                return {
                    "status": "mismatch",
                    "explanation": "Root account MFA is not enabled"
                }
            return {
                "status": "verified",
                "explanation": "Root account MFA is enabled"
            }

        if no_mfa:
            return {
                "status": "mismatch",
                "explanation": f"Users without MFA: {', '.join(no_mfa)}"
            }

        return {
            "status": "verified",
            "explanation": "All checked users have MFA enabled"
        }

    # Password policy checks
    if "password" in q:
        password_policy = evidence.get("password_policy", {})
        min_length = password_policy.get("min_length", 0)

        if "12" in q and min_length < 12:
            return {
                "status": "mismatch",
                "explanation": f"Minimum password length is {min_length}, expected at least 12"
            }

        return {
            "status": "verified",
            "explanation": f"Password policy minimum length is {min_length}"
        }

    # CloudTrail / logging checks
    if "cloudtrail" in q or "logging" in q or "log" in q:
        if not evidence.get("logging_active", False):
            return {
                "status": "mismatch",
                "explanation": "CloudTrail logging is not active"
            }

        if "all regions" in q and not evidence.get("multi_region", False):
            return {
                "status": "mismatch",
                "explanation": "CloudTrail is active but not multi-region"
            }

        if "validation" in q or "tampering" in q:
            if not evidence.get("log_validation", False):
                return {
                    "status": "mismatch",
                    "explanation": "Log file validation is not enabled"
                }

        return {
            "status": "verified",
            "explanation": "CloudTrail logging is properly enabled"
        }

    # Audit-ready / compliant type broad questions
    if "audit-ready" in q or "compliant" in q or "security misconfigurations" in q or "security standards" in q:
        mismatches = []

        for b in evidence.get("s3_buckets", []):
            if not b.get("encrypted", True):
                mismatches.append(f"{b['name']} not encrypted")
            if not b.get("public_access_blocked", True):
                mismatches.append(f"{b['name']} public access not blocked")

        iam = evidence.get("iam", {})
        for u in iam.get("users", []):
            if not u.get("mfa_enabled", True):
                mismatches.append(f"{u['username']} has no MFA")

        if iam.get("password_policy", {}).get("min_length", 0) < 12:
            mismatches.append("password length below 12")

        cloudtrail = evidence.get("cloudtrail", {})
        if not cloudtrail.get("logging_active", False):
            mismatches.append("CloudTrail not active")

        if mismatches:
            return {
                "status": "mismatch",
                "explanation": "; ".join(mismatches)
            }

        return {
            "status": "verified",
            "explanation": "No major misconfigurations found in scanned controls"
        }

    return {
        "status": "verified",
        "explanation": "No matching rule found, marked verified for demo"
    }


if __name__ == "__main__":
    fake_scan = {
        "s3_buckets": [
            {"name": "acme-customer-data", "encrypted": True, "public_access_blocked": True},
            {"name": "acme-internal-logs", "encrypted": False, "public_access_blocked": False}
        ],
        "iam": {
            "users": [
                {"username": "admin-user", "mfa_enabled": True},
                {"username": "developer-user", "mfa_enabled": False}
            ],
            "root_mfa_enabled": True,
            "password_policy": {"min_length": 8}
        },
        "cloudtrail": {
            "logging_active": True,
            "multi_region": True,
            "log_validation": True
        }
    }

    test_questions = [
        "Is all customer data encrypted at rest?",
        "Is MFA enabled for all IAM users?",
        "Is public access blocked for all S3 buckets?",
        "Is the minimum password length at least 12 characters?",
        "Is CloudTrail logging enabled across all regions?",
        "Is your infrastructure audit-ready?"
    ]

    for q in test_questions:
        evidence = map_question_to_evidence(q, fake_scan)
        result = verify_answer(q, "Yes", evidence)
        print(q)
        print(result)
        print("-" * 50)