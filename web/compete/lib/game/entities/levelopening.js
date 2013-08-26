ig.module(
	'game.entities.levelopening'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
    	
EntityLevelopening = EntityLevelscene.extend({
    name: 'Opening',
	nextLevel: 'Room',
    intervalVar: null,
    screenx : null,
    screeny : null,
	
	cutscene: {
		'opening':[

            {
                cmd: 'talk',
                who: 'Taylor',
                what: 'What\'s a file system? I should probably search for it on the Internet...'
            },
            {
                cmd: 'sound',
                name:'crash'
            },
            {
                cmd: 'custom',
                init: function()
                {
                    _this.intervalVar = setInterval(function(){
                        ig.game.screen.x += Math.random() * 10 - 5;
                        ig.game.screen.y += Math.random() * 10 - 5;
                    },25)
                    var player = ig.game.getEntityByName('JumpTaylor');
                    var chair = ig.game.getEntityByName('chair');
                    player.currentAnim = player.anims.jump;
                    player.pos.x += 60;
                    chair.pos.y += 40;
                }
            },
            {
                cmd:'sleep',
                sleeptime: 0.7
            },
            {
                cmd:'custom',
                init: function(){
                    var player = ig.game.getEntityByName('JumpTaylor');
                    player.currentAnim = player.anims.flip;
                }
            },
            {
                cmd:'sleep',
                sleeptime: 0.7
            },
            {
                cmd:'custom',
                init: function(){
                    var player = ig.game.getEntityByName('JumpTaylor');
                    player.currentAnim = player.anims.lay;
                }
            },
            {
                cmd:'sleep',
                sleeptime: 0.7
            },
            {
                cmd:'custom',
                init: function()
                {
                    clearInterval(_this.intervalVar);
                    ig.game.screen.x = 0;
                    ig.game.screen.y = 0;
                }
            },
            {
                cmd: 'talk',
                who: 'TaylorSurprise',
                what:'What happened in the yard? I need to check it out!'
            },
            {
                cmd:'custom',
                init: function(){
                    var player = ig.game.getEntityByName('JumpTaylor');
                    player.kill();
                    var taylor = ig.game.spawnEntity(EntityPlayer,266,252);
                }
            },
            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'WP2'
            },
            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'WP3'
            },
            {
                cmd: 'custom',
                init:function(){
                    ig.gm.loadLevel("Yard",true);
                }
            }

		]
	},	


	
	saveState: function(){
	},
	loadState: function(){
	},
	
	/******* callbacks ********/
	
	onTrigger: function(trigger,other){
		this.parent(trigger,other);

	},
	

	/******* events ********/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		if(typeof ig.gm!='undefined')
			ig.sm.playbgm('Game');
	},
	
	ready: function(){
        this.parent();
        _this = this;

        this.isFocusCamera = false;
        this.startCutscene('opening');
	}
});

});
