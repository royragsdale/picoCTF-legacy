ig.module(
	'game.entities.levelgalaxyselect'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
    	
EntityLevelgalaxyselect = EntityLevelscene.extend({
    name: 'Galaxyselect',
	//problemsInLevel: ['41','42','43','44','45','46'],
	//problemSolvedNeeded: 5,
	//nextLevel: 'Spaceship',
	
	cutscene: {

	},	

	
	
	
	/******* callbacks ********/

	

	/******* events ********/
	
	init: function( x, y, settings ) {

		this.parent( x, y, settings );       
	},
	
	ready: function(){
        this.isFocusCamera = false;
		this.parent();
    },
    //Upgrade Equipments

    onTrigger: function(trigger,other){
        this.parent(trigger,other);
        // player triggered a problem
    },
    onUI: function(name)
    {
        if(name == 'return')
        {
            ig.gm.loadLevel('Spaceship');
        }
    }
});

});