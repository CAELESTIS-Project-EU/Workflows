import xml.etree.ElementTree as ET


def workflow_type_parser(root):
    workflow_definition_element = root.find('.//{http://www.dke.de/CAEX}InternalElement[@Name="Workflow_definition"]')
    if workflow_definition_element is not None:
        value_element = workflow_definition_element.find('.//{http://www.dke.de/CAEX}Value')
        if value_element is not None:
            workflow_definition_value = value_element.text
            return workflow_definition_value
    raise Exception("Workflow_definition element not found")

def inputs_parser(root):
    namespace = {"caex": "http://www.dke.de/CAEX"}
    inputs_element = root.find('.//caex:InternalElement[@Name="Inputs"]', namespaces=namespace)
    inputs_data = {}

    if inputs_element is not None:
        for internal_element in inputs_element.findall('.//caex:InternalElement', namespaces=namespace):
            internal_element_name = internal_element.get('Name')
            attribute_source = internal_element.find('.//caex:Attribute[@Name="server"]/caex:Value', namespaces=namespace)
            attribute_destination = internal_element.find('.//caex:Attribute[@Name="path"]/caex:Value', namespaces=namespace)

            if attribute_source is not None and attribute_destination is not None:
                source_value = attribute_source.text if attribute_source.text is not None else ''
                destination_value = attribute_destination.text if attribute_destination.text is not None else ''

                inputs_data[internal_element_name] = [
                    {'server': source_value},
                    {'path': destination_value}
                ]

    return inputs_data



def outputs_parser(root):
    namespace = {"caex": "http://www.dke.de/CAEX"}
    outputs_element = root.find('.//caex:InternalElement[@Name="Outputs"]', namespaces=namespace)
    outputs_data = {}

    if outputs_element is not None:
        for internal_element in outputs_element.findall('.//caex:InternalElement', namespaces=namespace):
            internal_element_name = internal_element.get('Name')
            attribute_source = internal_element.find('.//caex:Attribute[@Name="path"]/caex:Value', namespaces=namespace)
            attribute_destination = internal_element.find('.//caex:Attribute[@Name="server"]/caex:Value', namespaces=namespace)

            if attribute_source is not None and attribute_destination is not None:
                source_value = attribute_source.text if attribute_source.text is not None else ''
                destination_value = attribute_destination.text if attribute_destination.text is not None else ''

                # Use the dynamic value as the key for outputs_data
                outputs_data[internal_element_name] = [
                    {'path': source_value},
                    {'server': destination_value},
                    {'overwrite': True}  # Assuming you always want to set overwrite to True
                ]

    return outputs_data


def phases_parser(root):
    namespace = {"caex": "http://www.dke.de/CAEX"}
    phases_element = root.find('.//caex:InternalElement[@Name="Phases"]', namespaces=namespace)
    phases_data = {}

    if phases_element is not None:
        for phase_element in phases_element.findall('.//caex:InternalElement[@Name="Phase"]', namespaces=namespace):
            phase_info = []
            # Extract information for the Phase
            namePhase = phase_element.find('.//caex:Attribute[@Name="name"]/caex:Value',
                                                    namespaces=namespace).text

            sequences=(phase_element.find('.//caex:Attribute[@Name="sequence"]/caex:Value',
                                                        namespaces=namespace).text).split(">>")

            for seq in sequences:
                for software_element in phase_element.findall('.//caex:InternalElement[@Name="Software"]',
                                                              namespaces=namespace):
                    if seq==software_element.find('.//caex:Attribute[@Name="type"]/caex:Value',namespaces=namespace).text:
                        software_info = {}
                        software_info['type'] = software_element.find('.//caex:Attribute[@Name="type"]/caex:Value',
                                                                      namespaces=namespace).text
                        parameters_data = {}
                        for parameter_element in software_element.findall('.//caex:InternalElement[@Name="Parameters"]',
                                                                          namespaces=namespace):
                            for attribute_element in parameter_element.findall('.//caex:Attribute', namespaces=namespace):
                                attribute_name = attribute_element.get('Name')
                                attribute_value = attribute_element.find('./caex:Value', namespaces=namespace).text
                                parameters_data[attribute_name] = attribute_value

                        software_info['arguments'] = parameters_data
                        phase_info.append(software_info)
            phases_data[namePhase]=phase_info
    return phases_data


def parameters_parser(root):
    namespace = {"caex": "http://www.dke.de/CAEX"}
    outputs_element = root.find('.//caex:InternalElement[@Name="Parameters"]', namespaces=namespace)
    parameters_data = {}

    if outputs_element is not None:
        for internal_element in outputs_element.findall('.//caex:InternalElement', namespaces=namespace):
            internal_element_name = internal_element.get('Name')
            attribute_param = internal_element.find('.//caex:Attribute[@Name="param"]/caex:Value',
                                                     namespaces=namespace)

            if attribute_param is not None :
                param_value = attribute_param.text if attribute_param.text is not None else ''
                parameters_data[internal_element_name]=param_value
    return parameters_data

def workflow_parser(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        workflow_data = {'workflow_type': None, 'phases': [], 'outputs': {}, 'inputs': {}, 'parameters': {}}
        print("workflow_data 1")
        print(workflow_data)
        workflow_data['workflow_type'] = workflow_type_parser(root)
        print("workflow_data 2")
        print(workflow_data)

        workflow_data['inputs'] = inputs_parser(root)
        print("workflow_data 3")
        print(workflow_data)

        workflow_data['outputs'] = outputs_parser(root)
        print("workflow_data 4")
        print(workflow_data)

        workflow_data['phases'] = phases_parser(root)
        print("workflow_data 5")
        print(workflow_data)

        workflow_data['parameters'] = parameters_parser(root)
        print("workflow_data 6")
        print(workflow_data)
        return workflow_data
    except Exception as e:
        print(f"Error: {e}")




def execution(path):
    try:
        result = workflow_parser(path)
        return result
    except Exception as e:
        print(f"Error: {e}")


