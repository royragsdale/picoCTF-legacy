ig.module(
	'game.entities.levelproblemselect'
)
.requires(
	'game.entities.levelselection',
	'game.entities.locksmall'
)
.defines(function(){
    	
EntityLevelproblemselect = EntityLevelselection.extend({		
    name: 'Problemselect',
	background: new ig.Image('media/ProblemMenu.png'),	
	indexMax:19,
	row:4,
	column:5,

	index2problem: {
		0:'21',
		1:'22',
		2:'23',
		3:'24',
		4:'25',
		5:'31',
		6:'32',
		7:'33',
		8:'34',
		9:'35',
		10:'36',
		11:'37',
		12:'41',
		13:'42',
		14:'43',
		15:'44',
		16:'45',
		17:'46',
	},
	
	doSelect: function(){
		this.parent();
		if(this.index<18){
			var p=this.index2problem[this.index];
			if(ig.gm.problemStates[p].unlocked){
				ig.gm.currentProblem=p;
				ig.gm.loadLevel('Problem',false);
			}
		}else if(this.index==18){
			if(ig.gm.levelStates['Spaceship'].unlocked){
				ig.gm.loadLevel('Galaxyselect',false);
			}
		}
	},
	
	init: function( x, y, settings ) {		
		this.parent( x, y, settings );		

	},
	
	ready: function(){
		this.parent();
		
		var upperleft=ig.game.getEntityByName('upperleft').pos;
		var bottomright=ig.game.getEntityByName('bottomright').pos;
		var index=0;
		for(var i=0;i<this.row;i++){
			for(var j=0;j<this.column;j++){				
				var x=upperleft.x+(bottomright.x-upperleft.x)/(this.column-1)*j;
				var y=upperleft.y+(bottomright.y-upperleft.y)/(this.row-1)*i;
				
				var zb=ig.game.spawnEntity(EntityZonebutton);
				zb.name=index+'';
				zb.size.x=100;
				zb.size.y=100;
				zb.pos.x=x-zb.size.x/2;
				zb.pos.y=y-zb.size.y/2;
				
				var v=ig.game.spawnEntity(EntityVoid);
				v.name='m'+index;
				v.pos.x=x;
				v.pos.y=y;
				
				var p=this.index2problem[index];
				if(index<=18){
					var m=ig.game.spawnEntity(EntityMark);
					m.pos.x=x-m.size.x/2;
					m.pos.y=y-m.size.y/2;
					m.enabled=true;		
				}
				if(index<18){			
					if(ig.gm.problemStates[p].solved){
						m.currentAnim=m.anims['solved'];
					}else if(ig.gm.problemStates[p].unlocked){
						m.currentAnim=m.anims['must'];
					}else{
						m.enabled=false;
						var l=ig.game.spawnEntity(EntityLocksmall);
						l.pos.x=x-l.size.x/2;
						l.pos.y=y-l.size.y/2;
					}					
				}else if(index==18){
					if(ig.gm.levelStates['Spaceship'].unlocked){
						m.currentAnim=m.anims['exit'];
					}else{						
						m.enabled=false;
						var l=ig.game.spawnEntity(EntityLocksmall);
						l.pos.x=x-l.size.x/2;
						l.pos.y=y-l.size.y/2;
					}
				}				
				index++;
				if(index==19)break;
			}
		}
	},
	
	update: function(){
		var selector=ig.game.getEntityByName('selector');
		var i=Math.floor(this.index/this.column);
		var j=this.index%this.column;
		var upperleft=ig.game.getEntityByName('upperleft').pos;
		var bottomright=ig.game.getEntityByName('bottomright').pos;
		var x=upperleft.x+(bottomright.x-upperleft.x)/(this.column-1)*j;
		var y=upperleft.y+(bottomright.y-upperleft.y)/(this.row-1)*i;
		selector.pos.x=x-selector.size.x/2;
		selector.pos.y=y-selector.size.y/2;
		
		if(ig.input.pressed('enter')){			
			this.doSelect();
		}
	},
	
	draw: function(){
		this.parent();
		if(typeof ig.gm!='undefined'){
			var s='';
			if(this.index<18){
				var p=this.index2problem[this.index];
				s=PROBLEMS[p].prob;
			}else if(this.index==18){
				s='Go to galaxy problems';
			}
			ig.gm.fonts[1].draw(s,68,616);
		}
	}
});

});