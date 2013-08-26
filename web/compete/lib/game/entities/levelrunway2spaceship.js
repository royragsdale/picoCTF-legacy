ig.module(
	'game.entities.levelrunway2spaceship'
)
.requires(
	'game.entities.levelscene',
    'game.entities.car',
    'game.entities.shadowship',
    'game.entities.transitionship',
    'game.entities.spacebkgd'
)
.defines(function(){
	
EntityLevelrunway2spaceship = EntityLevelscene.extend({
	name: 'runway2spaceship',
	size:{x:8,y:8},
    zIndex: 0,
    // Stored transition animation sheet
    // 1: Room to Spaceport
    // 2: Spaceport to Loadingbay
    // 3: Enter the Ship
    // 4: Ship to Galaxy

    animSheet: new ig.AnimationSheet('media/Transition4/Env_Runway_Outside Spaceport.png',1024,2048),

    cutscene: {
       'Galaxy Transition' : [
           {
               cmd:'custom',
               init: function(){
                    var shadow = ig.game.getEntityByName("Shadowship");
                   _this.focusTarget = shadow;
                   shadow.following = true;
                   shadow.followTarget = ig.game.getEntityByName("Transitionship");
               }
           },
           {
                cmd:'sound',
                name:'spaceship'
           },
           {
               cmd:'gotoPoint',
               who:'Transitionship',
               where:'WP1'
           },
           {
               cmd:'custom',
               init:function(){
                   var shadow = ig.game.getEntityByName("Shadowship");
                   var ship = ig.game.getEntityByName("Transitionship");

                   shadow.currentAnim  = shadow.anims.bigger;
                   ship.currentAnim = ship.anims.landoff;
                   shadow.speed = 120;
                   ship.speed = 150;
               }
           },
           {
               cmd:'gotoPoint',
               who:'Transitionship',
               where:'WP2'
           },
           {
               cmd:'custom',
               init:function(){
                   var shadow = ig.game.getEntityByName("Shadowship");
                   var ship = ig.game.getEntityByName("Transitionship");

                   shadow.currentAnim  = shadow.anims.smaller;
                   shadow.speed = 160;
                   ship.speed = 200;
                   //ship.currentAnim = ship.anims.air;
               }
           },
           {
               cmd:'gotoPoint',
               who:'Transitionship',
               where:'WP3'
           },
           {
               cmd:'custom',
               init:function(){
                   var shadow = ig.game.getEntityByName("Shadowship");
                   var ship = ig.game.getEntityByName("Transitionship");

                   shadow.currentAnim  = shadow.anims.smallest;
                   shadow.speed = 240;
                   ship.speed = 300;
                   //ship.currentAnim = ship.anims.space;
               }
           },
           {
               cmd:'gotoPoint',
               who:'Transitionship',
               where:'WP4'
           },
           {
               cmd:'custom',
               init:function(){
                   ig.game.spawnEntity(EntitySpacebkgd, 0, -1124, {zIndex: -100});
                   _this.addAnim('cutscene',1,[0],true);
                   _this.pos.x = -2000;
                   _this.pos.y  = -2000;
                   var shadow = ig.game.getEntityByName("Shadowship");
                   shadow.currentAnim = shadow.anims.none;
                   shadow.followMinDis  = 1;
               }
           },
           {
               cmd:'custom',
               init: function(){
                   ig.game.getEntityByName("Shadowship").kill();
                   var ship = ig.game.getEntityByName("Transitionship");
                   _this.focusTarget = ship;
                   ship.currentAnim = ship.anims.space;
               }
           },
           {
               cmd:'gotoPoint',
               who:'Transitionship',
               where:'WP5'
           },

           {
               cmd:'custom',
               init: function(){
                   ig.gm.loadLevel("Spaceship",true);
               }
           }
       ]
    },
    init: function( x, y, settings ) {
        this.parent( x, y, settings );

    },
    ready: function()
    {
        _this = this;
        this.addAnim('cutscene', 1,[0],true);
        this.galaxyTrans();
        this.parent();
    },
    update:function()
    {
        this.parent();
    },
    galaxyTrans: function()
    {
        ig.game.spawnEntity(EntityTransitionship,320,1160);
        ig.game.spawnEntity(EntityShadowship,320,1500);
        ig.game.spawnEntity(EntityVoid, 320, 1100,{name:"WP1"});
        ig.game.spawnEntity(EntityVoid,320,800,{name:"WP2"});
        ig.game.spawnEntity(EntityVoid,320,400,{name:"WP3"});
        ig.game.spawnEntity(EntityVoid,320,-260,{name:"WP4"});
        ig.game.spawnEntity(EntityVoid,320,-860,{name:"WP5"});
        this.startCutscene('Galaxy Transition');
    }
	
});


});