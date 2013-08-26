ig.module(
	'game.entities.menuselector'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityMenuselector = ig.Entity.extend({
	name:'selector',
	size: {x: 64, y: 64},
	zIndex: 10,
	animSheet: new ig.AnimationSheet( 'media/menuselector.png', 64, 64),
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle', 1, [0]);
	},
});

});