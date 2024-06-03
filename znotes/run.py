from main import *
import os.path

# test_note = "../sample_notes/note_1715024200.md"
#
# file_obj = open(test_note, "r")
# ddata = read_note_tags(file_obj)
# file_obj.close()
#
# print(ddata)

# tag_list = "../test-files/tags.md"
# file_obj = open(tag_list, "r")
# ddata = read_tags_and_references(file_obj)
# file_obj.close()
#
# print(ddata)


notes_list = ["../sample_notes/note_1715024200.md","../sample_notes/note_1715064425.md","../sample_notes/local_pdf_editing_suite_1715924445.md"]
tag_index_file = "../tag_index.md"

# Load the tag index data, check if the file is present and if not initialize empty tag index
# Load each note and extract tags
# For each tag append a reference to the note to the list
# Write the tag index data to the tag_index file

tag_index = {}
if os.path.exists(tag_index_file):
    file_obj = open(tag_index_file, 'r')
    tag_index = read_tags_and_references(file_obj)
    file_obj.close()

print(f"tag_index: {tag_index}")

tag_index = update_tag_index(tag_index, notes_list)

print("tag_index:")
for t in tag_index:
    print(f"Tag: {t}")
    for n in tag_index[t]:
        print(f"\t {n}")
