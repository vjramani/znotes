import typer


__VAULT_ROOT__ = "../vault/"
__VAULT_NOTES__ = "atomic-notes/"
__NEW_NOTE__ = "atomic-notes/"
__NOTE_TEMPLATE__ = "utils/note-template.md"
__TAG_INDEX__ = "utils/tag_index.md"


app = typer.Typer()


@app.command()
def newnote(title: str):
    create_new_note_from_template(title)

@app.command()
def updatetags():
    build_and_update_tag_index()

if __name__ == "__main__":
    app()

def build_and_update_tag_index():
    notes_list = get_note_paths()
    tag_index_file = get_tag_index_path()
    tag_index = {}
    fobj = read_file(tag_index_file)
    if fobj is not None:
        tag_index = read_tags_and_references(fobj)
        fobj.close()

    tag_index = update_tag_index(tag_index, notes_list)
    write_tag_index(tag_index, tag_index_file)

def create_new_note_from_template(title):
    nn_content = create_new_note(title)
    nn_path = write_new_note(title, nn_content)
    open_note_for_editing(nn_path)

def open_note_for_editing(path):
    import subprocess
    subprocess.call(['nvim', '+7', path])

def get_tag_index_path():
    return f"{__VAULT_ROOT__}{__TAG_INDEX__}"

def get_note_paths():
    import os
    notes_folder = f"{__VAULT_NOTES__}"
    lf = [notes_folder+f.name for f in os.scandir(__VAULT_ROOT__+notes_folder) if f.is_file()]
    return lf

def get_note_template_path():
    return f"{__VAULT_ROOT__}{__NOTE_TEMPLATE__}"

def get_new_note_path():
    return f"{__VAULT_ROOT__}{__NEW_NOTE__}"

def create_new_note(title):
    import datetime
    dt = datetime.datetime.today()
    d = dt.strftime('%Y-%m-%d')
    t = dt.strftime('%H:%M')
    fobj = read_file_or_fail(get_note_template_path())
    ncontent = fobj.read()
    fobj.close()
    ncontent = ncontent.replace("{{title}}", title)
    ncontent = ncontent.replace("{{date}}", d).replace("{{time}}", t)
    return ncontent
    
def gen_new_note_filename(title):
    import time
    ts = round(time.time()*1000)
    fn = title.strip().replace(" ", "_")

    return f"{fn}_{ts}.md"

def write_new_note(title, nn_content):
    nn_path = get_new_note_path()
    nn_filename = gen_new_note_filename(title)
    nn_path = f"{nn_path}{nn_filename}"
    fobj = open(nn_path, 'w')
    fobj.write(nn_content)
    fobj.close()
    return nn_path


# read the tags from the tag section of a given note
def read_note_tags(fhandle):
    skip_till_line_start(fhandle, "tags:")
    val = read_till_line_start(fhandle, "---")
    val = val.replace("\n","").replace("\r", "").replace("tags:","").replace(" ","")
    return list(filter(None, val.split("#")))

# read all tags from the global list of tags
def read_tags_and_references(fhandle):
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
        fobj = read_file_or_fail(__VAULT_ROOT__+n)
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







