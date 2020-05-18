var $ = django.jQuery;

$(function() {
    var data = $.parseJSON($("#json-renderer").text());
    $('#json-renderer').jsonViewer(data);
});
