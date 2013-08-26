ig.module(
	'game.entities.level'
)
.requires(
	'impact.entity'
)
.defines(function(){
    	
EntityLevel = ig.Entity.extend({
	logicIndex:-100,
	// editor
	_wmDrawBox: true,
	_wmBoxColor: 'rgba(0, 0, 255, 0.7)',	
	size: {x: 8, y: 8},
	isControlLevel: false,
	
	
	/******* callback functions *******/

	onTrigger: function(trigger,other){	
	},

	
	onUI: function(name){
		if(name=='return'){
			ig.gm.loadLevel('Menu', false);
		}
	},
	
		
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		// clear pressed key & mouse
		ig.input.clearPressed();
	},
	
	ready: function(){
		this.parent();
		// record level controller entity
		ig.gm.currentLevel=ig.game.getEntitiesByType(EntityLevel)[0];		
	},
        
	update: function(){
		this.parent();
	},
	
	draw: function(){		
		this.parent();
	}
});

});