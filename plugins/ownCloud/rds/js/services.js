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
      this._services_without_user = function() {
        var list = [];

        this._services.foreach(function(item, index) {
          if (this._user_services.indexOf(item["servicename"]) < 0) {
            list.push(item);
          }
        });
        return list;
      };
    };

    Services.prototype = {
      loadAll: function() {
        var deferred = $.Deferred();
        var counter = 2;
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
        $.get(this.baseUrl + "/user/service", "json")
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
        $.post(this.baseUrl + "/service/" + servicename, "json")
          .done(function(services) {
            this.loadAll();
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
      this._select = document.getElementById("svc-select");
    };

    View.prototype = {
      renderContent: function() {
        var source = $("#serviceStable > tbody:last-child");
        this._services._user_services.foreach(function(item, index, array) {
          source.append(
            "<tr><td>" +
              item +
              "</td><td>" +
              '<form class="form-inline delete" data-confirm="' +
              t("rds", "Are you sure you want to delete this item?") +
              '" action="' +
              OC.generateUrl(this._services._baseurl) +
              "/service/" +
              item +
              '/delete" method="post">' +
              '<input type="hidden" name="requesttoken" value=' +
              OC.requestToken +
              " />" +
              '<input type="submit" class="button icon-delete" value=""></form>' +
              "</td></tr>"
          );
        });
      },
      renderSelect: function() {
        this._services._services_without_user().foreach(function(item, index) {
          this._authorize_url[item.servicename] =
            item.authorize_url + "&state=" + item.state;
          var option = document.createElement("option");
          option.text = option.value = item.servicename;
          this._select.add(option, 0);
        });

        this._select.click(function() {
          this._btn.attr("value", t("rds", "Authorize " + this.val() + " now"));
        });
      },
      renderButton: function() {
        this._btn.click(function() {
          var win = window.open(
            this._authorize_url[this._select.value],
            "oauth2-service-for-rds"
          );
          ("width=100%,height=100%,scrollbars=yes");

          var timer = setInterval(function() {
            if (win.closed) {
              clearInterval(timer);
              location.reload();
            }
          }, 300);
        });
      },
      render: function() {
        this.renderSelect();
        this.renderButton();
        this.renderContent();
      }
    };

    var services = new Services(OC.generateUrl("apps/rds/api/v1"));
    var view = new View(services);
    services
      .loadAll()
      .done(function() {
        view.render();
      })
      .fail(function() {
        alert("Could not load services");
      });
  });
})(OC, window, jQuery);
