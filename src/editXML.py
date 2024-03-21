import xml.etree.ElementTree as ET
import os
import lxml
from lxml import etree
from lxml.html.clean import Cleaner

# Import XML File
filename = 'data/FCS_XML'
# filename = 'data/SOS_XML(Final)'
# filename = 'data/ASS_XML_v2'

tree = etree.parse('/content/' + filename + '.xml')
root = tree.getroot()

classTag_to_remove = ['isSpecification','ea_ntype','isActive','version','date_created', 'date_modified', 'gentype', 'tagged', 'phase', 'author', 'complexity', 'product_name','status','tpos','ea_localid','ea_eleType','style', '$ea_xref_property']
associationTag_to_remove = ['style','linemode','linecolor','linewidth','seqno','headStyle','lineStyle','ea_localid','ea_sourceID','ea_targetID','virtualInheritance']
collaborationTag_to_remove = ['isAbstract','isSpecification','ea_ntype','version','isActive','date_created','date_modified','gentype','tagged','phase','author','complexity','status','tpos','ea_localid','ea_eleType','style', '$ea_xref_property']
diagramTag_to_remove = ['version','author','created_date','modified_date','type','ea_localid', 'matrixitems','swimlanes','EAStyle']
internalDiagramTag_to_remove = ['version','author','created_date','modified_date','swimlanes','matrixitems','EAStyle']

pop_list = ['visibility', 'isRoot', 'isLeaf', 'isAbstract', 'aggregation', 'isOrdered', 'targetScope', 'changeable', 'isNavigable', 'seqno', 'style']
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
        popAttributes(g,pop_list)

        print("Hello World")

def modifyTag(elem):
  for j in elem:
    for g in j:
      if g.tag == '{omg.org/UML1.3}TaggedValue' and g.attrib['tag'] == 'styleex' and elem.attrib[
        'diagramType'] == 'ClassDiagram':
        g.set('value', 'MDGDgm=SysML1.4::BlockDefinition;SF=1;')
      elif g.tag == '{omg.org/UML1.3}TaggedValue' and g.attrib['tag'] == 'styleex' and elem.attrib[
        'diagramType'] == 'CompositeStructureDiagram':
        g.set('value', 'MDGDgm=SysML1.4::InternalBlock;SF=1;')

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
            elif i.tag == '{omg.org/UML1.3}Collaboration':
              # Namespace.ownedElement
              for k in i:
                # ClassifierRole
                for g in k:
                  removeTag(g, collaborationTag_to_remove)
                  popAttributes(i, pop_list)
editDiagram()
editPackage()
tree.write(filename + '_Condensed.xml')
tree = ET.parse(filename + '_Condensed.xml')
root = tree.getroot()

print(ET.tostring(root, encoding='utf8').decode('utf8'))