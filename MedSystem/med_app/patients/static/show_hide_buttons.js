function show_hide_buttons(show)
{
    const edit_button = document.getElementById('edit_measure')
    const del_button = document.getElementById('delete_measure')

    if(show == false)
    {
        edit_button.style.display = 'none'
        del_button.style.display = 'none'
    }

}