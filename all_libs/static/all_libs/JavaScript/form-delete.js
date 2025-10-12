del_button.addEventListener('click', function(event) {
    let dirContainer = document.querySelector(".directory_container");
    let button = document.createElement('button')
    let textButton = document.createTextNode('Удалить')
    formDelete = document.createElement('form');
    formDelete.method = 'post';
    formDelete.action = deleteAction;
    formDelete.className = "delete_container";
    button.type = "submit"
    button.class = "button"
    button.append(textButton)

    dirContainer.replaceWith(formDelete);
    formDelete.prepend(dirContainer);
    formDelete.insertAdjacentHTML('beforeend', csrf)
    formDelete.append(button)
    del_button.remove()
})