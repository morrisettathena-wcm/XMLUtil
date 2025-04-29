import os
import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo

folder = "20250207165914"

if folder == "":
    raise Exception("empty folder")

tz = ZoneInfo("America/New_York")
now = datetime.now(tz)
current_timeYMDHM = now.strftime("%Y%m%d%H%M")
current_timeYMD = now.strftime("%Y%m%d")
current_timeHM = now.strftime("%H%M%S")
ISO8601Unformat = now.strftime("%Y-%m-%dT%H:%M:%S%z")
ISO8601 = ISO8601Unformat[:-2] + ":" + ISO8601Unformat[-2:]

def setEventID(root: ET.Element):
    eventId = root.get("eventId")
    components = eventId.split("-")
    components[3] = current_timeYMDHM

    subcomponents = components[4].split("_")
    subcomponents[2] = current_timeYMD
    subcomponents[3] = current_timeHM

    components[4] = "_".join(subcomponents)
    newEventId = "-".join(components)

    root.set("eventId", newEventId)

if __name__ == "__main__":
    folderpath = os.path.join("output", folder)
    if not os.path.exists(folderpath):
        raise Exception("doesn't exist")
    cancelpath = os.path.join(folderpath, "cancel")

    if not os.path.exists(cancelpath):
        os.mkdir(cancelpath)

    files = os.listdir(folderpath)
    for file in files:
        if file != "cancel":
            filepath = os.path.join(folderpath, file)
            outputpath = os.path.join(cancelpath, file)
            if not os.path.exists(outputpath):
                tree = ET.parse(filepath)
                root = tree.getroot()
                root.set("eventCd", "C")
                
                setEventID(root)
                tree.write(outputpath)
    