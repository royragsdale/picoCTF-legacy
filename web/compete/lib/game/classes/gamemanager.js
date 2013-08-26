/******* globals *******/

LEVELS={
    'Room':0,
    'Airport':1,
    'Loadingbay':2,
    'Spaceship':3
}

MENUS={
    'Title':10,
    'Menu':11,
    'Levelselect':12,
    'Problemselect':13,
    'Galaxyselect':14,

    'Opening':15,
    'Yard':16,
    'Room2airport' :17,
    'Airport2loadingbay' :18,
    'Loadingbay2runway': 19,
    'Runway2spaceship':20,
    'Forensics':21,
    'Cryptography':22,
    'ReverseEngineering':23,
    'BinaryExploitation':24,
    'ScriptExploitation':25,
	'Credit':26,
	'Ending':27,


    'Test':99
}

PROBLEMS={

	'00':{prob:'idle',PID:'',before:'',after:'',failed:''},
	
	'21':{prob:'FailureToBoot', PID:'512a8622b393a33f2cf9b37f', before:'Enter Debug Mode Before', after:'Enter Debug After'},
	'22':{prob:'GrepIsYourFriend', PID:'5161cca02f0686520c000004', before:'Command line Before', after:'Command line After'},
	'23':{prob:'XMLOL', PID:'5161e8102f0686520c00000b', before:'Robotics 101 Before', after:'Robotics 101 After'},
	'24':{prob:'ReadTheManual', PID:'5161c04a2f0686520c000003',  before:'Repair Serial Number Before', after:'Repair Serial Number After'},
	'25':{prob:'First Contact', PID:'5161fa8a2f0686520c00000e', before:'Sending message Before', after:'Sending message After'},
	
	'31':{prob:'SpaceportMap',PID:'5161d2a92f0686520c000005', before:'SpaceportMap Before', after:'SpaceportMap After'},
	'32':{prob:'GETKey', PID:'5161eae22f0686520c00000d', before:'GETKey Before', after:'GETKey After'},
	'33':{prob:'Bitwise', PID:'5161d7582f0686520c000006', before:'Bitwise or Locked Door - MD5 Before', after:'Bitwise or Locked Door - MD5 After'},
	'34':{prob:'TechnicianChallenge', PID:'5161fea72f0686520c00000f', before:'TechnicianChallenge Before', after:'TechnicianChallenge After'},
	'35':{prob:'TryThemAll',PID:'5161be6f2f0686520c000002', before:'Bitwise or Locked Door - MD5 Before', after:'Bitwise or Locked Door - MD5 After'},
	'36':{prob:'Yummy',PID:'516a186c2f0686520c000010', before:'Cookie Before', after:'Cookie After'},
	'37':{prob:'CFGToC',PID:'5161e3b62f0686520c00000a', before:'CFG to C Before', after:'CFG to C After', fail:'CFG to C Fail'},
	
	'41':{prob:'ByteCode',PID:'5161de472f0686520c000008',before:'Byte Code Before',after:'Byte Code After',failed:'Byte Code Fail'},
	'42':{prob:'SharkingADOS',PID:'51788c396c342fba03000006',before:'Wireshark DOS Before',after:'Wireshark DOS After'},
	'43':{prob:'PilotLogic',PID:'5161e2402f0686520c000009',before:'Pilot Logic Before',after:'Pilot Logic After'},
	'44':{prob:'ClientsideIsTheBestSide',PID:'51788a1b6c342fba03000005',before:'Ship Problems Before',after:'Ship Problems After'},
	'45':{prob:'InjectingSQL',PID:'51784b1e6c342fba03000004',before:'Ship Problems Before',after:'Ship Problems After'},
	'46':{prob:'RSA',PID:'51745431054c91c14b00000f',before:'Ship Problems Before',after:'Ship Problems After'},

    '51':{prob:'Dark Star', PID:'516b2dc22f0686520c00001e'},
    '52':{prob:'NAVSAT', PID:'516b1e8f2f0686520c00001d'},
    '53':{prob:'SecondContact',PID:'516af3b22f0686520c00001a'},
    '54':{prob:'Chromatophoria',PID:'516ae8982f0686520c000019'},
    '55':{prob:'Decryption',PID:'516ae36c2f0686520c000017'},
    '56':{prob:'Spamcarver',PID:'516adba52f0686520c000015'},
    '57':{prob:'InHexNoOneCanHearYouComplain',PID:'516ad71b2f0686520c000012'},
    '58':{prob:'BlackHole',PID:'5176cb706c342fba03000001'},

    '61':{prob:'Classic',PID:'5174230c054c91c14b000002'},
    '62':{prob:'Trivial',PID:'51741fb4054c91c14b000001'},
    '63':{prob:'Robomunication',PID:'516ad9162f0686520c000014'},
    '64':{prob:'BrokenCBC',PID:'517712636c342fba03000002'},
    '65':{prob:'BrokenRSA',PID:'517b49f917f5e16305000001'},

    '71':{prob:'Evergreen',PID:'51744c0e054c91c14b00000d'},
    '72':{prob:'avaJ',PID:'51744070054c91c14b00000a'},
    '73':{prob:'HarderSerial',PID:'5174275e054c91c14b000003'},
    '74':{prob:'MildlyEvil',PID:'5177398c6c342fba03000003'},
    '75':{prob:'MoreEvil',PID:'5179eb80657debeb14000004'},
    '76':{prob:'HotCoffee',PID:'5179ee76657debeb14000005'},

    '81':{prob:'Format1',PID:'517464b7054c91c14b000010'},
    '82':{prob:'Overflow1',PID:'5175a89b56dce84c7d000006'},
    '83':{prob:'Overflow2',PID:'5175a8b256dce84c7d000007'},
    '84':{prob:'Overflow3',PID:'5175a8c856dce84c7d000008'},
    '85':{prob:'Overflow4',PID:'5175a8de56dce84c7d000009'},
    '86':{prob:'Overflow5',PID:'5175a8f356dce84c7d00000a'},
    '87':{prob:'ROP1',PID:'5175a37e56dce84c7d000002'},
    '88':{prob:'ROP2',PID:'5175a39356dce84c7d000003'},
    '89':{prob:'ROP3',PID:'5175a3b056dce84c7d000004'},
    '810':{prob:'ROP4',PID:'5175a3d156dce84c7d000005'},
    '811':{prob:'Format2',PID:'51759fef56dce84c7d000001'},

    '91':{prob:'PrettyHardProgramming',PID:'51744969054c91c14b00000c'},
    '92':{prob:'PythonEval1',PID:'517429d9054c91c14b000004'},
    '93':{prob:'PythonEval2',PID:'51743245054c91c14b000005'},
    '94':{prob:'PythonEval3',PID:'51743313054c91c14b000006'},
    '95':{prob:'PythonEval4',PID:'5174332a054c91c14b000007'},
    '96':{prob:'PythonEval5',PID:'51743341054c91c14b000008'},
    '97':{prob:'PHP2', PID:'5179a797657debeb14000001'},
    '98':{prob:'PHP3', PID:'5179dcc0657debeb14000002'},
    '99':{prob:'PHP4', PID:'5179e4f1657debeb14000003'}

}
//Represent Equipment level in the team experience
EQUIPMENT = {
    'laser': 1,
    'missile': 1,
    'radar': 1,
    'hull': 1,
    'engine': 1,
    'regularship': 1
}
GALAXYPROBLEMS = {
    'Forensics':{num:8, identifier: '5', equipment:'laser'},
    'Cryptography' : {num: 5, identifier: '6',equipment:'missile'},
    'ReverseEngineering' : {num: 6, identifier: '7',equipment:'radar'},
    'BinaryExploitation' : {num: 11, identifier: '8',equipment:'hull'},
    'ScriptExploitation':{num:9, identifier: '9',equipment:'engine'}
}



