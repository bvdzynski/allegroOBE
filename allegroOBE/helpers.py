import json


def jsonPrettyPrint(parsed):
    print(json.dumps(parsed, indent=4, sort_keys=True))
