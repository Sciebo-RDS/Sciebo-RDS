$(document).ready(function () {

	$('#rds_submit').on('click', function (event) {
		event.preventDefault();
		var url = $("#cloud_url");
		OC.AppConfig.setValue(app, url.attr('name'), url.val());
	});

	$('.section .icon-info').tipsy({ gravity: 'w' });
});