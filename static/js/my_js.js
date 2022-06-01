let for_sale = document.getElementById("id_for_sale");

for_sale.addEventListener("change", function (e) {

    let text = document.getElementById("id_price");
    if (for_sale.checked) {
        return text.style.visibility = "visible";
    } else {
        text.value = null;
        return text.style.visibility = "hidden";
    }
});


