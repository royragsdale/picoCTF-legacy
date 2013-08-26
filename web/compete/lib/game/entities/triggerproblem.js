ig.module(
	'game.entities.triggerproblem'
)
.requires(
	'game.entities.trigger'
)
.defines(function(){

EntityTriggerproblem = EntityTrigger.extend({
	animSheet: new ig.AnimationSheet('media/trigger.png',64,64),
	solved: false,
	bonus: false,
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.addAnim('0', 0.1, [4]);
		this.parent( x, y, settings );
		
		this.addAnim('idle', 0.1, [4]);
		this.addAnim('hover', 0.1, [5]);
	},
	
	ready: function(){
		this.parent();
		this.canFire=true;
		this.mark.enabled=true;
		if(this.solved){
			this.mark.currentAnim=this.mark.anims['solved'];
		}else{			
			if(this.bonus){
				this.mark.currentAnim=this.mark.anims['bonus'];
			}else{
				this.mark.currentAnim=this.mark.anims['must'];
			}
		}	
	},
	
	update: function(){
		this.parent();		
	}
});

});