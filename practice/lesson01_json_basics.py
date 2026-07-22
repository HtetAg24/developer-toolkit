import json

user_text = '{"tool": "JSON Formatter", "language": "Python", "completed": false, "features": ["load", "format", "print"], "name": "JSON Formatter"}'

data = json.loads(user_text)

print("Original JSON text:")
print(user_text)

print("\nPython dictionary:")
print(data)

print("\nTool name:")
print(data["tool"])

print("\nFeatures:")
print(data["features"])

formatted_json = json.dumps(data, indent=4)

print("\nFormatted JSON:")
print(formatted_json)
