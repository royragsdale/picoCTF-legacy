ig.module(
	'game.entities.endplayer'
)
.requires(
	'game.entities.mover'
)
.defines(function(){
	
EntityEndplayer=EntityMover.extend({

	followMinDis:	1,
	name: 'endplayer',
    size: {x:64,y:64},
    offset:{x:0,y:0},
    maxVel: {x: 3000, y : 3000},
    zIndex: 100,
    collides: ig.Entity.COLLIDES.NEVER,
	
	init: function( x, y, settings ) {
		this.control=false;
		this.following=false;
        this.animSheet  =  new ig.AnimationSheet( 'media/commandertransform.png',64 ,64),
        this.addAnim('start', 0.2, [0,1,2],false);
        this.addAnim('transition1',1,[3]);
        this.addAnim('upgrade1',0.2,[4,5,6],false);
        this.addAnim('transition2',1,[7]);
        this.addAnim('upgrade2',0.2,[8,9,10],false)
        this.addAnim('transition3',1,[11]);
        this.addAnim('upgrade3', 0.2,[12,13,14],false);
        this.speed = 60;
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