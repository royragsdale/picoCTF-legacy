ig.module(
	'game.entities.equipsprite'
)
.requires(
	'impact.entity'
)
.defines(function(){

EntityEquipsprite = ig.Entity.extend({
	size: {x:64, y:64},
	_wmScalable: true,
	path: 'media/robotsprite.png',
	enabled: true,
		
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		if(this.path.substring(0,6)!='media/')
			this.path='media/'+this.path;
		this.animSheet=new ig.AnimationSheet(this.path,this.size.x,this.size.y);
        this.addAnim('blue',1,[0])
        this.addAnim('silver',1,[1]);
        this.addAnim('yellow',1,[2]);
        this.addAnim('white',1,[3]);
	},

	draw: function() {
		if(!this.enabled)return;
		//this.zIndex=this.pos.y;
		this.parent();	
	}
});

});