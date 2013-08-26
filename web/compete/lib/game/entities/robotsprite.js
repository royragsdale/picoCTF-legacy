ig.module(
	'game.entities.robotsprite'
)
.requires(
	'impact.entity'
)
.defines(function(){

EntityRobotsprite = ig.Entity.extend({
	size: {x:64, y:64},
	_wmScalable: true,
	path: 'media/toastLights.png',
	enabled: true,
	zIndex:100,
	name :'Driver',
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		if(this.path.substring(0,6)!='media/')
			this.path='media/'+this.path;
		this.animSheet=new ig.AnimationSheet(this.path,this.size.x,this.size.y),
        this.addAnim('flash',0.4,[0,1,2,3],false);
	},

	draw: function() {
		if(!this.enabled)return;
		//this.zIndex=this.pos.y;
		this.parent();	
	}
});

});