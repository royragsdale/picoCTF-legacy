ig.module( 'game.levels.test' )
.requires( 'impact.image','game.entities.sprite','game.entities.dialogbox' )
.defines(function(){
LevelTest=/*JSON[*/{"entities":[{"type":"EntitySprite","x":232,"y":100,"settings":{"name":"testrobot"}},{"type":"EntityDialogbox","x":0,"y":412}],"layer":[{"name":"background","width":4,"height":3,"linkWithCollision":false,"visible":1,"tilesetName":"media/Env_House_Backyard with Objects.png","repeat":false,"preRender":false,"distance":"1","tilesize":256,"foreground":false,"data":[[40,0,0,0],[0,0,0,0],[0,0,0,0]]}]}/*]JSON*/;
LevelTestResources=[new ig.Image('media/Env_House_Backyard with Objects.png')];
});