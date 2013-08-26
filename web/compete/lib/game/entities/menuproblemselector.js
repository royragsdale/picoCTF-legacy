ig.module(
	'game.entities.menuproblemselector'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityMenuproblemselector = ig.Entity.extend({
	name:'selector',
	size: {x: 112, y: 100},
	zIndex: 10,
	animSheet: new ig.AnimationSheet( 'media/ProblemSelecter.png', 112, 100),
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle', 1, [0]);
	},
});

});