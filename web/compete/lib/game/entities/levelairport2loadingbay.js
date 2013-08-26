ig.module(
	'game.entities.levelairport2loadingbay'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
	
EntityLevelairport2loadingbay = EntityLevelscene.extend({
	name: 'airport2loadingbay',
	size:{x:8,y:8},
    zIndex: 0,
    animSheet: new ig.AnimationSheet ('media/Transition2.png', 768 ,704),
    init: function( x, y, settings ) {
        this.parent( x, y, settings );
        this.addAnim('cutscene',0.5,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],true);

    },
    ready: function()
    {
        this.parent();
    },
    update:function()
    {
        //Check if there is a animation sheet
        if(this.currentAnim){
            if(this.currentAnim.loopCount == 1)
                ig.gm.loadLevel("Loadingbay",true);
        }
        this.parent();
    }
	
});


});