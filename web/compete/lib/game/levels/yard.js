ig.module( 'game.levels.yard' )
.requires( 'impact.image','game.entities.levelyard','game.entities.void','game.entities.player','game.entities.sprite','game.entities.dialogbox' )
.defines(function(){
LevelYard=/*JSON[*/{"entities":[{"type":"EntityLevelyard","x":-204,"y":408},{"type":"EntityVoid","x":904,"y":920,"settings":{"name":"WP1"}},{"type":"EntityVoid","x":944,"y":1232,"settings":{"name":"WP2"}},{"type":"EntityPlayer","x":900,"y":596},{"type":"EntitySprite","x":892,"y":1288,"settings":{"path":"media/robotDEADsprite1.png","size":{"x":72,"y":32}}},{"type":"EntityDialogbox","x":0,"y":412}],"layer":[{"name":"background","width":3,"height":4,"linkWithCollision":false,"visible":1,"tilesetName":"media/Env_House_Backyard with Objects.png","repeat":false,"preRender":false,"distance":"1","tilesize":512,"foreground":false,"data":[[1,2,3],[4,5,6],[7,8,9],[10,11,12]]}]}/*]JSON*/;
LevelYardResources=[new ig.Image('media/Env_House_Backyard with Objects.png')];
});