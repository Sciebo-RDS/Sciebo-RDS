// taken a lot from https://github.com/owncloud/app-tutorial/blob/master/js/script.js

function MyFunction() {
  alert("Clicked");
}

$("#new-connection").click(function() {
  MyFunction();
  return false;
});

$("#btn-save-connection").click(function() {
  MyFunction();
  return false;
});

$("#btn-save-connection-and-continue").click(function() {
  MyFunction();
  return false;
});
