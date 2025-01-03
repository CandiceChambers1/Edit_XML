import xml.etree.ElementTree as ET
import os
import lxml
from lxml import etree
from lxml.html.clean import Cleaner

# Import XML File
filename = r'C:\Users\candice\PycharmProjects\Edit_XML\data\FCS_XML'
# filename = r'C:\Users\candice\PycharmProjects\Edit_XML\data\ASS_XML_v2'
# filename = r"C:\Users\candi\PycharmProjects\Edit_XML\data\coffeemaker_manual_2024"
# filename = r"C:\Users\candice\PycharmProjects\Edit_XML\data\coffeemaker_manual_2024"
tree = etree.parse(filename + '.xml')
root = tree.getroot()

classTag_to_remove = ['isSpecification', 'ea_ntype', 'isActive', 'version', 'date_created', 'date_modified', 'gentype',
                      'tagged', 'phase', 'author', 'complexity', 'product_name', 'status', 'tpos', 'ea_localid',
                      'ea_eleType', 'style', '$ea_xref_property']
associationTag_to_remove = ['style', 'linemode', 'linecolor', 'linewidth', 'seqno', 'headStyle', 'lineStyle',
                            'ea_localid', 'ea_sourceID', 'ea_targetID', 'virtualInheritance']

collaborationTag_to_remove = ['isAbstract', 'isSpecification', 'ea_ntype', 'version', 'isActive', 'date_created',
                              'date_modified', 'gentype', 'tagged', 'phase', 'author', 'complexity', 'status', 'tpos',
                              'ea_localid', 'ea_eleType', 'style', '$ea_xref_property']

collabActivityTag_to_remove = ['isAbstract', 'isSpecification', 'ea_ntype', 'version', 'isActive', 'date_created',
                               'date_modified', 'gentype', 'tagged', 'phase', 'author', 'complexity', 'status', 'tpos',
                               'ea_localid', 'ea_eleType', 'style']

diagramTag_to_remove = ['version', 'author', 'created_date', 'modified_date', 'type', 'ea_localid', 'matrixitems',
                        'swimlanes', 'EAStyle']
internalDiagramTag_to_remove = ['version', 'author', 'created_date', 'modified_date', 'swimlanes', 'matrixitems',
                                'EAStyle']
transitionTag_to_remove = ['style', 'linemode', 'linecolor', 'linewidth', 'seqno', 'headStyle', 'lineStyle',
                           'ea_localid', 'ea_sourceID', 'ea_targetID', 'virtualInheritance', 'src_visibility',
                           'src_aggregation', 'src_isOrdered', 'src_targetScope', 'src_changeable', 'src_isNavigable',
                           'src_containment', 'src_style', 'dst_visibility', 'dst_aggregation', 'dst_isOrdered',
                           'dst_targetScope', 'dst_changeable', 'dst_isNavigable', 'dst_containment', 'dst_style',
                           'privatedata5']
actionTag_to_remove = ['isAbstract', 'isSpecification', 'ea_ntype', 'version', 'isActive', 'date_created',
                       'date_modified', 'gentype', 'tagged', 'phase', 'author', 'complexity', 'status', 'tpos',
                       'ea_localid', 'ea_eleType', 'style', '$ea_xref_property']
pop_list = ['visibility', 'isRoot', 'isLeaf', 'isAbstract', 'aggregation', 'isOrdered', 'targetScope', 'changeable',
            'isNavigable', 'seqno', 'style']
activityDiagramTag_to_remove = ['version', 'author', 'created_date', 'modified_date', 'swimlanes', 'matrixitems',
                                'EAStyle']
blockName = []


def popAttributes(elem, pop_list):
    for attrib in elem.attrib:
        if attrib in pop_list:
            elem.attrib.pop(attrib)


def removeTag(elem, remove_list):
    # ModelElement.taggedValue
    for j in elem:
        if j.tag == '{omg.org/UML1.3}ModelElement.taggedValue':
            # TaggedValue
            for g in j:
                if g.tag == '{omg.org/UML1.3}TaggedValue':
                    if g.attrib['tag'] in remove_list:
                        j.remove(g)

        elif j.tag == '{omg.org/UML1.3}Diagram.element':
            # print('here')
            for g in j:
                popAttributes(g, pop_list)


