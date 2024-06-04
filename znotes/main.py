__VAULT_ROOT__ = "../vault/"
__VAULT_NOTES__ = "atomic-notes/"
__NOTE_TEMPLATE__ = "utils/note-template.md"
__TAG_INDEX__ = "utils/tag_index.md"

if __name__ == "__main__":
    pass


def get_tag_index_path():
    return "{vault_root}{tag_index_path}".format(vault_root = __VAULT_ROOT__, tag_index_path = __TAG_INDEX__)

def get_note_paths():
    import os
    notes_folder = "{vault_root}{notes_path}".format(vault_root = __VAULT_ROOT__, notes_path = __VAULT_NOTES__)
    lf = [notes_folder+f.name for f in os.scandir(notes_folder) if f.is_file()]

    return lf

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

def create_note_ref_view(note_ref):
    n = extract_file_name_from_path(note_ref)
    return "[{n}]({note_ref})".format(n=n, note_ref=note_ref)

def add_note_ref(tag_index, note_ref, tags):
    for t in tags:
        if t not in tag_index.keys():
            tag_index[t] = set()
        tag_index[t].add(create_note_ref_view(note_ref));
    return tag_index

def update_tag_index(tag_index, notes_list):
    for n in notes_list:
        fobj = read_file_or_fail(n)
        ntags = read_note_tags(fobj)
        fobj.close()
        add_note_ref(tag_index, n, ntags) 

    return tag_index

def read_file(path):
    import os.path
    if os.path.exists(path):
        fobj = open(path, 'r')
        return fobj
    return None

def read_file_or_fail(path):
    ret = read_file(path)
    if ret is not None:
        return ret
    raise Exception(f"File not Found at {uri}");


def extract_file_name_from_path(path):
    i0 = path.rfind('/')+1
    i1 = path.rfind('.md')
    fn = path[i0:i1]
    return fn


TAG_INDEX_HEADER = '''
# Tag Index
---

'''
def write_tag_index(tag_index, path):
    fobj = open(path, 'w')
    fobj.writelines(TAG_INDEX_HEADER)
    for t in tag_index:
        fobj.write(f"- {t}\n")
        for l in tag_index[t]:
            fobj.write(f"\t- {l}")
            fobj.write("\n")
    fobj.close()







