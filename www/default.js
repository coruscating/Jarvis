
// Default dialog options
$.extend($.ui.dialog.prototype.options, {
    modal: false,
    autoOpen: true,
    close: function(){
            var checkbox=this.id.replace("Dialog", "Check");
            $("#" + checkbox).prop('checked', false);
    }
});
$.extend($.ui.draggable.options, {
    containment: '#workingwindow',
    snap: true,
    snapTolerance: 10
});

//$.ui.draggable.defaults.containment = "#workingwindow";

$('.oneplace').spinner({
    stop: function (event, ui) {
        if ($(this).val().indexOf(".") >= 0) {
        }
        else {
            $(this).val($(this).val() + '.0');
        }
    }
});


