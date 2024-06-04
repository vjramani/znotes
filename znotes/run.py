from main import *

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


notes_list = [
        "../sample_notes/note_1715024200.md",
        "../sample_notes/note_1715064425.md",
        "../sample_notes/local_pdf_editing_suite_1715924445.md",
        "../sample_notes/load_vim_buffer_from_stdin_1715270271.md",
        "../sample_notes/visual_block_editing_in_vim_1716133283.md",
        "../sample_notes/re-arrange_files_and_folders_in_nvim-tree_1716542092.md",
        "../sample_notes/neovim_get_file_path_of_current_buffer_1716875414.md",
        "../sample_notes/run_zsh_command_from_neo-vim_key_bindings_1716874907.md"
        ]
tag_index_file = "../tag_index.md"

# Load the tag index data, check if the file is present and if not initialize empty tag index
# Load each note and extract tags
# For each tag append a reference to the note to the list
# Write the tag index data to the tag_index file

tag_index = {}
fobj = read_file(tag_index_file)
if fobj is not None:
    tag_index = read_tags_and_references(fobj)
    fobj.close()

tag_index = update_tag_index(tag_index, notes_list)

# for t in tag_index:
#     print(f"Tag: {t}")
#     for r in tag_index[t]:
#         print(f"    {r}")

write_tag_index(tag_index, tag_index_file)

# for n in notes_list:
#     fn = create_note_ref_view(n)
#     print(f"{fn}")
