$(document).ready(function() {
  var redirectURI = "";

  $("#svc-select").click(function() {
    var btn = document.getElementById("svc-button");
    btn.attr("value", t("rds", "Authorize " + this.val() + " now"));
    getServiceInformations(this.val());
  });

  $("#svc-button").click(function() {
    var win = window.open(redirectURI, "oauth2-service-for-rds");
    ("width=100%,height=100%,scrollbars=yes");

    var timer = setInterval(function() {
      if (win.closed) {
        clearInterval(timer);
        location.reload();
      }
    }, 1000);
  });

  function getServiceInformations(service) {
    $.ajax({
      type: "GET",
      async: "false",
      url: "http://sciebords-dev.uni-muenster.de/token-storage/svc/" + service,
      statusCode: {
        200: function(element) {
          response = element;
          redirectURI = response.redirect_uri_with_client_id;
          $("svc-button").disabled = false;
        },
        404: function(element) {
          document
            .getElementById("svc-button")
            .attr("value", t("rds", service + " not available."));
        }
      }
    });
  }
});
