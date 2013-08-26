ig.module(
	'game.entities.mutebutton'
)
.requires(
	'game.entities.button'
)
.defines(function(){

EntityMutebutton = EntityButton.extend({
	animSheet: new ig.AnimationSheet('media/mutebutton.png',64,64),	
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );		
		this.addAnim('idle',1,[2]);
		this.addAnim('hover',1,[3]);
		// fix position
		this.pos.x=612;
		this.pos.y=8;	
	},
	
	click: function(){		
		var ismute=ig.sm.switchMute();
		if(ismute){
			this.addAnim('idle',1,[0]);
			this.addAnim('hover',1,[1]);
		}else{
			this.addAnim('idle',1,[2]);
			this.addAnim('hover',1,[3]);
		}
		
		this.parent();		
	}

});

});