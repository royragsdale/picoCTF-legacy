ig.module(
	'game.entities.levelscene'
)
.requires(
	'game.entities.level'
)
.defines(function(){
    	
EntityLevelscene = EntityLevel.extend({
	cutscene:[],
	isFocusCamera:true,
	focusTarget:null,
	nextLevel:'',
	isInCutscene:false,
	isFinishedLastCutscene:false,
	csName:'',
	csItemIndex:0,
	waitTimer: new ig.Timer(),
	step: 0,
	levelStartLock: false,
	levelStartLockPos: {x:0,y:0},
	clickTrigger: null,	
	
	
	/******* cutscene *******/
	
	// list of all possible commands in cutscene
	// each command contains (optional) init(), update(), draw(), finish(), defaultFinishCondition
	cmdList:{
		'gotoPoint':{
			init:function(cs){
				var who=ig.game.getEntityByName(cs.who);
				who.dest=ig.game.getEntityByName(cs.where).pos;				
				if(typeof cs.back!='undefined' && cs.back)
					who.back=true;
			},
			update:function(cs){
			},
			finish:function(cs){
				var who=ig.game.getEntityByName(cs.who);
				who.back=false;				
			},
			defaultFinishCondition:'reach'
		},
		'jumptoPoint':{
			init:function(cs){
				var who=ig.game.getEntityByName(cs.who);
				who.jump(ig.game.getEntityByName(cs.where).pos);				
			},
			defaultFinishCondition:'instant'
		},
		'face':{
			init:function(cs){
				var who=ig.game.getEntityByName(cs.who);
				who.facing=cs.direction;
			},
			defaultFinishCondition:'instant'
		},
        'rotateTo':{
            init:function(cs){
                var who = ig.game.getEntityByName(cs.who);
                who.rotate(cs.angle,cs.rotatespeed);
            },
            update:function(cs){
            },
            finish:function(cs){
            },
            defaultFinishCondition:'reach'
        },
		'talk':{
			init:function(cs){
				var dialogbox=ig.game.getEntityByName('dialogbox');
				dialogbox.setWho(cs.who);
				dialogbox.setWhat(cs.what);
				dialogbox.enabled=true;
			},
			update:function(cs){
			},
			draw:function(cs){				
			},
			finish:function(cs){
				var dialogbox=ig.game.getEntityByName('dialogbox');
				dialogbox.enabled=false;
			},
			defaultFinishCondition:'click'
		},
		'message':{
			init:function(cs){
				var messagebox=ig.game.getEntityByName('messagebox');
				messagebox.setWhat(cs.what);
				messagebox.enabled=true;
			},
			update:function(cs){
			},
			draw:function(cs){				
			},
			finish:function(cs){
				var messagebox=ig.game.getEntityByName('messagebox');				
				messagebox.enabled=false;
			},
			defaultFinishCondition:'click'			
		},
		'follow':{
			init:function(cs){
				var who=ig.game.getEntityByName(cs.who);
				var target=ig.game.getEntityByName(cs.target);
				if(cs.who==cs.target){
					who.unfollow();
				}else{
					who.follow(target);
				}
			},
			update:function(cs){
			},
			finish:function(cs){
			},
			defaultFinishCondition:'instant'
		},
		'sleep':{
			init:function(cs){				
				ig.gm.currentLevel.waitTimer.set(cs.sleeptime);
			},
			update:function(cs){
			},
			finish:function(cs){
			},
			defaultFinishCondition:'timer'
		},
		'anim':{
			init:function(cs){
			},
			update:function(cs){
			},
			finish:function(cs){
			},
			defaultFinishCondition:'click'
		},
		'sound':{
			init:function(cs){
				ig.sm.play(cs.name);
			},
			defaultFinishCondition:'instant'
		},
		'bgm':{
			init:function(cs){
				ig.sm.playbgm(cs.name);
			},
			defaultFinishCondition:'instant'
		},
        'custom':{
            init:function(cs){
				if(typeof cs.init!='undefined')
					cs.init();
            },
			update:function(cs){
				if(typeof cs.update!='undefined')
					cs.update();
			},
			finish:function(cs){
				if(typeof cs.finish!='undefined')
					cs.finish();
			},
            defaultFinishCondition:'instant'
        }
	},
	
	// list of all finishing conditions of each cutscene item
	finishList:{
		'instant':function(cs){
			return true;
		},
		'click':function(cs){
			// TODO: debug jump talk
			if(ig.input.pressed('n'))return true;
			if(cs.cmd=='talk'){ // talk must be finished
				var dialogbox=ig.game.getEntityByName('dialogbox');
				if(typeof dialogbox!='undefined' && !dialogbox.finished)return false;
			}
			if(cs.cmd=='message'){ // message must be finished				
				var messagebox=ig.game.getEntityByName('messagebox');
				if(typeof messagebox!='undefined' && !messagebox.finished)return false;				
			}
			if(ig.input.pressed('enter') || ig.input.pressed('mouse')){
				ig.input.clearPressed();
				return true;
			}else{
				return false;
			}
		},
		'reach':function(cs){
			var who=ig.game.getEntityByName(cs.who);
			return !who.moving;
		},
		'timer':function(cs){
			return ig.gm.currentLevel.waitTimer.delta()>=0;
		},
	},
	
	
	/******* cutscene functions *******/
	
	startCutscene: function(_csName){
		if(_csName in this.cutscene==false){
			// TODO: alert cutscene not found
			return;
		}
		this.isInCutscene=true;
		
		// disable player control
		var player=ig.game.getEntityByName('Taylor');
		if(typeof player!='undefined'){
			player.control=false;
		}
		
		// init cutscene
		this.csName=_csName;
		this.csItemIndex=-1;
		this.isFinishedLastCutscene=true;		
		
		debugstring='In Cutscene';
	},
	
	finishCutscene: function(){
		this.isInCutscene=false;
		
		// resume player control
		var player=ig.game.getEntityByName('Taylor');
		if(typeof player!='undefined'){
			player.control=true;			
		}
				
		debugstring='';
	},
	
	
	/******* s/l state functions *******/

	enableEntity: function(s, e){
		var ent=ig.game.getEntityByName(s);
		if(typeof ent!='undefined')
			ent.enabled=e;
	},
	
	refreshProblemEntities: function(){
		for(var i=0;i<this.problemsInLevel.length;i++){
			this.enableEntity(this.problemsInLevel[i],false);
		}
		for(var i=0;i<this.problemsInSteps[this.step].length;i++){
			var s=this.problemsInSteps[this.step][i];
			var ent=ig.game.getEntityByName(s);
			ent.enabled=true;
			if(ig.gm.problemStates[s].solved){
				ent.solved=true;				
			}else{
				ent.solved=false;
			}
			ent.ready();
		}
		
	},
	
	alignEntity: function(s1,s2){
		var e1=ig.game.getEntityByName(s1);
		var e2=ig.game.getEntityByName(s2);
		centerAlign(e1,e2);
	},
	
	attachTrigger: function(s1, s2){
		var t=ig.game.getEntityByName(s1);
		var e=ig.game.getEntityByName(s2);
		t.following=true;
		t.followTarget=e;
	},
	
	loadEnt: function(name){
		var ent=ig.game.getEntityByName(name);
		var levelname=ig.gm.currentLevel.name;
		if(typeof ent=='undefined')return;
		if(typeof ig.gm.levelStates[levelname]=='undefined')return;
		if(typeof ig.gm.levelStates[levelname].ents[name]=='undefined')return;
		ent.pos.x=ig.gm.levelStates[levelname].ents[name].x;
		ent.pos.y=ig.gm.levelStates[levelname].ents[name].y;
		ent.following=ig.gm.levelStates[levelname].ents[name].following;
		if(ent.following)
			ent.follow(ig.game.getEntityByName('Taylor'));
		
	},
	
	loadState: function(){		
		this.loadEnt('Taylor');
		this.loadEnt('Toast');
		this.loadEnt('Guard');
		this.loadEnt('Patrol');
		this.loadEnt('Pilot');
	},
	
	saveEnt: function(name){
		var ent=ig.game.getEntityByName(name);
		var levelname=ig.gm.currentLevel.name;
		if(typeof ent!='undefined'){
			ig.gm.levelStates[levelname].ents[name]={};
			ig.gm.levelStates[levelname].ents[name].x=ent.pos.x;
			ig.gm.levelStates[levelname].ents[name].y=ent.pos.y;
			ig.gm.levelStates[levelname].ents[name].following=ent.following;
		}
	},
	
	saveState: function(){
		var levelname=ig.gm.currentLevel.name;
		ig.gm.levelStates[levelname].ents={};
		this.saveEnt('Taylor');
		this.saveEnt('Toast');
		this.saveEnt('Guard');
		this.saveEnt('Patrol');
		this.saveEnt('Pilot');
	},
	

	/******* callback functions *******/

	onTrigger: function(trigger,other){
		if(this.levelStartLock)
			return;
		
		this.parent(trigger,other);
		var t=trigger.name+'';
				
		// exit to next level

		
		// player triggers a problem
        if(typeof this.problemsInLevel != 'undefined')
        {
            if(this.problemsInLevel.indexOf(t)!=-1 && other.name=='Taylor') {
                trigger.canFire=false;
                ig.gm.currentProblem=t;
                ig.sm.play('select');
                if(typeof PROBLEMS[t].before!='undefined' && ig.gm.problemStates[t].solved==false){
                    this.startCutscene(PROBLEMS[ig.gm.currentProblem].before);
                }else{
                    ig.gm.loadLevel('Problem',false);
                }
            }
        }
	},
	
	onUI: function(name){
		this.parent(name);
	},
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );

		// init cutscene params
		this.isInCutscene=false;
		this.isFinishedLastCutscene=false;
		this.csName='';
		this.csItemIndex=0;
		this.clickTrigger=null;
	},
	
	ready: function(){		
		this.parent();
		       
		// by default, focus camera on player
		var player=ig.game.getEntityByName('Taylor');
		if(typeof player!='undefined'){
			this.isFocusCamera=true;
			this.focusTarget=player;
		}
	
		if(ig.gm.previousLevelName=='Problem' && this.isControlLevel){ // coming from problem			
			// load state and startcutscene (solved or failed)
			this.loadState();
			
			var player=ig.game.getEntityByName('Taylor');
			if(typeof player!='undefined'){
				this.levelStartLockPos.x=player.pos.x;
				this.levelStartLockPos.y=player.pos.y;
				this.levelStartLock=true;
			}
			
			if(ig.gm.problemStates[ig.gm.currentProblem].solved){
				if(typeof PROBLEMS[ig.gm.currentProblem].after!='undefined')
					this.startCutscene(PROBLEMS[ig.gm.currentProblem].after);
			}else{
				if(typeof PROBLEMS[ig.gm.currentProblem].failed!='undefined')
					this.startCutscene(PROBLEMS[ig.gm.currentProblem].failed)
			}
		}else{ // coming from menu or level select, this is the first load
			// init state and start initial cutscene
		}
		
		ig.gm.calculateStates();
	},	

	update: function(){		
		this.parent();
		// level start lock
		if(this.levelStartLock){
			var player=ig.game.getEntityByName('Taylor');
			var dx=Math.abs(player.pos.x-this.levelStartLockPos.x);
			var dy=Math.abs(player.pos.y-this.levelStartLockPos.y);
			var dm=50;
			if(dx>dm || dy>dm){
				this.levelStartLock=false;
			}
		}		
		
		// camera		
		if(this.isFocusCamera && (typeof this.focusTarget!= 'undefined') && this.focusTarget!=null){
			ig.game.screen.x = this.focusTarget.pos.x + this.focusTarget.size.x/2 - ig.system.width/2;
			ig.game.screen.y = this.focusTarget.pos.y + this.focusTarget.size.y/2 - ig.system.height/2;
		}
				
		// cutscene
		if(this.isInCutscene){
			// cutscene item update
			if(this.csItemIndex>=0){ // should load first item
				if(typeof this.curCSItemInfo.update!='undefined')
					this.curCSItemInfo.update(this.curCSItem);
					
				// current finish condition
				if(this.finishList[this.curCSItemFinishCondition](this.curCSItem)){
					this.isFinishedLastCutscene=true;
				}
			}
			
			// cutscene finish, jump and init
			if(this.isFinishedLastCutscene){
				// cutscene item finish
				if(typeof this.curCSItemInfo!='undefined' && typeof this.curCSItemInfo.finish!='undefined')
					this.curCSItemInfo.finish(this.curCSItem);
			
				this.csItemIndex++;								
				if(this.csItemIndex<this.cutscene[this.csName].length){				
					// a new cutscene item
					this.isFinishedLastCutscene=false;
					this.curCSItem=this.cutscene[this.csName][this.csItemIndex];
					this.curCSItemInfo=this.cmdList[this.curCSItem.cmd];	
					
					// cutscene item init
					if(typeof this.curCSItemInfo.init!='undefined')					
						this.curCSItemInfo.init(this.curCSItem);
						
					// get item finish-condition
					this.curCSItemFinishCondition=this.curCSItemInfo.defaultFinishCondition;
					if(typeof this.curCSItem.finishCondition!='undefined')
						this.curCSItemFinishCondition=this.curCSItem.finishCondition;					
				}else{
					// all cutscene items have been played
					this.finishCutscene();
				}
			}
			
		}
	},	
	
	draw: function(){		
		this.parent();
		if(typeof ig.gm!='undefined'){
			if(this.isInCutscene && typeof curCSItemInfo!='undefined' && typeof curCSItemInfo.draw!='undefined')
				curCSItemInfo.draw();
		}
	}
	
});

});