import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo
import os

numEpic = 0
numGX = 5
numEach = 0

def makeXMLs():
    tz = ZoneInfo("America/New_York")
    now = datetime.now(tz)
    form = now.strftime("%Y%m%d%H%M%S")
    output_folder = f"output/{form}"
    os.mkdir(output_folder)

    for _ in range(numEach):
        makeXML(True, output_folder)
        makeXML(False, output_folder)

    for _ in range(numEpic):
        makeXML(True, output_folder)
    
    for _ in range(numGX):
        makeXML(False, output_folder)

def makeXML(UseEpic: bool, output_folder: str):
    ls_f = os.listdir("input")
    xml_list = [file for file in ls_f if file.endswith(".xml")]
    xml = None

    if len(xml_list) == 0:
        raise Exception("No valid xmls present")
    elif len(xml_list) == 1:
        xml = xml_list[0]
    else:
        print("Select which xml to use: (number only)")
        for i, xml_file in enumerate(xml_list):
            print(f'{i + 1}: xml_file')
        selection = input("number: ")
        xml = xml_list[selection-1]
    


    tree = ET.parse(f"input/{xml}")
    root = tree.getroot()

    tz = ZoneInfo("America/New_York")
    now = datetime.now(tz)
    current_timeYMDHM = now.strftime("%Y%m%d%H%M")
    current_timeYMD = now.strftime("%Y%m%d")
    current_timeHM = now.strftime("%H%M%S")
    ISO8601Unformat = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    ISO8601 = ISO8601Unformat[:-2] + ":" + ISO8601Unformat[-2:]

    with open("GX.txt", "r") as file:
        newGXNum = int(file.read())

    with open("GX.txt", "w") as file:
        file.write(str(newGXNum+1))

    if UseEpic:
        with open("Epic.txt", "r") as file:
            epicOrder = int(file.read())

        with open("Epic.txt", "w") as file:
            file.write(str(epicOrder+1))

    def createNewID():
        oldID = root.get("genomicTestCid")
        components = oldID.split("$")
        subcomponents = components[0].split("-")
        subcomponents[1] = str(newGXNum)
        components[0] = "-".join(subcomponents)

        components[2] = current_timeYMDHM
        newID = "$".join(components)
        return newID

    newID = createNewID()

    def setEventID():
        eventId = root.get("eventId")
        components = eventId.split("-")
        components[1] = str(newGXNum)
        components[3] = current_timeYMDHM

        subcomponents = components[4].split("_")
        subcomponents[2] = current_timeYMD
        subcomponents[3] = current_timeHM

        components[4] = "_".join(subcomponents)
        newEventId = "-".join(components)

        root.set("eventId", newEventId)

    def setGenomicTestCid():
        if UseEpic:
            root.set("genomicTestCid", str(epicOrder))
        else:
            root.set("genomicTestCid", newID)

    def setPlacerOrderId():
        root.set("placerOrderId", newID)

    def setPlacerOrderDate():
        root.set("placerOrderDate", ISO8601)

    def setAlias():
        GTOCoreObjectAlias = root.find("aliases[@id='7']").find("GTOCoreObjectAlias[@id='4']")
        GTOCoreObjectAlias.set("alias", newID)

    setEventID()
    setGenomicTestCid()
    setPlacerOrderId()
    setPlacerOrderDate()
    setAlias()

    path = os.path.join(output_folder, root.get("eventId")) + ".xml"
    tree.write(path)
    if UseEpic:
        print("Wrote epic file")
    else:
        print("Wrote GX file")

if __name__ == "__main__":
    makeXMLs()