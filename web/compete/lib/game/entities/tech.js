ig.module(
	'game.entities.tech'
)
.requires(
	'game.entities.walker'
)
.defines(function(){
	
EntityTech=EntityWalker.extend({	
	name: 'Techie',
	animSheet: new ig.AnimationSheet('media/techsprite.png',64,64),
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.control=false;
		this.following=false;
	},
});


});