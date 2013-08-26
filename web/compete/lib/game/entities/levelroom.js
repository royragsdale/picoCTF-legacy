ig.module(
	'game.entities.levelroom'
)
.requires(
	'game.entities.levelscene'
)
.defines(function(){
    	
EntityLevelroom = EntityLevelscene.extend({
    name: 'Room',
	nextLevel: 'Airport',
	problemsInLevel: ['21','22','23','24','25'],
	problemsInSteps: {
		1:['21'],
		2:['22','23','24','25'],
		3:['22','23','24','25'],
	},
	isControlLevel:true,

	
	cutscene: {
		/*
			Reference: https://docs.google.com/document/d/1_VceSENx8EUU2BI1IIMr_4WkV-VOj2WBq-bPz5Up_nk/edit
		*/
		'Initialization':[
			{
				cmd: 'custom',
				init: function(){
					// unlock first problem
					ig.gm.problemStates['21'].unlocked=true;
				}			
			},
			{
				cmd: 'sleep', 
				sleeptime: '1'
			},
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'You may be a little toasty, but I think I can fix you!'
			},		
			{
				cmd: 'message', 
				what: 'Welcome to picoCTF!\n\nInteract with the marked objects to start your journey!'
			},
		],
		'Take a Nap':[
		/*
			Pos_bed: Bed position
		*/
			{
				cmd: 'gotoPoint', 
				who:'Taylor', 
				where: 'Pos_bed'
			},
			{
				cmd: 'sleep', 
				sleeptime: '1.5'
			},
		],
		'Enter Debug Mode Before':[
			//{
				//cmd: 'sound',
				//name: 'robot_hull_knock'
			//},
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Looks like you\'re having some trouble booting up...'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				},
			}
		],
		'Enter Debug After':[
		/*
			Pos_toast_debug: Toast position for debug mode, 
			Pos_toast_confuse1/2: animation checkpoints, 
			Pos_toast_net: Toast position for network problem
		*/
			//{
				//cmd: 'sound',
				//name: 'robot_jump'
			//},
			{
				cmd: 'sleep',
				sleeptime: '1',
			},
			{
				cmd: 'talk', 
				who: 'ToastRed', 
				what:'Damage Level --- High. \nSelf-repair system damaged... \nSearching for fallback systems...'
			},
			//{
				//cmd: 'sound',
				//name: 'robot_confuse'
			//},
			{
				cmd: 'gotoPoint', 
				who:'Toast',
				where: 'Pos_toast_confuse0'
			},
			{
				cmd: 'gotoPoint', 
				who:'Toast', 
				where: 'Pos_toast_confuse1'
			},
			{
				cmd: 'gotoPoint', 
				who:'Toast', 
				where: 'Pos_toast_confuse2'
			},
			{
				cmd: 'gotoPoint', 
				who:'Toast', 
				where: 'Pos_toast_net'
			},
			{
				cmd: 'face', 
				who:'Toast', 
				direction: 'down'
			},
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Uh...Are you okay?'
			},
		],
		'Sending message Before':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Seems like you need some help there. Let me try!'
			},		
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				},
			},
		],
		'Sending message After':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'That\'s what I\'m talking about!'
			},
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'Network connection established, entering self-repair mode.'
			},
		],
		'Robotics 101 Before':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'I received this book called \'Robotics 101\' last holiday. I thought I would never open it.'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				},
			},			
		],
		'Robotics 101 After':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Oh Yeah!'
			},
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'Boot file accepted, system clean.'
			},
		],
		'Command line Before':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Let me connect you with my computer, I should be able to replace the corrupted system files for you.'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				},
			},	
		],
		'Command line After':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'I knew this would work!'
			},
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'System file accepted.'
			},	
		],
		'Repair Serial Number Before':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'A piece of metal from the robot? It has some \ninstructions on it!'
			},
			{
				cmd: 'custom',
				init: function(){
					ig.gm.loadLevel('Problem',false);
				},
			},	
		],
		'Repair Serial Number After':[
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'I got this!'
			},
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'Entering self-repair mode.'
			},	
		],
		'Finished':[
		/*
			Pos_scared: where Taylor will be listening to the hologram
			Pos_excited_1: animation checkpoint
			Pos_toast_net: where toast is
		*/

			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Hooray! I fixed you! Can you talk now? Where are you from?'
			
			},
            {
                cmd: 'gotoPoint',
                who: 'Toast',
                where: 'Pos_Hologram_Toast'
            },
            {
                cmd: 'face',
                who: 'Toast',
                direction: 'left'
            },
            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'Pos_Hologram_Taylor'
            },
            {
                cmd: 'face',
                who: 'Taylor',
                direction: 'right'
            },
            {
                cmd: 'talk',
                who: 'TaylorSurprise',
                what: 'Are you okay?'
            },
            {
                cmd: 'sound',
                name: 'hologram_pulsa'
            },
            {
                cmd:'custom',
                init: function(){
                    var holoray =ig.game.getEntityByName('holoray')
                    holoray.enabled = true;
                }
            },
            {
                cmd: 'sleep',
                sleeptime: 0.4
            },
            {
                cmd:'custom',
                init: function(){
                    var holoray =ig.game.getEntityByName('holoray')
                    holoray.currentAnim = holoray.anims.holoray1;
                }
            },
            {
                cmd: 'sleep',
                sleeptime: 0.4
            },
            {
                cmd:'custom',
                init: function(){
                    var holoray =ig.game.getEntityByName('holoray')
                    holoray.currentAnim = holoray.anims.holoray2;
                }
            },
            {
                cmd: 'sleep',
                sleeptime: 0.4
            },
            {
                cmd:'custom',
                init: function(){
                    var holoray =ig.game.getEntityByName('holoray')
                    holoray.currentAnim = holoray.anims.holoray3;
                }
            },
            {
                cmd: 'sleep',
                sleeptime: 0.4
            },
            {
                cmd:'custom',
                init: function(){
                    //ig.game.getEntityByName('holoray').enabled = false,
                    ig.game.getEntityByName('hologram').enabled =true;
                }
            },

			{
				cmd: 'gotoPoint', 
				who: 'Taylor', 
				where: 'Pos_scared', 
				back: true
			},
			{
				cmd: 'talk', 
				who: 'TaylorSurprise',
				what: 'What is this? A hologram?'
			},
            {
                cmd: 'face',
                who: 'Taylor',
                direction: 'right'
            },
            {
                cmd: 'sound',
                name: 'hologram_speak'
            },
			{
				cmd: 'talk', 
				who: 'Hologram',
				what: 'The Galactic Overlord passed away last cycle. As we all mourn his passing we must think to the future. Though he had no heirs, he left specific instructions to determine who shall take the Iridium Throne.'
			},
			{
				cmd: 'talk', 
				who: 'Hologram',
				what: 'His will states that "All space pilots are invited to take part in a competition to upgrade their star-fighters and battle to determine a victor. The winner of this battle royale will be deemed worthy to take my place!"'
			},
            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'Pos_not_scared'
            },
			{
				cmd: 'talk', 
				who: 'Hologram',
				what: 'Pilot, it seems that you have been separated from your star-fighter. I am sending its current location to your robot now.'			
			},
            {
                cmd: 'sound',
                name: 'hologram_pulsa_end'
            },
            {
                cmd:'custom',
                init: function(){
                    ig.game.getEntityByName('hologram').enabled = false;
                    var holoray =ig.game.getEntityByName('holoray')
                    holoray.currentAnim = holoray.anims.holoray2;
                }
            },
            {
                cmd: 'sleep',
                sleeptime: 0.4
            },
            {
                cmd:'custom',
                init: function(){
                    var holoray =ig.game.getEntityByName('holoray')
                    holoray.currentAnim = holoray.anims.holoray1;
                }
            },
            {
                cmd: 'sleep',
                sleeptime: 0.4
            },
            {
                cmd:'custom',
                init: function(){
                    var holoray =ig.game.getEntityByName('holoray')
                    holoray.currentAnim = holoray.anims.holoray0;
                }
            },
            {
                cmd: 'sleep',
                sleeptime: 0.4
            },
            {
                cmd: 'custom',
                init: function(){
                    ig.game.getEntityByName('holoray').enabled = false;
                }
            },

			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'Must go to the Spaceport.'
			},
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'The Spaceport is located at - Planet Quax Area F Port-21, 4 miles from here.'
			},
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Pilot! A space battle! My own ship! It sounds so\ndangerous, yet so cool!'
			},
            {
                cmd: 'gotoPoint',
                who:'Toast',
                where: 'Pos_toast_net'
            },
            {
                cmd: 'face',
                who: 'Toast',
                direction: 'down'
            },
            {
                cmd: 'custom',
                init: function(){
                    ig.gm.hologramAnim = true;
                    localStorage.hologramAnim = true;
                }
            }
		],
		'What is your name':[
            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'Pos_Rename'
            },
            {
                cmd: 'face',
                who: 'Taylor',
                direction: 'left'
            },
            {
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'Oh, by the way, what\'s your name?'
			},
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'I am X3CTF01.'
			},
			{
				cmd: 'talk', 
				who: 'Taylor', 
				what: 'How about something a little more catchy? What about Toast? Since you were pretty burnt up when I found you.'
			},
			//{
				//cmd: 'sound',
				//name: 'toast_confirmation'
			//},
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'Name change accepted. I will assist you in your adventure.'
			},
			{
				cmd: 'follow',
				who: 'Toast',
				target: 'Taylor'			
			},
            {
                cmd:'sleep',
                sleeptime: 1.2
            },
            {
                cmd: 'sound',
                name: 'daydream'
            },
            {
                cmd: 'custom',
                init: function()
                {
                    ig.game.getEntityByName('daydream').enabled =true;
                }
            },
			{
				cmd: 'talk', 
				who: 'Toast', 
				what: 'When you become the new Galactic Overlord, I will be High Binar of all robots. Let us do this.'
			},
            {
                cmd: 'custom',
                init: function()
                {
                    ig.game.getEntityByName('daydream').enabled =false;
                }
            },
            {
                cmd: 'gotoPoint',
                who: 'Taylor',
                where: 'Pos_Exit'
            },
            {
                cmd: 'custom',
                init: function(){
                    ig.gm.loadLevel('Room2airport',true);
                }
            }
		]
	},

	/******* callbacks ********/
	firstExit: true,
	onTrigger: function(trigger,other){
		this.parent(trigger,other);
        var t=trigger.name+'';
        if(t=='exit' && other.name=='Taylor' && this.step == 3){
            if(this.firstExit){
                this.startCutscene('What is your name');
                this.firstExit = false;
            }
        }
	},
	
	/******* events ********/
	
	init: function( x, y, settings ) {
		this.parent( x, y, settings );		
		if(typeof ig.gm!='undefined')
			ig.sm.playbgm('Game');

	},
	
	ready: function(){
		this.parent();
		// room is small, don't need to focus camera
		this.isFocusCamera=false;				
        //Prepared for hologram
        ig.game.getEntityByName('hologram').enabled =false;
        ig.game.getEntityByName('daydream').enabled =false;
        _this = this;
		// get step
		this.step=1;
		if(ig.gm.problemStates['21'].solved)
			this.step=2;
		if(ig.gm.numSolved({'22':0,'23':0,'24':0,'25':0})>=2)
			this.step=3;
		
		// steps
		//this.enableEntity('exit',false);
		if(this.step==1){
			ig.game.getEntityByName('Toast').kill();			
			this.enableEntity('robotscrap',true);
			if(ig.gm.previousLevelName!='Problem')
				this.startCutscene('Initialization');
		}
		if(this.step==2 || this.step==3){
			if(ig.gm.previousLevelName!='Problem')
				this.alignEntity('Toast','Pos_toast_net');			
			this.enableEntity('deadrobot',false);						
		}
		if(this.step==3){
            var mark = ig.game.getEntityByName('exit').mark;
			mark.currentAnim = mark.anims.exit
            mark.currentAnim.angle = Math.PI;
            if(!ig.gm.hologramAnim)
                this.startCutscene('Finished');
		}
		
		this.refreshProblemEntities();
	}
	
});

});
