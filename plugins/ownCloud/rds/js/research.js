// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js
(function (OC, window, $, undefined) {
  "use strict";

  $(document).ready(function () {
    var studies = new Studies(OC.generateUrl("/apps/rds/research"));
    var services = new Services(OC.generateUrl("/apps/rds/service"));
    var metadata = new Metadata(OC.generateUrl("/apps/rds/metadata"));
    var files = new Files(undefined);

    var view = new View(studies, services, metadata, files);
    view
      .loadAll()
      .done(function () {
        view.render();
      })
      .fail(function () {
        alert("Could not load informations");
      });
  });
})(OC, window, jQuery);
