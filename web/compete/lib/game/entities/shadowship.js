ig.module(
	'game.entities.shadowship'
)
.requires(
	'game.entities.mover'
)
.defines(function(){
	
EntityShadowship=EntityMover.extend({

	followMinDis:	170,
	name: 'Shadowship',
    size: {x:400,y:400},
    offset:{x:0,y:0},
    maxVel: {x: 3000, y : 3000},
    zIndex: 0,
    collides: ig.Entity.COLLIDES.NEVER,
	
	init: function( x, y, settings ) {
		this.control=false;
		this.following=false;
        this.animSheet  =  new ig.AnimationSheet( 'media/Transition4/ShipShadow.png',400 ,400 ),
        this.addAnim('smallest', 1, [0],true);
        this.addAnim('smaller', 1,[1], true);
        this.addAnim('bigger',1,[2], true);
        this.addAnim('biggest',1,[3],true);
        this.addAnim("none",1,[4],true);
        this.speed = 50;
        this.currentAnim = this.anims.biggest;
		this.parent( x, y, settings );
	},
	
	ready: function() {
		//this.followTarget=ig.game.getEntityByName('Taylor');
	},
	
	update: function() {
		this.parent();
        this.currentAnim.angle = -90 /180 * Math.PI;
	},
	
	draw: function() {
		this.parent();
        this.zIndex = 20;
	}
});


});