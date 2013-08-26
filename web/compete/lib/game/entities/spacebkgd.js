ig.module(
	'game.entities.spacebkgd'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntitySpacebkgd = ig.Entity.extend({
	name: 'Spacebkgd',
	size: {x: 5, y: 5},
    animSheet:  new ig.AnimationSheet ("media/Transition4/Stars.png" ,1024, 1024),
    init: function(x,y,settings)
    {
        this.addAnim("idle",1,[0],true);
        this.parent(x,y,settings);
    }
	
});

});