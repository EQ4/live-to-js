#!/usr/bin/python

import argparse
import sys
import xml.etree.ElementTree as ET

# Array to store the samples present in the Live set
samples = []

def main():
    parser = argparse.ArgumentParser(
        description="Converts an Ableton XML file to a Pd patch.")
    parser.add_argument(
        "live_xml_file",
        help="A path to an unzipped XML file of an Ableton Live set.")
    parser.add_argument(
        "pd_output_file",
        help="A path to where the generated Pd patch will go.")
    args = parser.parse_args()

    parseLiveXML(args.live_xml_file)
    generatePdPatch(args.pd_output_file)

def parseLiveXML(file):
    tree = ET.parse(file)
    root = tree.getroot()

    # Find all Name elements (child of FileRef and SampleRef)
    for node in root.findall(".//SampleRef/FileRef/Name"):
        # Get the name of the sample and add it to the samples array
        sampleName = node.attrib.get("Value")
        samples.append(sampleName)
    
    print "Samples: ", samples

def generatePdPatch(path):
    file = open(path, 'w')
    # Write the initial canvas line
    file.write("#N canvas 203 222 450 300 10;")

    # Create a samplebank object for each sample
    for sample in samples:
        sampleObj = "#X obj 30 30 u_samplebank "+sample 
        file.write(sampleObj)

    file.close()


if __name__ == "__main__":
    main()
