from pydantic import create_model

def create_dynamic_model(schema):
    feilds = {}

    for feild, feild_type in schema.items():
        if feild_type == "string":
            feilds[feild] = (str | None, None)
        elif feild_type == "integer":
            feilds[feild] = (int | None, None)
        elif feild_type == "number":
            feilds[feild] = (float | None, None)
        elif feild_type == "boolean":
            feilds[feild] = (bool | None, None)
        elif feild_type == ['string']:
            feilds[feild] = (list[str] | None, None)

    return create_model("Dynamic_model", **feilds)



