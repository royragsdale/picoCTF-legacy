ig.module(
	'game.entities.returnbutton'
)
.requires(
	'game.entities.button'
)
.defines(function(){

EntityReturnbutton = EntityButton.extend({
	animSheet: new ig.AnimationSheet('media/Go Back Button.png',64,64),	

	
	/******* callbacks *******/
	
	click: function(){
		this.parent();	
		ig.gm.currentLevel.onUI('return');		
	},
	
	
	/******* events *******/	
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );		
		this.addAnim('idle',1,[0]);
		this.addAnim('hover',1,[1]);
		// fix position
		this.pos.x=688;
		this.pos.y=8;		
	},
	
	update: function(){
		this.parent();
		if(ig.input.pressed('esc')){
			this.click();
		}
	},

});

});