ig.module(
	'game.entities.galaxyselector'
)
.requires(
	'impact.entity'
)
.defines(function(){
	
EntityGalaxyselector = ig.Entity.extend({
     size: {x:200,y:200},
     enabled : false,
	 init: function(x, y , settings){
         this.parent(x, y , settings);

     },
     update: function(){
         this.parent();
         var mousex=ig.input.mouse.x+ig.game.screen.x;
         var mousey=ig.input.mouse.y+ig.game.screen.y;
         if((mousex>this.pos.x && mousex<this.pos.x+this.size.x) &&
             (mousey>this.pos.y && mousey<this.pos.y+this.size.y)){
             this.enabled = true;ig
             ig.gm.category = this.name;
             if (ig.input.pressed("mouse")){
                 ig.gm.loadLevel(this.name);
                 ig.sm.play('click');
             }
         }else{
             this.enabled = false;
         }
     },
     draw: function(){
         if (!this.enabled) return;
         this.parent();
     }
	
});

});