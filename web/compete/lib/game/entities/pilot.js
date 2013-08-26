ig.module(
	'game.entities.pilot'
)
.requires(
	'game.entities.walker'
)
.defines(function(){
	
EntityPilot=EntityWalker.extend({	
	name: 'Pilot',
	animSheet: new ig.AnimationSheet('media/pilotsprite.png',64,64),
	speed: 100,
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.control=false;
		this.following=false;
	},
	
	
	wayPoints:[
		'pilot0',
		'pilot1',
		'pilot2',
		'pilot3',
	],
	waitTimes:[
		3,
		4,
		2,
		3,
	],
	currWP:0,
	waitWP: false,
	waitTill:0,
	update: function(){
		this.parent();
		
		if(ig.gm.currentLevel.isInCutscene){
			this.resetdest();
		}else{			
			if(!this.moving){
				if(!this.waitWP){
					// start wait
					this.waitWP=true;
					this.waitTill=ig.gm.time+this.waitTimes[this.currWP];
				}else{
					// wait
					if(ig.gm.time<this.waitTill)return;
					this.waitWP=false;
					
					// start move to next
					var wp=ig.game.getEntityByName(this.wayPoints[this.currWP]);
					this.dest.x=wp.pos.x;
					this.dest.y=wp.pos.y;
					
					this.currWP++;
					if(this.currWP==this.wayPoints.length)
						this.currWP=0;
				}				
			}else{
			}			
		}				
	},	
});


});