
function getProductTotal(index) {
    var docNodes = document.getElementsByClassName("qty");
    //var index = document.getElementById("getProdTotal").innerHTML;
    var value = docNodes[index].getAttribute("value");
    docNodes = document.getElementsByClassName("qty-price");
    if(index == 0) {
        docNodes = docNodes[1];
    }
    else {
        docNodes = docNodes[index+(index*2)];
    }
    var priceText = docNodes.innerText;
    var dollar = "$";
    var total = priceText * value;
    total = total.toFixed(2);
    dollar += total;
    var pTotal = document.getElementsByClassName("prodTotalCalc");
    pTotal[index].innerText = dollar;
    return total
}


function getSubTotal() {
    var prodNodes = document.getElementsByClassName("prodTotalCalc");
    var len = prodNodes.length;
    var acc = 0;
    var dollar = "$";
    for(i = 0; i < len; i++) {
        var value = prodNodes[i].innerText;
        value = value.substr(1);
        value = parseFloat(value);
        var temp = acc;
        acc = temp + value;
    }
    var z = acc.toFixed(2);
    dollar += z;
    var pNode = document.getElementsByClassName("value");
    pNode[0].innerText = dollar;
    return z;
}

function getTax() {
    var subTotal = getSubTotal();
    var tax = subTotal * .09;
    var pNode = document.getElementsByClassName("value");
    var z = tax.toFixed(2);
    var dollar = "$";
    dollar += z;
    pNode[2].innerText = dollar;
    return z;
}
function getFinalTotal() {
    var pNodes = document.getElementsByClassName("value");
    var len = pNodes.length;
    var acc = 0;
    var dollar = "$"
    for(i = 0; i < len - 1; i++) {
        var value = pNodes[i].innerText;
        value = value.substr(1);
        value = parseFloat(value);
        acc = acc + value;
    }
    var z = acc.toFixed(2);
    dollar += z;
    var pNode = document.getElementsByClassName("value");
    pNode[3].innerText = dollar;
    return z;
}

function getWeight(value) {
    var weightNode = document.getElementsByClassName("item-weight");
    var len = weightNode.length;
    var acc = 0;
    for(i = 0; i < len; i++) {
        var text = weightNode[i].innerText;
        var weight = text.replace(/^\D+|\D+$/g, "");
        weight = parseFloat(weight);
        var docNodes = document.getElementsByClassName("qty");
        var value = docNodes[i].getAttribute("value");
        value = parseFloat(value);
        weight = weight * value;
        acc += weight;
    }
    var string = acc + " lbs";
    var pWeight = document.getElementById("weight");
    var inText = pWeight.innerText;
    inText = inText.replace(/^\D+|\D+$/g, "");
    pWeight.innerText = string;
    var button = document.getElementsByClassName("checkout");
    if(acc <= 15) {
        if (inText > 15) {
            changeCheckout("green");
        }
        pWeight.style.color = '#82ca9c';
    }
    else {
        if (inText <= 15) {
            changeCheckout("grey");
        }
        pWeight.style.color = '#ee2323';
    }
    return acc;
}

function changeCheckout(color) {
    var button = document.getElementsByClassName("checkout");
    if (color == "grey") {
        button[0].style.backgroundColor = "#a19c9a";
        button[0].setAttribute("href", "javascript: void(0)");
    }
    else {
        button[0].style.backgroundColor = "#82ca9c";
        button[0].setAttribute("href", "../home/checkout/");
    }

}
function parseIndex(id) {
    var index = id.replace(/^\D+|\D+$/g, "");
    index = parseInt(index);
    return index;
}

function changeValue(id, values) {
    var docNodes = document.getElementsByClassName("qty");
    docNodes[id].setAttribute("value", values);
}

$(document).on('change', 'input', function() {
    var index = parseIndex(event.target.id);
    var value = $(this).val();
    changeValue(index, value);
    getProductTotal(index);
    getSubTotal();
    getTax();
    getFinalTotal();
    getWeight();
});

/**$(document).on('click', 'a', function() {
    $.post("home/shoppingcart",
        {

        }
});**/