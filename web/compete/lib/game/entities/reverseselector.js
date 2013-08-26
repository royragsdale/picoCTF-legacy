ig.module(
	'game.entities.reverseselector'
)
.requires(
	'game.entities.galaxyselector'
)
.defines(function(){
	
EntityReverseselector = EntityGalaxyselector.extend({
	 init: function(x, y , settings){
         this.parent(x, y , settings)

         this.name = "ReverseEngineering",
         this.animSheet = new ig.AnimationSheet ('media/Galaxy Question Map UI/Reverse-Engineering.png',302,274);
         this.size = {x:302,y:274};
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