ig.module(
	'game.entities.levelmenu'
)
.requires(
	'game.entities.levelselection'
)
.defines(function(){
    	
EntityLevelmenu = EntityLevelselection.extend({		
    name: 'Menu',
	background: new ig.Image('media/MainMenu.png'),	
	indexMax:3,
	row:3,
	column:1,
	
	
	doSelect: function(){
		this.parent();
		switch(this.index){
		case 0:
			var s='Opening';
			if(ig.gm.levelStates['Room'].unlocked)
				s='Room';
			if(ig.gm.levelStates['Airport'].unlocked)
				s='Airport';
			if(ig.gm.levelStates['Loadingbay'].unlocked)
				s='Loadingbay';
			if(ig.gm.levelStates['Spaceship'].unlocked)
				s='Spaceship';
			
			ig.gm.loadLevel(s, true);
		break;
		case 1:
			ig.gm.loadLevel('Problemselect', false);
		break;
		case 2:
			ig.gm.loadLevel('Levelselect', false);
		break;
		}
	},

});

});