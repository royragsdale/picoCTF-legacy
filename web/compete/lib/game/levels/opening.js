ig.module( 'game.levels.opening' )
.requires( 'impact.image','game.entities.levelopening','game.entities.void','game.entities.taylorsprite','game.entities.sprite','game.entities.dialogbox' )
.defines(function(){
LevelOpening=/*JSON[*/{"entities":[{"type":"EntityLevelopening","x":0,"y":0},{"type":"EntityVoid","x":640,"y":296,"settings":{"name":"WP2"}},{"type":"EntityVoid","x":640,"y":472,"settings":{"name":"WP3"}},{"type":"EntityTaylorsprite","x":196,"y":204,"settings":{"zIndex":5}},{"type":"EntitySprite","x":196,"y":204,"settings":{"zIndex":10,"name":"chair","path":"media/chairroomship.png"}},{"type":"EntityDialogbox","x":0,"y":412}],"layer":[{"name":"Background","width":2,"height":2,"linkWithCollision":false,"visible":1,"tilesetName":"media/tilesheet-boys-room_NEW.png","repeat":false,"preRender":false,"distance":"1","tilesize":512,"foreground":false,"data":[[1,2],[3,4]]}]}/*]JSON*/;
LevelOpeningResources=[new ig.Image('media/tilesheet-boys-room_NEW.png')];
});