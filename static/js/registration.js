function checkRegiterededUser() {
  getContract();
  contract.methods
    .isalreadyRegisteredUser()
    .call()
    .then(function (obj) {
      if (obj == true) {
        window.location.replace("/dashboard");
      }
    })
    .catch(function (error) {
      swal({
        title: "Error!",
        text: "Error while checking user is regitred or not" + error,
        icon: "error",
        allowOutsideClick: false,
        closeOnClickOutside: false,
      });
    });
}

$(document).ready(function () {
  $("#main-loader").hide().fadeOut("slow");
  $(".collapsible").collapsible();
  $("#dash_btn a").removeAttr("href");
  checkRegiterededUser();
});

$("#resident_registration").submit(function (e) {
  e.preventDefault();
  $("#main-loader").show();

  $(".btn").attr("disabled", true);

  var fname = $("#first_name").val();
  var lname = $("#last_name").val();
  var email = $("#email").val();
  var confirm_email = $("#confirm_email").val();

  var cno = $("#contact_no").val();
  var mkey = $("#master_key").val();
  var mkey_c = $("#master_key_confirm").val();

  if (mkey != mkey_c) {
    swal({
      title: "Warning!",
      text: "Enter master key correctly.",
      icon: "warning",
      allowOutsideClick: false,
      closeOnClickOutside: false,
    });
    return false;
  }

  if (email != confirm_email) {
    swal({
      title: "Warning!",
      text: "Enter email correctly.",
      icon: "warning",
      allowOutsideClick: false,
      closeOnClickOutside: false,
    });
    return false;
  }

  $("#main-loader").show();
  var request = new XMLHttpRequest();
  var register_url = "/api/user/registration/";
  request.open("POST", register_url, true);
  request.onload = function () {
    $("#main-loader").hide().fadeOut("slow");

    if (request.status == 200) {
      // Success!
      var resp = JSON.parse(request.responseText);
      if (resp.success) {
        let access_key = "0x" + resp.master_key_hash;
        let pu = "";
        let utype = 1;
        // calling registerUser method
        // TODO: error resolution: use try catch
        var r = contract.methods
          .registerUser(fname, lname, email, utype, cno, access_key, pu)
          .send()
          .then(function (res) {
            // console.log("xx", err, res)
            swal({
              title: "Success!",
              text: "Registration Successful!! You will recieve credentials via mail.",
              icon: "success",
              allowOutsideClick: false,
              closeOnClickOutside: false,
            }).then((value) => {
              if (value) window.location.replace(resp.redirect_url);
            });
          })
          .catch(function (error) {
            $(".btn").attr("disabled", false);
            console.log("Registration failed - " + error.message);
          });
      }
    } else {
      alert("Error in sending mail");
    }
  };

  request.onerror = function () {
    $("#main-loader").hide().fadeOut("slow");
    console.log("Registration failed - there was an error");
  };
  request.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded; charset=UTF-8",
  );
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

  // TODO: send the key with encryption
  var formData =
    "first_name=" + fname + "&last_name=" + lname + "&utype=" + "1";
  formData += "&email=" + email + "&contact_no=" + cno + "&master_key=" + mkey;
  formData += "&user_address=" + address;
  $("#main-loader").show();
  request.send(formData);
  $("#main-loader").hide().fadeOut("slow");
});

var masterKeyValid = false;

function validateMasterCode() {
  data = {
    master_code: $("#master_code").val(),
  };
  $.ajax({
    url: "/api/get/verify/master/code",
    data: data,
    type: "GET",
    success: function (res) {
      if (res.valid == false) {
        swal({
          title: "Master code invalid",
          text: "Please enter the master Code corrctly!",
          icon: "warning",
          allowOutsideClick: false,
          closeOnClickOutside: false,
        }).then((value) => {
          if (value) {
            $("#master_code").val("");
            $("#master_code").focus();
            masterKeyValid = false;
          }
        });
      } else masterKeyValid = true;
    },
    error: function (res) {
      console.log(res, "error");
    },
  });
}

$("#master_code").focusout(function () {
  if ($("#master_code").val().length != 0) validateMasterCode();
});

$("#requestor_registration").submit(function (e) {
  e.preventDefault();
  $("#main-loader").show();
  $(".btn").attr("disabled", true);

  var fname = $("#org_name").val();
  var lname = "";
  var email = $("#org_email").val();
  var confirm_email = $("#confirm_org_email").val();
  var master_code = $("#master_code").val();

  validateMasterCode();
  if (!masterKeyValid || master_code.length == 0) return false;

  var cno = $("#org_contact_no").val();

  if (email != confirm_email) {
    swal({
      title: "Warning!",
      text: "Enter email correctly.",
      icon: "warning",
      allowOutsideClick: false,
      closeOnClickOutside: false,
    });
    return false;
  }

  $("#main-loader").show();
  var request = new XMLHttpRequest();
  var register_url = "/api/user/registration/";
  request.open("POST", register_url, true);
  request.onload = function () {
    $("#main-loader").show();
    if (request.status == 200) {
      // Success!
      var resp = JSON.parse(request.responseText);
      // console.log(resp)
      if (resp.success) {
        var access_key = "0x0000000000000000000000000000000000000000";
        var utype = 2;
        var r = contract.methods
          .registerUser(fname, lname, email, utype, cno, access_key, resp.pu)
          .send()
          .then(function (res) {
            swal({
              title: "Success!",
              text: "Registration Successful!! You will recieve credentials via mail.",
              icon: "success",
              allowOutsideClick: false,
              closeOnClickOutside: false,
            }).then((value) => {
              if (value) {
                $("#main-loader").hide();
                window.location.replace(resp.redirect_url);
              }
            });
          })
          .catch(function (error) {
            $("#main-loader").hide();
            console.log("registerUser() is rejected" + error.message);
            $(".btn").attr("disabled", false);
          });
      } else {
        $("#main-loader").hide();
        $(".btn").attr("disabled", false);
        alert("Not valid");
      }
    } else {
      $("#main-loader").hide().fadeOut("slow");
      alert("Error in sending mail");
    }
  };

  request.onerror = function () {
    alert("Registration failed - there was an error");
    $("#main-loader").hide();
    $(".btn").attr("disabled", false);
  };
  request.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded; charset=UTF-8",
  );
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

  // TODO: send the key with encryption
  var formData = "first_name=" + fname;
  formData += "&email=" + email + "&contact_no=" + cno + "&utype=" + "2";
  formData += "&user_address=" + address;
  formData += "&mastercode=" + master_code;
  $("#main-loader").show();
  request.send(formData);
  $("#main-loader").hide().fadeOut("slow");
});
