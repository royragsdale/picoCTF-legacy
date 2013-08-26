ig.module(
	'game.entities.mark'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityMark = ig.Entity.extend({	
	size: {x: 64, y: 64},
	zIndex: 5000,
	enabled: false,
	animSheet: new ig.AnimationSheet( 'media/MarkSheetsNew.png',64,64),
    collides: ig.Entity.COLLIDES.NEVER,
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {		
		this.parent( x, y, settings );
		this.addAnim('must',1,[2]);
		this.addAnim('bonus',1,[6]);
		this.addAnim('solved',1,[1]);
		this.addAnim('exit',1,[4]);
        this.addAnim('stop',1,[0]);
	},	
	
	update: function(){
		if(!this.enabled)return;
		this.parent();
	},
	
	draw: function(){
		if(!this.enabled)return;
		this.parent();		
	},
	
});


});