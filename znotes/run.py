from md import *

# test_note = "../sample_notes/note_1715024200.md"
#
# file_obj = open(test_note, "r")
# ddata = read_note_tags(file_obj)
# file_obj.close()
#
# print(ddata)

tag_list = "../test-files/tags.md"
file_obj = open(tag_list, "r")
ddata = read_tags_and_references(file_obj)
file_obj.close()

print(ddata)
