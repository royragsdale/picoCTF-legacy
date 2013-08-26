ig.module(
	'game.entities.guard'
)
.requires(
	'game.entities.walker'
)
.defines(function(){
	
EntityGuard=EntityWalker.extend({	
	name: 'Guard',
	animSheet: new ig.AnimationSheet('media/guardsprite.png',64,64),
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.control=false;
		this.following=false;
	},
});


});