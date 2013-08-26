ig.module(
	'game.entities.levelspaceship'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
    	
EntityLevelspaceship = EntityLevelscene.extend({
    name: 'Spaceship',
	isControlLevel:true,

	
	/******* callbacks ********/


	/******* events ********/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
	},
	
	ready: function(){
        this.parent();
        //equipText = ''

        var equipSprite = ig.game.getEntitiesByType(EntityEquipsprite);

        for(var i in equipSprite)
        {
            var shipEquip  = equipSprite[i];
            if (shipEquip.name != "regularship"){
                switch (EQUIPMENT[shipEquip.name])
                {
                    case 1:
                    {
                        shipEquip.currentAnim = shipEquip.anims.blue;
                        break;
                    }
                    case 2:
                    {
                        shipEquip.currentAnim = shipEquip.anims.silver;
                        break;
                    }
                    case 3:
                    {
                        shipEquip.currentAnim = shipEquip.anims.yellow;
                        break;
                    }
                    case 4:
                    {
                        shipEquip.currentAnim = shipEquip.anims.white;
                        break;
                    }
                }
            }
        }

        //console.log(equipText);
        //this.cutscene = {
        //    'Display Equipment':[
        //        {
        //            name: 'message',
        //            what: equipText
        //        }
        //    ]
        //}
        //this.startCutscene('Display Equipment');
	},
    //Upgrade Equipments
    changeEquip: function(equipment, level)
    {

    },
    onTrigger: function(trigger,other){
        this.parent(trigger,other);
        var t=trigger.name+'';

        // exit to next level
        if(t=='question' && other.name=='Taylor'){
            //this.startCutscene('Finished');
            ig.sm.play('click');
            ig.gm.loadLevel("Galaxyselect");
        }

        // player triggered a problem
    },
    update: function(){
        this.parent();
        var mark = ig.game.getEntityByName('question').mark;
        mark.pos.y += 40;
        mark.pos.x += 16;
    }





});

});