ig.module(
	'game.entities.zone'
)
.requires(
	'impact.entity'
)
.defines(function(){

EntityZone = ig.Entity.extend({	
	size: {x: 64, y: 64},
	_wmScalable: true,
	_wmDrawBox: true,
	_wmBoxColor: 'rgba(196, 196, 0, 0.7)',
	type: ig.Entity.TYPE.A,
	checkAgainst: ig.Entity.TYPE.A,
	collides: ig.Entity.COLLIDES.NEVER,		
	
	enabled: true,
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
	},	

	check: function(other){
		if(!this.enabled)return;			
		ig.gm.currentLevel.onTrigger(this,other);
		if(!this.enabled){
			other.stopping=true;
		}
	},	

});

});