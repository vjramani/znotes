












if __name__ == "__main__":
    pass












# import markdown_to_json
#
# value = """
# # Nested List
#
# - Item 1
#     - Item 1.1
# - Item 2
#     - Item 2.1
#     - Item 2.2
#         - Item 2.2.1
# """

# The simple way:
# dictified = markdown_to_json.dictify(value)
# assert dictified == {'Nested List': ['Item 1', ['Item 1.1'], 'Item 2']}
# print(dictified)

# Or, if you want a json string
# jsonified = markdown_to_json.jsonify(value)
# assert jsonified == """{"Nested List": ["Item 1", ["Item 1.1"], "Item 2"]}"""
# print(jsonified)


# read the tags from the tag section of a given note
def read_note_tags(fhandle):
    # print("read_note_tags")
    skip_till_line_start(fhandle, "tags:")
    val = read_till_line_start(fhandle, "---")
    val = val.replace("\n","").replace("\r", "").replace("tags:","").replace(" ","")
    return list(filter(None, val.split("#")))

# read all tags from the global list of tags
def read_tags_and_references(fhandle):
    # print("read_tags_and_references")
    tr = {}
    skip_till_line_start(fhandle, "- ")
    while line := fhandle.readline():
        t = line.replace("- ", "").strip()
        links = read_till_line_start(fhandle, "- ").replace("\t-", "").split("\n")
        links = set(map(lambda x: x.strip(), filter(None, links)))
        tr[t] = links

    return tr


def skip_till_line_start(fhandle, sentinel):
    last_pos = fhandle.tell()
    while line := fhandle.readline():
        if line.find(sentinel) == 0:
            break;
        last_pos = fhandle.tell()
    fhandle.seek(last_pos)

def read_till_line_start(fhandle, sentinel):
    last_pos = fhandle.tell()
    fcontent = ""
    while line := fhandle.readline():
        if line.find(sentinel) == 0:
            break;
        fcontent += line
        last_pos = fhandle.tell()
    fhandle.seek(last_pos)

    return fcontent

def add_note_ref(tag_index, note_ref, tags):
    for t in tags:
        if t not in tag_index.keys():
            tag_index[t] = set()

        tag_index[t].add(note_ref);
    return tag_index

def update_tag_index(tag_index, notes_list):
    for n in notes_list:
        fobj = open(n, 'r')
        ntags = read_note_tags(fobj)
        fobj.close()
        add_note_ref(tag_index, n, ntags) 

    return tag_index

