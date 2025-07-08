def make_tool(fn, name, description, param_schema):
    import functools

    @functools.wraps(fn)
    async def wrapper(**kwargs):
        return await fn(**kwargs)

    wrapper.name = name
    wrapper.description = description
    wrapper.parameters = param_schema
    return wrapper
