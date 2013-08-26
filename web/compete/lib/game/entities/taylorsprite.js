ig.module(
	'game.entities.taylorsprite'
)
.requires(
	'impact.entity'
)
.defines(function(){

EntityTaylorsprite = ig.Entity.extend({
	size: {x:64, y:64},
	_wmScalable: true,
	animSheet: new ig.AnimationSheet('media/taylorJump.png',64,64),
	enabled: true,
	zIndex:100,
	name :'JumpTaylor',
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );

		this.addAnim('idle', 1, [0]);
        this.addAnim('jump', 1,[1],true);
        this.addAnim('flip',1,[2],true);
        this.addAnim('lay',1,[3],true);
	},

	draw: function() {
		if(!this.enabled)return;
		//this.zIndex=this.pos.y;
		this.parent();	
	},
});

});