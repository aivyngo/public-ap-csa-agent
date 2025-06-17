def make_tool(fn, name: str, description: str, param_schema: dict):
    fn.__name__ = name
    fn.description = description
    fn.parameters = param_schema
    return fn
