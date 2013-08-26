ig.module(
	'game.entities.transitionship'
)
.requires(
	'game.entities.mover'
)
.defines(function(){
	
EntityTransitionship=EntityMover.extend({

	followMinDis:	1,
	name: 'Transitionship',
    size: {x:400,y:400},
    offset:{x:0,y:0},
    maxVel: {x: 3000, y : 3000},
    zIndex: 100,
    collides: ig.Entity.COLLIDES.NEVER,
	
	init: function( x, y, settings ) {
		this.control=false;
		this.following=false;
        this.animSheet  =  new ig.AnimationSheet( 'media/Transition4/TransparentShip.png',400 ,400),
        this.addAnim('start', 1, [0],true);
        this.addAnim('landoff', 1,[1], true);
        this.addAnim('air',1,[2], true);
        this.addAnim('space',1,[3],true);
        this.speed = 50;
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