ig.module(
	'game.entities.levelroom2airport'
)
.requires(
	'game.entities.levelscene',
    'game.entities.car'
)
.defines(function(){
	
EntityLevelroom2airport = EntityLevelscene.extend({
	name: 'room2airport',
	size:{x:8,y:8},
    zIndex: 0,
    myTween: null,
    endingflag: false,

    animSheet: new ig.AnimationSheet ('media/Transition1/YardTransition2.png', 3900,1500),

    cutscene: {
       'Room Transition':[
		   {
			   cmd: 'gotoPoint',
			   who: 'Taylor',
			   where: 'WP1'
		   },
           {
               cmd: 'gotoPoint',
               who: 'Taylor',
               where: 'WP2'
           },
           {
               cmd:'custom',
               init: function(){

                   var car = ig.game.getEntityByName("Car");
                   car.currentAnim = car.anims.open;
               }
           },
           {
               cmd: 'sleep',
               sleeptime: 0.4
           },
           {
               cmd:'custom',
               init: function(){
                   var car = ig.game.getEntityByName("Car");
                   ig.game.getEntityByName("Taylor").kill();
                   ig.game.getEntityByName("Toast").kill();
                   car.currentAnim = car.anims.getin;
               }
           },
           {
               cmd: 'sound',
               name: 'car_driving'
           },
           {
               cmd: 'sleep',
               sleeptime: 0.4
           },
           {
               cmd:'custom',
               init: function(){
                   var car = ig.game.getEntityByName("Car");
                   car.currentAnim = car.anims.drive;
                   _this.focusTarget = car;
               }
           },

           {
               cmd:'gotoPoint',
               who:'Car',
               where:'WP3'
           },
           {
               cmd:'custom',
               init: function(){
                   var car = ig.game.getEntityByName("Car");
                   car.speed = 300;
               }
           },
           {
               cmd: 'gotoPoint',
               who:'Car',
               where:'WP4'

           },

           {
               cmd:'custom',
               init: function(){
                   //_this.myTween.stop();
                   ig.gm.loadLevel("Airport",true)
               }
           }
	   ]
    },

    init: function( x, y, settings ) {
        this.parent( x, y, settings );
        //Just test

    },
    ready: function()
    {
        _this = this;
        this.addAnim('cutscene',1,[0],true);
        this.roomTrans();
        this.parent();
    },
    update:function()
    {
        this.parent();
    },
    roomTrans: function()
    {
        ig.game.spawnEntity(EntityPlayer,1120,1150);
        var robot = ig.game.spawnEntity(EntityRobot,1120,1130);
        robot.following = true;
        robot.followTarget = ig.game.getEntityByName("Taylor");
        ig.game.spawnEntity(EntityCar,500,280);
        ig.game.spawnEntity(EntityVoid, 500,1100,{name:"WP1"});
        ig.game.spawnEntity(EntityVoid, 500,430,{name:"WP2"});
        ig.game.spawnEntity(EntityVoid, 2500,380,{name:"WP3"});
        ig.game.spawnEntity(EntityVoid, 3350,480,{name:"WP4"});
        this.startCutscene('Room Transition');
    }
	
});


});