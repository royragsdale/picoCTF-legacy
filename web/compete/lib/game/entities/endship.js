ig.module(
	'game.entities.endship'
)
.requires(
	'game.entities.mover'
)
.defines(function(){
	
EntityEndship=EntityMover.extend({

	followMinDis:	1,
	name: 'endship',
    size: {x:511,y:508},
    offset:{x:0,y:0},
    maxVel: {x: 3000, y : 3000},
    zIndex: 100,
    collides: ig.Entity.COLLIDES.NEVER,
	
	init: function( x, y, settings ) {
		this.control=false;
		this.following=false;
        this.animSheet  =  new ig.AnimationSheet( 'media/shipend.png',511 ,508),
        this.addAnim('start', 1, [0],true);
        this.speed = 500;
		this.parent( x, y, settings );
	},
	
	ready: function() {
		//this.followTarget=ig.game.getEntityByName('Taylor');
	},
	
	update: function() {
		this.parent();
	},
	
	draw: function() {
		this.parent();
        this.zIndex = 1000;
	}
});


});