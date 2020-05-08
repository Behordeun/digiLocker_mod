var contractAddress = "0x25534C00E7AF759E136D41b4eD7e92AbFe387ce5"

var web3 = new Web3(window.web3.currentProvider);
var address = window.web3.currentProvider.selectedAddress;

var contract = new web3.eth.Contract(abi, contractAddress, {
    from: address,
    gasLimit: 3000000,
});

if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function checkWeb3(callback) {
    window.web3.eth.getAccounts(function (err, accounts) { // Check for wallet being locked
        if (err) {
            throw err;
        }
        callback(accounts.length !== 0);
    });
}


$("#logout-btn").click(function (e) {
    e.preventDefault();
    var request = new XMLHttpRequest();
    let logout_url = "/api/logout/metamask";
    request.open('GET', logout_url, true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            var resp = JSON.parse(request.responseText);
            window.location.replace(resp.redirect_url);
        }
        else{
            alert("Logout failed")
        }
    };
    request.onerror = function () {
        alert("Logout failed");
    };
    request.send();
});


function checkAlreadyRegiteredUser(redirect = false){
    contract.methods.isalreadyRegisteredUser().call().then(function(obj){
        if(obj == false){
            window.location.replace("/registration");
            swal({
                title: "Alert!",
                text: "You have to register yourself first!!",
                icon: "warning",
            });
        }
        else{
            if(redirect){
                window.location.replace("/dashboard");
            }
        }
    }).catch(function (error) {
        swal({
            title: "Error!",
            text: "Error while checking user is regitred or not" + error,
            icon: "error",
        });
   });
}