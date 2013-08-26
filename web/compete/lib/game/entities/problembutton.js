ig.module(
	'game.entities.problembutton'
)
.requires(
	'game.entities.button'
)
.defines(function(){

EntityProblembutton = EntityButton.extend({
	animSheet: new ig.AnimationSheet('media/Hints Buttons.png',64,64),
    mark: null,
    size: {x:64, y: 64},
    solved: false,
    _wmScalable: true,
    _wmDrawBox: true,
    _wmBoxColor: 'rgba(196, 255, 0, 0.7)',
	name: '',
    dy: 0,
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.addAnim('idle',1,[2]);
        if(typeof ig.gm!='undefined'){
            this.mark=ig.game.spawnEntity(EntityMark);
            this.mark.enabled = true
            this.mark.pos.x=this.pos.x;
            this.mark.pos.y=this.pos.y-this.mark.size.y;
        }
	},
	
	update: function(){
		this.parent();
        if(this.solved){
            this.mark.currentAnim=this.mark.anims['solved'];
        }
        this.mark.pos.x=this.pos.x;
        this.mark.pos.y=this.pos.y-this.mark.size.y - this.dy;
    },
	
	click: function(){
		this.parent();
        ig.gm.currentLevel.problemName = this.name;
		ig.gm.currentLevel.onUI('problem');
	},

    hover: function(){
        this.parent();
        this.dy = 10;
    },
    draw: function(){
        ig.gm.fonts[1].draw(PROBLEMS[this.name].prob,this.pos.x,this.pos.y,ig.Font.ALIGN.LEFT);
    }

});

});