def modifyTag(elem):
    for j in elem:
        for g in j:
            if g.tag == '{omg.org/UML1.3}TaggedValue' and g.attrib['tag'] == 'styleex' and elem.attrib[
                'diagramType'] == 'ClassDiagram':
                g.set('value', 'MDGDgm=SysML1.4::BlockDefinition;SF=1;')
            elif g.tag == '{omg.org/UML1.3}TaggedValue' and g.attrib['tag'] == 'styleex' and elem.attrib[
                'diagramType'] == 'CompositeStructureDiagram':
                g.set('value', 'MDGDgm=SysML1.4::InternalBlock;SF=1;')
            ## MDGDgm=SysML1.4::Activity;SF=1;


def removeAssociationEnd(elem):
    for j in elem:
        if j.tag == '{omg.org/UML1.3}Association.connection':
            for i in j:
                popAttributes(i, pop_list)
                for k in i:
                    i.remove(k)


def modifyIBD_Blocks(elem, remove_list):
    unwanted = {'ea_ntype', '$ea_xref_property'}

    if elem.attrib['name'] in blockName:
        remove_list = [e for e in remove_list if e not in unwanted]
        removeTag(elem, remove_list)
        popAttributes(elem, pop_list)
    else:
        removeTag(elem, remove_list)
        popAttributes(elem, pop_list)


def editDiagram():
    for elem in root.iter():
        if elem.tag == '{omg.org/UML1.3}Diagram' and elem.attrib['diagramType'] == 'ClassDiagram':
            removeTag(elem, diagramTag_to_remove)
            modifyTag(elem)
        elif elem.tag == '{omg.org/UML1.3}Diagram' and elem.attrib['diagramType'] == 'CompositeStructureDiagram':
            removeTag(elem, internalDiagramTag_to_remove)
            modifyTag(elem)
            blockName.append(elem.attrib['name'])
        elif elem.tag == '{omg.org/UML1.3}Diagram' and elem.attrib['diagramType'] == 'ActivityDiagram':
            removeTag(elem, activityDiagramTag_to_remove)
            # modifyTag(elem)


def process_tag(elem, g, i, value, remove_list):
    if elem.attrib['value'] == value:
        removeTag(g, remove_list)
        popAttributes(i, pop_list)


def editPackage():
    for elem in root.iter():

        if elem.tag == '{omg.org/UML1.3}Package':
            for j in elem:
                if j.tag == '{omg.org/UML1.3}ModelElement.taggedValue':
                    elem.remove(j)
                else:
                    for i in j:
                        if i.tag == '{omg.org/UML1.3}Class':
                            if i[0].tag == '{omg.org/UML1.3}ModelElement.stereotype':
                                modifyIBD_Blocks(i, classTag_to_remove)
                            else:
                                removeTag(i, classTag_to_remove)
                                popAttributes(i, pop_list)
                        elif i.tag == '{omg.org/UML1.3}Association':
                            removeTag(i, associationTag_to_remove)
                            popAttributes(i, pop_list)
                            removeAssociationEnd(i)
                        elif i.tag == '{omg.org/UML1.3}ActivityModel':
                            for k in i:
                                # print(k)
                                if k.tag == '{omg.org/UML1.3}StateMachine.transitions':
                                    for g in k:
                                        # Remove stuff from transitions
                                        removeTag(g, transitionTag_to_remove)
                                        popAttributes(g, pop_list)
                                        # print(g)
                                elif k.tag == '{omg.org/UML1.3}StateMachine.top':
                                    for g in k:
                                        for j in g:
                                            for u in j:
                                                # Remove stuff from action state
                                                removeTag(u, actionTag_to_remove)
                                                popAttributes(u, pop_list)
                                                # print(u)

                        elif i.tag == '{omg.org/UML1.3}Collaboration':
                            # Namespace.ownedElement
                            for k in i:
                                # ClassifierRole
                                for g in k:
                                    # print(g.attrib['name'])
                                    for u in g.iter('{omg.org/UML1.3}TaggedValue'):
                                        # print("U           " + u.attrib['tag'])
                                        process_tag(u, g, i, 'ActivityParameter', collabActivityTag_to_remove)
                                        process_tag(u, g, i, 'ActionPin', collaborationTag_to_remove)
                                        process_tag(u, g, i, 'Part', collaborationTag_to_remove)

editDiagram()
editPackage()
tree.write(filename + '_Condensed.xml')
tree = ET.parse(filename + '_Condensed.xml')
# root = tree.getroot()

# print(ET.tostring(root, encoding='utf8').decode('utf8'))
