ig.module(
	'game.entities.dialogbox'
)
.requires(
	'game.entities.ui'
)
.defines(function(){

EntityDialogbox = EntityUi.extend({
	name: 'dialogbox',
	animSheet: new ig.AnimationSheet('media/Dialog_Picts_Final_384x144.png',768,288),	
	size: {x:768, y:288},
	textOffset: {x:30, y:140},
	displayWidth: 400,
	text: '',
	displayText: '',
	currentLine: '',
	textIndex: 0,
	font: null,
	enabled: true,
	finished: true,
	
	/******* functions *******/
	
	setWho: function(who){
		this.currentAnim=this.anims[who];
		
		if(who.indexOf('Toast')!=-1 || who.indexOf('Patrol')!=-1 || who.indexOf('Guard')!=-1 ){
			this.font=ig.gm.fonts[0];
		}else{
			this.font=ig.gm.fonts[1];
		}
	},
	
	setWhat: function(what){
		this.text=what;
		this.displayText='';
		this.currentLine='';
		this.textIndex=0;
		this.finished=false;
	},
	
	
	/******* events *******/
	
	init: function( x, y, settings ) {
		this.parent( 0, 412, settings );
		
		this.addAnim('Taylor', 1, [0]);
		this.addAnim('TaylorSurprise', 1, [1]);
		this.addAnim('ToastRed', 1, [2]);
		this.addAnim('Toast', 1, [3]);
		this.addAnim('ToastGreen', 1, [3]);
		this.addAnim('ToastBlue', 1, [4]);
		this.addAnim('ToastYellow', 1, [5]);
		this.addAnim('Dropa', 1, [6]);
		this.addAnim('Patrol', 1, [6]);
		this.addAnim('Captain', 1, [7]);
		this.addAnim('Pilot', 1, [7]);
		this.addAnim('Techie', 1, [8]);
		this.addAnim('Guard', 1, [9]);
		this.addAnim('Hologram', 1, [10]);
		
		if(typeof ig.gm!='undefined'){
			this.font=ig.gm.fonts[1];
			this.enabled=false;
			this.currentAnim=this.anims['Taylor'];
		}
	},
		
	update: function(){			
		if(!this.enabled)return;
		this.parent();
		
		if(this.textIndex<this.text.length){
			var ch=this.text[this.textIndex];
			this.currentLine+=ch
			this.displayText+=ch
			
			// break new line
			if(ch==' '){
				if(this.font.widthForString(this.currentLine)>this.displayWidth){
					ch='\n';
					this.displayText+='\n';
				}			
			}
			
			if(ch=='\n')
				this.currentLine='';
			// a new char
			this.textIndex++;
		}else{
			this.finished=true;
		}		
	},	
	
	draw: function(){
		if(!this.enabled)return;				
		this.parent();
		if(typeof ig.gm!='undefined'){
			// should draw on screen coord
			this.font.draw(this.displayText,
					   this.pos.x-ig.game.screen.x+this.textOffset.x,
					   this.pos.y-ig.game.screen.y+this.textOffset.y,
					   ig.Font.ALIGN.LEFT);				
		}
	}
});

});