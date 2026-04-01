def map_question_to_evidence(question, scan):
    q = question.lower()
    if "encrypt" in q or "s3" in q:
        return scan["s3_buckets"]
    if "mfa" in q or "user" in q:
        return scan["iam"]["users"]
    return None

def verify_answer(question, answer, evidence):
    q = question.lower()
    
    if "encrypt" in q:
        # Check if any bucket is NOT encrypted
        flaws = [b for b in evidence if not b.get("encrypted")]
        if flaws:
            return {"status": "mismatch", "explanation": f"Found unencrypted bucket: {flaws[0]['name']}"}
            
    if "mfa" in q:
        # Check if any user has MFA disabled
        flaws = [u for u in evidence if not u.get("mfa_enabled")]
        if flaws:
            return {"status": "mismatch", "explanation": f"User {flaws[0]['username']} has MFA disabled."}

    return {"status": "verified", "explanation": "Matches infrastructure configuration."}