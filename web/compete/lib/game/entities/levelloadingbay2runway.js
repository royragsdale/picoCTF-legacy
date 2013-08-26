ig.module(
	'game.entities.levelloadingbay2runway'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
	
EntityLevelloadingbay2runway = EntityLevelscene.extend({
	name: 'loadingbay2runway',
	size:{x:8,y:8},
    zIndex: 0,
    endingFlag: false,
    cutscene: {
        "Stair Cutscene": [
            {
                cmd:'talk',
                who: 'Taylor',
                what: 'Are you OK Toast?'

            },
            {
                cmd:'talk',
                who: 'ToastRed',
                what: 'Not really, but I can still fly the ship!'
            },
            {
                cmd:'custom',
                init:function(){
                    ig.gm.loadLevel("Runway2spaceship",true);
                }
            }
        ]
    },
    animSheet: new ig.AnimationSheet ('media/Transition3.png', 768 ,704),
    init: function( x, y, settings ) {
        this.parent( x, y, settings );
        this.addAnim('cutscene', 0.6, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],true);
    },
    ready: function()
    {
        this.parent();
    },
    update:function()
    {
        //Check if there is a animation sheet
        if(this.currentAnim){
            if(this.currentAnim.loopCount == 1){
                if (!this.endingFlag)
                {
                    this.endingFlag = true;
                    ig.game.spawnEntity(EntityDialogbox, -800, -800);
                    this.startCutscene("Stair Cutscene");
                }
            }
        }
        this.parent();
    }
	
});


});