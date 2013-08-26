$(document).ready(function(){	
    var btn = $.fn.button.noConflict();
    $.fn.btn = btn;
    $( "#problemhintdialog" ).dialog({
        autoOpen: false,
        modal:true,        
        width: 600,
        position: [350,300]
    });
})
