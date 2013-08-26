ig.module(
	'game.entities.levellevelselect'
)
.requires(
	'game.entities.levelselection',
	'game.entities.menulevelfill',
	'game.entities.menulevellock'
)
.defines(function(){
    	
EntityLevellevelselect = EntityLevelselection.extend({		
    name: 'Levelselect',
	background: new ig.Image('media/LevelsMenu.png'),	
	indexMax:4,
	row:2,
	column:2,
	
	
	doSelect: function(){
		this.parent();
		
		var names={
			0:'Room',
			1:'Airport',
			2:'Loadingbay',
			3:'Spaceship',
		};
		var name=names[this.index];
		
		// TODO: comment this for debug convenience, remember to uncomment!
		if(ig.gm.levelStates[name].unlocked)
			ig.gm.loadLevel(name, true);
	},
	
	ready: function(){
		this.parent();					
		for(var s in LEVELS){
			var fill=ig.game.spawnEntity(EntityMenulevelfill);				
			var pos=ig.game.getEntityByName('m'+LEVELS[s]);
			centerAlign(fill,pos);
			fill.currentAnim=fill.anims[s];
			if(ig.gm.levelStates[s].unlocked){			
			}else{
				var lock=ig.game.spawnEntity(EntityMenulevellock);				
				centerAlign(lock,pos);
			}
		}
	}	
});

});