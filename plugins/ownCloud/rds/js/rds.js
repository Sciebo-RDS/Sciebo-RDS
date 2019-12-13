(function($, OC) {
  $(document).ready(function() {
    var btn = document.getElementById("svc-button");
    var select = document.getElementById("svc-select");
    var authorize_url = {}
    var registered_services = []

    printAllRegisteredServices();
    printServicesToBtn();

    select.click(function() {
      btn.attr("value", t("rds", "Authorize " + this.val() + " now"));
    });

    btn.click(function() {
      var win = window.open(authorize_url[select.value], "oauth2-service-for-rds");
      ("width=100%,height=100%,scrollbars=yes");

      var timer = setInterval(function() {
        if (win.closed) {
          clearInterval(timer);
          location.reload();
        }
      }, 300);
    });

    function printAllRegisteredServices() {
      $.ajax({
        type: "GET",
        async: "false",
        url: "http://sciebords-dev.uni-muenster.de/token-service/user/" + OC.getCurrentUser().uid + "/service",
        dataType: "json",
        statusCode: {
          200: function(element) {
            response = element;

            select.options.length = 0;
            response.foreach(function(value, index, array) {
              registered_services.push(value.servicename)
            });
            
            //return state;
          },
          404: function(element) {
            btn.attr("value", t("rds", "Services not available."));
          }
        }
      });

        registered_services.foreach(function(value, index, array) {
          $('#serviceStable > tbody:last-child').append('<tr><td>' + value +  
          '</td><td>' + 
          '<form class="form-inline delete" data-confirm="' + t("rds", "Are you sure you want to delete this item?") + 
          '" action="URL" method="post">' +
          '<input type="hidden" name="requesttoken" value='+ OC.requestToken + ' />' +
          '<input type="submit" class="button icon-delete" value=""></form>' +
          '</td></tr>');
        })
    }

    function printServicesToBtn() {
      $.ajax({
        type: "GET",
        async: "false",
        url: "http://sciebords-dev.uni-muenster.de/token-service/service",
        dataType: "json",
        statusCode: {
          200: function(element) {
            response = element;

            select.options.length = 0;
            response.foreach(function(value, index, array) {
              state = parseJwt(value.jwt)

              if (registered_services.indexOf(state.servicename) < 0) {
                authorize_url[state.servicename] = state.authorize_url + "&state=" + value.jwt
                
                var option = document.createElement("option");
                option.text = option.value = state.servicename;
                select.add(option, 0);
              }
            });

            btn.disabled = false;
            //return authorize_url;
          },
          404: function(element) {
            btn.attr("value", t("rds", "Services not available."));
          }
        }
      });
    }

    const parseJwt = (token) => {
      try {
        return JSON.parse(atob(token.split('.')[1]));
      } catch (e) {
        return null;
      }
    };

      return JSON.parse(jsonPayload);
    }
  });
})(jQuery, OC);