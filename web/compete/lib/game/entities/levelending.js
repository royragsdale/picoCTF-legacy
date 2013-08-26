ig.module(
	'game.entities.levelending'
)
.requires(
	'game.entities.levelscene',
    'game.entities.endplayer'
)
.defines(function(){
	
EntityLevelending = EntityLevelscene.extend({
	name: 'ending',
	size:{x:8,y:8},
    teaminfo: null,
    displayTeamname: new Array(),
    displayScore:new Array(),
    zIndex: 0,
    displayWidth: 15,
    cutscene:{
        'Ending':[
            {
                cmd:'gotoPoint',
                who:'endship',
                where:'WP1'
            },
            {
                cmd:'custom',
                init: function()
                {
                    ig.game.getEntityByName('endship').kill();
                    ig.game.getEntityByName('spaceBackground').kill();
                    ig.game.spawnEntity(EntitySprite,0,0,{size:{x:768,y:704},path:'media/endingawardscene.png'});
                    ig.game.spawnEntity(EntityEndplayer,352,200);
                    ig.game.spawnEntity(EntityVoid,352,310,{name:'WP2'});
                    ig.game.spawnEntity(EntityVoid,352,420,{name:'WP3'});
                    ig.game.spawnEntity(EntityVoid,352,530,{name:'WP4'});
                    ig.game.spawnEntity(EntityVoid,352,640,{name:'WP5'});
                    var posleftx = 242;
                    var posrightx = 502;
                    var posy = 350;
                    for(var i = 0; i < 10; i++)
                    {
                        if (i % 2 == 0)
                        {
                            var player = ig.game.spawnEntity(EntityPlayer,posleftx,posy,{name:i});
                            player.facing = DIRECTIONS.RIGHT;
                            posleftx -= 40;
                        }
                        else
                        {
                            var player = ig.game.spawnEntity(EntityPlayer,posrightx,posy,{name:i});
                            player.facing = DIRECTIONS.LEFT;
                            posy += 80
                            posrightx += 40;
                        }
                    }
                    var player = ig.game.getEntitiesByType(EntityPlayer);
                    for (var i in player)
                    {
                        player[i].control = false;
                    }
                }
            },
            {
                cmd:'gotoPoint',
                who:'endplayer',
                where:'WP2'
            },
            {
                cmd:'custom',
                init:function()
                {
                    var player = ig.game.getEntityByName('endplayer');
                    player.currentAnim = player.anims.transition1;
                    /*var robot = ig.game.spawnEntity(EntityRobot,352,200);
                    robot.following = true;
                    robot.followTarget = ig.game.getEntityByName("endplayer");*/
                }
            },
            {
                cmd:'sleep',
                sleeptime: 0.2
            },
            {
                cmd:'custom',
                init:function()
                {
                    var player = ig.game.getEntityByName('endplayer');
                    player.currentAnim = player.anims.upgrade1;
                }
            },
            {
                cmd:'gotoPoint',
                who:'endplayer',
                where:'WP3'
            },
            {
                cmd:'custom',
                init:function()
                {
                    var player = ig.game.getEntityByName('endplayer');
                    player.currentAnim = player.anims.transition2;
                }
            },
            {
                cmd:'sleep',
                sleeptime: 0.2
            },
            {
                cmd:'custom',
                init:function()
                {
                    var player = ig.game.getEntityByName('endplayer');
                    player.currentAnim = player.anims.upgrade2;
                }
            },
            {
                cmd:'gotoPoint',
                who:'endplayer',
                where:'WP4'
            },
            {
                cmd:'custom',
                init:function()
                {
                    var player = ig.game.getEntityByName('endplayer');
                    player.currentAnim = player.anims.transition3;
                }
            },
            {
                cmd:'sleep',
                sleeptime: 0.2
            },
            {
                cmd:'custom',
                init:function()
                {
                    var player = ig.game.getEntityByName('endplayer');
                    player.currentAnim = player.anims.upgrade3;
                }
            },
            {
                cmd:'gotoPoint',
                who:'endplayer',
                where:'WP5'
            },
            {
                cmd:'custom',
                init:function()
                {
                   ig.gm.loadLevel("Credit",true);
                }
            }
        ]
    },
    init: function( x, y, settings ) {
        this.parent( x, y, settings );

    },
    ready: function()
    {

        this.teaminfo = getTopScores();
        if (typeof this.teaminfo[0] != "undefined")
        {
            for(var i in this.teaminfo)
            {
                this.displayTeamname[i] = "" + this.teaminfo[i].teamname;
                if(this.displayTeamname[i].length > this.displayWidth)
                {
                    for(var j = this.displayWidth; j< this.displayTeamname[i].length; j++)
                    {
                        if (this.displayTeamname[i][j] == ' ')
                        {
                             this.displayTeamname[i] = this.displayTeamname[i].slice(0,j) + "\n" + this.displayTeamname[i].slice(j+1);
                             break;
                        }
                    }
                }
                this.displayScore[i] = "Score: " + this.teaminfo[i].score;

            }
        }
        else
        {
            for (var i = 0; i< 10; i++)
            {
                this.displayTeamname[i] = " ";
            }
        }
        this.startCutscene('Ending');
        this.parent();
    },
    update: function()
    {
        this.parent();
    }
	
});


});