DIRECTIONS={
	DOWN:'down',
	LEFT:'left',
	UP:'up',
	RIGHT:'right',
}
DIRBACK={
	'down':'up',
	'up':'down',
	'right':'left',
	'left':'right',
}
ig.module(
	'game.entities.walker'
)
.requires(
	'game.entities.mover'
)
.defines(function(){
	
EntityWalker = EntityMover.extend({	
	size: {x: 32, y: 16},
	offset: {x: 16, y: 48},
	animSheet: new ig.AnimationSheet('media/playersprite.png',64,64),	
	facing: DIRECTIONS.DOWN,
	back: false,
	

	/******* events *******/
	
	init: function( x, y, settings ) {		
		this.parent( x, y, settings );
		
		// Animation
		this.addAnim('idle',     0.2, [1]);
		
		this.addAnim('facedown', 0.2, [1]);
		this.addAnim('faceleft', 0.2, [5]);
		this.addAnim('faceup',   0.2, [9]);
		this.addAnim('faceright',0.2, [13]);
		
		this.addAnim('walkdown', 0.2, [0,1,2,1]);
		this.addAnim('walkleft', 0.2, [4,5,6,5]);
		this.addAnim('walkup',   0.2, [8,9,10,9]);
		this.addAnim('walkright',0.2, [12,13,14,13]);		
		
		this.addAnim('backdown', 0.2, [8,9,10,9]);
		this.addAnim('backleft', 0.2, [12,13,14,13]);
		this.addAnim('backup',   0.2, [0,1,2,1]);
		this.addAnim('backright',0.2, [4,5,6,5]);

	},	
	
	update: function(){
		this.parent();
		
		// direction
		if(this.moving){
			var vx=this.vel.x;
			var vy=this.vel.y;
			if(vx>vy && vx>-vy)this.facing=DIRECTIONS.RIGHT;
			if(vx<vy && vx<-vy)this.facing=DIRECTIONS.LEFT;
			if(vy>vx && vy>-vx)this.facing=DIRECTIONS.DOWN;
			if(vy<vx && vy<-vx)this.facing=DIRECTIONS.UP;		
			if(this.back)this.facing=DIRBACK[this.facing];
		}
		
		// animation
		if(!this.moving){			
			this.currentAnim=this.anims['face'+this.facing];
		}else{
			this.currentAnim=this.anims['walk'+this.facing];
		}
	},
	
});


});