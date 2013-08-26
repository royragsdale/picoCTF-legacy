ig.module(
	'game.entities.mover'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityMover = ig.Entity.extend({	
	maxVel: {x: 200, y: 200},
	speed: 200,
	
	type: ig.Entity.TYPE.A,
	checkAgainst: ig.Entity.TYPE.A,
	collides: ig.Entity.COLLIDES.FIXED,
	
	visible:	true,
	moving:		false,
	following:	false,
	followTarget:	null,
	followMinDis:	1,
	control:	false,	
	dest: {x:0, y:0},
    angle: 0,
	stopping:false,


	
	/*@Function rotate entity
     *@angle ranging from -180 to 180, absolute angle value;
     */
	rotate: function(angle, rotatespeed){
        if (angle - this.angle > 0)
        {
            this.currentAnim.angle += Math.PI / 9 * ig.system.tick * rotatespeed;
            this.angle  = this.currentAnim.angle;
            if(Math.PI * (angle / 180) > this.angle )
            {
                _this = this;
                setTimeout(function(){
                    _this.rotate(angle, rotatespeed);
                },25)
            }
        }
        else
        {
            this.currentAnim.angle -= Math.PI / 9 * ig.system.tick * rotatespeed;
            this.angle  = this.currentAnim.angle;
            if(Math.PI * (angle / 180) < this.angle )
            {
                _this = this;
                setTimeout(function(){
                    _this.rotate(angle, rotatespeed);
                },25)
            }
        }
    },

	follow: function(target){
		this.following=true;
		this.followTarget=target;
		this.collides=ig.Entity.COLLIDES.LITE;
	},
	
	unfollow: function(){
		this.following=false;
		this.followMinDis=1;
		this.collides=ig.Entity.COLLIDES.FIXED;
	},
		
	jump: function(pos){
		this.pos.x=pos.x;
		this.pos.y=pos.y;
		this.resetdest();
	},
	
	resetdest: function(){
		this.dest.x=this.pos.x;
		this.dest.y=this.pos.y;
		this.vel.x=0;
		this.vel.y=0;
		this.moving=false;
	},
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {		
		this.parent( x, y, settings );
		this.dest=this.pos;
	},	
	
	update: function() {
		this.parent();
		
		// keyboard & mouse control
		if(!ig.gm.currentLevel.isInCutscene && this.control){			
			var d=10;
			var dx=0,dy=0;
			if(ig.input.state("up"))   dy-=d*1.1;
			if(ig.input.state("down")) dy+=d*1.1;
			if(ig.input.state("left")) dx-=d;
			if(ig.input.state("right"))dx+=d;				
			if(dx!=0 || dy!=0){
				this.dest.x=this.pos.x+dx;
				this.dest.y=this.pos.y+dy;
			}else{			
				if(ig.input.pressed("mouse")){			
					this.dest.x=ig.input.mouse.x+ig.game.screen.x-this.size.x/2;
					this.dest.y=ig.input.mouse.y+ig.game.screen.y;
				}
			}
		}
		
		// follow
		if(this.following && typeof this.followTarget!='undefined') {
			this.dest.x=this.followTarget.pos.x+this.followTarget.size.x/2-this.size.x/2;
			this.dest.y=this.followTarget.pos.y+this.followTarget.size.y/2-this.size.y/2;
		}
		
		// move
		if(this.stopping){
			this.resetdest();
			this.stopping=false;
		}
		
		var dx=this.dest.x-this.pos.x;
		var dy=this.dest.y-this.pos.y;
		if(dx!=0 || dy!=0){
			var d=Math.sqrt(dx*dx+dy*dy);
			var dxi=dx/d;
			var dyi=dy/d;		
			
			this.vel.x=0;
			this.vel.y=0;
			
			if(this.following && d>this.followMinDis || !this.following && d>1){			
				var vx=dxi*this.speed;
				var vy=dyi*this.speed;
				
				// check mover won't pass destination
				var mx=vx*ig.system.tick;			
				var my=vy*ig.system.tick;
				var md=Math.sqrt(mx*mx+my*my);			
				if(md<d){
					this.vel.x=vx;
					this.vel.y=vy;
				}			
			}
			this.moving=this.vel.x!=0 || this.vel.y!=0;		
		}else{
			this.vel.x=0;
			this.vel.y=0;
			this.moving=false;
		}
				
		
	},

	draw: function() {
		this.zIndex=this.pos.y;
		if(this.visible){
			this.parent();	
		}
	},
	
});


});