ig.module(
	'game.entities.zonebutton'
)
.requires(
	'game.entities.button'
)
.defines(function(){

EntityZonebutton = EntityButton.extend({
	size:{ x:300,y:50},
	
	click: function(){
		this.parent();		
		ig.gm.currentLevel.onClick(this.name);
	},
	
	hover: function(){
		ig.gm.currentLevel.onHover(this.name);
	},
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle',1,[0]);
		this.addAnim('hover',1,[1]);		
	},
	
	draw: function(){
		// invisible
	},
});

});