$(function() {
	$('#playbutton').click(function(e) {
        e.preventDefault();
        $('#presentingtext').remove();
        $('#toastertext').remove();
        $('#playbutton').remove();        
        $('<iframe src="//player.vimeo.com/video/63972607?autoplay=1" width="500" height="281" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>').appendTo('#playbox');
    });        
});