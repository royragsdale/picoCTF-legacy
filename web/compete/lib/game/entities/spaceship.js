ig.module(
	'game.entities.spaceship'
)
.requires(
	'game.entities.mover'
)
.defines(function(){
	
EntitySpaceship = EntityMover.extend({	
	name: 'spaceship',
	size: {x: 306, y: 300},
	offset: {x: 0, y: 0},	
	animSheet: new ig.AnimationSheet('media/NEW - spaceship_without-gun-cannon.png',306,300),
	followMinDis: 1,
	collides: ig.Entity.COLLIDES.NEVER,
	
	
	/******* events *******/
	
	// This removes collision to the collision map
	handleMovementTrace: function( res ) {		
		this.pos.x += this.vel.x * ig.system.tick;
		this.pos.y += this.vel.y * ig.system.tick;
	},

	init: function( x, y, settings ) {		
		this.parent( x, y, settings );
		
		this.addAnim('form1', 1, [0]);		
		this.addAnim('form2', 1, [1]);		
		this.currentAnim=this.anims['form1'];		
	},	
		
	update: function() {		
		this.parent();
	},

	draw: function() {
		this.parent();	
	}
});


});