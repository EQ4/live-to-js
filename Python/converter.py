#!/usr/bin/python

import argparse
import sys
import xml.etree.ElementTree as ET

# Array to store the samples present in the Live set
samples = []
tracks = []

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
        samples.append(sampleName.replace(" ", "_"))
    
    print "Samples: ", samples

    # Find all audio tracks
    for node in root.findall(".//Tracks/AudioTrack/Name/EffectiveName"):
        trackName = node.attrib.get("Value")
        # To do: remove whitespace from track name
        tracks.append(trackName.replace(" ", "_"))

    print "Tracks: ", tracks

def generatePdPatch(path):
    file = open(path, 'w')
    # Write the initial canvas line
    file.write("#N canvas 203 222 450 300 10;\n")

    # INIT
    # Add the declare objects for extra paths (inside init subpatch)
    file.write("#X declare -path abs;\n")
    file.write("#X declare -path audio;\n")
    file.write("#N canvas 30 30 450 300 init 0;\n")
    file.write("#X obj 30 30 declare -path abs;\n")
    file.write("#X obj 30 50 declare -path audio;\n")
    file.write("#X restore 30 30 pd init;\n")

    # SAMPLES
    # Subpatch for samplebank objects
    file.write("#N canvas 30 50 450 300 samplebanks 0;\n")
    # Starting y-pos for objects
    yPos = 60
    # Create a samplebank object for each sample
    for sample in list(set(samples)):
        sampleObj = "#X obj 30 "+str(yPos)+" u_samplebank "+sample+";\n"
        file.write(sampleObj)
        yPos = yPos+20
    # Close subpatch
    file.write("#X restore 30 50 pd samplebanks;\n")

    # TRACKS
    # Subpatch for tracks
    file.write("#N canvas 30 70 450 300 tracks 0;\n")
    # Starting y-pos for objects
    yPos = 60
    # Create a subpatch for each track
    for track in tracks:
        trackObj = "#X obj 30 "+str(yPos)+" u_track "+track+";\n"
        file.write(trackObj)
        # restoreObj = "#X restore 30 "+str(yPos)+" pd "+track+";\n"
        # file.write(restoreObj)
        yPos = yPos+20
    # Close subpatch
    file.write("#X restore 30 70 pd tracks;\n")

    # Create timebase abstraction
    file.write("#X obj 30 90 u_timebase;\n")
    # Create output abstraction
    file.write("#X obj 30 110 u_output;\n")

    file.close()


if __name__ == "__main__":
    main()
