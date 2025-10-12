let fields = document.querySelector('.images-form')
let form = document.querySelectorAll(".image-container");
let cont = document.querySelector(".images-container");
let total = document.querySelector("#id_form-TOTAL_FORMS");
let maxCountForm = Number(document.querySelector("#id_form-MAX_NUM_FORMS").value) / 2;
console.log(maxCountForm)
let addIcon = document.querySelector('.add_entry_im')
let formNum = form.length - 1;
let plus = document.querySelectorAll('.input__file-icon')[formNum].getAttribute('src')
let inputLabel = document.querySelectorAll('.add_entry_photo_input')[formNum]

function countWarn() {
    let warn = document.querySelector('.add_img_entry > section');
    warn = document.createElement('section');
    textWarn = document.createTextNode("Нельзя добавить более 4 изображений");
    warn.appendChild(textWarn);
    warn.style.backgroundColor = '#3467eb';
    warn.style.position = 'absolute';
    warn.style.textAlign = 'center';
    warn.style.margin = '1rem';
    warn.style.color = '#fff';
    warn.style.padding = '0.5rem';
    warn.style.borderRadius = '5px';
    warn.setAttribute('class', 'warn');
    form[formNum].after(warn);
}
function delWarn()
{
    let child = document.querySelector('.warn');
    if (child) {
        fields.removeChild(child);
    }
}

function changeFormNum(deleteNum)
{
    let inputs = document.querySelectorAll('.add_entry_photo_input')
    for (let ind = deleteNum +1; ind <= inputs.length; ind++)
    {
        let current = document.getElementById(`form-${ind}-image-clear_id`)
        if (current)
        {
            current.setAttribute('id', `form-${ind-1}-image-clear_id`)
            current.setAttribute('name', `form-${ind-1}-image`)
            let label = current.parentNode.querySelector('label');
            label.setAttribute('for', `form-${ind-1}-image-clear_id`)
            if (!(ind == inputs.length))
            {
                current.removeEventListener('input', addForm)
                current.removeEventListener('click', checkImagesCount)
            } else
            {
                current.addEventListener('input', addForm)
                current.addEventListener('click', checkImagesCount)
                current.addEventListener('change', setPreviewImage)
            }
        }
    }
}

function deleteImageAndForm(event)
{
    let parent = this.parentNode.parentNode;
    let deleteCheckbox = parent.querySelector('.delete_image_checkbox');
    deleteCheckbox.checked = true;
    maxCountForm++;
    parent.style.display = "none";
}


function addForm(event)
{
    form = document.querySelectorAll(".image-container")
    if (form.length <= maxCountForm + 1)
    {
        formNum = form.length - 1
        let newForm = form[formNum].cloneNode(true);
        console.log(newForm)
        let img = newForm.querySelector('.input__file-icon')
        img.setAttribute('src', plus)
        let formRegex = RegExp(`form-(\\d){1}-`, 'g');
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum+1}-`);

        let cancel = form[formNum].querySelector(".clearble_icon_container")
        cancel.style.display = 'flex';
        cancel.style.width = '50%';
        cancel.style.justifyContent = 'center';
        cancel.style.alignItems = 'center';
        cancel.style.padding = '0.5rem';
        cancel.addEventListener('click', deleteForm);
        cancel = newForm.querySelector(".clearble_icon_container")
        cancel.style.display = 'none';



        form[formNum].after(newForm);

        inputLabel.removeEventListener('input', addForm)
        inputLabel = newForm.querySelector('.add_entry_photo_input')
        inputLabel.addEventListener('input', addForm)
        inputLabel.addEventListener('click', checkImagesCount)
        inputLabel.addEventListener('change', setPreviewImage)
    }
    total.setAttribute('value', `${form.length}`);
}

function checkImagesCount(event)
{
    let form = document.querySelectorAll(".image-container")
    if (form.length > maxCountForm)
    {
        event.preventDefault()

        setTimeout(countWarn, 0);
        setTimeout(delWarn, 2000);
    }
}

function setPreviewImage(event)
{
    if (this.files) {
        var file = this.files;
        var parent = this.parentNode
        var inputImg = parent.querySelector('.input__file-icon')
        var currentFile = file[file.length - 1]
        inputImg.setAttribute('src', URL.createObjectURL(currentFile))
    }
}

function deleteForm(e)
{
    var par = this.parentNode;
    num = Number(par.querySelector('.add_entry_photo_input').getAttribute('id').match(/\d/));
    var parChild = par.parentNode;
    par = parChild.parentNode;
    par.removeChild(parChild);
    changeFormNum(num)
}

let initial_form_cancel = document.querySelectorAll('.clearble_icon_initial_container');
for (let block=0; block<=initial_form_cancel.length - 1; block++)
{
    initial_form_cancel[block].addEventListener('click', deleteImageAndForm);
}

inputLabel.addEventListener('click', checkImagesCount)
inputLabel.addEventListener('input', addForm)
inputLabel.addEventListener('change', setPreviewImage)

