del_button.addEventListener('click', function(event) {
    commandsName = document.querySelector(commandClassName);
    checkbox = document.createElement('input');
    checkbox.name = checkboxName;
    checkbox.type = "checkbox";
    commandsName.before(checkbox);
})