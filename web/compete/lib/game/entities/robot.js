ig.module(
	'game.entities.robot'
)
.requires(
	'game.entities.walker'
)
.defines(function(){
	
EntityRobot=EntityWalker.extend({	
	name: 'Toast',
	animSheet: new ig.AnimationSheet('media/robotsprite.png',64,64),
	followMinDis: 100,
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.control=false;
		this.following=false;
	},
	
});


});