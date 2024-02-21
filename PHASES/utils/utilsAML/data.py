
xml_schema_to_python_type = {
    'xs:string': str,
    'xs:integer': int,
    'xs:decimal': float,  # or decimal.Decimal
    'xs:boolean': bool,
    'xs:date': str,  # You may convert it to datetime.date if needed
    'xs:time': str,  # You may convert it to datetime.time if needed
    'xs:dateTime': str,  # You may convert it to datetime.datetime if needed
    'xs:duration': str,  # You may convert it to a custom duration representation if needed
    'xs:float': float,
    'xs:double': float,
    'xs:hexBinary': bytes,  # or str (hexadecimal representation)
    'xs:base64Binary': bytes,  # or str (base64 encoded)
    'xs:anyURI': str,
    'xs:QName': str,  # Qualified name
    'xs:ID': str,
    'xs:IDREF': str,
    'xs:IDREFS': list,  # List of str
    # Add more mappings as needed for your specific use case
}


def convert_string_to_datatype(input_string, data_type):
    # Use the specified data type to convert the input string
    converted_value = data_type(input_string)
    return converted_value


class Data:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value


def resolve_data(data_dict, variables):
    resolved_data = dict()
    for key, data in data_dict.items():
        if data.type is str:
            value = data.value.format(**variables)
        else:
            value = data.value
            if isinstance(value, str) and value[0] == '{' and value[-1] == '}':
                variable_name = value[1:-1]
                value = variables[variable_name]
        resolved_data[key] = value
    return resolved_data


def generate_data(xml_type, value_str):
    if xml_type in xml_schema_to_python_type:
        type = xml_schema_to_python_type[xml_type]
        if value_str :
            value = convert_string_to_datatype(value_str, xml_schema_to_python_type[xml_type])
        else:
            value = None
        return Data(type,value)
    else:
        return Data(xml_type,value_str)
