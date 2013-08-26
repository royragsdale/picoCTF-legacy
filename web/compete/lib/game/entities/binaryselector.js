ig.module(
	'game.entities.binaryselector'
)
.requires(
	'game.entities.galaxyselector'
)
.defines(function(){
	
EntityBinaryselector = EntityGalaxyselector.extend({
	 init: function(x, y , settings){
         this.parent(x, y, settings);
         this.name = "BinaryExploitation",
         this.animSheet = new ig.AnimationSheet ('media/Galaxy Question Map UI/Binary-Exploitation.png',264,272);
         this.size = {x:264, y:272};
         this.addAnim('hover',1,[0],true);


     },
     update: function(){
         this.parent();

     },
     draw: function(){
         this.parent();
     }
	
});

});