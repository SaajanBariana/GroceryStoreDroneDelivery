var totalPrice;
var itemQty = [];
var itemName = [];
var imgSrc = [];
var itemWeight = [];
var itemPrice = [];
var totalQty = [];

function getProductTotal(index) {
    var docNodes = document.getElementsByClassName("qty");
    //var index = document.getElementById("getProdTotal").innerHTML;
    var value = docNodes[index].value;
    docNodes = document.getElementsByClassName("qty-price");
    if(index == 0) {
        docNodes = docNodes[1];
    }
    else {
        docNodes = docNodes[1+(index*2)];
    }
    var priceText = docNodes.innerText;
    priceText = priceText.replace(/^\D+|\D+$/g, "");
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
    totalPrice = z;
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
        var value = docNodes[i].value;
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
        button[0].setAttribute("href", "../home/creditcard");
        
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

function getProductList() {
    for(i = 0; i < itemName.length-1; i++) {
        var ul = document.createElement("ul");
        ul.className = 'cartWrap';
        document.getElementById("myCart").appendChild(ul);

        var li = document.createElement("li");
        li.className = 'items';
        ul.appendChild(li);

        var div = document.createElement("div");
        div.id = "info-wrap";
        li.appendChild(div);

        var div1 = document.createElement("div");
        div1.id = "cart-section";
        div.appendChild(div1);

        var img = document.createElement("img");
        img.src = imgSrc[i];
        img.className = "itemImg";
        div1.appendChild(img);

        var p = document.createElement("p");
        p.className = "item-weight";
        p.innerHTML = "Product Weight: " + itemWeight[i] + "lbs";
        div1.appendChild(p);

        var h3 = document.createElement("h3");
        h3.innerHTML = itemName[i];
        div1.appendChild(h3);

        var p2 = document.createElement("p");
        p2.className = "qty-price";
        div1.appendChild(p2);

        var inp = document.createElement("input");
        inp.type = "number";
        inp.className = "qty";
        inp.id = "qtyIn " + i;
        inp.min = 1;
        inp.value = itemQty[i];
        p2.appendChild(inp);


        var p3 = document.createElement("p");
        p3.className = "qty-price";
        p3.id = "qtyPrice";
        p3.innerText = " x $" + itemPrice[i];
        div1.appendChild(p3);

        var p4 = document.createElement("p");
        p4.className = "stock-status";
        p4.innerText = " In Stock";
        div1.appendChild(p4);

        var div2 = document.createElement("div");
        div2.id = "prodTotal";
        div.appendChild(div2);

        var p5 = document.createElement("p");
        p5.className = "prodTotalCalc";
        p5.id = "pTotal";

        var sc = document.createElement("script");
        sc.innerText = "getProductTotal(" + i + ");";
        p5.appendChild(sc);
        div2.appendChild(p5);

    }
}

function parseMainCookie() {
    var MainCookie = readCookie("MainCookie");
    if (MainCookie != "" && MainCookie != null) //check if that Cookie is empty
    {
      //alert("MainCookie: " + MainCookie);
      var array = MainCookie.split(","); //split that result and turn it into an array with all the items
      itemName = array;                  //put array into global array
      for (var i = 0; i < array.length-1; i++)
      {
          var targetCookie = readCookie(array[i]);    //retrieve each cookie in string format
          targetCookie = targetCookie.split(',');     //split element into array
          itemQty.push(targetCookie[0]);               //this is amt customer want
          itemPrice.push(targetCookie[1]);
          itemWeight.push(targetCookie[2]);
          totalQty.push(targetCookie[3]);
          imgSrc.push(targetCookie[4]);
          //alert("Current cookie being read\nQty: " + itemQty[i] + "\nPrice: " + itemPrice[i] + "\nWeight: " + itemWeight[i] + "\nTotal Quantity: " + totalQty[i] + "\nImages: " + imgSrc[i] );
      }
    }
}

function setCookie(cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = "Total" + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    return decodedCookie;
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return null;
}

$(document).on('click', 'a', function() {
    setCookie(totalPrice, 7);
    alert(getCookie("Total"));
    console.log(getCookie("Total"));
});
