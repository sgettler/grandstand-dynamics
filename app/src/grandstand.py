# grandstand.py
"""Grandstand FEA model module.

This module provides a representation of a typical FEA model for a grandstand
structure and utility methods for loading FEA output files.
"""

import argparse
from lxml import etree



class Grandstand:
    """Grandstand FEA model object.

    Representation of FEA model data. Limited model including only nodes/joints
    and shell elements/areas as required for dynamics analysis.

    Attributes:
        groups: dict with Group objects
        joints: dict with Joint objects for model nodes/joints
        areas: dict with Area objects for model elements/areas
    """

    def __init__(self):
        self.joints = {}
        self.areas = {}
        self.groups = {}
        self.cases = {}


class Joint:
    """Node/joint with FEA analysis results.

    Attributes:
        cases: dict with OutputCase objects of joint displacements
    """
    def __init__(self):
        self.cases = {}


class Area:
    """Shell element/area.

    Attributes:
        joints: list of joints defining the element
    """

    def __init__(self):
        self.joints = []


class Group:
    """Element group.

    Attributes:
        areas: list of area numbers
    """

    def __init__(self):
        self.areas = []


class OutputCase:
    """Results case.

    Attributes:
        steps: dict with displacement results per step
    """

    def __init__(self):
        self.steps = {}


def load_sap2000_xml(xmlfile):
    """Load FEA model from SAP2000 XML results file."""
    g = Grandstand()
    context = etree.iterparse(xmlfile, events=("start", "end"))
    _, root = next(context)
    currenttag = None
    for event, elem in context:
        if event == "start" and currenttag == None:
            currenttag = elem.tag
        if event == "end" and elem.tag == currenttag:
            if elem.tag == "Program_x0020_Control":
                g.currunits = elem.find("CurrUnits").text
            elif elem.tag == "Groups_x0020_2_x0020_-_x0020_Assignments":
                groupName = elem.find("GroupName").text
                if elem.find("ObjectType").text == "Area":
                    group = g.groups.get(groupName)
                    if group == None:
                        group = Group()
                        g.groups.update({groupName: group})
                    group.areas.append(elem.find("ObjectLabel").text)
            elif elem.tag == "Joint_x0020_Displacements":
                jointNum = elem.find("Joint").text
                joint = g.joints.get(jointNum)
                if joint == None:
                    joint = Joint()
                    g.joints.update({jointNum: joint})
                outputCase = elem.find("OutputCase").text
                case = joint.cases.get(outputCase)
                if case == None:
                    case = OutputCase()
                    joint.cases.update({outputCase: case})
                case.steps.update({elem.find("StepNum").text:
                        float(elem.find("U3").text)})
            elif elem.tag ==\
                    "Objects_x0020_And_x0020_Elements_x0020_-_x0020_Joints":
                jointNum = elem.find("JointElem").text
                joint = g.joints.get(jointNum)
                if joint == None:
                    joint = Joint()
                    g.joints.update({jointNum: joint})
                joint.x = float(elem.find("GlobalX").text)
                joint.y = float(elem.find("GlobalY").text)
            elif elem.tag ==\
                    "Objects_x0020_And_x0020_Elements_x0020_-_x0020_Areas":
                areaNum = elem.find("AreaElem").text
                area = g.areas.get(areaNum)
                if area == None:
                    area = Area()
                    g.areas.update({areaNum: area})
                area.label = elem.find("AreaObject").text
                area.joint1 = g.joints.get(elem.find("ElemJt1").text)
                area.joint2 = g.joints.get(elem.find("ElemJt2").text)
                area.joint3 = g.joints.get(elem.find("ElemJt3").text)
                area.joint4 = g.joints.get(elem.find("ElemJt4").text)
            elif elem.tag ==\
                    "Modal_x0020_Periods_x0020_And_x0020_Frequencies":
                outputCase = elem.find("OutputCase").text
                case = g.cases.get(outputCase)
                if case == None:
                    case = OutputCase()
                    g.cases.update({outputCase: case})
                case.steps.update({elem.find("StepNum").text:
                    float(elem.find("Frequency").text)})
            currenttag = None
            root.clear()
    return g



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="FEA model source")
    args = parser.parse_args()

    with open(args.inputfile, "rb") as xmlfile:
        g = load_sap2000_xml(xmlfile)
        print(len(g.joints),"joint(s) found")
        print(len(g.areas),"area(s) found")
        print(len(g.groups),"group(s) found:")
        for groupName, group in g.groups.items():
            print(groupName,"with",len(group.areas),"area objects")
        print(len(g.cases),"case(s) found:")
        for outputCase, case in g.cases.items():
            print(outputCase,"with",len(case.steps),"steps")
