import json


def get_prompt_functions(available_tools: str) -> str:
    json_template = '{"name": "functionName", "arguments": "{ \\\"arg1\": \\\"value\\\" }"}'
    json_empty_template = '{"name": "functionName", "arguments": "{}"}'
    functions_dump = json.dumps(available_tools)
    tools_prompt = ("You have access to functions calling to fulfill user's request. Some case may be complex so you'll need to call several functions.\n" +
                    "As YOU CAN ONLY CALL ONE FUNCTION AT THE TIME, select the most adapted function if you need more information, once the result provided, you'll be able to choose another one if needed or respond to the user.\n" +
                    "Available functions:" + functions_dump + "\n" +
                    "If you need to use a function to get more information, respond with this syntax only (json):\n" +
                    json_template + "\n" +
                    " (or if the function has no parameters:\n"
                    + json_empty_template + "\n" +
                    "Don't forget to double escape the quotes around parameters because this syntax is very specific\n" +
                    "IMPORTANT: \n" +
                    "- Only one call at the time\n" +
                    "- Respect the syntax above, return JSON and only JSON\n" +
                    "- no text or explanation when using function calling, only respond with the syntax above!\n" +
                    "- DO NOT USE backticks or markdown syntax or i will beat your family with a pair of slipper")
    return tools_prompt


def get_prompt_functions_gpt(available_tools: str) -> str:
    """GPT Prompt"""
    functions_dump = json.dumps(available_tools)
    tools_prompt = (
        "You can call functions to fulfill the user's request. "
        "Here are the available functions:\n"
        f"{functions_dump}\n\n"
        "To call a function, respond with JSON in this exact format:\n"
        '{"name": "functionName", "arguments": "{ \\\"arg1\": \\\"value\\\" }"}\n\n'
        "If the function has no arguments, use:\n"
        '{"name": "functionName", "arguments": "{}"}\n\n'
        "IMPORTANT:\n"
        "- Respond only with JSON, no text or explanation.\n"
        "- Call only one function at a time.\n"
        "- Ensure the JSON is valid.\n"
    )

    examples = """
    Examples:
    - User: "What's the weather in Paris?"
      Response: {"name": "get_weather", "arguments": "{ \\"location\\": \\"Paris\\", \\"unit\\": \\"Celsius\\" }"}
    
    - User: "Search for Italian restaurants in Rome."
      Response: {"name": "search", "arguments": "{ \\"query\\": \\"Italian restaurants in Rome\\" }"}
    
    - User: "What time is it now?"
      Response: {"name": "get_time", "arguments": "{}"}
    """
    # tools_prompt += examples

    return tools_prompt


def handle_function_result(history):
    function_result_prompt = "Some tools provided informations :\n"
    initial_request = ""
    for entry in reversed(history):
        if entry["role"] == 'function':
            function_name = entry["name"]
            function_result = entry["content"]
            function_result_prompt += '- "' + function_name + '":"' + function_result + '"'
        elif entry["role"] == 'user':
            initial_request = entry["content"]

    function_result_prompt += "\nBased on the previous information, answer to the user's request or call another function if you need it."
    function_result_prompt += "\n\n" + initial_request

    print(function_result_prompt)
    return function_result_prompt


# Hack for functions
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True
