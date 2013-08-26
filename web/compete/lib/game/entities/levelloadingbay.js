ig.module(
	'game.entities.levelloadingbay'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
    	
EntityLevelloadingbay = EntityLevelscene.extend({		
    name: 'Loadingbay',
	nextLevel: 'Spaceship',	
	problemsInLevel: ['41','42','43','44','45','46'],
	problemsInSteps: {
		1:['41'],
		2:['41','42','43'],
		3:['41','42','43','44','45','46'],
		4:['41','42','43','44','45','46']
	},
	isControlLevel:true,
	
	cutscene: {
		'Initialization':[
		/*
		 *	Pos_Guard: the position where guard appears
		 */
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'So here\'s the Loading Bay. The star-fighter is just over there!'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'Be cautious, there are probably guards around...'
			},
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Taylor'
			}
		],
		//step 1
		'Byte Code Before':[
		/*
		 *	Pos_Guard: the position where guard appears
		 */
			{
				cmd: 'gotoPoint',
				who: 'Guard',
				where: 'Pos_Guard',                
			},
			{
				cmd: 'face',
				who: 'Guard',
				direction: 'down'
			},
			{
				cmd: 'talk',
				who: 'Guard',
				what: 'Who are you? Only Pilots are permitted to be in the Loading Bay!'
			},
			{
				cmd: 'gotoPoint',
				who: 'Taylor',
				where: 'Pos_player'
			},
			{
				cmd: 'face',
				who: 'Taylor',
				direction: 'left'
			},
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'I can pass the authentication.'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'Byte Code Fail':[
		/*
		 *	Failing means: Wrong answer.
		 *  Pos_back: the position where Taylor will be sent back
		 */
			{
				cmd: 'talk',
				who: 'Guard',
				what: 'Your presence here is unauthorized.  Please return to the public areas of the starport.'
			},
			{
				cmd: 'gotoPoint',
				who: 'Taylor',
				where: 'Pos_back',
				back: true 
			},
			{
				cmd: 'gotoPoint',
				who: 'Guard',
				where: 'Pos_Guard_leave'
			},
			{
				cmd: 'face',
				who: 'Guard',
				direction: 'down',
			},
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Toast, what should I do to get past this security guard?'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'Try using a HINT.'
			}
		],
		'Byte Code After':[
		/*
		 *  Pos_wireshark_DOS: the position where the wireshark_DOS problem is
		 */
			{
				cmd: 'talk',
				who: 'Guard',
				what: 'Authentication Result: True'
			},
			{
				cmd: 'gotoPoint',
				who: 'Guard',
				where: 'Pos_Guard_leave',
                back: true
			},
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Good job, let\'s use that Computer Pad over there and see if we can find some useful information.'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: '^_^'
			},
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Toast'
			},
			{
				cmd: 'gotoPoint',
				who: 'Toast',
				where: 'Pos_Terminal'
			}
		],
		//step 2
		'Wireshark DOS Before':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Toast, what\'s wrong?'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'Connecting to network ... ... ...'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'DoS attack detected... need help ...'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'Wireshark DOS After':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Cool, now all we need to do is get past the physical security system of the ship.'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'We are almost ready to board the ship!'
			},
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Taylor'
			}
		],
		'Pilot Logic Before':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Let\'s find out what can we do with this Terminal.'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'Try to find the information of the last Pilot, maybe we can circumvent the ship\'s authentication system with that!'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'Pilot Logic After':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Cool, now all we need to do is get around the physical security system of the ship.'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'We are almost ready to board the ship!'
			},
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Taylor'
			}
		],
		'Ship Problems Before':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Now all that\'s left is to get one of the ship\'s hatches open!'
			},
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'By the way, Toast, do you know how to fly a\nstar-fighter?'
			},			
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'All maintenance robots are programmed to fly in an emergency situation. \nWe have to get to space first, though, Taylor.'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'Ship Problems After':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Yeah! Let\'s board the ship and get off this planet.'
			},
            {
                cmd: 'message',
                what: 'You are now heading to space!\n\nIf you wish to finish the other questions on your planet, you can use the level viewer in the menu.'
            },
			{
				cmd: 'custom',
				init: function(){
                    ig.gm.loadLevel('Loadingbay2runway',true);
				}
			}
		]
	},

	
	
	boardship: function(){		
		var player=ig.game.getEntityByName('Taylor');
		var robot=ig.game.getEntityByName('Toast');
		player.kill();
		robot.kill();
		spaceship=ig.game.getEntityByName('spaceship');
		this.focusTarget=spaceship;
	},
	
	
	
	/******* callbacks ********/
	
	onTrigger: function(trigger,other){
		this.parent(trigger,other);
		if(this.isInCutscene)return;
		if(trigger.name=='guardzone' && other.name=='Taylor'){
			trigger.enabled=false;
			this.onTrigger(ig.game.getEntityByName('41'),other);
		}
	},
	

	/******* events ********/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );  
		if(typeof ig.gm!='undefined')
			ig.sm.playbgm('Loadingbay');
	},
	
	ready: function(){
		this.parent();
		
		this.attachTrigger('41','Guard');		
		                
		this.step=1;
		if(ig.gm.problemStates['41'].solved)
			this.step=2;
		if(ig.gm.problemStates['42'].solved || ig.gm.problemStates['43'].solved)
			this.step=3;
		if(ig.gm.problemStates['44'].solved || ig.gm.problemStates['45'].solved || ig.gm.problemStates['46'].solved)
			this.step=4;
			
		// steps		
		if(this.step==1){
			if(ig.gm.previousLevelName!='Problem')
				this.startCutscene('Initialization');
		}
		if(this.step==2){
			ig.game.getEntityByName('guardzone').enabled=false;
						
			if(ig.gm.previousLevelName!='Problem'){
				this.alignEntity('Guard','Pos_Guard_leave');
				this.alignEntity('Toast','Pos_Terminal');
			}
		}
		if(this.step==3){
			ig.game.getEntityByName('guardzone').enabled=false;			
			this.alignEntity('Guard','Pos_Guard_leave');
			var robot=ig.game.getEntityByName('Toast');
			var player=ig.game.getEntityByName('Taylor');			
			robot.follow(player);
		}
		if(this.step==4){
			ig.game.getEntityByName('guardzone').enabled=false;
			this.alignEntity('Guard','Pos_Guard_leave');
			var robot=ig.game.getEntityByName('Toast');
			var player=ig.game.getEntityByName('Taylor');			
			robot.follow(player);
		}
		
		
		this.refreshProblemEntities();
	}
});

});
