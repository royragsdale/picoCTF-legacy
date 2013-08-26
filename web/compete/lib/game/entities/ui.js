ig.module(
	'game.entities.ui'
)
.requires(
	'impact.entity'
)
.defines(function(){	
	
EntityUi = ig.Entity.extend({
	zIndex: 10000,
	logicIndex: 100,
	screenpos: {x:0,y:0},
	
	
	/******* events *******/
	
	init: function( x,y,settings ) {
		this.parent(x,y,settings);
		
	},
	
	ready: function(){
		this.screenpos.x=this.pos.x;
		this.screenpos.y=this.pos.y;
	},
	
	update: function(){
		
	},
	
	draw: function(){
		if(typeof ig.gm!='undefined'){
			this.pos.x=this.screenpos.x+ig.game.screen.x;
			this.pos.y=this.screenpos.y+ig.game.screen.y;
		}
		this.parent();
	}
	
});

});