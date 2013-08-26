ig.module(
	'game.entities.triggerrobotscrap'
)
.requires(
	'game.entities.trigger'
)
.defines(function(){

EntityTriggerrobotscrap = EntityTrigger.extend({
	animSheet: new ig.AnimationSheet('media/robotscrap.png',64,64),
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );		
		this.addAnim('idle', 0.1, [0]);
		this.addAnim('hover', 0.1, [0]);
	},
	
});

});