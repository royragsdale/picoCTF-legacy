ig.module(
	'game.entities.holoraysprite'
)
.requires(
	'impact.entity'
)
.defines(function(){

EntityHoloraysprite = ig.Entity.extend({
	size: {x:128, y:64},
	enabled: false,
    zIndex: 2000,
	animSheet: new ig.AnimationSheet('media/hologramrays.png',128,64),
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
        this.addAnim('holoray0',1,[0]);
        this.addAnim('holoray1',1,[1]);
        this.addAnim('holoray2',1,[2]);
        this.addAnim('holoray3',1,[3]);
	},

	draw: function() {
		if(!this.enabled)return;
		this.parent();	
	}
});

});