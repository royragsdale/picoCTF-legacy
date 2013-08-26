ig.module(
	'game.entities.solvebutton'
)
.requires(
	'game.entities.button'
)
.defines(function(){

EntitySolvebutton = EntityButton.extend({
	animSheet: new ig.AnimationSheet('media/Main Menu Button.png',64,64),	
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle',1,[0]);
		this.addAnim('hover',1,[1]);		
	},
	
	click: function(){
		this.parent();		
		ig.gm.currentLevel.onUI('solve');
	}

});

});