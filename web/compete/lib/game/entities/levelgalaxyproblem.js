ig.module(
	'game.entities.levelgalaxyproblem'
)
.requires(
	'game.entities.level'
)
.defines(function(){
    	
EntityLevelgalaxyproblem = EntityLevel.extend({
    name: '',
    spawnNumber: 0,
	problemName: '',

    cutscene: {

	},






    /******* callbacks ********/

	

	/******* events ********/
	onSubmit: function(success, message)
    {
        this.parent(success, message);
    },
	init: function( x, y, settings ) {

		this.parent( x, y, settings );       
	},
	
	ready: function(){
		this.parent();
        ig.gm.category = window.location.hash.slice(1);
        this.spawnNumber = GALAXYPROBLEMS[ig.gm.category].num;
        this.name = ig.gm.category
        var problemButton = ig.game.getEntitiesByType(EntityProblembutton);
        for (var i = 0; i < this.spawnNumber; i++)
        {
            problemButton[i].solved = ig.gm.problemStates[problemButton[i].name].solved;
        }
    },


    onTrigger: function(trigger,other){
        this.parent(trigger,other);

    },
    onUI :function(name){
        this.parent(name);
        if(name == 'return')
        {
            ig.gm.loadLevel('Galaxyselect');
        }
        if(name == 'problem')
        {
            ig.gm.currentProblem = this.problemName;
            ig.gm.loadLevel("Problem");
        }
    }
});

});