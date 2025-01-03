# Edit_XML
Model-based engineering (MBSE) is an essential step in the design of a system to automate the evaluation of inconsistencies, dependencies, and information flows before its actual implementation. The primary step in automating the evaluation is in the representation of the system or systems of systems, which can be achieved in a systems modeling language. One such systems modeling language is SysML, which allows users to model a wide variety of diagram types for structural and behavioral representation. SysML leverages the Object Management Group XML Metadata Interchange (XMI) to exchange modeling data between tools. These languages can be interchanged into XMI; however, the XMI generated in modeling environments contains irrelevant information that can be refined using an algorithmic approach. 

Extracting these redundancies is essential to building a knowledge base of the vital components needed to replicate these XMI files outside the modeling environment using NLP strategies. Towards that end, we present XMLSlim, a robust and persistent algorithm that optimizes XML files by modifying elements and attributes without altering their meaning. Specifically, XMLSlim can condense SysML models that comprise Block Definition Diagrams (BDD), Internal Block Diagrams (IBD), and Activity Diagrams (ACT). By implementing XMLSlim on aerospace and electromechanical use cases, we illustrated the effectiveness of our approach with a 60\% reduction in the file size while preserving the model's semantic meaning. This algorithm is built on reverse-engineered information retrieval techniques to assist with our ultimate goal of developing an automated model that generates SysML diagrams from the technical text.

## Contact
For questions, suggestions, or collaborations:

Candice Chambers - chambersc2017@my.fit.edu
Parth Ganeriwala - pganeriwala2022@my.fit.edu
