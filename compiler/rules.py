from typing import Dict, List

def compile_security_auth_required(policy: Dict) -> List[Dict]:
    if policy["value"] is not True:
        return []

    return [{
        "id": "AUTH_001",
        "description": "All API routes must enforce authentication",
        "severity": policy["severity"],
        "executor": "auth_check",
        "params": {
            "framework": "fastapi"
        }
    }]