// debug
debugstring='';
debugbuffer='';
debug=function(s){
    debugbuffer+=s+'\n';
};

/******* utilities *******/

lerp=function(a,b,t){
    return a*(1-t)+b*t;
}

centerAlign=function(a,b){
    a.pos.x=b.pos.x-a.size.x/2+b.size.x/2;
    a.pos.y=b.pos.y-a.size.y/2+b.size.y/2;
}

isInside=function(a,b){
    return a.x>b.pos.x && a.x<b.pos.x+b.size.x &&
        a.y>b.pos.y && a.y<b.pos.y+b.size.y;
}

ig.module( 
	'game.classes.gamemanager' 
)
.requires(
	'impact.game',
	'impact.font',
		
	'game.levels.title',	
	'game.levels.menu',	
	'game.levels.levelselect',
	'game.levels.problemselect',
	
	'game.levels.yard',
    'game.levels.opening',
	'game.levels.room',	
	'game.levels.airport',
	'game.levels.loadingbay',
    'game.levels.spaceship',
    'game.levels.galaxyselect',
    'game.levels.forensics',
    'game.levels.cryptography',
    'game.levels.reverseEngineering',
    'game.levels.binaryExploitation',
    'game.levels.scriptExploitation',
	'game.levels.empty',
	'game.levels.problem',
	'game.levels.test',
    'game.levels.room2airport',
    'game.levels.airport2loadingbay',
    'game.levels.loadingbay2runway',
    'game.levels.runway2spaceship',
	'game.levels.credit',
    'game.levels.ending',
	
	'plugins.screen-fader'
)
.defines(function(){
		
GameManager = ig.Class.extend({		
	
	/******* game states *******/
	
	// level states
	levelStates: new Array(),
	
	// problem states
	problemStates: new Array(),
	
	// current problem, should be '21', '22'...
	currentProblem: '0',
	
	// current level controller, should be entity levelxxx
	currentLevel: null,
	
	// previous level name, should be 'Room', 'Problem'... 
	previousLevelName: '',

	// time since beginning
	time: 0,
	
	myHash: '',

	//Represent Question Category
    category: '',
    //Represent hologram animation
    hologramAnim: false,
    endingFlag: false,
	/******* fonts *******/

	fonts: [
		//new ig.Font('media/font/04b03.font.png'),//white
		//new ig.Font('media/font/fixedsys.png'),//black
		new ig.Font('media/font/pixel2xwhite.png'),
		new ig.Font('media/font/pixel2xblack.png')
	],

	// load a level and save/load level state.
	// levelName should be 'Yard'...
	loadLevel: function(levelName, fade, problem){
		this.ProblemHide();
		
		// record previous level name
		if(ig.gm.currentLevel!=null){		
			if(typeof ig.gm.currentLevel.saveState!='undefined' && ig.gm.currentLevel.isControlLevel)
				ig.gm.currentLevel.saveState();
			ig.gm.previousLevelName=ig.gm.currentLevel.name;
		}
		// load level with screen fade, record current level
		ig.game.loadLevelDeferred(ig.global['Level' + levelName]);
		if(fade==true){
			this.screenFader=new ig.ScreenFader({ fade: 'out', speed: 2 });			
		}

		// Record current problem
		// Set RESTful Hash
		if(levelName=='Problem'){
			if(typeof problem!='undefined')
		    	ig.gm.currentProblem=problem;
			ig.gm.myHash=PROBLEMS[ig.gm.currentProblem].prob;

		}else {
			ig.gm.myHash=levelName;			
		}
		
		
		window.location.hash=ig.gm.myHash;
		//debug
		debugstring='Loaded Level: '+levelName;
	},
	
    ProblemHide: function(){
        var problemContent = $("#problemcontent");
        var problemInput =  $("#probleminput");
        var problemSubmit = $("#problemsubmit");
        problemContent.html('');
        problemContent.hide();
        problemInput.hide();
        problemInput.val('');
        problemSubmit.hide();
    },

    ProblemDisplay:function() {
        var problemContent = $("#problemcontent");
        var problemInput =  $("#probleminput");
        var problemSubmit = $("#problemsubmit");
        var databaseID = PROBLEMS[ig.gm.currentProblem].PID;
        problemContent.html(getProblemInfo(databaseID));
        problemContent.show();
        problemInput.show();
        problemSubmit.show();
    },    
	
	numSolved: function(p){
		var sum=0;
		for(var s in p){
			if(ig.gm.problemStates[s].solved){
				sum++;
			}
		}
		return sum;
	},
	
	calculateStates: function(){
		ig.gm.levelStates['Room'].unlocked=true;
		ig.gm.levelStates['Airport'].unlocked=ig.gm.numSolved({'22':0,'23':0,'24':0,'25':0})>=2;
		ig.gm.levelStates['Loadingbay'].unlocked=ig.gm.problemStates['33'].solved||ig.gm.problemStates['35'].solved;
		ig.gm.levelStates['Spaceship'].unlocked=ig.gm.problemStates['44'].solved||ig.gm.problemStates['45'].solved||ig.gm.problemStates['46'].solved;
				
		ig.gm.problemStates['21'].unlocked=ig.gm.levelStates['Room'].unlocked;		
		ig.gm.problemStates['22'].unlocked=ig.gm.problemStates['21'].solved;
		ig.gm.problemStates['23'].unlocked=ig.gm.problemStates['21'].solved;
		ig.gm.problemStates['24'].unlocked=ig.gm.problemStates['21'].solved;
		ig.gm.problemStates['25'].unlocked=ig.gm.problemStates['21'].solved;
		
		ig.gm.problemStates['31'].unlocked=ig.gm.levelStates['Airport'].unlocked;
		ig.gm.problemStates['32'].unlocked=ig.gm.levelStates['Airport'].unlocked;
		ig.gm.problemStates['33'].unlocked=ig.gm.problemStates['31'].solved||ig.gm.problemStates['32'].solved;
		ig.gm.problemStates['35'].unlocked=ig.gm.problemStates['31'].solved||ig.gm.problemStates['32'].solved;
		ig.gm.problemStates['34'].unlocked=ig.gm.levelStates['Airport'].unlocked;
		ig.gm.problemStates['36'].unlocked=ig.gm.levelStates['Airport'].unlocked;
		ig.gm.problemStates['37'].unlocked=ig.gm.levelStates['Airport'].unlocked;
		
		ig.gm.problemStates['41'].unlocked=ig.gm.levelStates['Loadingbay'].unlocked;
		ig.gm.problemStates['42'].unlocked=ig.gm.problemStates['41'].solved;
		ig.gm.problemStates['43'].unlocked=ig.gm.problemStates['41'].solved;
		ig.gm.problemStates['44'].unlocked=ig.gm.problemStates['42'].solved||ig.gm.problemStates['43'].solved;
		ig.gm.problemStates['45'].unlocked=ig.gm.problemStates['42'].solved||ig.gm.problemStates['43'].solved;
		ig.gm.problemStates['46'].unlocked=ig.gm.problemStates['42'].solved||ig.gm.problemStates['43'].solved;		
	},
	
	
	getStatesAPI: function(){
				
		if(typeof ig.gm.problemStates[s].solved=='undefined'){
			ig.gm.problemStates[s].solved=false;
			ig.gm.problemStates[s].unlocked=ig.gm.problemStates[s].solved;
		}
	
	},
	
	/******* events *******/
	
	init: function() {
		ig.gm=this;
	
		// input bindings
		ig.input.bind(ig.KEY.ENTER, 'enter');
		ig.input.bind(ig.KEY.SPACE, 'enter');
		ig.input.bind(ig.KEY.N, 'n');
		ig.input.bind(ig.KEY.MOUSE1, 'mouse');
		ig.input.bind(ig.KEY.ESC, 'esc');
		ig.input.bind(ig.KEY.UP_ARROW,'up');
		ig.input.bind(ig.KEY.DOWN_ARROW,'down');
		ig.input.bind(ig.KEY.LEFT_ARROW,'left');
		ig.input.bind(ig.KEY.RIGHT_ARROW,'right');
		ig.input.bind(ig.KEY.W,'up');
		ig.input.bind(ig.KEY.S,'down');
		ig.input.bind(ig.KEY.A,'left');
		ig.input.bind(ig.KEY.D,'right');

        if(typeof(Storage)!=="undefined")
        {
            if (localStorage.hologramAnim)
            {
                this.hologramAnim = localStorage.hologramAnim;
            }
            else
            {
                this.hologramAnim = false;
            }
        }
		// Read game record (must have one)
		for(var s in PROBLEMS){
			ig.gm.problemStates[s]={
				unlocked: false,
				solved: false
			};
		}
		for(var s in LEVELS){
			ig.gm.levelStates[s]={
				unlocked: true
			}
		}
			
		// API get 
		ig.gm.getStatesFromAPI();
			
		this.calculateStates();		
		
		// RESTful
		window.onhashchange = this.RESTfulCheck2;
		
		var hash = window.location.hash.slice(1);
		if(hash=='compete' || hash==''){
			this.loadLevel('Title', false);
		}else{
			this.RESTfulCheck2();
		}

        this.checkEquip();
		// debug
		debugstring='game start';
		
		// debug		
		//ig.gm.loadLevel('Credit',true);

	},

	update: function() {
		// all level-related logic in level controllers (level***.js)		
		
		// time since beginning
		this.time+=ig.system.tick;
	},
	
    getStatesFromAPI: function()
    {
        var rdata = getAllProblemInfo();
        for (var problem in rdata)
        {
            for (var localproblem in PROBLEMS)
            {
                if (rdata[problem].pid == PROBLEMS[localproblem].PID)
                {
                    ig.gm.problemStates[localproblem].solved = rdata[problem].correct;
                }
            }
        }
	},

	RESTfulCheck2: function(){
		var hash = window.location.hash.slice(1); // Slice off the #
		if(hash==ig.gm.myHash){
			// in game jump
		}else{
			// restful jump
			var isProblem=false;
			for(var s in PROBLEMS){
				if(PROBLEMS[s].prob==hash){
					isProblem=true;
					ig.gm.currentProblem=s;
					var levelID = Math.floor(s.slice(0,1)) - 2
					if (levelID > 2)
						levelID = 3;
					ig.gm.loadLevel('Problem',false);
					for (var level in LEVELS)
					{
						if (LEVELS[level] == levelID)
						{
							if(ig.gm.currentLevel != null)
								if(ig.gm.currentLevel.name == level)
								{
									if(ig.gm.levelStates[level].unlocked)
									{
										ig.gm.previousLevelName = level;
									}
									else
									{
										ig.gm.previousLevelName = "Levelselect";
									}
								}
								else ig.gm.previousLevelName = "Problemselect";
							else ig.gm.previousLevelName = "Problemselect";
						}
					}

					//ig.gm.previousLevelName='Menu';
				}
			}

			if(isProblem){
			}else if(hash in LEVELS){
				if(ig.gm.levelStates[hash].unlocked){
					ig.gm.loadLevel(hash,true);
					ig.gm.previousLevelName='Menu';
				}else{
					ig.gm.loadLevel('Levelselect',true);
					ig.gm.previousLevelName='Menu';
				}
			}else if(hash in MENUS){
				ig.gm.loadLevel(hash,false);
				ig.gm.previousLevelName='Menu';
			}
		}
	},

    checkEquip: function(){
        for (var i in ig.gm.problemStates)
        {
            var levelID = Math.floor(i.slice(0,1));
            for(var j in GALAXYPROBLEMS)
            {
                if(levelID == Math.floor(GALAXYPROBLEMS[j].identifier))
                {
                    if(EQUIPMENT[GALAXYPROBLEMS[j].equipment] < 4 && ig.gm.problemStates[i].solved)
                    {
                        EQUIPMENT[GALAXYPROBLEMS[j].equipment]++;
                    }
                }
            }
        }
    },
	draw: function() {
		// screen fade
		if (this.screenFader) {
			this.screenFader.draw();
		}

		// debug info in upperleft corner
		//this.fonts[1].draw(debugstring,0,0,ig.Font.ALIGN.LEFT);
		//this.fonts[1].draw(debugbuffer,0,30,ig.Font.ALIGN.LEFT);
	}

});

});
