ig.module(
	'game.entities.button'
)
.requires(
	'game.entities.ui'
)
.defines(function(){

EntityButton = EntityUi.extend({
	size: {x:64, y:64},
	animSheet: new ig.AnimationSheet('media/Go Back Button.png',64,64),
	sClick: new ig.Sound('media/sound/click.mp3',true,false,false),
	dy: 0,
	click: function(){				
		this.sClick.play();
	},
	
	hover: function(){
	},
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
	},
		
	update: function(){
		this.parent();
		
		// decide idle/hover accroding to mouse position		
		var mousex=ig.input.mouse.x+ig.game.screen.x;
		var mousey=ig.input.mouse.y+ig.game.screen.y;
		if((mousex>this.pos.x && mousex<this.pos.x+this.size.x) &&
			(mousey>this.pos.y && mousey<this.pos.y+this.size.y)){
			if (ig.input.pressed("mouse")){
				ig.input.clearPressed();
				this.currentAnim=this.anims['idle'];
				this.click();
			}else{
				this.currentAnim=this.anims['hover'];
				this.hover();
			}
		}else{
            this.dy = 0;
			this.currentAnim=this.anims['idle'];
		}
	},	
	
	draw: function(){
		this.parent();
	}
});

});