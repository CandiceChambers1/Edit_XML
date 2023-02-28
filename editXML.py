import xml.etree.ElementTree as ET
import os
import lxml
from lxml import etree
from lxml.html.clean import Cleaner

# Import XML File
tree = etree.parse('C:\Users\candi\PycharmProjects\pythonProject\SOS_XML(with tags and connections)_v2.xml')

root = tree.getroot()

classTag_to_remove = ['isSpecification','ea_ntype','isActive','version','date_created', 'date_modified', 'gentype', 'tagged', 'phase', 'author', 'complexity', 'product_name','status','tpos','ea_localid','ea_eleType','style']
associationTag_to_remove = ['style','linemode','linecolor','linewidth','seqno','headStyle','lineStyle','ea_localid','ea_sourceID','ea_targetID','virtualInheritance']
collaborationTag_to_remove = ['isAbstract','isSpecification','ea_ntype','version','isActive','date_created','date_modified','gentype','tagged','phase','author','complexity','status','tpos','ea_localid','ea_eleType','style']
diagramTag_to_remove = ['version','author','created_date','modified_date','type','ea_localid','swimlanes','EAStyle']
internalDiagramTag_to_remove = ['version','author','created_date','modified_date','swimlanes','matrixitems','EAStyle']

def removeTag(elem, remove_list):
  # ModelElement.taggedValue
  for j in elem:
    # TaggedValue
        for g in j:
          if g.tag == '{omg.org/UML1.3}TaggedValue':
            if g.attrib['tag'] in remove_list:
              j.remove(g)

def editXML():
  for elem in root.iter():
    if elem.tag == '{omg.org/UML1.3}Class':
      removeTag(elem, classTag_to_remove)
    elif elem.tag == '{omg.org/UML1.3}Association':
      removeTag(elem, associationTag_to_remove)
    elif elem.tag == '{omg.org/UML1.3}Diagram' and elem.attrib['diagramType'] == 'ClassDiagram':
      removeTag(elem, diagramTag_to_remove)
    elif elem.tag == '{omg.org/UML1.3}Diagram' and elem.attrib['diagramType'] == 'CompositeStructureDiagram':
      removeTag(elem, internalDiagramTag_to_remove)
    elif elem.tag == '{omg.org/UML1.3}Collaboration':
      # Namespace.ownedElement
      for j in elem:
        # ClassifierRole
        for g in j:
          removeTag(g, collaborationTag_to_remove)

editXML()
tree.write('output.xml')
tree = ET.parse('output.xml')
root = tree.getroot()

print(ET.tostring(root, encoding='utf8').decode('utf8'))