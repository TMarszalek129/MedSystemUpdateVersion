function show_hide_buttons(show)
{
    const edit_button = document.getElementById('edit_measure');
    const del_button = document.getElementById('delete_measure');

    if(show == false)
    {
        edit_button.style.display = 'none';
        del_button.style.display = 'none';

    }
    //alert("From global");
}

function to_do_list(problems){

    var ul_element = document.getElementById("myUL");

    const textnode_basic = document.createTextNode("Create account in MedSystem");
    const basic_li = document.createElement("li");
    basic_li.appendChild(textnode_basic);
    ul_element.appendChild(basic_li);

    if(problems[0])
    {
        const textnode_bmi = document.createTextNode("Remember about proper nutition");
        const bmi_li = document.createElement("li");
        bmi_li.appendChild(textnode_bmi);
        ul_element.appendChild(bmi_li);
    }
    if(problems[1])
    {
        const textnode_heart = document.createTextNode("Visit the cardiologist");
        const heart_li = document.createElement("li");
        heart_li.appendChild(textnode_heart);
        ul_element.appendChild(heart_li);
    }


    var to_do_list = document.getElementById("myUL").getElementsByTagName("li");
    var i;

    for(i = 0; i < to_do_list.length; i++)
    {
        var span = document.createElement("SPAN");
        var txt = document.createTextNode("\u00D7");
        span.className = "close";
        span.appendChild(txt);
        to_do_list[i].appendChild(span);

    }
    var close = document.getElementsByClassName("close");
    var i;
    for (i = 0; i < close.length; i++) {
        close[i].onclick = function () {
            var div = this.parentElement;
            div.style.display = "none";
        }
    }
    var list = document.querySelector('ul');
    list.getElementsByTagName("li")[0].classList.toggle('checked')
    list.addEventListener('click', function(ev) {
    if (ev.target.tagName === 'LI') {
        ev.target.classList.toggle('checked');

        }

    }, false);



}
