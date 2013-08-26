ig.module(
	'game.entities.leveltitle'
)
.requires(
	'game.entities.level'
)
.defines(function(){
    	
EntityLeveltitle = EntityLevel.extend({		
    name: 'Title',
	titleImage: [
		new ig.Image('media/Toaster-Wars_Demo-Title-Screen.png'),
		//new ig.Image('media/Toaster-Wars_Demo-Prompt.png'),
	],
	titleIndex:0,
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		if(typeof ig.gm!='undefined')
			ig.sm.playbgm('Title');
	},
		
	update: function(){
		this.parent();
		
		if(ig.input.pressed('enter') || ig.input.pressed('mouse')){
			this.titleIndex++;
			if(this.titleIndex==this.titleImage.length){
				if(ig.gm.problemStates['21'].solved){
					ig.gm.loadLevel('Menu', true);								
				}else{
					ig.gm.loadLevel('Opening', true);			
				}
				
			}
		}
	},
	
	draw: function(){
		this.parent();
		if(typeof this.titleImage[this.titleIndex]!='undefined')
			this.titleImage[this.titleIndex].draw(0,0);
	},

});

});