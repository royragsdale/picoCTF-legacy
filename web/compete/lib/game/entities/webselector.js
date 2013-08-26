ig.module(
	'game.entities.webselector'
)
.requires(
	'game.entities.galaxyselector'
)
.defines(function(){
	
EntityWebselector = EntityGalaxyselector.extend({
	 init: function(x, y , settings){
         this.parent(x, y , settings)

         this.name = "ScriptExploitation",
         this.animSheet = new ig.AnimationSheet ('media/Galaxy Question Map UI/script-exploitation.png',362,162);
         this.size = {x:362, y:162};
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