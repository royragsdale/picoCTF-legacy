ig.module(
	'game.entities.sprite'
)
.requires(
	'impact.entity'
)
.defines(function(){

EntitySprite = ig.Entity.extend({
	size: {x:64, y:64},
	_wmScalable: true,
	path: 'media/robotsprite.png',
	enabled: true,
	zIndex:100,
		
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		if(this.path.substring(0,6)!='media/')
			this.path='media/'+this.path;
		this.animSheet=new ig.AnimationSheet(this.path,this.size.x,this.size.y),
		this.addAnim('idle', 1, [0]);
	},

	draw: function() {
		if(!this.enabled)return;
		this.zIndex=this.pos.y;
		this.parent();	
	},
});

});