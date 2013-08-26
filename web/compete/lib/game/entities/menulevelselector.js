ig.module(
	'game.entities.menulevelselector'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityMenulevelselector = ig.Entity.extend({
	name:'selector',
	size: {x: 230, y: 212},
	zIndex: 10,
	animSheet: new ig.AnimationSheet( 'media/LevelSelecter.png', 230, 212),
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle', 1, [0]);
	},
});

});