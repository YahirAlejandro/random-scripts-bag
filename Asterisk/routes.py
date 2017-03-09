conf_path = $CONF_PATH

def findAll(conf_path):
    result = []
    for line in open(conf_path):
        if "Dial" in line:
            result.append(line[9:])
    return result

def findByDID(did, results):
    print "DIDs found with %s" % did
    result_dids = []
    for dids in results:
        if did in dids:
            result_dids.append(dids)
    unwrapResults(result_dids)

def findByBox(box_name, results):
    print "Boxes found with %s" % box_name
    result_boxes = []
    for boxes in results:
        if box_name in boxes:
            result_boxes.append(boxes)
    unwrapResults(result_boxes)

def unwrapResults(result_set):
    for i in result_set:
        outputCleaner(i)

def outputCleaner(string):
    dial_app_start = string.index('(')
    dial_app_total = len(string)
    dial_tech = str(string)[dial_app_start:dial_app_total]

    dest_end = string.index(',')
    dest = str(string)[1:dest_end]

    print dest + " -> " + dial_tech

if __name__ == "__main__":
    print (
        "************************************************************************"
        "\n"
        "Enter search terms. Leave blank will show everything. CTRL + C to gtfo"
        "\n"
        "Boxes needs full trunk name: e.g. 'Box123'."
        "\n"
        "************************************************************************"
    )
    find_did = raw_input("Enter the DID: ")
    find_box = raw_input("Enter box name: ")
    results = findAll(conf_path)

    if find_did:
        findByDID(str(find_did), results)
    elif find_box:
        findByBox(str(find_box), results)
    else:
        print results
