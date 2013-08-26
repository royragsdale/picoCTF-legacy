ig.module(
	'game.entities.locksmall'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityLocksmall = ig.Entity.extend({
	name:'fill',
	size: {x: 40, y: 58},
	zIndex: 10,
	animSheet: new ig.AnimationSheet( 'media/LockSmall.png', 40, 58),
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle', 1, [0]);
	},
});

});