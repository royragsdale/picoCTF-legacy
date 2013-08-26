ig.module(
	'game.entities.forensicsselector'
)
.requires(
	'game.entities.galaxyselector'
)
.defines(function(){
	
EntityForensicsselector = EntityGalaxyselector.extend({
	 init: function(x, y , settings){
         this.parent(x, y , settings)

         this.name = "Forensics",
         this.animSheet = new ig.AnimationSheet ('media/Galaxy Question Map UI/Forensics.png',256,176);
         this.size = {x:256,y:176};
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