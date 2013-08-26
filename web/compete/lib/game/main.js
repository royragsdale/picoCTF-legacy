ig.module( 
	'game.main' 
)
.requires(
	'impact.game',
	'impact.font',
	//'impact.debug.debug',
	
	'game.classes.gamemanager',
	'game.classes.soundmanager'
)
.defines(function(){

MyGame = ig.Game.extend({
	init: function() {
	    ig.sm=new SoundManager();
		ig.gm=new GameManager();
	},
	
	update: function() {
		this.parent();
		ig.gm.update();
		ig.sm.update();
	},
	
	draw: function() {
		this.parent();
		ig.gm.draw();
	}	
});

ig.main('#canvas', MyGame, 60, 768, 704, 1);

});