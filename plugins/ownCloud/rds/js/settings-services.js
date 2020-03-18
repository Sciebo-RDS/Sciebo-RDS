(function(OC, window, $, undefined) {
  "use strict";
  $(document).ready(function() {
    const parseJwt = token => {
      try {
        return JSON.parse(atob(token.split(".")[1]));
      } catch (e) {
        return null;
      }
    };

    // holds all services
    var Services = function(baseUrl) {
      this._baseurl = baseUrl;
      this._services = []; // holds object with servicename, authorize_url, state, date
      this._user_services = []; // holds strings

      var self = this;
      this._services_without_user = function() {
        var list = [];

        self._services.forEach(function(service, index) {
          var found = false;
          self._user_services.forEach(function(user_service, index) {
            if (service["servicename"] === user_service["servicename"]) {
              found = true;
            }
          });

          if (!found) {
            list.push(service);
          }
        });
        return list;
      };
    };

    Services.prototype = {
      loadAll: function() {
        var deferred = $.Deferred();
        var counter = 2;

        var self = this;

        this.loadServices()
          .done(function() {
            counter -= 1;
            if (counter == 0) {
              deferred.resolve();
            }
          })
          .fail(function() {
            alert("Could not load all services");
            deferred.reject();
          });

        this.loadUserServices()
          .done(function() {
            counter -= 1;
            if (counter == 0) {
              deferred.resolve();
            }
          })
          .fail(function() {
            alert("Could not load user services");
            deferred.reject();
          });
        return deferred.promise();
      },

      loadServices: function() {
        var deferred = $.Deferred();
        var self = this;

        $.get(this._baseurl + "/service", "json")
          .done(function(services) {
            self._services = services;
            deferred.resolve();
          })
          .fail(function() {
            deferred.reject();
          });
        return deferred.promise();
      },

      loadUserServices: function() {
        var deferred = $.Deferred();
        var self = this;

        $.get(this._baseurl + "/user/service", "json")
          .done(function(services) {
            self._user_services = services;
            deferred.resolve();
          })
          .fail(function() {
            deferred.reject();
          });
        return deferred.promise();
      },

      removeServiceFromUser: function(servicename) {
        var deferred = $.Deferred();
        var self = this;
        $.delete(this._baseurl + "/service/" + servicename, "json")
          .done(function(services) {
            self.loadAll();
            deferred.resolve();
          })
          .fail(function() {
            deferred.reject();
          });
        return deferred.promise();
      }
    };

    // used to update the html
    var View = function(services) {
      this._services = services;
      this._authorize_url = {};
      this._btn = document.getElementById("svc-button");
      this._btn.disabled = true;
      this._select = document.getElementById("svc-selector");
    };

    View.prototype = {
      renderContent: function() {
        var self = this;
        var source = $("#serviceStable > tbody:last-child");

        this._services._user_services.forEach(function(item, index) {
          source.append(
            "<tr><td>" +
              item["servicename"] +
              "</td><td>" +
              '<form class="form-inline delete" data-confirm="' +
              t("rds", "Are you sure you want to delete this item?") +
              '" action="' +
              OC.generateUrl("apps/rds") + "/service/" +
              item["servicename"] +
              '" method="delete">' +
              '<input type="hidden" name="requesttoken" value=' +
              OC.requestToken +
              " />" +
              '<input type="submit" class="button icon-delete" value=""></form>' +
              "</td></tr>"
          );
        }, this);

        if (this._services._user_services.length > 0) {
          var serviceDiv = document.getElementById("services");
          if (serviceDiv) {
            serviceDiv.style.display = "block";
          }
        }
      },
      renderSelect: function() {
        var self = this;
        var notUsedServices = self._services._services_without_user();

        self._select.addEventListener("change", function() {
          var select = self._select;
          var btn = self._btn;

          btn.textContent = t(
            "rds",
            "Authorize " + select.options[select.selectedIndex].text + " now"
          );
          btn.value = select.options[select.selectedIndex].value;
          btn.disabled = false;
        });

        notUsedServices.forEach(function(item, index) {
          self._authorize_url[item.servicename] =
            item.authorize_url + "&state=" + item.state;
          var option = document.createElement("option");
          option.text = option.value = item.servicename;
          self._select.add(option, 0);
          self._select.selectedIndex = 0;
        });

        self._select.value = 0;
      },
      renderButton: function() {
        var self = this;

        self._btn.onclick = function() {
          var select = self._select;
          var win = window.open(
            self._authorize_url[select.options[select.selectedIndex].text],
            "oauth2-service-for-rds",
            "width=100%,height=100%,scrollbars=yes"
          );

          var timer = setInterval(function() {
            if (win.closed) {
              clearInterval(timer);
              location.reload();
            }
          }, 300);
        };
      },
      render: function() {
        this.renderSelect();
        this.renderButton();
        this.renderContent();
      }
    };

    var services = new Services(OC.generateUrl("apps/rds"));
    var view = new View(services);
    services.loadAll().done(function() {
      view.render();
    });
  });
})(OC, window, jQuery);
