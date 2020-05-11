(function (OC, window, $, undefined) {
  "use strict";

  OC.rds = OC.rds || {};

  var state = 0;
  var services;

  function reload() {
    var btns = $(".service :button");
    btns.each(function (index, elem) {
      btns[index].disabled = true;
    });

    if (state === 1) {
      $("#activateOwncloud").prop("disabled", false);
    }
    if (state === 2) {
      $("#activateZenodo").prop("disabled", false);
    }
    if (state === 3) {
      $("#activateResearch").prop("disabled", false);
    }
  }

  function render() {
    var owncloud = undefined;
    var zenodo = undefined;

    services.getServices().forEach(function (service) {
      if (service.servicename === "Owncloud") {
        owncloud = service;
      }

      if (service.servicename === "Zenodo") {
        zenodo = service;
      }
    });

    $("#activateOwncloud").click(function () {
      var win = window.open(
        owncloud.authorize_url,
        "oauth2-service-for-rds",
        "width=100%,height=100%,scrollbars=yes"
      );

      var timer = setInterval(function () {
        if (win.closed) {
          clearInterval(timer);

          if (
            window.location.href.startsWith(
              "https://sciebords-dev.uni-muenster.de/token-service/"
            )
          ) {
            state += 1;
            reload();
          }
        }
      }, 300);
    });

    $("#activateZenodo").click(function () {
      var win = window.open(
        zenodo.authorize_url,
        "oauth2-service-for-rds",
        "width=100%,height=100%,scrollbars=yes"
      );

      var timer = setInterval(function () {
        if (win.closed) {
          clearInterval(timer);

          if (
            window.location.href.startsWith(
              "https://sciebords-dev.uni-muenster.de/token-service/"
            )
          ) {
            state += 1;
            reload();
          }
        }
      }, 300);
    });

    $("#activateResearch").click(function () {
      console.log("Create research and open it.");
    });

    reload();
  }

  $(document).ready(function () {
    services = new OC.rds.Services();
    reload();

    services.loadService().done(function () {
      state += 1;
      render();
      reload();
    });
  });
})(OC, window, jQuery);
