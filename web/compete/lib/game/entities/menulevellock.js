ig.module(
	'game.entities.menulevellock'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityMenulevellock = ig.Entity.extend({
	name:'fill',
	size: {x: 74, y: 108},
	zIndex: 10,
	animSheet: new ig.AnimationSheet( 'media/Lock-for-Menu.png', 74, 108),
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle', 1, [0]);
	},
});

});