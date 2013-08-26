ig.module(
	'game.entities.car'
)
.requires(
	'game.entities.mover'
)
.defines(function(){
	
EntityCar=EntityMover.extend({

	followMinDis:	1,
	name: 'Car',
    size: {x:360,y:180},
    offset:{x:200,y:0},
    maxVel: {x: 3000, y : 3000},
    collides: ig.Entity.COLLIDES.NEVER,
	
	init: function( x, y, settings ) {
		this.control=false;
		this.following=false;
        this.animSheet  =  new ig.AnimationSheet( 'media/Transition1/CarYard.png',360 ,180 ),
        this.addAnim('idle', 1, [0],true);
        this.addAnim('open', 1,[1], true);
        this.addAnim('getin',1,[2], true);
        this.addAnim('drive',1,[3],true);
        this.speed = 1000;
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
	}
});


});