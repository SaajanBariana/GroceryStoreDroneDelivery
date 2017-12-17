var totalPrice;
var itemQty = [];
var itemName = [];
var imgSrc = [];
var itemWeight = [];
var itemPrice = [];
var totalQty = [];
var deleteItems = [];

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
    docNodes[id].value = values;
}

$(document).on('change', 'input', function() {
               var index = parseIndex(event.target.id);
               var value = $(this).val();
               if (parseInt(value) > parseInt(totalQty[index])) {
               value = totalQty[index];
               }
               var status = stockChecker(index, value);
               var node = document.getElementsByClassName('stock-status');
               if (status == 'out of stock') {
               node[index].style.color = '#ee2323';
               node[index].innerText = 'out of stock';
               }
               else {
               node[index].style.color = '#82ca9c';
               node[index].innerText = 'in stock';
               }
               updateItemCookie(index, value);
               changeValue(index, value);
               getProductTotal(index);
               getSubTotal();
               getTax();
               getFinalTotal();
               getWeight();
               });
function updateItemCookie(index, value) {
    var cookie = readCookie(itemName[index]);
    if (cookie != "" && cookie != null) //check if that Cookie is empty
    {
        //alert("MainCookie: " + MainCookie);
        var array = cookie.split(",");
        createCookie(itemName[index], value + ',' + array[1] + ',' + array[2] + ',' + array[3] + ',' + array[4], 1);
    }
}
function getProductList() {
    for(i = 0; i < itemName.length-1; i++) {
        var ul = document.createElement("ul");
        ul.className = 'cartWrap' + " " + i;
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

        var div5 = document.createElement("div");
        div5.className = "prodinfo-container";
        div1.appendChild(div5);

        var p = document.createElement("p");
        p.className = "item-weight";
        p.innerHTML = "Product Weight: " + itemWeight[i] + "lbs";
        div5.appendChild(p);

        // var h3 = document.createElement("h3");
        // h3.innerHTML = itemName[i];
        // div5.appendChild(h3);

        var div4 = document.createElement("div");
        div4.id = 'pContainer';
        div5.appendChild(div4);

        var p2 = document.createElement("p");
        p2.className = "qty-price";
        div4.appendChild(p2);

        var inp = document.createElement("input");
        inp.type = "number";
        inp.className = "qty";
        inp.id = "qtyIn " + i;
        inp.min = 1;
        inp.max = totalQty[i];
        inp.value = itemQty[i];
        p2.appendChild(inp);


        var p3 = document.createElement("p");
        p3.className = "qty-price";
        p3.id = "qtyPrice";
        p3.innerText = " x $" + itemPrice[i];
        div4.appendChild(p3);

        var p4 = document.createElement("p");
        p4.className = "stock-status";
        var status = stockChecker(i, itemQty[i]);
        p4.innerText = status;
        if (status == 'in stock') {
            p4.style.color = '#82ca9c';
        }
        else {
            p4.style.color = '#ee2323';
        }
        div4.appendChild(p4);

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

        var button = document.createElement('button');
        button.className = 'delete-item';
        div2.appendChild(button);

        var div3 = document.createElement("div");
        div3.style.clear = 'both';
        div.appendChild(div3);
    }
}

function stockChecker(index, value) {
    var status = "out of stock";
    var inventory = totalQty[index];
    if (parseInt(inventory)>parseInt(value)){
        status = "in stock";
    }
    return status;
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
            if (targetCookie != null || targetCookie != "")
            {
                targetCookie = targetCookie.split(',');     //split element into array
                itemQty.push(targetCookie[0]);               //this is amt customer want
                itemPrice.push(targetCookie[1]);
                itemWeight.push(targetCookie[2]);
                totalQty.push(targetCookie[3]);
                imgSrc.push(targetCookie[4]);
            }
            //alert("Current cookie being read\nQty: " + itemQty[i] + "\nPrice: " + itemPrice[i] + "\nWeight: " + itemWeight[i] + "\nTotal Quantity: " + totalQty[i] + "\nImages: " + imgSrc[i] );
        }
    }
    else {
        changeCheckout('grey');
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

$(document).on('click', '.checkout', function() {
               setCookie(totalPrice, 7);
               //alert(getCookie("Total"));
               console.log(getCookie("Total"));
               });

$(document).on('click', '.goback', function() {

               createCookie("MainCookie", newItems, 1);
               setCookie(totalPrice, 7);
               //alert(getCookie("Total"));
               console.log(getCookie("Total"));
               });

$(document).on('click', 'a', function() {
               if (deleteItems.length >0){
               for (var i = 0; i < deleteItems.length; i++) {
               createCookie(deleteItems[i], "", -1);
               }
               }

               });
$(document).on('click', '.delete-item', function() {
               var parent = $(this).parent().parent().parent().parent();
               var cart = parent.parent();
               var index = parseInt(parent[0].className.replace ( /[^\d.]/g, '' ));
               cart[0].removeChild(parent[0]);
               deleteUpdate(index);
               });

function deleteUpdate(index) {
    deleteItems[deleteItems.length] = itemName[index];
    createCookie(itemName[index], "", -1);
    console.log(
                [itemQty.splice(index, 1),
                 itemName.splice(index, 1),
                 imgSrc.splice(index,1),
                 itemWeight.splice(index,1),
                 itemPrice.splice(index,1),
                 totalQty.splice(index,1)]
                );
    createCookie("MainCookie", itemName.join(), 1);
    getSubTotal();
    getTax();
    getFinalTotal();
    getWeight();
    checkCookie();

}

function createCookie(name,value,days)
{
    if (days)
    {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 *1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else
    {
        var expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}
function checkCookie() {
    var MainCookie = readCookie("MainCookie");
    if (MainCookie == "") {
        changeCheckout('grey');
    }
}
// function checkAmountOfItems()
// {
//   var MainCookie = readCookie("MainCookie");
//   if(MainCookie != "" and MainCookie != null)
//   {
//     window.location.href = '/home/creditcard';
//   }
//   else {
//     alert("No items currently in the cart");
//   }
// }
