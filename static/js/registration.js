
$(document).ready(function(){
    checkAlreadyRegiteredUser(true);

    $("#main-loader").hide();
})


$("#registration").submit(function(e){
    e.preventDefault();
    var fname = $("#first_name").val()
    var lname = $("#last_name").val()
    var email = $("#email").val()
    var cno = $("#contact_no").val()
    var mkey = $("#master_key").val()
    var mkey_c = $("#master_key_confirm").val()

    if(mkey != mkey_c){
        alert("Enter master key correctly");
        return false;
    }
    var request = new XMLHttpRequest();
    var register_url = "/api/register/metamask";
    request.open('POST', register_url, true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            var resp = JSON.parse(request.responseText);
            if (resp.success){
                let master_key = "0x" + resp.master_key_hash;
                // calling registerUser method
                // TODO: error resolution: use try catch
                var r = contract.methods.registerUser(
                    fname, lname,email, 1, cno, 
                    master_key, resp.pu
                ).send().then(function(res){
                    // console.log("xx", err, res)
                    window.location.replace(resp.redirect_url);
                    swal({
                        title: "Success!",
                        text: "Registration Successful!! You will recieve credentials via mail.",
                        icon: "success",
                    });
                });
            }
        } else {
            alert("Error in sending mail")
        }
    };

    request.onerror = function () {
        console.log("Registration failed - there was an error");
    };
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    
    // TODO: send the key with encryption
    var formData = 'first_name=' + fname + '&last_name=' + lname;
    formData += "&email=" + email + "&contact_no=" + cno + "&master_key=" + mkey;
    formData += "&user_address=" + address;
    console.log(formData)
    request.send(formData);

})