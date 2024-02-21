# -*- coding: utf-8 -*-
"""
Created on Sept 15 2023

@author: Jorge Ejarque (BSC)
"""

import importlib
import xml.etree.ElementTree as ET
from PHASES.utils.utilsAML.data import generate_data
from PHASES.utils.utilsAML.software import Software

NAMESPACE = {'aml': 'http://www.dke.de/CAEX',
             'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
WORKFLOW_DEFINITION_TAG = "Workflow_definition"
WORKFLOW_TYPE_TAG = "Type"
WORKFLOW_INPUTS_TAG = "Inputs"
WORKFLOW_OUTPUTS_TAG = "Outputs"
WORKFLOW_PHASES_TAG = "Phases"
WORKFLOW_PHASE_TAG = "Phase"
WORKFLOW_SOFTWARE_TAG = "Software"
PARAMETER_SOURCE_TAG = "source"
PARAMETER_DESTINATION_TAG = "destination"
SOFTWARE_PARAMETERS_TAG = "Parameters"
SOFTWARE_ID_TAG = "id"
PHASE_SEQUENCE_TAG = "sequence"
PHASE_NAME_TAG = "name"


class Workflow:
    def __init__(self, wf_type, inputs, outputs, phases):
        self.type = wf_type
        self.inputs = inputs
        self.outputs = outputs
        self.phases = phases

    def get_object(self):
        module = importlib.import_module(self.module)
        func = getattr(module, self.function)
        return func(self.inputs, self.outputs, self.phases)


class AutomationMLDocument:
    def __init__(self, file_path) -> None:
        tree = ET.parse(file_path)
        self.root = tree.getroot()
        self.workflows = dict()

    def parse(self):
        workflow_elements = self.root.findall(
            './/aml:InternalElement[@Name="{}"]'.format(WORKFLOW_DEFINITION_TAG), NAMESPACE)
        if workflow_elements is None:
            raise Exception("No workflows found in the document")
        for we in workflow_elements:
            name, workflow = parse_workflow(we)
            self.workflows[name] = workflow

    def get_workflows(self):
        return self.workflows


def parse_workflow(workflow_element):
    type = get_attribute_value(workflow_element, WORKFLOW_TYPE_TAG)
    if type is None:
        raise Exception("No Type found in workflow")
    inputs = parse_workflow_parameters(workflow_element, WORKFLOW_INPUTS_TAG, PARAMETER_DESTINATION_TAG)
    outputs = parse_workflow_parameters(workflow_element, WORKFLOW_OUTPUTS_TAG, PARAMETER_SOURCE_TAG)
    phases = parse_phases(workflow_element)
    return type, Workflow(type, inputs, outputs, phases)


def get_internal_elements(wf_element, tag, internal_tag):
    tag_element = wf_element.find(
        './/aml:InternalElement[@Name="{}"]'.format(tag), NAMESPACE)
    if tag_element is None:
        raise Exception("No element of type " + tag + " found in workflow")
    if internal_tag:
        match_str = './/aml:InternalElement[@Name="{}"]'.format(internal_tag)
    else:
        match_str = './/aml:InternalElement'
    elements = tag_element.findall(match_str, NAMESPACE)
    if elements is None:
        raise Exception("No internal elements in " + tag)
    return elements


def parse_workflow_parameters(wf_element, tag, attribute_name):
    params = dict()
    elements = get_internal_elements(wf_element, tag, None)
    if elements is None:
        raise Exception("No internal elements in " + tag)
    for element in elements:
        attribute = element.find(
            './/aml:Attribute[@Name="{}"]'.format(attribute_name), NAMESPACE)
        if attribute is None:
            raise Exception("No attribute " + attribute_name + " in " + tag)
        print("Adding data for " + element.attrib['Name'])
        params[element.attrib['Name']] = get_data_from_attribute(attribute)
    return params


def get_data_from_attribute(attribute):
    attribute_data_type = attribute.attrib['AttributeDataType']
    attribute_value_element = attribute.find('aml:Value', NAMESPACE)

    # Some attributes may not have a Value element, handle accordingly
    if attribute_value_element is not None:
        attribute_value = attribute_value_element.text
    else:
        attribute_value = None
    return generate_data(attribute_data_type, attribute_value)


def parse_parameters(element, tag):
    params = dict()
    params_element = element.find(
        './/aml:InternalElement[@Name="{}"]'.format(tag), NAMESPACE)
    if params_element is None:
        raise Exception("No Parameters of type " + tag + " found in element " + str(element))
    attributes = params_element.findall('.//aml:Attribute', NAMESPACE)
    if attributes is None:
        raise Exception("No Parameters attributes of type " +
                        tag + " found in Parameter")

    # Iterate over the attributes within the internal element
    for attribute in attributes:
        attribute_name = attribute.attrib['Name']
        params[attribute_name] = get_data_from_attribute(attribute)
    return params


def parse_phases(wf_element):
    phases = dict()
    phases_elements = get_internal_elements(wf_element, WORKFLOW_PHASES_TAG, WORKFLOW_PHASE_TAG);
    for phase_element in phases_elements:
        phase_name = get_attribute_value(phase_element, PHASE_NAME_TAG)
        print("Getting Phase: " + phase_name)
        phases[phase_name] = get_phase_from_element(phase_element)
    return phases


def parse_softwares_in_phase(phase_element):
    softwares = dict()
    software_elements = phase_element.findall(
        './/aml:InternalElement[@Name="{}"]'.format(WORKFLOW_SOFTWARE_TAG), NAMESPACE)
    if software_elements is None:
        raise Exception("No Software in phase")
    for element in software_elements:
        name = get_attribute_value(element, SOFTWARE_ID_TAG)
        print("Parsing software: " + name)
        parameters = parse_parameters(element, SOFTWARE_PARAMETERS_TAG)
        mod_name, func_name = name.rsplit('.', 1)
        softwares[name] = Software(mod_name, func_name, parameters)
    return softwares


def get_attribute_value(element, attribute_name):
    attribute = element.find(
        './/aml:Attribute[@Name="{}"]'.format(attribute_name), NAMESPACE)
    if attribute is None:
        raise Exception("No attribute " + attribute_name + " in element " + element.attrib['Name'])
    else:
        value = attribute.find('aml:Value', NAMESPACE)
        if value is None:
            raise Exception("No value in attribute " + attribute_name)
        else:
            return value.text


def get_phase_from_element(element):
    softwares = parse_softwares_in_phase(element)

    seq_element = element.find(
        './/aml:Attribute[@Name="{}"]'.format(PHASE_SEQUENCE_TAG), NAMESPACE)
    if seq_element is None:
        return softwares.values()
    else:
        seq_value = seq_element.find('aml:Value', NAMESPACE)
        if seq_value is None:
            raise Exception("No Value tag in Phase sequence.")
        else:
            sequence = list()
            soft_list = seq_value.text.split(">>")
            print("List: ", soft_list)
            for soft in soft_list:
                sequence.append(softwares[soft])
            return sequence
