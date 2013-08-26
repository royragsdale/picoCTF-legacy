ig.module(
	'game.entities.menulevelfill'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityMenulevelfill = ig.Entity.extend({
	name:'fill',
	size: {x: 230, y: 212},
	zIndex: 5,
	animSheet: new ig.AnimationSheet( 'media/Levels.png', 230, 212),
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('Room', 1, [0]);
		this.addAnim('Airport', 1, [1]);
		this.addAnim('Loadingbay', 1, [2]);
		this.addAnim('Spaceship', 1, [3]);
	},
});

});