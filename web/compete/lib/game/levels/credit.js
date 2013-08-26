ig.module( 'game.levels.credit' )
.requires( 'impact.image','game.entities.sprite','game.entities.levelcredit' )
.defines(function(){
LevelCredit=/*JSON[*/{"entities":[{"type":"EntitySprite","x":0,"y":0,"settings":{"name":"thankyou","path":"Ending-Art_Thank-you.png","size":{"x":768,"y":699}}},{"type":"EntitySprite","x":0,"y":0,"settings":{"path":"Ending-Art_Great-Job.png","name":"goodjob","size":{"x":768,"y":699}}},{"type":"EntitySprite","x":0,"y":0,"settings":{"path":"Ending-Art_Credits.png","size":{"x":768,"y":1542},"name":"credit"}},{"type":"EntityLevelcredit","x":-52,"y":92}],"layer":[{"name":"background","width":1,"height":1,"linkWithCollision":false,"visible":1,"tilesetName":"media/Ending-Art_Background.png","repeat":false,"preRender":false,"distance":"1","tilesize":768,"foreground":false,"data":[[1]]}]}/*]JSON*/;
LevelCreditResources=[new ig.Image('media/Ending-Art_Background.png')];
});