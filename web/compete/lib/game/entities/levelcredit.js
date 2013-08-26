ig.module(
	'game.entities.levelcredit'
)
.requires(
	'game.entities.level'
)
.defines(function(){
    	
EntityLevelcredit = EntityLevel.extend({
    name: 'Credit',
	isControlLevel:false,
	state:0,
	credity: 700,

	/******* events ********/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
	},
	
	ready: function(){
        this.parent();
        goodjob=ig.game.getEntityByName('goodjob');
		credit=ig.game.getEntityByName('credit');
		thankyou=ig.game.getEntityByName('thankyou');
		
		credit.enabled=true;
		goodjob.enabled=false;
		thankyou.enabled=false;
	},

    update: function(){
        this.parent();
		if(this.state==0){
			if(this.credity>=-900)
				this.credity-=2;
			
			credit.pos.x=0;
			credit.pos.y=this.credity;
			if(ig.input.pressed('mouse')||ig.input.pressed('enter')){
				this.state++;
				credit.enabled=false;
				goodjob.enabled=true;
			}
		}else if(this.state==1){
			if(ig.input.pressed('mouse')||ig.input.pressed('enter')){
				this.state++;
				goodjob.enabled=false;
				thankyou.enabled=true;
			}
		}else if(this.state==2){
			if(ig.input.pressed('mouse')||ig.input.pressed('enter')){
				this.state++;
                ig.gm.endingFlag = true;
                ig.gm.loadLevel("Menu",true);
				
			}
		}
    }



});

});