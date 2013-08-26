ig.module(
	'game.entities.levelselection'
)
.requires(
	'game.entities.level'
)
.defines(function(){
    	
EntityLevelselection = EntityLevel.extend({		
	index:0,
	indexMax:4,
	row:1,
	column:4,
	background: new ig.Image('media/MainMenu.png'),	
	selector: null,
	
	doSelect: function(){
		ig.sm.play('select');
	},
	

	/******* callbacks *******/
	
	onClick: function(name){
		this.doSelect();
	},
	
	onHover: function(name){
		var t=parseInt(name);
		if(t!=this.index){
			this.index=t;
			ig.sm.play('select');
		}
	},
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {		
		this.parent( x, y, settings );		
	},
	
	ready: function(){
		this.parent();
		
	},
		
	update: function(){
		this.parent();
		
		if(ig.input.pressed('down')||
		   ig.input.pressed('up')||
		   ig.input.pressed('right')||
		   ig.input.pressed('left')){
			if(ig.input.pressed('down'))this.index+=this.column;
			if(ig.input.pressed('up'))this.index-=this.column;			
			if(ig.input.pressed('right'))this.index++;
			if(ig.input.pressed('left'))this.index--;
			if(this.index>=this.indexMax)
				this.index-=this.indexMax;
			if(this.index<0)
				this.index+=this.indexMax;
						
			ig.sm.play('select');  
		}	
		var selector=ig.game.getEntityByName('selector');
		var pos=ig.game.getEntityByName('m'+this.index);
		centerAlign(selector,pos);
		
		if(ig.input.pressed('enter')){			
			this.doSelect();
		}
	},
	
	draw: function(){
		this.parent();
		this.background.draw(0,0);		
	},

});

});