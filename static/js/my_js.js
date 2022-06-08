let for_sale = document.getElementById("id_for_sale");
let recipient_username = '';
let recipient = '';

function get_recipient_username() {
    recipient_username = document.getElementById('recipient-username').innerText;
    console.log(recipient_username)
}

function set_recipient_username() {
    recipient = document.querySelector('input[name="recipient"]').value = recipient_username;
    console.log(recipient)
}


for_sale.addEventListener("change", function (e) {

    let text = document.getElementById("id_price");
    if (for_sale.checked) {
        return text.style.visibility = "visible";
    } else {
        text.value = null;
        return text.style.visibility = "hidden";
    }
});

// search

// profile
