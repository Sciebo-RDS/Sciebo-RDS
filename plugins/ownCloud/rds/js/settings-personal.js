(function (OC, window, $, undefined) {
  "use strict";
  $(document).ready(function () {
    const parseJwt = (token) => {
      try {
        return JSON.parse(atob(token.split(".")[1]));
      } catch (e) {
        return null;
      }
    };

    // holds all services
    var Services = function (baseUrl) {
      this._baseUrl = baseUrl;
      this._services = []; // holds object with servicename, authorizeUrl, state, date
      this._user_services = []; // holds strings

      var self = this;
      this._services_without_user = function () {
        var list = [];

        self._services.forEach(function (service, index) {
          var found = false;
          self._user_services.forEach(function (user_service, index) {
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
      loadAll: function () {
        var deferred = $.Deferred();
        var counter = 2;

        var self = this;

        this.loadServices()
          .done(function () {
            counter -= 1;
            if (counter == 0) {
              deferred.resolve();
            }
          })
          .fail(function () {
            deferred.reject();
          });

        this.loadUserservices()
          .done(function () {
            counter -= 1;
            if (counter == 0) {
              deferred.resolve();
            }
          })
          .fail(function () {
            deferred.reject();
          });
        return deferred.promise();
      },

      loadServices: function () {
        var deferred = $.Deferred();
        var self = this;

        $.get(this._baseUrl + "/service", "json")
          .done(function (services) {
            self._services = services;
            deferred.resolve();
          })
          .fail(function () {
            deferred.reject();
          });
        return deferred.promise();
      },

      loadUserservices: function () {
        var deferred = $.Deferred();
        var self = this;

        $.get(this._baseUrl + "/userservice", "json")
          .done(function (services) {
            self._user_services = services;
            deferred.resolve();
          })
          .fail(function () {
            deferred.reject();
          });
        return deferred.promise();
      },

      removeServiceFromUser: function (servicename) {
        var deferred = $.Deferred();
        var self = this;

        $.ajax({
          type: "DELETE",
          url: this._baseUrl + "/userservice/" + servicename,
          success: function (result) {
            self
              .loadAll()
              .done(function () {
                deferred.resolve();
              })
              .fail(function () {
                deferred.reject();
              });
          },
          error: function (result) {
            deferred.reject();
          },
        });

        return deferred.promise();
      },
    };

    // used to update the html
    var View = function (services) {
      this._services = services;
      this._authorizeUrl = {};
      this._btn = document.getElementById("svc-button");
      this._btn.disabled = true;
      this._select = document.getElementById("svc-selector");
    };

    View.prototype = {
      removeServiceFromUser: function (servicename) {
        var self = this;

        OC.dialogs.confirm(
          t("rds", "Are you sure, that you want to delete {servicename}?", {
            servicename: servicename,
          }),
          t("rds", "RDS Settings services"),
          function (confirmation) {
            {
              if (confirmation == false) {
                return;
              }

              self._services
                .removeServiceFromUser(servicename)
                .done(function () {
                  self.render();
                })
                .fail(function () {
                  OC.dialogs.alert(
                    t("rds", "Could not remove the service {servicename}", {
                      servicename: servicename,
                    }),
                    t("rds", "RDS Settings services")
                  );
                })
                .always(function () {
                  if (servicename === "Owncloud") {
                    $.ajax({
                      type: "DELETE",
                      url: self._services._baseUrl + "/research",
                    }).always(function (result) {
                      location.reload();
                    });
                  }
                });
            }
          }
        );
      },
      renderContent: function () {
        var self = this;
        $("#serviceStable > tbody").html("");
        var source = $("#serviceStable > tbody:last-child");

        this._services._user_services.forEach(function (item, index) {
          if (item["servicename"] !== "Owncloud") {
            source.append(
              "<tr><td>" +
              item["servicename"] +
              "</td><td>" +
              '<button data-servicename="' +
              item["servicename"] +
              '" class="button icon-delete"></button>' +
              "</td></tr>"
            );
          }
        }, this);

        var btns = $("#serviceStable :button");
        btns.click(function () {
          var $this = $(this);
          var servicename = $this.data("servicename");

          self.removeServiceFromUser(servicename);
        });

        if (this._services._user_services.length > 0) {
          var serviceDiv = document.getElementById("services");
          if (serviceDiv) {
            serviceDiv.style.display = "block";
          }
        }

        $("#owncloud-button-removal").click(function () {
          self.removeServiceFromUser("Owncloud");
          return false;
        });
      },
      renderSelect: function () {
        var self = this;
        var notUsedServices = self._services._services_without_user();

        self._select.addEventListener("change", function () {
          var select = self._select;
          var btn = self._btn;

          btn.textContent = t("rds", "Authorize {servicename} now", {
            servicename: select.options[select.selectedIndex].text,
          });
          btn.value = select.options[select.selectedIndex].value;
          btn.disabled = false;
        });

        notUsedServices.forEach(function (item, index) {
          self._authorizeUrl[item.servicename] =
            item.authorizeUrl + "&state=" + item.state + "FROMSETTINGS";
          var option = document.createElement("option");
          option.text = option.value = item.servicename;
          self._select.add(option, 0);
          self._select.selectedIndex = 0;
        });

        self._select.value = 0;
      },
      renderButton: function () {
        var self = this;

        self._btn.onclick = function () {
          var select = self._select;
          var win = window.open(
            self._authorizeUrl[select.options[select.selectedIndex].text],
            "_self",
            "width=100%,height=100%,scrollbars=yes"
          );

          var timer = setInterval(function () {
            if (win.closed) {
              clearInterval(timer);
              location.reload();
            }
          }, 300);
        };
      },

      render: function () {
        this.renderSelect();
        this.renderButton();
        this.renderContent();
      },
    };

    var services = new Services(OC.generateUrl("apps/rds"));
    var view = new View(services);
    services.loadAll().done(function () {
      view.render();
    });
  });
})(OC, window, jQuery);
