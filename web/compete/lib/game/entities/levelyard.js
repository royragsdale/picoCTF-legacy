ig.module(
	'game.entities.levelyard'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
    	
EntityLevelyard = EntityLevelscene.extend({		
    name: 'Yard',
	problemsInLevel: [],
	problemSolvedNeeded: 0,
	nextLevel: 'Room',
	
	cutscene: {
		'get toast':[

            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'WP1'
            },
            {
                cmd: 'talk',
                who: 'TaylorSurprise',
                what: 'Whoooooooooaaaa! What is that, a satellite?'
            },
            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'WP2'
            },
            {
                cmd: 'talk',
                who: 'Taylor',
                what: 'Is this a robot? I think it is!'
            },
            {
                cmd: 'custom',
                init: function(){
					ig.gm.levelStates['Room'].unlocked=true;
					ig.gm.problemStates['21'].unlocked=true;
                    ig.gm.loadLevel('Room',true);
                }
            }
		]
	},
	
	
	/******* inlevel states ********/
	
	gottost: false,
	
	
	/******* callbacks ********/
	
	onTrigger: function(trigger,other){
		this.parent(trigger,other);

	},	
	
	onUI:function(name){
		this.parent(name);
	},
	
	
	/******* events ********/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );

	},
    ready: function(){
        this.parent();
        this.startCutscene('get toast');
    },
    loadState: function(){

    },
    saveState: function(){

    }

});

});