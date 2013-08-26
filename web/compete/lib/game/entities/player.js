ig.module(
	'game.entities.player'
)
.requires(
	'game.entities.walker'
)
.defines(function(){
	
EntityPlayer=EntityWalker.extend({	
	name: 'Taylor',
	animSheet: new ig.AnimationSheet('media/playersprite.png',64,64),
	followMinDis: 1,
	collides: ig.Entity.COLLIDES.ACTIVE,
    ignoreCollision: false,
    enginePos1 : null,
    enginePos2 : null,
    enginePos3 : null,
	
	
	/******* events *******/

	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		this.control=true;
		this.following=false;
				
	},
	
	update: function(){
		this.parent();
        if (ig.gm.currentLevel.name == 'Spaceship')
        {
            this.enginePos3 = (this.pos.x > 560 && this.pos.y > 850 && this.pos.x < 730 && this.pos.y < 910);
            this.enginePos2 = (this.pos.x > 850 && this.pos.y > 788 && this.pos.x < 930 && this.pos.y < 850);
            this.enginePos1 = (this.pos.x > 915 && this.pos.y > 850 && this.pos.x < 958 && this.pos.y < 910);
            this.calculateCollision();
        }
        else this.ignoreCollision = false;
	},
    draw: function(){
        this.parent();
        if(this.name != "Taylor")
        {
            if(typeof ig.gm != 'undefined' && typeof ig.game.getEntityByName("ending").displayTeamname[this.name] != 'undefined');
            {
                ig.gm.fonts[0].draw(ig.game.getEntityByName("ending").displayTeamname[this.name],this.pos.x,this.pos.y - 60,ig.Font.ALIGN.LEFT);
            }
        }
    },
    handleMovementTrace: function( res ) {
        if (ig.gm.currentLevel.name == "Spaceship")
        {
            if (this.ignoreCollision)
            {
                this.pos.x += this.vel.x * ig.system.tick;
                this.pos.y += this.vel.y * ig.system.tick;
            }
            else this.parent(res);
        }
        else
        {
            this.parent( res );
        }
    },
    calculateCollision: function(){
        switch(EQUIPMENT['engine'])
        {
            case 1:
            {
                this.ignoreCollision = this.enginePos3 || this.enginePos2 || this.enginePos1;
                break;
            }
            case 2:
            {
                this.ignoreCollision = this.enginePos3 || this.enginePos2;
                break;
            }
            case 3:
            {
                this.ignoreCollision = this.enginePos3
                break;
            }
            case 4:
            {
                this.ignoreCollision = false;
                break;
            }
        }
    }
});


});