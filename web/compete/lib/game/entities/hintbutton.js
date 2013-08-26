ig.module(
	'game.entities.hintbutton'
)
.requires(
	'game.entities.button'
)
.defines(function(){

EntityHintbutton = EntityButton.extend({
	animSheet: new ig.AnimationSheet('media/Hints Buttons.png',64,64),	
	mark: null,
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle',1,[0]);
		this.addAnim('hover',1,[1]);			
	},
	
	update: function(){
		this.parent();		
	},
	
	click: function(){
		this.parent();
		ig.gm.currentLevel.onUI('hint');		
	}

});

});