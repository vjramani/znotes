# create a new note with a title string as the first argument
nn ()
{
    note_title=$1
    if [[ -z $1 ]]; then
        note_title="new_note"
    fi

    vault_dir=$HOME/Documents/obsidian-vaults/main

    file_name=$(echo $note_title | sed "s| |_|g")

    note_file="$vault_dir/atomic-notes/${file_name}_$(date +%s).md"
    note_date="$(date +%Y-%m-%d)"
    note_time="$(date +%H:%M)"

    cp $vault_dir/templates/note.md $note_file

    sed -i .bak "s|{{title}}|$note_title|g" $note_file
    sed -i .bak "s|{{date}}|$note_date|g" $note_file
    sed -i .bak "s|{{time}}|$note_time|g" $note_file

    rm ${note_file}.bak

    nvim +7 $note_file
}

nt()
{
    if [[ -n $1 ]]; then
        echo "tester-function: $1"
    else
        echo "tester-function -"
    fi

}
