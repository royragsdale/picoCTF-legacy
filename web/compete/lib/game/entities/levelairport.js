ig.module(
	'game.entities.levelairport'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
    	
EntityLevelairport = EntityLevelscene.extend({		
    name: 'Airport',
	nextLevel: 'Loadingbay',
	problemsInLevel: ['31','32','33','34','35','36','37'],
	problemsInSteps: {
		1:['31','32','34','36','37'],
		2:['31','32','33','35','34','36','37'],
		3:['31','32','33','35','34','36','37']
	},
	isControlLevel:true,
		
	cutscene: {
		'Initialization':[
		/*
		 *	Pos_screen: right in front of the LED screen
		 *	Pos_toast_wifi: beside the LED screen where toast connected to the spaceport wifi
		 */
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'What a big Spaceport! Where can I find my\nstar-fighter? Oh, the screen over there should have some information.'
			},
            {
                cmd: 'face',
                who: 'Taylor',
                direction: 'up'
            },
			{
				cmd: 'talk',
				who: 'Captain',
				what: 'Do you want to know how to use radar? In space you must be able to see your enemies.'
			},
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Taylor'
			},
			{
				cmd: 'gotoPoint',
				who: 'Taylor',
				where: 'Pos_screen'
			},
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Toast'
			},
			{
				cmd: 'gotoPoint',
				who: 'Toast',
				where: 'Pos_toast_wifi0'
			},						
			{
				cmd: 'gotoPoint',
				who: 'Toast',
				where: 'Pos_toast_wifi'
			}
		],
		
//step 1
		'SpaceportMap Before':[
		/*
		 *	Pos_toast_screen: right in front of the LED screen, besides taylor
		 */
			{
				cmd: 'gotoPoint',
				who: 'Toast',
				where: 'Pos_toast_screen'
			},			
			{
				cmd: 'face',
				who: 'Toast',
				direction: 'up'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'Oh no! This only shows commercial spaceships. We are going to have to hack the system to find fighter-class spaceships.'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'SpaceportMap After':[
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Taylor'
			},
			{
				cmd: 'sound',
				name: 'toast_happy'
			},
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'We\'re the best! It\'s located in the Loading Bay, which is through the door farthest to the left.'
			}
		],
		'GETKey Before':[
		/*
		 *	Pos_toast_screen: right in front of the LED screen, besides taylor
		 */
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'My radar is picking up a wireless network here. Let me connect to it. Oh, it is the starport\'s internal website.'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'GETKey After':[
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Taylor'
			},
			{
				cmd: 'sound',
				name: 'toast_happy'
			},
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'So, Loading Bay it is. Toast, let\'s go to the door farthest to the left.'
			}
		],
		//Step 2
		'Bitwise or Locked Door - MD5 Before':[
		/*
		 *	Pos_toast_screen: right in front of the LED screen, besides taylor
		 */
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Hmm. This door is locked.'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'A piece of cake! I can do it.'
			},
            {
                cmd: 'face',
                who: 'Toast',
                direction: 'left'
            },
			{
				cmd: 'sleep',
				sleeptime: '0.5'
			},
            {
                cmd: 'face',
                who: 'Toast',
                direction: 'down'
            },
            {
                cmd: 'sleep',
                sleeptime: '0.5'
            },
            {
                cmd: 'face',
                who: 'Toast',
                direction: 'right'
            },
            {
                cmd: 'sleep',
                sleeptime: '0.5'
            },
            {
                cmd: 'face',
                who: 'Toast',
                direction: 'up'
            },
            {
                cmd: 'sleep',
                sleeptime: '0.5'
            },
			{
				cmd: 'talk',
				who: 'Toast',
				what: '(5 minutes later) I give up. It is beyond my ability. Maybe we can work together?'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'Bitwise or Locked Door - MD5 After':[
			{
				cmd: 'sound',
				name: 'toast_suprise'
			},
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'You are weak sauce! That was so easy that I solved it all by myself. Maybe I should upgrade your hardware...'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'Nooooooooooo! An adept programmmer must know how to use limited hardware resources...'
			}
		],
		//Optional Problems
		'Cookie Before':[
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'Cookie After':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'That\'s correct!'
			}
		],		
		'TechnicianChallenge Before':[
		/*
		 *	Pos_techie_excited: animation checkpoint
		 */
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Hello. May I ask you a question?'
			},
			{
				cmd: 'gotoPoint',
				who: 'Techie',
				where: 'Pos_techie_excited'
			},
			{
				cmd: 'talk',
				who: 'Techie',
				what: 'Hmmm. You look smart.  Perhaps if you answer one of mine first...'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'TechnicianChallenge After':[
			{
				cmd: 'talk',
				who: 'Techie',
				what: 'This younger generation really knows their stuff!'
			}
		],
		'CFG to C Before':[
			{
				cmd: 'talk',
				who: 'Patrol',
				what: 'Your ID and boarding pass, please?'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				}
			}
		],
		'CFG to C Fail':[
		/*
		 *	Failing means: Here's my ID|Wrong answer.
		 */
			{
				cmd: 'talk',
				who: 'Patrol',
				what: 'You are too young to travel alone.  Please exit the starport.'
			}
		],
		'CFG to C After':[
			{
				cmd: 'talk',
				who: 'Patrol',
				what: 'Must obey...'
			},
			{
				cmd: 'talk',
				who: 'TaylorSurprise',
				what: 'So, I have a drone now?'
			},
			{
				cmd: 'talk',
				who: 'Toast',
				what: 'We will not really need it in space, Taylor..'
			},
            {
                cmd: 'talk',
                who: 'Taylor',
                what: 'OK, OK.'
            }
		],
		'Finished':[
			{
				cmd: 'talk',
				who: 'Taylor',
				what: 'Let\'s go Toast, things are really getting exciting!'
			}
		]		
	},
	
	
	/******* callbacks ********/
	
	onTrigger: function(trigger,other){
		this.parent(trigger,other);
        var t=trigger.name+'';
        if(t=='exit' && other.name=='Taylor' && this.step == 3){
            ig.gm.loadLevel('Airport2loadingbay',true);
        }
	},
	
	
	/******* events ********/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );
		if(typeof ig.gm!='undefined')
			ig.sm.playbgm('Airport');
	},
	
	ready: function(){
		this.parent();
		
		this.attachTrigger('34','Techie');
		this.attachTrigger('36','Pilot');
		this.attachTrigger('37','Patrol');
		this.attachTrigger('32','Toast');
		ig.game.getEntityByName('34').bonus=true;
		ig.game.getEntityByName('36').bonus=true;
		ig.game.getEntityByName('37').bonus=true;
		
		this.step=1;
		if(ig.gm.problemStates['31'].solved || ig.gm.problemStates['32'].solved)
			this.step=2;
		if(ig.gm.problemStates['33'].solved || ig.gm.problemStates['35'].solved)
			this.step=3;		
		
		// steps
		//this.enableEntity('exit',false);
		if(this.step==1){
			if(ig.gm.previousLevelName!='Problem')
				this.startCutscene('Initialization');
		}
		if(this.step==2){			
			var robot=ig.game.getEntityByName('Toast');
			var player=ig.game.getEntityByName('Taylor');			
			robot.follow(player);
		}
		if(this.step==3){
			var robot=ig.game.getEntityByName('Toast');
			var player=ig.game.getEntityByName('Taylor');
			robot.follow(player);
            var mark = ig.game.getEntityByName('exit').mark;
            mark.currentAnim = mark.anims.exit
		}
		
		this.refreshProblemEntities();
	}

});

});
