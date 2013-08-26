ig.module(
	'game.entities.void'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityVoid = ig.Entity.extend({
	_wmDrawBox: true,
	_wmBoxColor: 'rgba(128, 28, 230, 0.7)',
	name: 'number',
	size: {x: 5, y: 5},
	
});

});