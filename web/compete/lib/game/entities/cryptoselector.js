ig.module(
	'game.entities.cryptoselector'
)
.requires(
    'game.entities.galaxyselector'
)
.defines(function(){
	
EntityCryptoselector = EntityGalaxyselector.extend({
	 init: function(x, y , settings){
         this.parent(x, y , settings);
         this.name = "Cryptography",
         this.animSheet = new ig.AnimationSheet ('media/Galaxy Question Map UI/Cryptography.png',276,210);
         this.size = {x:276, y:210};
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