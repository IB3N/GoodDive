let hint = 'null';
function display() {
    hint = 'Please use a simple password. Not your regular password. This site is not yet fully secure.';
    document.querySelector('#display-hint').innerHTML = hint;
}