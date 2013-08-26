ig.module(
	'game.entities.trigger'
)
.requires(
	'impact.entity',
	'game.entities.mark'
)
.defines(function(){

EntityTrigger = ig.Entity.extend({	
	size: {x: 64, y: 64},
	_wmScalable: true,
	_wmDrawBox: true,
	_wmBoxColor: 'rgba(196, 255, 0, 0.7)',
	type: ig.Entity.TYPE.A,
	checkAgainst: ig.Entity.TYPE.A,
	collides: ig.Entity.COLLIDES.NEVER,		
	
	canFire: true,
	mark: null,
	enabled: true,
	following: false,
	followTarget: null,
	dy: 0,
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		
		if(typeof ig.gm!='undefined'){
			this.mark=ig.game.spawnEntity(EntityMark);
			if(this.name=='exit')
				this.mark.currentAnim=this.mark.anims['stop'];
		}
	},	
	
	update: function(){
		if(!this.enabled)return;
		this.parent();						
		
		// following
		if(this.following){
			if(typeof this.followTarget!='undefined')
				centerAlign(this,this.followTarget);				
		}
		
		// mark pos		
		this.mark.pos.x=this.pos.x;
		this.mark.pos.y=this.pos.y-this.mark.size.y+this.dy;				
						
		// mouse interactions		
		if(!ig.gm.currentLevel.isInCutscene){
            this.mark.enabled=true;
			
			if(this.canFire){
				var mousex=ig.input.mouse.x+ig.game.screen.x;
				var mousey=ig.input.mouse.y+ig.game.screen.y;
				if((mousex>this.pos.x && mousex<this.pos.x+this.size.x) &&
					(mousey>this.pos.y && mousey<this.pos.y+this.size.y)){					
					
					this.dy=-10;
					if(ig.input.pressed('mouse')){
						ig.gm.currentLevel.levelStartLock=false;				
						ig.gm.currentLevel.clickTrigger=this;
                        if(Math.floor(this.name) > 50 && Math.floor(this.name) < 100)
                        {
                            ig.gm.currentProblem=this.name;
                            ig.gm.loadLevel('Problem',false);
                        }
                        else ig.gm.category = '';
					}
				}else{
					this.dy=0;
				}
			}
		}else{
			this.mark.enabled=false;
		}
	},
	
	check: function(other){
		if(!this.enabled)return;
		
		if(ig.input.state("up")||
		   ig.input.state("down")||
		   ig.input.state("left")||
		   ig.input.state("right")){			
		}else{
			if(ig.gm.currentLevel.clickTrigger!=this)
				return;
		}
		if(this.canFire){			
			ig.gm.currentLevel.onTrigger(this,other);		
			if(!this.canFire){ // trigger fired
				other.stopping=true;
			}
		}
				
	},	

	draw: function(){
		if(!this.enabled)return;
		this.zIndex=this.pos.y;
		this.parent();
	}
		
});

});